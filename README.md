# agents-stack

A collection of composable agent skills, built for local-first execution and
portable deployment.

Each directory is a standalone skill with its own `SKILL.md` protocol. Most
skills can be copied into any repo independently. Directories stay at the repo
root on purpose — grouping is by job, not by extra path depth.

## Pick a skill

| If you need | Use |
|---|---|
| Fuzzy product / business / architecture decision | `meta-thinking-framework` |
| "What will happen?" probability or a calibrated refusal | `epistemic-boundary-oracle` |
| Multi-party entry strategy with playbooks | `structural-decision-stress-test` |
| What product to build (discovery, not implementation) | `interview-to-build` |
| High-risk protocol races / state machines | `protocol-adversarial-design` |
| System prompt that keeps ignoring rules | `system-prompt-sop` |
| UI / image / video generation without a design spec | `design-context` |
| Pitch, cold email, landing copy, deck opener, value prop | `plain-sales-copy` |
| Feature or bugfix through spec → code → evidence | `agentic-dev-e2e` |
| Review an AI refactor / architecture proposal | `refactor-review` |
| Create or eval a new skill | `skill-creator` |
| Graduate or deprecate a rule from real usage | `skill-evolution` |
| Turn HITL corrections into a versioned workflow | `feedback2workflow` |
| Learn a domain to ~80% practitioner | `learn-anything-about-x` |
| Local generate / read / RAG / memory | `local-agent-pack/` |

Upstream of implementation: decide, then specify, then build. `epistemic-boundary-oracle`
routes uncalibratable futures to `structural-decision-stress-test`. `skill-creator`
owns short-cycle skill drafts; `skill-evolution` owns long-cycle case-driven change.

## Decide

High-stakes thinking before anyone writes code.

| Skill | Purpose |
|---|---|
| `meta-thinking-framework` | Six-lens analysis for complex, irreversible decisions |
| `epistemic-boundary-oracle` | Prediction routing with domain-class boundaries |
| `structural-decision-stress-test` | Multi-agent stress test for entry strategy |
| `interview-to-build` | Map builder intuition onto a grounded discovery process |

## Specify

Turn a decision into a checkable contract.

| Skill | Purpose |
|---|---|
| `protocol-adversarial-design` | Design-time contracts for high-risk protocols |
| `system-prompt-sop` | Route each prompt constraint to its enforcement layer |
| `design-context` | Design-context gate before frontend or visual generation |
| `plain-sales-copy` | 3-5 sentence sales/business copy: no puff, four elements, "tell me more" |

## Build

Execute and review work in a repo.

| Skill | Purpose |
|---|---|
| `agentic-dev-e2e` | End-to-end feature development and bug-fix workflow |
| `refactor-review` | Structured review of AI-proposed refactors |

## Meta

Skills that create, evolve, or extract other skills and workflows.

| Skill | Purpose |
|---|---|
| `skill-creator` | Create and evaluate agent skills (L0 generation, L1 evals) |
| `skill-evolution` | Evolve skills from real usage evidence (L2 + L3) |
| `feedback2workflow` | Turn human corrections into versioned workflow learning |

## Learn

| Skill | Purpose |
|---|---|
| `learn-anything-about-x` | Adaptive domain mentor for structured learning |

## Local Agent Pack

`local-agent-pack/` bundles nine runtime capabilities for local agents:

| Skill | Purpose |
|---|---|
| `generate-image` | Generate or edit raster images via OpenRouter |
| `generate-video` | Generate video jobs via OpenRouter |
| `generate-text` | Generate text via OpenRouter |
| `generate-audio` | Generate speech via OpenRouter |
| `read-image` | Answer questions about local images |
| `read-video` | Answer questions about local or remote video |
| `read-audio` | Transcribe or analyze local audio |
| `local-rag` | SQLite FTS5 multimedia retrieval with source locators and citations |
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

To install a protocol skill from the repo root:

```bash
cp -R meta-thinking-framework ./.agents/skills/meta-thinking-framework
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
