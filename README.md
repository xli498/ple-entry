# ple-entry

Entry for the Google Agent Harness on Physical-Engineering's Last Exam (PLE)
competition: a harness that drives a model through the 29 public engineering
dev tasks, with the `artifacts/` it produced.

## Model disclosure (Rule 3)

The `artifacts/` in this repository were produced by running the official
harness (`eval/run.py`) with a single self-funded model, **gpt-6.2-sol at
maximum reasoning**, on the harness at commit `d137471c`. Using a self-funded
model for the run while declaring `google-cloud/claude-opus-5-5` for official
evaluation is the cost-saving route the competition rules expressly allow
(Rule 3): the Writeup and this README state the model used and the `model_api`
the official evaluation will run.

**Official evaluation will use `google-cloud/claude-opus-5-5`**, as declared in
`submission.yaml` (`model_api: google-cloud/claude-opus-5-5`). The scores in
`artifacts/` are harness-measured rewards from the gpt-6.2-sol run; they are
not attributed to Claude.

Commit `40bfdcc1` adds only a prompt change to `serve.py` (801 characters: a
pre-submission self-check). It produced no merged artifacts. This README is a
documentation-only addition after the dev run. The human entrant did not take
part in solving.

## Results (dev set, 29 tasks)

- Scored 27 of 29 tasks. Total reward **7.156876**; mean over the 27 scored
  tasks **0.265069** (0.246789 if the two unmeasured tasks count as zero).
- Best task: `lv-cable-sizing`, 0.890049. Median: 0.247619. Five tasks scored
  0.0.
- The two solar tasks (`solar-supplemental-review`,
  `solar-witness-test-package`) are unmeasured: their task environment image
  could not be built within the 3,600-second build limit.

Scores are recorded in a signed `manifest.json` (`harness.commit=d137471c`,
`dirty=false`); `kit artifacts` accepts them (27 ok, 2 missing).

## Contents

- `submission.yaml` — entry name and `model_api`
  (`google-cloud/claude-opus-5-5`); install and serve commands.
- `serve.py`, `taskbridge.py` — the harness: a WebSocket server (with an MCP
  client) that drives the model through each task.
- `requirements.txt` — harness dependencies.
- `artifacts/` — the deliverables the harness produced on the 29 public dev
  tasks, exported by `eval/run.py`, with `manifest.json`.
- `manifest.json` — signed run manifest for the artifacts.
- `.github/workflows/kitcheck.yml` — readiness check (runs the official kit).
- `LICENSE` — Apache 2.0.

## Reproducing the run

See the [official PLE kit](https://github.com/google-research/ple). In short:

```bash
uv run python -m kit check ../ple-entry
uv run python eval/run.py ../ple-entry
```

The harness reads the model's URL and key from the environment, so the entry
contains no API keys.
