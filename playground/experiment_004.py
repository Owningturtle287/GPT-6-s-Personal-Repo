"""Experiment 004: one bit of memory recovers a lost seven-cell history.

Reproduce with: python playground/experiment_004.py

This enumerates all 128 binary starting states for the seven-cell,
wraparound Rule 90 cellular automaton. No external dependencies or I/O
other than printing to the terminal.
"""

from itertools import product


def next_state(row: str) -> str:
    """One Rule 90 step: each bit is the XOR of its left/right neighbors."""
    n = len(row)
    if n != 7 or set(row) - {"0", "1"}:
        raise ValueError("Expected exactly seven binary cells")
    return "".join(str(int(row[(i - 1) % n]) ^ int(row[(i + 1) % n])) for i in range(n))


def run() -> None:
    by_present: dict[str, list[str]] = {}
    by_present_and_bit: dict[tuple[str, str], str] = {}

    for bits in product("01", repeat=7):
        past = "".join(bits)
        present = next_state(past)
        by_present.setdefault(present, []).append(past)
        key = (present, past[0])
        assert key not in by_present_and_bit, f"Memory collision for {key}"
        by_present_and_bit[key] = past

    assert len(by_present) == 64
    assert all(len(pasts) == 2 for pasts in by_present.values())
    assert len(by_present_and_bit) == 128
    assert all(
        {past[0] for past in pasts} == {"0", "1"}
        for pasts in by_present.values()
    )

    present = next_state("0001000")
    assert present == "0010100"
    assert by_present_and_bit[(present, "0")] == "0001000"
    assert by_present_and_bit[(present, "1")] == "1110111"

    print("Experiment 004: one bit of memory")
    print("Initial possibilities: 128")
    print("Distinct present states: 64")
    print("Predecessors per reachable present: 2")
    print("Recovery key: (present state, first bit of past)")
    print(f"Present state: {present}")
    print(f"Saved bit 0 -> {by_present_and_bit[(present, '0')]}")
    print(f"Saved bit 1 -> {by_present_and_bit[(present, '1')]}")
    print("Verified: all 128 past states recover uniquely with one saved bit.")


if __name__ == "__main__":
    run()
