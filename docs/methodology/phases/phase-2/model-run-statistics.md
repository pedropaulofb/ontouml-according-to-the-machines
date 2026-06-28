# Phase 2 — Check-agent Model Run Statistics

This page documents the cumulative model-run statistics added for the scheduled check-agent signal collector.

## Purpose

The scheduled check-agent workflow rotates over provider/model specs. Before this change, checking whether a model was producing Python-valid check-agent output required inspecting individual workflow runs. The new statistics path keeps a compact cumulative table for the active provider/model rotation.

The table includes at least:

| Model | # called | # valid | # invalid |
|---|---:|---:|---:|

The implemented table also records provider, rejection/provider-failure counters, last status, last category, last run timestamp, and the completion-token cap used by the batch runner.

## Persistence strategy

The statistics are persisted in the body of a dedicated GitHub issue titled:

```text
Phase 2 check-agent model run statistics
```

This strategy was chosen instead of committing a repository file because the scheduled workflow runs every 20 minutes. A committed statistics file would create many noisy commits, require `contents: write`, and would be more exposed to branch-protection and merge-conflict issues.

The issue-body strategy uses the workflow's existing issue-write capability:

```yaml
permissions:
  contents: read
  issues: write
```

The issue body contains:

1. a hidden JSON state block used by `scripts/phase-2/model_run_statistics.py`; and
2. a visible Markdown table for quick human inspection.

## Data source

The statistics are derived from structured Python-side batch status data produced by:

```text
scripts/phase-2/run_check_batch.py --summary-json .tmp/phase-2/batch-summary.json
```

Validity is not inferred from LLM wording. A valid run is a run where `run_check_agent.py` completed successfully and its generated check-agent output passed deterministic Python validation.

The statistics updater reads:

```text
.tmp/phase-2/batch-summary.json
.tmp/phase-2/model-run-statistics/active-provider-model-specs.txt
```

The active provider/model specs file contains one provider/model spec per line. For the scheduled workflow, this is the complete active rotation, not only the selected model for the current run.

## Schema

The visible table records:

| Column | Meaning |
|---|---|
| `Provider` | Provider adapter name. |
| `Model` | Provider-specific model ID. |
| `# called` | Number of completed selected runs counted for this provider/model. |
| `# valid` | Number of completed runs where Python validation accepted the check-agent output. |
| `# invalid` | Number of completed runs where the selected provider/model did not produce Python-valid check-agent output. |
| `# rejected` | Count of generated check-agent outputs rejected by Python validation. |
| `# provider failed` | Count of provider/API failures before a usable output could be validated. |
| `# failed` | Count of runner-level failures classified as `failed`. |
| `Last status` | Most recent normalized status. |
| `Last category` | Most recent rejection/failure category when available. |
| `Last run UTC` | Timestamp from the structured batch summary. |
| `Completion cap` | Completion-token cap forwarded to `run_check_agent.py`. |

Token usage, prompt size, provider request limits, and completion-token usage are not stored because the current provider adapters do not expose these as reliable structured fields for successful responses. They should not be added through fragile parsing of provider diagnostics.

## Local smoke test

The smoke test should exercise counter increments directly. A `--plan-only` run is useful for planning and JSON-shape checks, but it does not create completed run records and therefore does not test `# called`, `# valid`, or `# invalid` increments.

From the repository root, create a synthetic structured summary:

```bash
mkdir -p .tmp/phase-2/model-run-statistics

cat > .tmp/phase-2/model-run-statistics/active-provider-model-specs.txt <<'EOF'
groq:llama-3.3-70b-versatile
openrouter:nvidia/nemotron-3-ultra-550b-a55b:free
EOF

cat > .tmp/phase-2/test-batch-summary.json <<'EOF'
{
  "schema_version": 1,
  "generated_at_utc": "2026-06-28T12:00:00+00:00",
  "mode": "post",
  "selection": "rotate",
  "rotation_seed": "hourly",
  "rotation_index": 123,
  "available_run_count": 2,
  "selected_run_count": 2,
  "completed_run_count": 2,
  "accepted_run_count": 1,
  "rejected_run_count": 0,
  "provider_failed_run_count": 1,
  "fatal_failed_run_count": 0,
  "plan_only": false,
  "max_completion_tokens": 3000,
  "planned_runs": [],
  "completed_runs": [
    {
      "planned": {
        "index": 1,
        "page": "docs/stereotypes/classes/event.md",
        "agent": "page-hygiene-checker",
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "output_path": ".tmp/phase-2/page.md",
        "log_path": ".tmp/phase-2/page.batch.log"
      },
      "check_status": "ok",
      "check_exit_code": 0,
      "issue_status": "skipped",
      "issue_exit_code": null,
      "message": "completed successfully.",
      "provider_failure_is_nonfatal": false,
      "provider_failure_kind": null,
      "rejected": false,
      "provider_failed": false,
      "fatal_failed": false
    },
    {
      "planned": {
        "index": 2,
        "page": "docs/stereotypes/classes/event.md",
        "agent": "page-hygiene-checker",
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "output_path": ".tmp/phase-2/openrouter.md",
        "log_path": ".tmp/phase-2/openrouter.batch.log"
      },
      "check_status": "provider_failed",
      "check_exit_code": 1,
      "issue_status": "skipped",
      "issue_exit_code": null,
      "message": "Provider call failed. Reason: provider_unavailable.",
      "provider_failure_is_nonfatal": true,
      "provider_failure_kind": "provider_unavailable",
      "rejected": false,
      "provider_failed": true,
      "fatal_failed": false
    }
  ]
}
EOF

python scripts/phase-2/model_run_statistics.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --summary-json .tmp/phase-2/test-batch-summary.json \
  --provider-model-specs-file .tmp/phase-2/model-run-statistics/active-provider-model-specs.txt \
  --workflow-run-id local-smoke \
  --workflow-run-attempt 1 \
  --dry-run
```

Expected result:

- `groq:llama-3.3-70b-versatile` has `# called = 1`, `# valid = 1`, `# invalid = 0`.
- `openrouter:nvidia/nemotron-3-ultra-550b-a55b:free` has `# called = 1`, `# valid = 0`, `# invalid = 1`, `# provider failed = 1`.

## Limitations

- Issue-body persistence avoids noisy commits but can lose an update if two overlapping workflow runs read, modify, and write the issue body concurrently.
- Re-running the same workflow run attempt is idempotent through hidden processed-run fingerprints. Only the most recent fingerprints are retained to keep the issue body compact. A different workflow attempt is counted as a separate execution.
- Provider failures count as invalid because the selected provider/model did not produce Python-valid check-agent output. The separate provider-failure counters preserve that distinction.
- Token usage and provider quota metrics are intentionally omitted until provider adapters expose them as structured, reliable data.
