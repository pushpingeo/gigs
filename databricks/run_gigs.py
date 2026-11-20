# Databricks notebook source
# MAGIC %md
# MAGIC # GIGS for agents: run the pilot on Databricks
# MAGIC
# MAGIC This notebook builds a packet of coordinate tasks, lets a model served in this workspace work through them,
# MAGIC and grades the answers. Run the cells from top to bottom (Shift+Enter on each).
# MAGIC
# MAGIC Nothing leaves the workspace except the prompts sent to your own model serving endpoint. Results are written
# MAGIC into this Git folder under `results/`; nothing is pushed back to GitHub.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Install the two libraries it needs
# MAGIC `pyproj` (PROJ, the coordinate engine) and the Databricks SDK. Python restarts afterwards; that's expected.

# COMMAND ----------

# MAGIC %pip install pyproj "databricks-sdk[openai]"

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. See which models this workspace can use
# MAGIC Pick one of the names printed below for `ENDPOINT` in the next cell. Names starting `databricks-` are the
# MAGIC ready-made Foundation Model API endpoints.

# COMMAND ----------

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
for e in w.serving_endpoints.list():
    print(e.name)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Settings
# MAGIC - `ENDPOINT`: the model to test (from the list above).
# MAGIC - `SKILLS`: `True` gives the agent the two skills; `False` tests it without them.
# MAGIC - `SEED`: the same seed gives the same points and codes, so runs compare like for like. 101 matches the
# MAGIC   published runs.

# COMMAND ----------

ENDPOINT = "databricks-claude-sonnet-4-5"   # change to a name from the list above
SKILLS = True
SEED = 101

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Run and grade
# MAGIC Takes a few minutes. The agent reads the tasks, runs Python with pyproj, and writes its answers; then the
# MAGIC grader scores them.

# COMMAND ----------

import json, os, sys
from pathlib import Path

ROOT = Path(os.getcwd()).parent          # this notebook sits in <repo>/databricks/
sys.path.insert(0, str(ROOT))
from harness import agents, grade, packet

label = f"{ENDPOINT}-{'skills' if SKILLS else 'no-skills'}-databricks"
run_dir = ROOT / "runs" / label
_, meta = packet.build(run_dir, SEED, "pilot", SKILLS)
print("Packet built, seed", meta["seed"])

client = w.serving_endpoints.get_open_ai_client()
info = agents.run_openai_compatible(run_dir / "packet", ENDPOINT, client=client)
info["agent"] = "Databricks model serving (built-in loop)"
(run_dir / "agent.json").write_text(json.dumps(info, indent=2))

scores = grade.grade(run_dir, ROOT / "results" / label, label)
print(scores["summary"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Read the report
# MAGIC Every check, with what the agent said and what was expected. The same file is saved at
# MAGIC `results/<label>/report.md`.

# COMMAND ----------

print((ROOT / "results" / label / "report.md").read_text())
