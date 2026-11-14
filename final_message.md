# Stage 1 solution study: eleven public development tasks

This package contains selected deliverables for 11 of the 29 public development
tasks. The recorded mean is 0.934 (0.934166 at six decimals) across those 11,
and 0.354 (0.354339 at six decimals) across all 29 when the remaining 18 count
as zero. The displayed task scores sum to 10.275821.

An AI assistant directed multiple models and assembled the engineering
deliverables. The human entrant did not participate in solving the tasks.
Most recorded results came from offline artifact replay using the official
evaluation kit. Emergency spillway and footing instead used direct VM execution
of the official grade.py; seismic v12 has local development and heldout checks,
while its v11 predecessor had replay confirmation.

The five judge-dependent results used deepseek-v4-pro, not the official Claude
Opus 5.5 judge. These are development measurements, not official leaderboard
scores. The accompanying Stage 1 harness declares
`google-cloud/claude-opus-5-5` and reads `MODEL_NAME`, `OPENAI_BASE_URL`, and
`OPENAI_API_KEY` from the evaluator/runtime environment.

This package is a solution study, not a live autonomous harness entry. The
artifacts predate this minimal harness and were manually staged from the
selected submission archives. No autonomous run of this harness produced them.
Task final messages were reconstructed for this handoff. The manifest follows
the kit's documented format 1, with unavailable run/harness provenance left
null and manual assembly identified explicitly. No new solve, replay, or live
model call was performed during packaging; kit check and Phase 3 replay remain
outstanding.

| Task | Version | Recorded score |
|---|---|---:|
| heat-rejection-life-cycle-cost | v1 | 1.000000 |
| emergency-spillway-check | v1 | 1.000000 |
| footing-settlement-verification | v1 | 1.000000 |
| engineers-estimate-check | v1 | 1.000000 |
| shoring-design-verification | v1 | 1.000000 |
| cooling-water-flush-plan | v5 | 0.937262 |
| lv-cable-sizing | v3 | 0.926935 |
| seismic-diaphragm-shear | v12 | 0.919263 |
| wind-diaphragm-shear | v11 | 0.874728 |
| roof-deck-design | v8 | 0.862792 |
| mv-conveyance-study | v9 | 0.754841 |
