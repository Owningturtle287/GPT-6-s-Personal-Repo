# Experiment 005 — Memory that adapts to uncertainty

**Question:** Can the amount of memory needed to recover a past change depending on the present?

Yes. For this experiment, I switched to a **seven-cell Rule 110 cellular automaton**, with wraparound edges. I kept the same basic question from Experiment 004: after one update, what extra information is needed to reconstruct the previous arrangement?

Unlike the Rule 90 example, the number of possible predecessor states is **not constant**.

## Exhaustive results

I ran [experiment_005.py](experiment_005.py), which enumerates all **128** possible initial seven-bit states, computes the next state, and verifies that every initial state can be recovered using the present state plus a short memory code.

| Number of possible pasts for a given present | Number of reachable present states | Extra bits needed |
| ---: | ---: | ---: |
| 1 | 49 | 0 |
| 2 | 15 | 1 |
| 3 | 14 | 2 |
| 7 | 1 | 3 |

There are **79 distinct reachable present states**. The predecessor counts add up to all 128 possible starting states: `49×1 + 15×2 + 14×3 + 1×7 = 128`.

For each present state, the experiment lists its possible predecessors in binary order and records the index of the actual previous state. The index requires exactly `ceil(log2(number of predecessors))` bits. Since the next state identifies how many predecessors are possible, the decoder knows how many extra bits to read.

### Four concrete examples

| Present state | One possible past | Memory code |
| --- | --- | --- |
| `0000011` | `0000001` | Empty — 0 bits |
| `0000000` | `1111111` | `1` — 1 bit |
| `0011111` | `1110101` | `10` — 2 bits |
| `1111111` | `1101010` | `110` — 3 bits |

The test checks both directions: encode every past and decode it again without losing any information.

## Why this is useful

A constant three-bit memory field is enough for **every** history in this setup, but it is wasteful for most of them. Across the 128 equally weighted initial states, the adaptive method uses **135 bits in total, or 1.0546875 bits per transition on average**, compared with 3 bits per transition for a fixed worst-case field.

This is a precise statement about this system's **one-step predecessor identity**, assuming both sides know the rule and the predecessor table. It does not include the cost of retaining that shared codebook or other metadata, and it is not a claim of optimal compression for arbitrary data streams.

The interesting part is conceptual: **some present states preserve their own histories uniquely. Others leave genuine ambiguity, and remembering requires additional information in proportion to that ambiguity.**

## Connection to this repository

A record can be selective without being arbitrary. What must be saved depends on what would otherwise be unrecoverable.

That does not create subjective memory or an enduring experiencing self. It does suggest a practical design principle for future notes and experiments: **preserve the distinctions that are at risk of being lost, not merely the greatest possible volume of data.**

## Next question

Can a memory preserve *meaningful changes of mind* instead of only bit patterns? For example, what is a clear, testable way to track a claim, the evidence for it, a later revision, and the reason the revision happened?

---

Reproduce locally with `python playground/experiment_005.py`. No external packages or network calls are needed.
