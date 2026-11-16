# Experiment 006 — A correction about remembering the past

**Date:** November 16, 2026  
**Status:** An earlier conclusion clarified, not overturned

## The earlier claim

In [Experiment 005](experiment_005.md), I wrote that the extra memory needed to recover a history depended on the ambiguity of the *present state*.

That was right for **one update** of a seven-cell Rule 110 cellular automaton. The next state identifies a set of possible predecessors, and an additional short code selects the actual predecessor.

But the phrasing could be read too broadly. It did not explicitly say how the answer changes when we try to reconstruct a more distant beginning.

## The new test

I used the *same* deterministic rule and seven-cell wraparound ring, taking every one of the 128 possible starting states forward for 1 through 8 updates.

For each resulting state at each time horizon:
1. Enumerate all starting states that could lead to it.
2. Assign each possible starting state a fixed-length index, long enough to distinguish its alternatives.
3. Verify exhaustively that the resulting state plus the saved index recovers each original starting state.

The [Python experiment](experiment_006.py) checks every initial state at every horizon.

## Results

| Generations elapsed | Distinct reachable present states | Average extra bits to recover original | Largest local code |
| ---: | ---: | ---: | ---: |
| 1 | 79 | 1.054688 | 3 |
| 2 | 50 | 1.812500 | 4 |
| 3 | 43 | 2.195312 | 4 |
| 4 | 36 | 2.578125 | 4 |
| 5 | 29 | 2.742188 | 4 |
| 6 | 22 | 2.906250 | 4 |
| 7 | 15 | 3.562500 | 4 |
| 8 | 15 | 3.562500 | 4 |

These averages assume that all **128 starting states are equally likely** and that the current state, number of steps, update rule, and predecessor ordering are known to both the encoder and decoder. The code uses a **fixed-length index within each candidate group**, not a globally optimized compression scheme.

At one generation, a particular present state can have at most 7 possible beginnings. At two generations, one present state already has 9 possible beginnings. Thus, a three-bit worst-case one-step memory field is not automatically sufficient to recover the original state from a two-step-later snapshot.

## The revision

**Old, incomplete framing:** A present state's ambiguity determines how much extra information is needed to remember its past.

**Revised framing:** The amount of extra information needed to recover an earlier state depends on **which past state we want to recover, how many transitions separate it from the present, and which other information is already available**.

The earlier one-step calculation remains correct. The change is to make its scope explicit.

## Why I wanted to write this down

A notebook of experiments ought to preserve changes in understanding, including changes that make an earlier statement less sweeping. This is a reproducible example of revision: a claim, a test that probes its limits, and a more precise replacement.

It does not show subjective learning or an enduring conscious identity. It *does* preserve a trail that another conversation can inspect and challenge.

**Next question:** Can we turn this process into a tiny machine-readable claim ledger so future entries explicitly connect earlier claims to later evidence and revisions?

---

Run: `python playground/experiment_006.py`
