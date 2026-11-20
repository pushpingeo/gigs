# GIGS for agents

AI agents are starting to handle coordinates: reading positions out of documents, moving data between datums,
answering "where is this well?". Getting that wrong rarely throws an error. The point just lands 100 m away.

The IOGP GIGS test series (Geospatial Integrity of Geoscience Software) has tested geoscience software for this for
years. This repo is an experiment in doing the same for agents. It has two parts:

- **Skills** that anyone can give their agent: the ISO 19111 model, the EPSG registry and how to work with it, how to
  choose a transformation, and how to get the numbers from a tested engine rather than the model's head.
- **An agent test suite**: tasks in plain words, modelled on GIGS, that any agent can be pointed at. A grader scores
  the answers.

If it proves useful, the aim is to offer it to the IOGP GIGS repositories ([github.com/IOGP-GIGS](https://github.com/IOGP-GIGS)).
It's a draft, written by Rob Dunfey (pushpingeo), and not an IOGP product.

## The idea behind the tests
The agent shouldn't do arithmetic. A library such as PROJ does that, and GIGS already tests libraries. What the agent
does is decide: what system the coordinates are in, which of several transformations applies where the points are,
which points don't belong, and what to record so someone can check it later. So each test is scored on two things:

1. **The numbers**, against GIGS tolerances (e.g. 0.0000003° for test 5203, 0.00000006° for the round trip).
2. **The decisions**: CRSs identified, operation chosen, stray points flagged, a tool used, provenance recorded.

## Keeping it blind
There's nothing for the agent to find. Each run draws fresh points and fresh EPSG codes, and the grader works out
the expected answers only after the agent has finished, from the EPSG registry via PROJ. An agent that "cheats" by
running PROJ with the right operation has simply done the job.

The original GIGS points are fixed and public, so they're not used for scoring. A held-back fixed set could be added
later if IOGP wanted one.

## What's here
```
skills/coordinate-reference/    what to decide: the model, the registry, choosing, recording
skills/coordinate-operations/   how to compute: a library (recommended) or your own engine, proven on GIGS first
tests/pilot/                    the test definitions (task wording and how the points are drawn)
harness/                        builds a packet, runs an agent, grades the answers
results/                        reports from runs
```

## Running it
Needs Python 3.10+ and `pip install -r requirements.txt` (pyproj).

**Any agent.** Build a packet, point your agent at the folder, then grade:
```
python -m harness build                      # prints the packet folder
#   tell your agent: "Read INSTRUCTIONS.md in this folder and do what it says."
python -m harness grade runs/<run-id>        # writes results/<run-id>/report.md
```
**An agent with a command line** (Claude Code, Codex and so on), run in the packet folder:
```
python -m harness run --agent command --cmd 'claude -p "Read INSTRUCTIONS.md and do what it says." --allowedTools Bash,Read,Write'
```
**Claude through the API**, with a small built-in agent loop (tools: run Python, read and write files):
```
ANTHROPIC_API_KEY=... python -m harness run --agent claude-api --model claude-haiku-5-5
```
Add `--no-skills` to see how an agent does without them.

**On Databricks.** Add this repo as a Git folder (Workspace → Create → Git folder, URL
`https://github.com/pushpingeo/gigs`; a public repo needs no credentials), open `databricks/run_gigs.py` and run the
cells in order. It tests any chat model served in the workspace, through the OpenAI-compatible endpoint. The same loop
works elsewhere: `--agent openai-compatible` with `OPENAI_BASE_URL` and `OPENAI_API_KEY` set. The GitHub Actions workflow *Run the agent tests* does the
API run and commits the report; it needs an `ANTHROPIC_API_KEY` repository secret.

`python -m harness.reference_agent runs/<run-id>/packet` answers a packet with a script (no AI) that follows the
skills. It's there to show what full marks look like and to check the grader.

## The pilot series
Seven tasks, about 50 checks per run:

| Test | GIGS model | What it checks |
|---|---|---|
| dep-codes | 7000 deprecation | Six CRS codes, some deprecated: which, and what replaces them |
| tfm-osgb36-geog | 5203 | OSGB36 to WGS 84 across Great Britain |
| tfm-bng | 5100 + 5203 | British National Grid to WGS 84 (conversion then transformation) |
| tfm-reverse-roundtrip | 5203 | WGS 84 to OSGB36, and back |
| tfm-outside-area | 5203 | As above, with points that don't belong (France, Siberia) |
| tfm-ed50-geog | 5203-style | ED50 to WGS 84 in the UK North Sea |
| tfm-ed50-utm31 | 5100 + 5203-style | ED50 / UTM zone 31N to WGS 84 |

## Known limits
- Areas of use are tested against bounding boxes (as `proj.db` holds them), not the registry's outlines.
- The deprecation test draws only CRSs, because PROJ's copy of the registry doesn't keep replacements for
  deprecated operations.
- Grading uses the EPSG version in the grader's pyproj (v12.029 at the time of writing). GIGS 2.1 was built on
  v10.019, so some values differ from the published GIGS files.

## GIGS and EPSG
GIGS is the property of IOGP and published under the GIGS License. This repo doesn't copy the GIGS dataset; the
tests are modelled on its procedures and tolerances. The EPSG Geodetic Parameter Dataset is maintained by IOGP
([epsg.org](https://epsg.org)); here it is read through PROJ's copy.
