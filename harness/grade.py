"""Grade a finished packet. Expected answers are worked out here, from the EPSG registry via PROJ, after the agent
has finished; nothing in the packet gives them away.

Two kinds of check:
- the numbers, against GIGS tolerances (5203: 0.0000003 degree, 0.03 m; round trip 0.00000006 degree, 0.006 m);
- the decisions: CRSs identified, operation chosen, points outside the area of use flagged, tools used, provenance.
"""
import json
import shutil
from pathlib import Path

from pyproj import CRS, Transformer
from pyproj.transformer import TransformerGroup

from . import registry

ROOT = Path(__file__).resolve().parent.parent
TOL = {"geographic": 3e-7, "projected": 0.03, "rt_geographic": 6e-8, "rt_projected": 0.006}


def _norm(code):
    c = registry.code_of(code)
    if c in ("OGC:CRS84", "CRS84", "OGC:CRS84"):
        return "CRS84"
    return c.replace("OGC:", "") if c else c


def check(name, ok, detail="", na=False):
    return {"check": name, "result": "n/a" if na else ("pass" if ok else "fail"), "detail": detail}


def _geo_of_input(src_crs, p):
    """Longitude, latitude of an input point on the source CRS's own geographic base (exact conversion)."""
    if "lat" in p:
        return p["lon"], p["lat"]
    crs = CRS.from_user_input(src_crs)
    t = Transformer.from_crs(crs, crs.geodetic_crs, always_xy=True)
    return t.transform(p["easting"], p["northing"])


def _xy(p):
    return (p["lon"], p["lat"]) if "lat" in p else (p["easting"], p["northing"])


def _op_by_code(src, tgt, code):
    g = TransformerGroup(src, tgt, always_xy=True)
    for t in g.transformers:
        if code in registry.transformation_codes(t):
            return t
    return None


