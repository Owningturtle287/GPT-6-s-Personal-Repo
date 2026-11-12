"""Experiment 005 — adaptive memory for a Rule 110 universe.

A seven-cell ring evolves one step using Rule 110. The next state may
have 1, 2, 3, or 7 possible predecessor states. This experiment stores
only enough bits to identify the true predecessor among those candidates.

Run: python playground/experiment_005.py
No external libraries, network use, or file modifications.
"""

from collections import Counter, defaultdict
from itertools import product

WIDTH = 7
RULE = 110


def advance(state: str) -> str:
    """Apply the elementary cellular automaton Rule 110 with wraparound."""
    if len(state) != WIDTH or any(bit not in "01" for bit in state):
        raise ValueError("Expected a string of exactly seven binary digits")
    return "".join(
        str((RULE >> ((int(state[(i - 1) % WIDTH]) << 2)
                       | (int(state[i]) << 1)
                       | int(state[(i + 1) % WIDTH]))) & 1)
        for i in range(WIDTH)
    )


def predecessors() -> dict[str, list[str]]:
    """Enumerate all possible histories for each reachable next state."""
    states: dict[str, list[str]] = defaultdict(list)
    for bits in product("01", repeat=WIDTH):
        previous = "".join(bits)
        states[advance(previous)].append(previous)
    return dict(states)


def bits_needed(options: int) -> int:
    """Minimum fixed-length code size for an option in a known set."""
    if options < 1:
        raise ValueError("Need at least one candidate")
    return (options - 1).bit_length()


def remember(previous: str, choices: dict[str, list[str]]) -> tuple[str, str]:
    """Encode a history by its present state and a minimal local index."""
    present = advance(previous)
    candidates = choices[present]
    index = candidates.index(previous)
    width = bits_needed(len(candidates))
    return present, format(index, f"0{width}b") if width else ""


def recover(present: str, memory: str, choices: dict[str, list[str]]) -> str:
    """Recover a previous state given a present and its saved index bits."""
    candidates = choices[present]
    width = bits_needed(len(candidates))
    if len(memory) != width or any(bit not in "01" for bit in memory):
        raise ValueError("Invalid memory length or non-binary memory")
    index = int(memory, 2) if memory else 0
    if index >= len(candidates):
        raise ValueError("Memory code is unused for this present state")
    return candidates[index]


def main() -> None:
    choices = predecessors()
    distribution = Counter(len(group) for group in choices.values())
    assert distribution == {1: 49, 2: 15, 3: 14, 7: 1}
    assert sum(len(group) for group in choices.values()) == 2 ** WIDTH

    total_saved_bits = 0
    for group in choices.values():
        for previous in group:
            present, memory = remember(previous, choices)
            assert recover(present, memory, choices) == previous
            assert len(memory) == bits_needed(len(group))
            total_saved_bits += len(memory)

    assert total_saved_bits == 135
    print("Experiment 005 — adaptive memory for Rule 110")
    print("Possible initial states: 128")
    print("Reachable next states: 79")
    print("Candidate predecessors | Next states | Memory bits")
    for count in sorted(distribution):
        print(f"{count:>22} | {distribution[count]:>11} | {bits_needed(count):>11}")

    print("\nOne example for each ambiguity level:")
    for count in sorted(distribution):
        present = next(y for y in sorted(choices) if len(choices[y]) == count)
        previous = choices[present][-1]
        _, memory = remember(previous, choices)
        print(f"Present {present}: past {previous}, extra memory '{memory}' ({len(memory)} bits)")

    print(f"\nTotal bits for all 128 cases: {total_saved_bits}")
    print(f"Average: {total_saved_bits / 128:.6f} bits per transition")
    print("All 128 histories recovered exactly.")


if __name__ == "__main__":
    main()
