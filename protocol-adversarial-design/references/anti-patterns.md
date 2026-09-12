# Anti-patterns

## 1. Whole-system modeling

**Looks like:** "Let's TLA+ the entire agent / service."  
**Why it dies:** State space explosion; learner quits before first insight.  
**Do:** One thin protocol slice; ≤ ~15 variables.

## 2. Dual truth

**Looks like:** Invariants that mention both `workspace` and `pathJail` as peers.  
**Why it dies:** Model encodes the bug (ambiguous authority).  
**Do:** One source predicate; derived guards must be entailed or absent.

## 3. Formalism halo

**Looks like:** "TLC green ⇒ production safe" or "script enumerator green ⇒ production safe."  
**Why it dies:** Gaps in the model (symlink, TOCTOU, human ops) stay invisible.  
**Do:** Always list uncovered surfaces; keep human/adversarial QA for outside-model attacks.

## 3b. Language / tool canon

**Looks like:** Skill run insists on TypeScript (or Python, or TLA+) as the only
valid explore backend.  
**Why it dies:** Binds the SOP to a stack; fights the repo; confuses spirit with tooling.  
**Do:** Pick any runner that can check Inv and print a trace; default remains the table.

## 4. Test-case cosplay

**Looks like:** A single happy-path scenario labeled as the "spec."  
**Why it dies:** No exploration power; false confidence.  
**Do:** Rules (Init/Next) + invariant; let exploration generate paths.

## 5. Skipping the gate

**Looks like:** Modeling CRUD or UI because the skill sounded cool.  
**Why it dies:** Negative EV; skill reputation burns.  
**Do:** STOP with alternative.

## 6. Fix-the-trace-with-an-if

**Looks like:** Counterexample → sprinkle another conditional without revisiting precedence.  
**Why it dies:** Whack-a-mole; dual truth returns.  
**Do:** Change the source rule; then simplify implementation.

## 7. Spec drift

**Looks like:** Code evolves; contract abandoned.  
**Why it dies:** Green checks on a lie.  
**Do:** Bind the spec to the **design decision**, not every refactor. Re-run explore when the invariant or movers change.

## 8. Colliding with meta-thinking

**Looks like:** Using this skill for "should we build X?" product calls.  
**Why it dies:** Wrong tool; muddy triggers.  
**Do:** `meta-thinking-framework` for fuzzy decisions; this skill after the protocol is named.