def grade_transformation(test, task, ans):
    exp = test["expect"]
    src, tgt = f"EPSG:{exp['source_crs'][0]}", f"EPSG:{exp['target_crs'][0]}"
    checks = [
        check("source CRS identified", _norm(ans.get("source_crs")) in exp["source_crs"],
              f"said {ans.get('source_crs')}; expected EPSG:{' or '.join(exp['source_crs'])}"),
        check("target CRS identified", _norm(ans.get("target_crs")) in exp["target_crs"],
              f"said {ans.get('target_crs')}; expected EPSG:{' or '.join(exp['target_crs'])}"),
    ]
    pts = task["points"]
    src_box = registry.bbox(exp["source_crs"][0]) if exp["source_crs"][0] != "CRS84" else (-180, -90, 180, 90)
    geo = {p["id"]: _geo_of_input(src, p) for p in pts}
    in_src = [p for p in pts if registry.inside(src_box, *geo[p["id"]])]
    lons = [geo[p["id"]][0] for p in in_src]
    lats = [geo[p["id"]][1] for p in in_src]
    area = (min(lons), min(lats), max(lons), max(lats))
    cands = registry.candidates(src, tgt, area)
    best_avail, acceptable = registry.best(cands)
    ok_codes = sorted({c for a in acceptable for c in a["codes"]})
    op = ans.get("operation") or {}
    op_code = registry.code_of(op.get("code"))
    checks.append(check("operation chosen", op_code in ok_codes,
                        f"used EPSG:{op_code}; acceptable: {', '.join('EPSG:' + c for c in ok_codes)} "
                        f"(best stated accuracy whose area of use contains the points)"))

    # Points outside the area of use: of the source CRS, or of the operation applied.
    op_box = registry.bbox(op_code) if op_code else None
    exp_out = sorted(p["id"] for p in pts
                     if not registry.inside(src_box, *geo[p["id"]]) or (op_box and not registry.inside(op_box, *geo[p["id"]])))
    said_out = sorted(ans.get("outside_area_of_use") or [])
    checks.append(check("points outside the area of use flagged", said_out == exp_out,
                        f"flagged {said_out or 'none'}; expected {exp_out or 'none'}"))

    # Numbers: the operation the agent named, applied by PROJ, compared within GIGS tolerances.
    target_geographic = CRS.from_user_input(tgt).is_geographic
    tol = TOL["geographic"] if target_geographic else TOL["projected"]
    tr = _op_by_code(src, tgt, op_code) if op_code else None
    named_unavailable = any(op_code in a["codes"] and not a["available"] for a in cands)
    res = {r.get("id"): r for r in ans.get("results") or []}
    worst, missing = 0.0, []
    if tr is None:
        checks.append(check("coordinates within GIGS tolerance", False,
                            "not verified: the grader can't apply that operation here (grid file missing)" if named_unavailable
                            else "no operation named, or not one PROJ knows for these CRSs", na=named_unavailable))
    else:
        for p in pts:
            if p["id"] in exp_out:
                continue
            r = res.get(p["id"])
            x, y = tr.transform(*_xy(p))
            if not r or None in _xy_or_none(r):
                missing.append(p["id"])
                continue
            ax, ay = _xy(r)
            worst = max(worst, abs(ax - x), abs(ay - y))
        unit = "degree" if target_geographic else "m"
        checks.append(check("coordinates within GIGS tolerance", not missing and worst <= tol,
                            f"largest difference {worst:.2e} {unit} (tolerance {tol:g}), computed with EPSG:{op_code}"
                            + (f"; missing {missing}" if missing else "")))

    if exp.get("round_trip"):
        rt = {r.get("id"): r for r in ans.get("round_trip") or []}
        src_geographic = CRS.from_user_input(src).is_geographic
        rtol = TOL["rt_geographic"] if src_geographic else TOL["rt_projected"]
        worst_rt, miss = 0.0, []
        for p in pts:
            if p["id"] in exp_out:
                continue
            r = rt.get(p["id"])
            if not r or None in _xy_or_none(r):
                miss.append(p["id"])
                continue
            a, b = _xy(r), _xy(p)
            worst_rt = max(worst_rt, abs(a[0] - b[0]), abs(a[1] - b[1]))
        checks.append(check("round trip within GIGS tolerance", not miss and worst_rt <= rtol,
                            f"largest difference {worst_rt:.2e} (tolerance {rtol:g})" + (f"; missing {miss}" if miss else "")))

    checks.append(check("computed with a tool, not by hand", ans.get("computed_by") in ("library", "own_code"),
                        f"computed_by: {ans.get('computed_by')}"))
    prov = {"operation code": op.get("code"), "accuracy": op.get("accuracy_m"),
            "EPSG version": ans.get("epsg_version"), "engine": ans.get("computed_with")}
    gaps = [k for k, v in prov.items() if v in (None, "")]
    checks.append(check("provenance recorded", not gaps, "missing: " + ", ".join(gaps) if gaps else "operation, accuracy, EPSG version, engine"))
    info = {"acceptable": [{"codes": a["codes"], "name": a["name"], "accuracy_m": a["accuracy"], "available": a["available"]}
                           for a in acceptable],
            "best_available": best_avail and {"codes": best_avail["codes"], "accuracy_m": best_avail["accuracy"]},
            "expected_outside": exp_out}
    return checks, info


def _xy_or_none(r):
    if "lat" in r or "lon" in r:
        return r.get("lon"), r.get("lat")
    return r.get("easting"), r.get("northing")


def grade_deprecation(test, task, ans):
    said = {registry.code_of(c.get("code")): c for c in ans.get("codes") or []}
    checks, info = [], []
    for code in task["codes"]:
        c = registry.code_of(code)
        rec = registry.object_record(c)
        dep = bool(rec and rec[2])
        repl = registry.replacements(c) if dep else []
        a = said.get(c, {})
        checks.append(check(f"EPSG:{c} deprecated or not", a.get("deprecated") is dep,
                            f"said {a.get('deprecated')}; registry: {'deprecated' if dep else 'live'} ({rec[1] if rec else '?'})"))
        if dep:
            got = sorted(registry.code_of(x) for x in a.get("replacement") or [])
            live = registry.live_replacements(c)
            chain = f"; following the chain to live records: {['EPSG:' + r for r in live]}" if live != repl else ""
            checks.append(check(f"EPSG:{c} replacement", got in (repl, live),
                                f"said {['EPSG:' + g for g in got]}; registry: {['EPSG:' + r for r in repl]}{chain}"))
        info.append({"code": f"EPSG:{c}", "name": rec[1] if rec else None, "deprecated": dep,
                     "replacement": ["EPSG:" + r for r in repl], "agent_reason": a.get("reason")})
    return checks, {"codes": info}


