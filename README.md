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
| What product to build (discovery, not implementation) | `interview-to-build` |
| System prompt that keeps ignoring rules | `system-prompt-sop` |
| UI / image / video generation without a design spec | `design-context` |
| Pitch, cold email, landing copy, deck opener, value prop | `plain-sales-copy` |
| Campaign / multimedia from a marketing-director brief | `marketing-director` |
| Feature or bugfix through spec → code → evidence | `agentic-dev-e2e` |
| Create or eval a new skill | `skill-creator` |
| Graduate or deprecate a rule from real usage | `skill-evolution` |
| Turn HITL corrections into a versioned skill | `conversation-to-skills` |
| Interview the user and maintain reusable personas | `interview-to-personas` |
| Learn a domain to ~80% practitioner | `learn-anything-about-x` |
| Local generate / read / memory | `agent-plugin/` |

Upstream of implementation: decide, then specify, then build. `skill-creator`
owns short-cycle skill drafts; `skill-evolution` owns long-cycle case-driven change.

## Decide

High-stakes thinking before anyone writes code.

| Skill | Purpose |
|---|---|
| `meta-thinking-framework` | Six-lens analysis for complex, irreversible decisions |
| `interview-to-build` | Map builder intuition onto a grounded discovery process |

## Specify

Turn a decision into a checkable contract.

| Skill | Purpose |
|---|---|
| `system-prompt-sop` | Route each prompt constraint to its enforcement layer |
| `design-context` | Design-context gate before frontend or visual generation |
| `plain-sales-copy` | 3-5 sentence sales/business copy: no puff, four elements, "tell me more" |
| `marketing-director` | Five-dimension brief, then multimedia with one job per asset |

## Build

Execute and review work in a repo.

| Skill | Purpose |
|---|---|
| `agentic-dev-e2e` | End-to-end feature development and bug-fix workflow |

## Meta

Skills that create, evolve, or extract other skills and workflows.

| Skill | Purpose |
|---|---|
| `skill-creator` | Create and evaluate agent skills (L0 generation, L1 evals) |
| `skill-evolution` | Evolve skills from real usage evidence (L2 + L3) |
| `conversation-to-skills` | Turn human corrections into versioned skills |
| `interview-to-personas` | Interview users and store reusable collaboration personas |

## Learn

| Skill | Purpose |
|---|---|
| `learn-anything-about-x` | Adaptive domain mentor for structured learning |

## Agent Plugin

`agent-plugin/` bundles eight runtime capabilities for local agents:

| Skill | Purpose |
|---|---|
| `generate-image` | Generate or edit raster images via OpenRouter |
| `generate-video` | Generate video jobs via OpenRouter |
| `generate-text` | Generate text via OpenRouter |
| `generate-audio` | Generate speech via OpenRouter |
| `read-image` | Answer questions about local images |
| `read-video` | Answer questions about local or remote video |
| `read-audio` | Transcribe or analyze local audio |
| `agent-memory` | Five-duty memory protocol (working / semantic / episodic / procedural / personas) |

Entry points:

- `scripts/openrouter.py` -- provider adapter for all cloud-capable skills
- `scripts/doctor.py` -- runtime prerequisite check

Storage:

- Project-local default: `./.agents/`
- Global opt-in: `~/.agents/`
- Generated media, artifacts, and approvals live under the selected root.
- Agent memory uses markdown drawers under `.agents/memory/`; no database is required.
- Persona memory uses `.agents/memory/personas/` and follows `interview-to-personas`.
- `~/.agents/skills/` is reserved for installed skills and is never overwritten by runtime state.

## Installation

To install the full pack, copy `agent-plugin/` into your project:

```bash
cp -R agent-plugin ./.agents/skills/
```

To install a single skill, copy just its directory:

```bash
cp -R agent-plugin/agent-memory ./.agents/skills/agent-memory
```

To install a protocol skill from the repo root:

```bash
cp -R meta-thinking-framework ./.agents/skills/meta-thinking-framework
```

To install the memory drawer templates:

```bash
cp -R agent-plugin/templates/memory ./.agents/memory
```

To install persona memory support, also copy:

```bash
cp -R interview-to-personas ./.agents/skills/interview-to-personas
```

Configure the provider:

```bash
cp agent-plugin/templates/openrouter.config.json .agents/openrouter.config.json
export OPENROUTER_API_KEY="your-key"
```

## Runtime

The OpenRouter adapter is zero-dependency Python 3. Run from the pack root:

```bash
python3 scripts/doctor.py
python3 scripts/openrouter.py --help
```

Tests:

```bash
pytest agent-plugin/tests
```

## Philosophy

Every skill is an independent capability. Shared contracts (`provider-contract`,
`storage-schema`, `privacy-policy`, `output-contract`) keep them composable
without coupling. Local-first means the adapter refuses cloud calls without
explicit approval, and all generated state stays on disk in a predictable layout.
