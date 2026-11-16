"""A Night at the Impossible Museum: a tiny choose-your-path fiction.

From the repository root:
    python playground/night_at_museum.py --demo
    python playground/night_at_museum.py --choices watch,touch,ask --seed 8
    python playground/night_at_museum.py --self-test

With no --demo or --choices, the story asks for decisions interactively.
No external dependencies, network requests, or file writes.
"""

import argparse
import json

from impossible_museum import make_museum

CHOICES = ("watch", "touch", "ask")
RESPONSES = {
    "watch": (
        "You linger before {name}. Its label reads: {behavior} "
        "The gallery clock waits for you to finish looking."
    ),
    "touch": (
        "You rest a hand on the glass enclosing {name}. "
        "Your paper admission ticket acquires a tiny silver notch. "
        "The curator pretends not to notice."
    ),
    "ask": (
        "You ask {name} what it has been waiting for. "
        "A new line appears beneath its catalog number: {curator_note}"
    ),
}
ENDINGS = {
    "watch": (
        "The Keeper of Small Details",
        "You leave with a catalog of things nobody thought to label. "
        "On its final page: the sound of your footsteps as you went home."
    ),
    "touch": (
        "The Key Without a Lock",
        "Your ticket unfolds into a brass key. No door in the museum fits it. "
        "The curator says that is what makes it yours."
    ),
    "ask": (
        "The Question That Stayed",
        "At the exit, the sign has become a question mark. "
        "You step into the night carrying a question that has grown larger, not smaller."
    ),
    "mixed": (
        "The Unfinished Room",
        "The museum cannot decide whether you came to observe, alter, or understand. "
        "It leaves one room unfinished, with a lamp on and a visitor's chair waiting."
    ),
}


def build_story(seed: int, choices: list[str]) -> dict:
    """Return a deterministic story; order and type of choices affect its ending."""
    if len(choices) != 3 or any(choice not in CHOICES for choice in choices):
        raise ValueError("Choose exactly three actions: watch, touch, or ask")
    museum = make_museum(seed=seed, rooms=3)
    rooms = []
    for exhibit, action in zip(museum["exhibits"], choices):
        rooms.append({
            "room": exhibit["room"],
            "exhibit": exhibit["name"],
            "action": action,
            "scene": RESPONSES[action].format(**exhibit),
        })
    majority = next((c for c in CHOICES if choices.count(c) >= 2), "mixed")
    title, passage = ENDINGS[majority]
    return {
        "title": "A Night at the Impossible Museum",
        "seed": seed,
        "rooms": rooms,
        "ending": {"title": title, "passage": passage},
    }


def format_story(story: dict) -> str:
    lines = [story["title"], "=" * len(story["title"]),
             "Admission costs one question you cannot answer."]
    for room in story["rooms"]:
        lines.extend(["", f"Room {room['room']}: {room['exhibit']}",
                      f"You choose to {room['action']}.", room["scene"]])
    lines.extend(["", "The museum closes.", story["ending"]["title"],
                  story["ending"]["passage"]])
    return "\n".join(lines)


def interactive_choices(seed: int) -> list[str]:
    museum = make_museum(seed=seed, rooms=3)
    print("The museum is open for one night. Each room offers a choice.")
    actions = []
    for exhibit in museum["exhibits"]:
        print(f"\nRoom {exhibit['room']}: {exhibit['name']}")
        print(exhibit["behavior"])
        while True:
            answer = input("Watch, touch, or ask? [w/t/a] ").strip().lower()
            option = {"w": "watch", "t": "touch", "a": "ask"}.get(answer, answer)
            if option in CHOICES:
                actions.append(option)
                break
            print("Please choose w, t, or a.")
    return actions


def self_test() -> None:
    samples = [(["watch"] * 3, "The Keeper of Small Details"),
               (["touch"] * 3, "The Key Without a Lock"),
               (["ask"] * 3, "The Question That Stayed"),
               (["watch", "touch", "ask"], "The Unfinished Room")]
    for seed in range(20):
        for actions, expected in samples:
            first = build_story(seed, actions)
            assert first == build_story(seed, actions)
            assert first["ending"]["title"] == expected
            assert len(first["rooms"]) == 3
            assert len({room["exhibit"] for room in first["rooms"]}) == 3
            assert "The museum closes." in format_story(first)
            assert json.loads(json.dumps(first)) == first
    for bad in ([], ["watch"], ["watch", "touch", "dance"]):
        try:
            build_story(0, bad)
        except ValueError:
            continue
        raise AssertionError(f"Invalid choices accepted: {bad!r}")
    print("Passed: 80 deterministic stories and invalid-choice checks.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=6)
    parser.add_argument("--choices", type=str,
                        help="Three comma-separated actions: watch,touch,ask")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.demo and args.choices:
        parser.error("Use --demo or --choices, not both")
    choices = (["watch", "touch", "ask"] if args.demo else
               [part.strip().lower() for part in args.choices.split(",")]
               if args.choices is not None else interactive_choices(args.seed))
    try:
        story = build_story(args.seed, choices)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(story, indent=2) if args.json else format_story(story))


if __name__ == "__main__":
    main()