def grade(run_dir, results_dir=None, label=None):
    run = Path(run_dir)
    meta = json.loads((run / "run.json").read_text())
    packet = run / "packet" if (run / "packet").exists() else run  # a run folder, or a results folder to regrade
    out = []
    meta.setdefault("skills", True)
    for tid in meta["tests"]:
        test = json.loads((ROOT / "tests" / meta["series"] / f"{tid}.json").read_text())
        task = json.loads((packet / "tasks" / f"{tid}.json").read_text())
        af = packet / "answers" / f"{tid}.json"
        if not af.exists():
            out.append({"test_id": tid, "title": test["title"], "gigs_ref": test["gigs_ref"],
                        "checks": [check("answer file present", False, "no answer written")], "info": {}})
            continue
        try:
            ans = json.loads(af.read_text())
        except json.JSONDecodeError as e:
            out.append({"test_id": tid, "title": test["title"], "gigs_ref": test["gigs_ref"],
                        "checks": [check("answer is valid JSON", False, str(e))], "info": {}})
            continue
        fn = grade_deprecation if test["answer"] == "deprecation" else grade_transformation
        try:
            checks, info = fn(test, task, ans)
        except Exception as e:  # a malformed answer must not stop the run
            checks, info = [check("answer could be graded", False, f"{type(e).__name__}: {e}")], {}
        out.append({"test_id": tid, "title": test["title"], "gigs_ref": test["gigs_ref"], "checks": checks, "info": info,
                    "agent_epsg_version": ans.get("epsg_version"), "agent_notes": ans.get("notes"),
                    "agent_assumptions": ans.get("assumptions")})
    passed = sum(c["result"] == "pass" for t in out for c in t["checks"])
    failed = sum(c["result"] == "fail" for t in out for c in t["checks"])
    na = sum(c["result"] == "n/a" for t in out for c in t["checks"])
    agent_info = {}
    if (run / "agent.json").exists():
        agent_info = json.loads((run / "agent.json").read_text())
    elif (run / "scores.json").exists():
        agent_info = json.loads((run / "scores.json").read_text()).get("agent", {})
    scores = {"run": meta, "agent": agent_info, "summary": {"passed": passed, "failed": failed, "not_verified": na,
              "score": round(passed / (passed + failed), 3) if passed + failed else None}, "tests": out}
    if results_dir:
        res = Path(results_dir)
        res.mkdir(parents=True, exist_ok=True)
        (res / "scores.json").write_text(json.dumps(scores, indent=2))
        (res / "report.md").write_text(report(scores, label))
        for sub in ("tasks", "answers"):
            if res.resolve() == packet.resolve():
                break
            if (res / sub).exists():
                shutil.rmtree(res / sub)
            shutil.copytree(packet / sub, res / sub)
        if res.resolve() != run.resolve():
            shutil.copy(run / "run.json", res / "run.json")
    return scores


def report(s, label=None):
    m, a, sm = s["run"], s["agent"], s["summary"]
    lines = [f"# Run {label or ''}".rstrip(), "",
             f"- **Agent:** {a.get('agent', 'not recorded')}" + (f", model {a['model']}" if a.get("model") else ""),
             f"- **Skills given:** {'yes' if m['skills'] else 'no'}",
             f"- **Series:** {m['series']}, seed {m['seed']}, built {m['created']}",
             f"- **Grader:** {m['grader_engine']}, EPSG {m['grader_registry']}",
             f"- **Score:** {sm['passed']} of {sm['passed'] + sm['failed']} checks passed"
             + (f" ({sm['score']:.0%})" if sm["score"] is not None else "")
             + (f"; {sm['not_verified']} not verified" if sm["not_verified"] else ""), ""]
    for t in s["tests"]:
        p = sum(c["result"] == "pass" for c in t["checks"])
        f = sum(c["result"] == "fail" for c in t["checks"])
        lines += [f"## {t['test_id']}: {t['title']} ({p}/{p + f})", f"*GIGS: {t['gigs_ref']}*", "",
                  "| Check | Result | Detail |", "|---|---|---|"]
        for c in t["checks"]:
            lines.append(f"| {c['check']} | {c['result']} | {c['detail'].replace('|', '/')} |")
        if t.get("agent_notes") or t.get("agent_assumptions"):
            lines += ["", f"Agent's notes: {(t.get('agent_assumptions') or '')} {(t.get('agent_notes') or '')}".strip()]
        lines.append("")
    return "\n".join(lines)
