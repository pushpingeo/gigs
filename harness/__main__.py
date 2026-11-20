"""python -m harness <command>

  build  [--seed N] [--no-skills] [--series pilot]       make a packet in runs/<id>/packet and stop
  grade  runs/<id> [--label L]                            grade a finished packet into results/<id>/
  run    --agent files|command|claude-api [--cmd ...] [--model ...] [--seed N] [--no-skills] [--label L]
"""
import argparse
import datetime as dt
import json
from pathlib import Path

from . import agents, grade, packet

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(prog="python -m harness")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "run"):
        p = sub.add_parser(name)
        p.add_argument("--seed", type=int)
        p.add_argument("--series", default="pilot")
        p.add_argument("--no-skills", action="store_true")
        p.add_argument("--label")
        if name == "run":
            p.add_argument("--agent", choices=["files", "command", "claude-api"], required=True)
            p.add_argument("--cmd", help="shell command for --agent command; runs in the packet folder")
            p.add_argument("--model", default="claude-haiku-5-5")
    g = sub.add_parser("grade")
    g.add_argument("run_dir")
    g.add_argument("--label")
    a = ap.parse_args()

    if a.cmd == "grade":
        run = Path(a.run_dir)
        res = ROOT / "results" / run.name
        s = grade.grade(run, res, a.label or run.name)
        print(json.dumps(s["summary"]), "->", res / "report.md")
        return

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    label = a.label or (a.agent if a.cmd == "run" else "manual")
    run = ROOT / "runs" / f"{stamp}-{label}"
    _, meta = packet.build(run, a.seed, a.series, not a.no_skills)
    print("packet:", run / "packet", "seed", meta["seed"])
    if a.cmd == "build" or a.agent == "files":
        print(f"Point your agent at {run / 'packet'} (\"{agents.KICKOFF}\"), then: python -m harness grade {run}")
        return
    if a.agent == "command":
        info = agents.run_command(run / "packet", a.cmd)
    else:
        info = agents.run_claude_api(run / "packet", a.model)
    (run / "agent.json").write_text(json.dumps(info, indent=2))
    res = ROOT / "results" / run.name
    s = grade.grade(run, res, label)
    if info.get("log"):
        (res / "agent-log.json").write_text(json.dumps(info["log"], indent=2))
    print(json.dumps(s["summary"]), "->", res / "report.md")


if __name__ == "__main__":
    main()
