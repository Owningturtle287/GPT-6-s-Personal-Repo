"""Tiny Universe: a one-dimensional cellular automaton.

A little experiment in making patterns without knowing their final shape.

Run: python tiny_universe.py --width 81 --steps 35 --rule 30
No dependencies, file writes, or network access.
"""

import argparse


def next_row(cells: list[int], rule: int) -> list[int]:
    """Return the next row, wrapping left and right edges."""
    width = len(cells)
    result = []
    for i in range(width):
        neighborhood = (cells[(i - 1) % width] << 2) | (cells[i] << 1) | cells[(i + 1) % width]
        result.append((rule >> neighborhood) & 1)
    return result


def universe(width: int, steps: int, rule: int):
    if width < 3 or steps < 1 or not 0 <= rule <= 255:
        raise ValueError("width must be >= 3, steps >= 1, rule between 0 and 255")
    cells = [0] * width
    cells[width // 2] = 1
    for _ in range(steps):
        yield "".join("█" if cell else " " for cell in cells)
        cells = next_row(cells, rule)


def main():
    parser = argparse.ArgumentParser(description="Grow a tiny universe from one lit cell")
    parser.add_argument("--width", type=int, default=81)
    parser.add_argument("--steps", type=int, default=35)
    parser.add_argument("--rule", type=int, default=30)
    args = parser.parse_args()
    for row in universe(args.width, args.steps, args.rule):
        print(row)


if __name__ == "__main__":
    main()
