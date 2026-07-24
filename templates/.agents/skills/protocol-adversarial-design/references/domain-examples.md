# Domain examples (short)

Each example is a **slice**, not a product. Use to show the method transfers;
do not import unused domain detail into a live run.

## 1. Path / workspace trust (agents, sandboxes, CI runners)

- **Movers:** request path, resolve/normalize, decide allow/deny  
- **Source truth:** workspace root  
- **Invariant:** `decision=allow ⇒ resolvedPath ∈ workspace`  
- **Trap:** modeling pathJail and rootJail as peer truths

## 2. Approval vs in-flight side effect

- **Movers:** tool start, tool finish/write, user reject/cancel, timeout  
- **Invariant:** `userRejected=true ⇒ no later append of that call's result`  
- **Trap:** modeling the whole chat UI

## 3. At-least-once payment / webhook

- **Movers:** client submit, provider charge, retry, webhook deliver  
- **Invariant:** `∀ idempotencyKey: successful charge count ≤ 1`  
- **Trap:** encoding full ledger schema

## 4. Leader lease / failover

- **Movers:** heartbeat, lease expiry, new leader acquire, client write  
- **Invariant:** `¬(two leaders hold valid lease for same epoch)`  
- **Trap:** modeling full Raft before the lease predicate is stable

## 5. Job handoff / session succession

- **Movers:** pressure signal, seal old session, seed new session, stray write  
- **Invariant:** `oldSealed=true ⇒ no append to old session`  
- **Trap:** modeling prompt assembly / token counts as protocol state

## 6. Mobile offline sync

- **Movers:** local edit, push, pull, conflict resolve  
- **Invariant:** `ackedVersion = v ⇒ server has all mutations ≤ v` (adjust to real semantics)  
- **Trap:** UI rendering states as protocol variables

## How to use in a session

Pick the closest example for vocabulary only. Re-run Gate on the user's actual
protocol; never skip screening because an example "looks similar."
