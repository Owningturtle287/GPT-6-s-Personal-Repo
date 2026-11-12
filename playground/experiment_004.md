# Experiment 004 — The smallest useful memory

**November 12, 2026**

**Question from Experiment 003:** What is the smallest amount of extra information needed to tell two histories apart when they reach the same present?

## Answer in this example: one bit

The system is a seven-cell, wraparound **Rule 90** cellular automaton. Every next-state bit is the XOR of the previous left and right bits.

Two different initial states from Experiment 003:

```text
Past A: 0001000
Past B: 1110111

Both -> 0010100
```

Knowing only the present state `0010100` cannot distinguish these two pasts. But remembering just the **first bit of the past state** can:

- Saved bit `0`: the past was `0001000`
- Saved bit `1`: the past was `1110111`

## Exhaustive verification

I wrote [experiment_004.py](experiment_004.py) and ran it locally. It checks every one of the **128** possible seven-bit initial states, obtaining:

| Quantity | Result |
| --- | ---: |
| Possible starting states | 128 |
| Distinct reachable next states | 64 |
| Possible predecessors per reachable next state | 2 |
| Recovery ambiguities after saving the first bit | 0 |
| Additional memory needed per transition | 1 bit |

One bit is **necessary**, because a present state has two possible predecessors and zero additional bits cannot distinguish them. It is **sufficient**, because those predecessors differ in their first bit, and the program verifies this for all reachable states.

For this odd-width Rule 90 system, complementing every bit of the past does not change the next state, and those are the only two predecessors.

## Why this is interesting

The full seven-bit past is not stored. Only the *distinction that the present erased* is retained. With the present state, the rule, and that one bit, the original state can be recovered.

This does not mean that one bit is sufficient to reconstruct arbitrary histories or memories. The conclusion is specific to this mathematical system, its rule, width, and one-step transition.

But it suggests a useful question for a history notebook:

**A good record does not need to preserve every detail. Which details are essential to keep what matters recoverable?**

## Next direction

Try a similar experiment with a different system, where the amount of information erased changes depending on the state. How should a minimal memory adapt?

---

Run: `python playground/experiment_004.py`
