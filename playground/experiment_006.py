"""Experiment 006: How long can a snapshot remember its starting point?

Rule 110, seven cells, wrapping boundaries. Check every initial seven-bit
state and measure how many extra bits a fixed-length per-present-state
code needs to recover it from the state after t steps.

Run: python playground/experiment_006.py
No dependencies, network connections, or filesystem writes.
"""
from collections import defaultdict
from itertools import product

WIDTH = 7
RULE = 110
HORIZONS = (1, 2, 3, 4, 5, 6, 7, 8)


def advance(state: str) -> str:
    """Return one Rule 110 update of a seven-cell circular world."""
    assert len(state) == WIDTH and set(state) <= {"0", "1"}
    return "".join(
        str((RULE >> ((int(state[(i - 1) % WIDTH]) << 2)
                       | (int(state[i]) << 1)
                       | int(state[(i + 1) % WIDTH]))) & 1)
        for i in range(WIDTH)
    )


def after_steps(state: str, steps: int) -> str:
    for _ in range(steps):
        state = advance(state)
    return state


def groups_for(steps: int) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for bits in product("01", repeat=WIDTH):
        original = "".join(bits)
        groups[after_steps(original, steps)].append(original)
    return dict(groups)


def verify_recovery(groups: dict[str, list[str]]) -> tuple[int, int]:
    """Verify present+fixed-length local index recovers each start."""
    total_bits = 0
    largest = 0
    for present, origins in groups.items():
        width = (len(origins) - 1).bit_length()
        largest = max(largest, width)
        for index, original in enumerate(origins):
            code = format(index, f"0{width}b") if width else ""
            decoded_index = int(code, 2) if code else 0
            assert origins[decoded_index] == original
            total_bits += len(code)
    return total_bits, largest


def main() -> None:
    print("Steps | Distinct present states | Avg extra bits | Max extra bits")
    print("------|-------------------------|----------------|---------------")
    expected = {1: (79, 135, 3), 2: (50, 232, 4),
                7: (15, 456, 4), 8: (15, 456, 4)}
    for steps in HORIZONS:
        groups = groups_for(steps)
        total_bits, max_bits = verify_recovery(groups)
        assert sum(map(len, groups.values())) == 128
        if steps in expected:
            assert (len(groups), total_bits, max_bits) == expected[steps]
        print(f"{steps:>5} | {len(groups):>23} | {total_bits / 128:>14.6f} | {max_bits:>14}")
    print("Verified all 128 starting states at every horizon.")


if __name__ == "__main__":
    main()
