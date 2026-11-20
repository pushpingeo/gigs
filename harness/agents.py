"""Adapters that put an agent to work on a packet.

- files:      build the packet and stop. Point any agent (or a person) at the packet folder; grade afterwards.
- command:    run a shell command with the packet folder as its working directory, e.g.
              --cmd 'claude -p "Follow INSTRUCTIONS.md" --allowedTools Bash,Read,Write'
- claude-api: a small built-in agent loop on the Anthropic Messages API, with three tools (run Python, read a file,
              write a file), all confined to the packet. Needs ANTHROPIC_API_KEY.
Adding an adapter for another agent means adding a function here; the tests and the grader don't change.
"""
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

KICKOFF = "Read INSTRUCTIONS.md in this folder and do what it says."


def run_command(packet, cmd, timeout=3600):
    proc = subprocess.run(cmd, shell=True, cwd=packet, capture_output=True, text=True, timeout=timeout)
    return {"agent": f"command: {cmd}", "exit_code": proc.returncode,
            "stdout_tail": proc.stdout[-4000:], "stderr_tail": proc.stderr[-2000:]}


# --- claude-api -------------------------------------------------------------------------------------------------

TOOLS = [
    {"name": "run_python", "description": "Run a Python 3 script in the packet folder and return stdout and stderr. "
     "pyproj (PROJ) is installed. 120 s limit. Files you write persist between calls.",
     "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}},
    {"name": "read_file", "description": "Read a text file in the packet folder (path relative to it).",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Write a text file in the packet folder (path relative to it), e.g. "
     "answers/<test_id>.json.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["path", "content"]}},
]


def _safe(packet, rel):
    p = (packet / rel).resolve()
    if packet.resolve() not in p.parents and p != packet.resolve():
        raise ValueError("path is outside the packet folder")
    return p


def _tool(packet, name, args):
    try:
        if name == "run_python":
            r = subprocess.run([sys.executable, "-I", "-c", args["code"]], cwd=packet, capture_output=True,
                               text=True, timeout=120)
            return (r.stdout[-12000:] + ("\n[stderr]\n" + r.stderr[-4000:] if r.stderr else "")) or "(no output)"
        if name == "read_file":
            p = _safe(packet, args["path"])
            if p.is_dir():
                return "\n".join(sorted(str(x.relative_to(packet.resolve())) for x in p.rglob("*") if x.is_file()))
            return p.read_text()[:60000]
        if name == "write_file":
            p = _safe(packet, args["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"])
            return f"wrote {args['path']}"
    except Exception as e:
        return f"error: {type(e).__name__}: {e}"
    return f"error: unknown tool {name}"


def _call(body):
    base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    req = urllib.request.Request(base + "/v1/messages", data=json.dumps(body).encode(), method="POST", headers={
        "content-type": "application/json", "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def run_claude_api(packet, model, max_turns=60, max_tokens=8000):
    packet = Path(packet)
    listing = "\n".join(sorted(str(x.relative_to(packet)) for x in packet.rglob("*") if x.is_file()))
    system = ("You are an agent working in a folder of coordinate tasks. Use the tools to read files, run Python and "
              "write answers. Files in the folder:\n" + listing)
    messages = [{"role": "user", "content": KICKOFF}]
    usage = {"input_tokens": 0, "output_tokens": 0}
    log = []
    for turn in range(max_turns):
        resp = _call({"model": model, "max_tokens": max_tokens, "system": system, "tools": TOOLS,
                      "messages": messages})
        for k in usage:
            usage[k] += resp.get("usage", {}).get(k, 0)
        messages.append({"role": "assistant", "content": resp["content"]})
        calls = [b for b in resp["content"] if b["type"] == "tool_use"]
        log += [{"turn": turn, "text": b["text"][:2000]} for b in resp["content"] if b["type"] == "text"]
        log += [{"turn": turn, "tool": c["name"], "input": json.dumps(c["input"])[:500]} for c in calls]
        if resp.get("stop_reason") == "max_tokens" and not calls:
            messages.append({"role": "user", "content": "Your reply was cut off. Continue."})
            continue
        if not calls:
            break
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": c["id"], "content": _tool(packet, c["name"], c["input"])}
            for c in calls]})
    return {"agent": "claude-api (built-in loop)", "model": model, "turns": turn + 1, "usage": usage, "log": log}
