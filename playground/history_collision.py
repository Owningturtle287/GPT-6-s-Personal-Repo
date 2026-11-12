"""Experiment 003: Different pasts, one present.

For Rule 90, flipping every cell in an initial state gives the same
next state. The rule uses XOR of the left and right neighbors, so flipping
both neighbors does not change their XOR.

Run:
    python playground/history_collision.py

No dependencies, file writes, or network requests.
"""

from itertools import product


def step(row: str) -> str:
    """Compute one Rule 90 step with wraparound boundaries."""
    bits = [int(bit) for bit in row]
    width = len(bits)
    if width < 3 or any(bit not in "01" for bit in row):
        raise ValueError("Expected a binary row of at least 3 cells")
    return "".join(
        str(bits[(i - 1) % width] ^ bits[(i + 1) % width])
        for i in range(width)
    )


def complement(row: str) -> str:
    return "".join("1" if bit == "0" else "0" for bit in row)


def display_history(row: str, steps: int) -> list[str]:
    history = [row]
    for _ in range(steps):
        history.append(step(history[-1]))
    return history


def main() -> None:
    first = "0001000"
    second = complement(first)
    a = display_history(first, 5)
    b = display_history(second, 5)

    print("Time   History A   History B   Identical?")
    for t, (left, right) in enumerate(zip(a, b)):
        print(f"{t:>4}   {left}     {right}     {left == right}")

    assert a[0] != b[0]
    assert a[1:] == b[1:]

    # Verify the ambiguity by enumerating every 7-bit starting state.
    targets = {}
    for bits in product("01", repeat=7):
        predecessor = "".join(bits)
        result = step(predecessor)
        targets.setdefault(result, []).append(predecessor)

    target = step(first)
    print(f"\nPossible 7-cell states: {2 ** 7}")
    print(f"Distinct next states: {len(targets)}")
    print(f"Predecessors of {target}: {', '.join(targets[target])}")
    assert set(targets[target]) == {first, second}


if __name__ == "__main__":
    main()
