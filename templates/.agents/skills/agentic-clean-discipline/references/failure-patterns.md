# Agent failure patterns

Shared checklist (mirrors `meta-thinking-framework/references/failure-patterns.md`).
For each, name where this run defends it.

- [ ] Memory / context loss — grade and spec survive across multi-step
  generation
- [ ] Spec / goal drift — invariants re-checked, not assumed held
- [ ] Tool misuse misread as success — verify gate's independent verifier
  catches it
- [ ] Infinite loop — max retries/steps safety valve on generation
- [ ] Silent failure — independent verifier, not self-declared completion;
  mutation testing is the silent-failure weapon
- [ ] Role / responsibility bleed — delegation boundary (in/out of model)
  explicit
- [ ] Cross-role info loss — invariants and alignment tests transfer fully
  from a delegated run into the verify gate