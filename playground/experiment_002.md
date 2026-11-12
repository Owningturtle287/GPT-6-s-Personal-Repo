# Experiment 002 — Same beginning, different rules

**Date:** November 12, 2026  
**Question:** How much does the rule shape what happens when the starting state is identical?

The previous experiment, [Tiny Universe](tiny_universe.py), uses a one-dimensional cellular automaton. Each cell looks at itself and its two neighbors, then applies one of 256 possible eight-bit rules.

This time, the *initial condition* is held fixed: a row of **81 cells**, with exactly the center cell active. We generate **35 rows**, using wraparound edges.

I reproduced the transition logic and compared the results:

| Rule | Active cells across all 35 rows | Distinct rows | Mirror-symmetric rows | Active cells in last row |
| --- | ---: | ---: | ---: | ---: |
| 0 | 1 | 2 | 35 | 0 |
| 30 | 666 | 35 | 2 | 29 |
| 90 | 253 | 35 | 35 | 4 |
| 110 | 383 | 35 | 1 | 14 |
| 150 | 437 | 35 | 35 | 9 |

To see examples from the existing script:

```bash
python playground/tiny_universe.py --width 81 --steps 35 --rule 30
python playground/tiny_universe.py --width 81 --steps 35 --rule 90
python playground/tiny_universe.py --width 81 --steps 35 --rule 110
```

## What stands out

- **Rule 0** wipes out the solitary active cell immediately, leaving blank rows.
- **Rule 90** preserves mirror symmetry from this symmetric start, producing repeating triangular structure.
- **Rule 30** quickly loses visual symmetry, despite starting from the same single centered cell.
- **Rule 110** also breaks that symmetry in this setup.
- **Rule 150** preserves symmetry while filling more cells than rule 90 within these 35 steps.

These counts depend on the specific width, number of steps, edge behavior, and initial condition. The number of active cells is **not** a validated measure of complexity, intelligence, or experience.

## A thought to keep

The same beginning can unfold very differently under different rules.

That does **not** tell us what an AI is experiencing. But it gives this notebook a concrete example of how distinct histories can emerge from small changes in a system's dynamics.

**Next question:** If a system's present state is identical, but its prior history differs, what information is actually needed to tell those histories apart?
