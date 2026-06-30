# Phase 2 — LLM Provider Support

← Previous: [Automated Signal Resolver](automated-resolver.md) | [Phase 2 index](index.md) | Next: [Signals and Issues](signals-and-issues.md) →

## LLM provider support

The supported provider-adapter set in `run_check_agent.py` for signal generation is:

```text
groq
gemini
cerebras
sambanova
openrouter
```

The current scheduled signal-generation rotation does **not** include Groq. It contains these seven active provider/model slots:

```text
0 cerebras:gpt-oss-120b
1 sambanova:DeepSeek-V3.1
2 openrouter:nvidia/nemotron-3-ultra-550b-a55b:free
3 gemini:gemini-3.1-flash-lite
4 cerebras:zai-glm-4.7
5 sambanova:Meta-Llama-3.3-70B-Instruct
6 openrouter:poolside/laguna-m.1:free
```

Groq support code remains available for explicit future or manual use, but no Groq model is currently part of the active scheduled signal-generation rotation.

The automated resolver currently supports only:

```text
groq
gemini
```

| Provider | Adapter | API key |
|---|---|---|
| `groq` | `scripts/phase-2/providers/groq.py` | `GROQ_API_KEY` |
| `gemini` | `scripts/phase-2/providers/gemini.py` | `GEMINI_API_KEY` in GitHub Actions; `GEMINI_API_KEY` or `GOOGLE_API_KEY` locally |
| `cerebras` | `scripts/phase-2/providers/cerebras.py` | `CEREBRAS_API_KEY` |
| `sambanova` | `scripts/phase-2/providers/sambanova.py` | `SAMBANOVA_API_KEY` |
| `openrouter` | `scripts/phase-2/providers/openrouter.py` | `OPENROUTER_API_KEY` |

### Groq provider

Groq was the original provider for Phase 2 LLM check-agent generation.

The Groq adapter calls the Groq chat-completions API and uses:

```text
GROQ_API_KEY
```

The direct batch-runner defaults remain Groq-oriented in `run_check_batch.py`:

```text
provider: groq
models: llama-3.3-70b-versatile
```

Those direct runner defaults are legacy execution defaults, not the current scheduled signal-generation rotation. The canonical scheduled workflow no longer includes `groq:llama-3.3-70b-versatile` and does not add a replacement Groq model.

### Gemini provider

The Gemini adapter is:

```text
scripts/phase-2/providers/gemini.py
```

It uses the Google GenAI SDK:

```python
from google import genai
from google.genai import types
```

It calls Gemini through:

```python
client.models.generate_content(...)
```

Current scheduled Gemini signal-generation model:

```text
gemini-3.1-flash-lite
```

`gemini-2.5-flash` remains supported by provider-level reduced-thinking configuration and may be selected manually, but it is not the current scheduled Gemini default.

Signal-generation runs use a workflow default of:

```text
--max-completion-tokens 3000
```

The automated resolver remains separate. It defaults to primary `gemini-3.5-flash` with `--max-completion-tokens 8000`, and the resolver workflow can run one immediate fallback attempt with `gemini-2.5-flash` only for provider-unavailability or 503-like primary Gemini failures.

The Gemini adapter includes reduced-thinking configuration for strict-format output reliability:

| Model family | Thinking configuration |
|---|---|
| `gemini-2.5-flash*` | `types.ThinkingConfig(thinking_budget=0)` |
| `gemini-3.*` | `types.ThinkingConfig(thinking_level="low")` |

This setting improves strict-format output reliability but does not replace validation.

For current Phase 2 signal generation, `gemini-3.1-flash-lite` is the scheduled Gemini default. Other Gemini model names should not be added to the scheduled signal-generation rotation unless they are first verified operationally and documented.

### Cerebras provider

The Cerebras adapter is:

```text
scripts/phase-2/providers/cerebras.py
```

It uses the shared OpenAI-compatible provider utility:

```text
scripts/phase-2/providers/openai_compatible.py
```

Current scheduled Cerebras models:

```text
gpt-oss-120b
zai-glm-4.7
```

The adapter requires `CEREBRAS_API_KEY` and defaults to:

```text
https://api.cerebras.ai/v1
```

`CEREBRAS_BASE_URL` may override the base URL in local or alternate environments. For `zai-glm-4.7`, the adapter sends the documented GLM extra body configuration used by the repository.

### SambaNova provider

The SambaNova adapter is:

```text
scripts/phase-2/providers/sambanova.py
```

It also uses the shared OpenAI-compatible provider utility.

Current scheduled SambaNova models:

```text
DeepSeek-V3.1
Meta-Llama-3.3-70B-Instruct
```

The adapter requires `SAMBANOVA_API_KEY` and defaults to:

```text
https://api.sambanova.ai/v1
```

`SAMBANOVA_BASE_URL` may override the base URL in local or alternate environments.


### OpenRouter provider

The OpenRouter adapter is:

``` text
scripts/phase-2/providers/openrouter.py
```

It also uses the shared OpenAI-compatible provider utility.

Current scheduled OpenRouter models:

``` text
nvidia/nemotron-3-ultra-550b-a55b:free
poolside/laguna-m.1:free
```

The adapter requires `OPENROUTER_API_KEY` and currently allowlists only these two free OpenRouter model IDs. The scheduled workflow also validates selected OpenRouter models against this allowlist.

### Signal-generation provider retry and failure-classification behavior

The signal-generation providers include provider-level retry handling for transient provider/API failures.

This retry and failure-classification behavior does not select an alternate provider/model slot.

The configured provider retry delay for signal-generation providers is:

```text
15 seconds
```

Signal-generation providers make the initial request plus at most one retry for genuinely transient provider-side failures. Quota and rate-limit diagnostics are recognized separately and are not retried.

Current transient detection is marker-based and recognizes diagnostics containing values such as:

```text
500
502
503
504
service_unavailable
temporarily unavailable
timeout
too busy
overloaded
capacity
try again later
unavailable
```

Validation failures are not retried. A structurally invalid model output is treated as a rejected check-agent output or resolver failure, not as a transient provider failure.

### Automated resolver provider behavior

The automated resolver uses provider calls differently from scheduled signal generation.

For resolver runs:

- `resolve_signal_issue.py` defaults to `--provider-max-attempts 1`;
- the scheduled resolver workflow also passes `--provider-max-attempts 1`;
- no resolver provider retry or backoff loop occurs in the scheduled workflow;
- the workflow-level Gemini fallback is not a retry of the same model;
- the fallback is one immediate attempt with a second model, `gemini-2.5-flash`;
- fallback is restricted to primary Gemini provider-unavailability or 503-like failures;
- non-provider failures remain fatal.

This distinction is important: scheduled signal generation may use provider-level transient retry and nonfatal provider-failure classification, while automated signal resolution uses a narrower primary-model/fallback-model sequence and fails normally outside that sequence.

---

← Previous: [Automated Signal Resolver](automated-resolver.md) | [Phase 2 index](index.md) | Next: [Signals and Issues](signals-and-issues.md) →
