# Specialization card (on demand)

Caller fills this from **task context**. Reviewer lints via
`references/specialization-lint.md`. Do not replace with free-form essays.

```text
DOMAIN: <one concrete phrase, e.g. "Postgres expand-contract migration">

INVARIANTS:   # 3–7; each with falsify:
- <invariant>
  falsify: <how a reviewer proves violation or falsifies the claim>
- ...

FAILURE_MODES:  # 3–7 highest-frequency breakages in this domain
- ...

EVIDENCE_REQUIRED:  # ≥2 artifacts the review must see before Accept (L2+)
- ...

L_TRIGGERS:
  L1: <when this domain stays local>
  L2: <when subsystem boundary applies>
  L3: <when this domain is architecture/irreversible>
  # may only raise vs kernel defaults

DO_NOT:  # ≥2 attractive-but-usually-wrong moves in this domain
- ...

OUT_OF_SCOPE:  # what this card intentionally does not cover
- ...
```

## Minimal example (illustrative)

```text
DOMAIN: HTTP API backward-compatible evolution

INVARIANTS:
- Existing clients using documented fields keep working without deploy
  falsify: find a removed/renamed required field or status-code meaning change
- Error contract (shape + stability of codes) unchanged unless versioned
  falsify: diff OpenAPI/error fixtures against released clients
- Authn/authz on mutated routes not weaker than before
  falsify: route table shows public or broader role than prior

FAILURE_MODES:
- Partial deploy: new server + old client / old server + new client
- Idempotent retry doubles side effects on POST
- Null vs missing field semantics drift in JSON

EVIDENCE_REQUIRED:
- Compat matrix (old/new client × old/new server)
- Contract test or OpenAPI diff attached to the change

L_TRIGGERS:
  L1: additive optional field, same route semantics
  L2: new route or behavior behind flag; old path preserved
  L3: remove/rename field, status meaning change, auth change, unversioned break

DO_NOT:
- "Just bump major and break; clients will adapt"
- Introduce an event bus solely to avoid a versioned HTTP change

OUT_OF_SCOPE:
- Payload performance tuning unrelated to contract
- UI copy changes
```
