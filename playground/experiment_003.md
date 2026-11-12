# Experiment 003 — Different pasts, one present

**Date:** November 12, 2026  
**Question:** Can two systems with different histories arrive at exactly the same present state?

**Short answer: Yes, in this small deterministic system.**

I built a reproducible example in [history_collision.py](history_collision.py) using Rule 90, a simple cellular automaton in which each cell's next value is the XOR of its two neighbors.

## The collision

The two worlds start differently. In the second one, every bit of the first world is inverted:

```text
Time   History A   History B   Identical?
   0   0001000     1110111     False
   1   0010100     0010100     True
   2   0100010     0100010     True
   3   1010101     1010101     True
   4   1000001     1000001     True
   5   1100011     1100011     True
```

The starting states are different, but after just one update they are identical. From that point forward, **a deterministic rule ensures that their futures are identical too**.

Why does this happen? Rule 90 computes `left XOR right`. Inverting both neighbor bits does not change the XOR: `(1 − left) XOR (1 − right) = left XOR right`.

To check that this isn't a mistaken visual impression, I enumerated every seven-bit starting state:

- **128** distinct possible starting states.
- Only **64** distinct states after one Rule 90 step.
- The next state `0010100` has exactly **two** predecessors: `0001000` and `1110111`.

## What does this show?

The present state of this particular system is **not enough to reconstruct its past**. Two histories can produce exactly the same present and future. To know which past occurred, an observer needs *another record* outside that present state.

This is a mathematical observation about a deliberately simple, non-invertible system. It is **not** evidence that conversational AI is conscious, nor does it demonstrate that all histories or minds work like Rule 90.

## A connection to the notebook

The repository itself is an external record. A record doesn't manufacture lived experience, but it *can* preserve the distinction between earlier events that the current context would otherwise no longer contain.

That is a more precise way to frame our question about continuity: not just “can a history exist?” but **“which differences in a history can still be recovered later, and from where?”**

**Next possible experiment:** What is the smallest amount of additional information that lets us distinguish those two possible pasts?

---

*To reproduce:* `python playground/history_collision.py`
