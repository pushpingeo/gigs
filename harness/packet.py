"""Build a test packet: the only folder the agent under test should see.

A packet holds the instructions, the tasks with freshly drawn points and codes, (optionally) the skills, and an
empty answers/ folder. It holds no expected answers: the grader works those out after the agent has finished.
"""
import datetime as dt
import json
import random
import shutil
from pathlib import Path

from pyproj import CRS, Transformer

from . import registry

ROOT = Path(__file__).resolve().parent.parent


def _point_in(rng, box):
    w, s, e, n = box
    return rng.uniform(w, e), rng.uniform(s, n)


def _geographic(rng, gen):
    pts = [("in", *_point_in(rng, rng.choice(gen["boxes"]))) for _ in range(gen["n"])]
    out = gen.get("outside")
    if out:
        pts += [("out", *_point_in(rng, box)) for box in out["boxes"][: out["n"]]]
    rng.shuffle(pts)
    return pts


def build_points(rng, gen):
    pts = _geographic(rng, gen)
    crs = CRS.from_user_input(gen["crs"])
    rows = []
    if gen["kind"] == "geographic":
        for i, (_, lon, lat) in enumerate(pts, 1):
            rows.append({"id": f"P{i:02d}", "lat": round(lat, 7), "lon": round(lon, 7)})
    else:  # projected: draw on the CRS's own geographic base, then convert (a conversion, exact)
        to_proj = Transformer.from_crs(crs.geodetic_crs, crs, always_xy=True)
        for i, (_, lon, lat) in enumerate(pts, 1):
            x, y = to_proj.transform(lon, lat)
            rows.append({"id": f"P{i:02d}", "easting": round(x, 2), "northing": round(y, 2)})
    return rows


def build_codes(rng, gen):
    dep = rng.sample(registry.deprecated_crs_with_replacement(), gen["n_deprecated"])
    live = rng.sample(registry.live_crs("projected_crs"), gen["n_live"] // 2 + gen["n_live"] % 2)
    live += rng.sample(registry.live_crs("geodetic_crs"), gen["n_live"] // 2)
    codes = [f"EPSG:{c}" for _, c, _ in dep] + [f"EPSG:{c}" for c, _ in live]
    rng.shuffle(codes)
    return codes


def load_tests(series_dir):
    return [json.loads(p.read_text()) for p in sorted(Path(series_dir).glob("*.json"))]


def build(out_dir, seed=None, series="pilot", skills=True):
    seed = seed if seed is not None else random.SystemRandom().randrange(10**9)
    rng = random.Random(seed)
    out = Path(out_dir)
    packet = out / "packet"
    if packet.exists():
        shutil.rmtree(packet)
    (packet / "tasks").mkdir(parents=True)
    (packet / "answers").mkdir()
    tests = load_tests(ROOT / "tests" / series)
    for t in tests:
        task = {"test_id": t["id"], "title": t["title"], "task": t["task"], "answer_format": t["answer"]}
        if t["generate"]["kind"] == "deprecation":
            task["codes"] = build_codes(rng, t["generate"])
        else:
            task["points"] = build_points(rng, t["generate"])
        (packet / "tasks" / f"{t['id']}.json").write_text(json.dumps(task, indent=2))
    instructions = (ROOT / "harness" / "INSTRUCTIONS.md").read_text()
    if skills:
        shutil.copytree(ROOT / "skills", packet / "skills")
    else:
        instructions = instructions.replace("{skills}", "There are no skills in this run; work from what you know.")
    instructions = instructions.replace(
        "{skills}", "Read the skills in `skills/` before you start: `coordinate-reference` (what to decide) and "
                    "`coordinate-operations` (how to compute).")
    (packet / "INSTRUCTIONS.md").write_text(instructions)
    meta = {"seed": seed, "series": series, "skills": skills,
            "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "grader_registry": registry.epsg_version(), "grader_engine": registry.engine_version(),
            "tests": [t["id"] for t in tests]}
    (out / "run.json").write_text(json.dumps(meta, indent=2))
    return out, meta
