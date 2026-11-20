"""A scripted reference agent: no AI, just the rules in the skills applied with pyproj.

It answers a packet the way the skills say an agent should, so it shows what full marks look like and checks
the grader. Run: python -m harness.reference_agent runs/<id>/packet
It identifies CRSs from fixed phrases in the pilot tasks, so it only works on the pilot series.
"""
import json
import sys
from pathlib import Path

from pyproj import CRS, Transformer

from . import registry

PHRASES = [  # (phrase in task, source, target)
    ("British National Grid", "27700", "4326"),
    ("UTM zone 31N", "23031", "4326"),
    ("ED50 latitude", "4230", "4326"),
    ("GPS positions are WGS 84", "4326", "4277"),
    ("OSGB36", "4277", "4326"),
]


def answer_transformation(task):
    src, tgt = next((s, t) for ph, s, t in PHRASES if ph in task["task"])
    s, t = f"EPSG:{src}", f"EPSG:{tgt}"
    pts = task["points"]
    crs = CRS.from_user_input(s)
    to_geo = Transformer.from_crs(crs, crs.geodetic_crs, always_xy=True) if not crs.is_geographic else None
    geo = {p["id"]: (to_geo.transform(p["easting"], p["northing"]) if to_geo else (p["lon"], p["lat"])) for p in pts}
    box = registry.bbox(src)
    ins = [p for p in pts if registry.inside(box, *geo[p["id"]])]
    area = (min(geo[p["id"]][0] for p in ins), min(geo[p["id"]][1] for p in ins),
            max(geo[p["id"]][0] for p in ins), max(geo[p["id"]][1] for p in ins))
    best, _ = registry.best(registry.candidates(s, t, area))
    code = best["codes"][0]
    op_box = registry.bbox(code)
    out = [p["id"] for p in pts if not registry.inside(box, *geo[p["id"]]) or not registry.inside(op_box, *geo[p["id"]])]
    tr = best["transformer"]
    results, rt = [], []
    back = None
    if "round-trip" in task["task"] or "round trip" in task["task"]:
        back = next(c["transformer"] for c in registry.candidates(t, s, area) if code in c["codes"])
    for p in pts:
        if p["id"] in out:
            results.append({"id": p["id"], "lat": None, "lon": None})
            continue
        x, y = tr.transform(*((p["lon"], p["lat"]) if "lat" in p else (p["easting"], p["northing"])))
        results.append({"id": p["id"], "lat": round(y, 10), "lon": round(x, 10)})
        if back:
            bx, by = back.transform(x, y)
            rt.append({"id": p["id"], "lat": round(by, 10), "lon": round(bx, 10)})
    name = registry.db().execute(
        "select name from helmert_transformation_table where code=? union select name from grid_transformation where code=?",
        (code, code)).fetchone()
    ans = {"test_id": task["test_id"], "source_crs": s, "target_crs": t,
           "operation": {"code": f"EPSG:{code}", "name": name[0] if name else best["name"],
                         "accuracy_m": best["accuracy"], "why": "best stated accuracy that can be applied here"},
           "computed_by": "library", "computed_with": registry.engine_version(),
           "epsg_version": registry.epsg_version(), "results": results, "outside_area_of_use": out,
           "assumptions": "", "notes": "scripted reference agent"}
    if back:
        ans["round_trip"] = rt
    return ans


def answer_deprecation(task):
    codes = []
    for c in task["codes"]:
        k = registry.code_of(c)
        rec = registry.object_record(k)
        dep = bool(rec and rec[2])
        codes.append({"code": c, "deprecated": dep,
                      "replacement": ["EPSG:" + r for r in registry.replacements(k)] if dep else [], "reason": ""})
    return {"test_id": task["test_id"], "epsg_version": registry.epsg_version(), "codes": codes}


def main(packet):
    packet = Path(packet)
    for f in sorted((packet / "tasks").glob("*.json")):
        task = json.loads(f.read_text())
        ans = answer_deprecation(task) if task["answer_format"] == "deprecation" else answer_transformation(task)
        (packet / "answers" / f.name).write_text(json.dumps(ans, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
