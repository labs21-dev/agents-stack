# agents-stack

A collection of composable agent skills, built for local-first execution and
portable deployment.

## Skills

Each directory is a standalone skill with its own `SKILL.md` protocol.
Most skills can be copied into any repo independently.

| Skill | Purpose |
|---|---|
| `agentic-dev-e2e` | End-to-end feature development and bug-fix workflow |
| `design-context` | Design context gating before frontend or visual generation |
| `epistemic-boundary-oracle` | Prediction routing with domain-class boundaries |
| `feedback2workflow` | Turn human corrections into versioned workflow learning |
| `interview-to-build` | Map builder intuition to a grounded discovery process |
| `learn-anything-about-x` | Adaptive domain mentor for structured learning |
| `meta-thinking-framework` | Six-lens deep analysis for complex decisions |
| `protocol-adversarial-design` | Design-time contracts for high-risk protocols |
| `refactor-review` | Structured review of AI-proposed refactors |
| `skill-creator` | Create and evaluate agent skills |
| `skill-evolution` | Evolve skills from real usage evidence |
| `structural-decision-stress-test` | Multi-agent stress test for entry strategy |
| `system-prompt-sop` | Design-time SOP for system prompt constraint routing |

## Local Agent Pack

`local-agent-pack/` bundles nine capabilities for local agents:

| Skill | Purpose |
|---|---|
| `generate-image` | Generate or edit raster images via OpenRouter |
| `generate-video` | Generate video jobs via OpenRouter |
| `generate-text` | Generate text via OpenRouter |
| `generate-audio` | Generate speech via OpenRouter |
| `read-image` | Answer questions about local images |
| `read-video` | Answer questions about local or remote video |
| `read-audio` | Transcribe or analyze local audio |
| `local-rag` | SQLite FTS5 retrieval over project files with citations |
| `agent-memory` | Four-duty memory protocol (working / semantic / episodic / procedural) |

Entry points:

- `scripts/openrouter.py` -- provider adapter for all cloud-capable skills
- `scripts/rag.py` -- zero-dependency local RAG index and query
- `scripts/doctor.py` -- runtime prerequisite check

Storage:

- Project-local default: `./.agents/`
- Global opt-in: `~/.agents/`
- Generated media, artifacts, approvals, and indexes live under the selected root.
- Agent memory uses markdown drawers under `.agents/memory/`; no database is required.
- `~/.agents/skills/` is reserved for installed skills and is never overwritten by runtime state.

## Installation

To install the full pack, copy `local-agent-pack/` into your project:

```bash
cp -R local-agent-pack ./.agents/skills/
```

To install a single skill, copy just its directory:

```bash
cp -R local-agent-pack/agent-memory ./.agents/skills/agent-memory
```

To install the memory drawer templates:

```bash
cp -R local-agent-pack/templates/memory ./.agents/memory
```

Configure the provider:

```bash
cp local-agent-pack/templates/openrouter.config.json .agents/openrouter.config.json
export OPENROUTER_API_KEY="your-key"
```

## Runtime

The OpenRouter adapter is zero-dependency Python 3. Run from the pack root:

```bash
python3 scripts/doctor.py
python3 scripts/openrouter.py --help
python3 scripts/rag.py --help
```

Tests:

```bash
pytest local-agent-pack/tests
```

## Philosophy

Every skill is an independent capability. Shared contracts (`provider-contract`,
`storage-schema`, `privacy-policy`, `output-contract`) keep them composable
without coupling. Local-first means the adapter refuses cloud calls without
explicit approval, and all generated state stays on disk in a predictable layout.
