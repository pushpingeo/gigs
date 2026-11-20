"""Write results/index.json: a summary of every run, read by the explanation page (index.html)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    runs = []
    for d in sorted((ROOT / "results").glob("*/")):
        f = d / "scores.json"
        if not f.exists():
            continue
        s = json.loads(f.read_text())
        title = (d / "report.md").read_text().splitlines()[0].replace("# Run", "").strip() if (d / "report.md").exists() else d.name
        tests = []
        for t in s["tests"]:
            p = sum(c["result"] == "pass" for c in t["checks"])
            n = sum(c["result"] in ("pass", "fail") for c in t["checks"])
            tests.append({"id": t["test_id"], "title": t["title"], "passed": p, "total": n,
                          "fails": [c for c in t["checks"] if c["result"] == "fail"],
                          "not_verified": [c for c in t["checks"] if c["result"] == "n/a"]})
        a = s.get("agent", {})
        runs.append({"id": d.name, "label": title, "agent": a.get("agent"), "model": a.get("model"),
                     "skills": s["run"].get("skills", True), "seed": s["run"]["seed"], "created": s["run"]["created"],
                     "grader": f"{s['run']['grader_engine']}, EPSG {s['run']['grader_registry']}",
                     "summary": s["summary"], "usage": a.get("usage"), "tests": tests})
    (ROOT / "results" / "index.json").write_text(json.dumps({"runs": runs}, indent=1))
    print(len(runs), "runs")


if __name__ == "__main__":
    main()
