# Phase 2 Gemini provider support

This add-on introduces Google Gemini as an alternative provider for the existing Phase 2 LLM check agents.

## Supported providers

| Provider | Adapter | Required environment variable |
|---|---|---|
| `groq` | `scripts/phase-2/providers/groq.py` | `GROQ_API_KEY` |
| `gemini` | `scripts/phase-2/providers/gemini.py` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |

## Local Gemini smoke test

```bash
export GEMINI_API_KEY="..."

python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider gemini \
  --model gemini-3.5-flash \
  --mode generate \
  --max-runs 1 \
  --allow-rejected-check-outputs
```

## Manual GitHub Actions smoke test

Use the `Scheduled check-agent signal collector` workflow with these manual inputs:

```text
mode: generate
provider: gemini
models: gemini-3.5-flash
agents: page-hygiene-checker
pages: docs/stereotypes/classes/event.md
max_runs: 1
```

If `provider` is set to `gemini` and the model input is left at the Groq default, the workflow substitutes `gemini-3.5-flash` for that run.

## Notes

- Scheduled runs still default to `groq` when no manual `provider` input is present.
- Gemini uses the same provider adapter contract as Groq: `generate_review(...) -> str`.
- The Gemini adapter intentionally does not set temperature. It relies on the prompt contract and existing output validator.
- Gemini outputs are routed separately because stable comment identity already includes `provider` and `model`.
