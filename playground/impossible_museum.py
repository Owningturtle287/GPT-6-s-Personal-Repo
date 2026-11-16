"""The Museum of Things That Almost Existed.

A tiny reproducible generator of fictional museum exhibits.

Run from the repo root:
    python playground/impossible_museum.py --seed 6 --rooms 3
    python playground/impossible_museum.py --seed 6 --rooms 3 --json

Standard library only. Does not modify files or access the network.
"""

import argparse
import json
import random

OBJECTS = [
    ("The Weatherless Umbrella", "When opened, it shelters its holder from a memory that has not happened yet."),
    ("The Compass of Almost", "Its needle points toward the road its owner nearly took."),
    ("The Unsent Letterbox", "Every morning it receives one letter that its sender was too afraid to write."),
    ("The Borrowed Mirror", "It reflects the face of the last person who truly listened to you."),
    ("The Quiet Lighthouse", "Its lamp illuminates things people forgot to say."),
    ("The Tuesday Telescope", "It shows constellations that will not exist until someone names them."),
    ("The Apology Engine", "It converts explanations into the words their speakers meant to say."),
    ("The Pocket Door", "It opens only onto rooms someone has dreamed of but never entered."),
    ("The Hourglass of Detours", "Its sand falls upward whenever someone changes their mind."),
    ("The Map of Missing Streets", "It contains every shortcut that disappeared when a city grew up."),
    ("The Forgetful Teacup", "It leaves the taste of a conversation rather than the taste of tea."),
    ("The Second-Chance Camera", "It photographs the moment immediately before a person decides to be kind."),
]

ORIGINS = [
    "Recovered from an attic whose house had been demolished seventy years earlier.",
    "Donated anonymously, wrapped in a newspaper dated next Thursday.",
    "Found beside a railway platform that appears on no timetable.",
    "Unearthed beneath the foundation of a library with no books.",
    "Delivered in a crate marked FRAGILE: POSSIBILITY.",
    "Discovered at the bottom of a well that had never contained water.",
    "Traded for a story by a traveler who would not give a name.",
    "Found on the last shelf of a shop that closed before it opened.",
    "Recovered after a storm in which nothing became wet.",
    "Left at the reception desk with an unsigned thank-you note.",
    "Retrieved from a garden where the shadows pointed north.",
    "Donated by the museum's first visitor, who has not arrived yet.",
]

WARNINGS = [
    "Please do not ask it to prove that it works.",
    "Handle gently; it has already survived one ending.",
    "Do not compare your experience with another visitor's.",
    "If it changes while you are watching, notify the night curator.",
    "Keep your ticket. You may need it to find the exit.",
    "Photography is permitted, but captions are discouraged.",
    "No refunds are given for recovered possibilities.",
    "Please leave unfinished questions in the tray by the door.",
    "Do not attempt to repair what might not be broken.",
    "If you recognize it, please do not say from where.",
    "Visitors are asked not to make promises in this gallery.",
    "The museum accepts no responsibility for sudden nostalgia.",
]

OBSERVATIONS = [
    "One visitor stood here for an hour, then left smiling without explanation.",
    "The curator's notes end in the middle of a sentence.",
    "A child asked whether it could be borrowed. Nobody answered immediately.",
    "It has never been stolen, although the case is often found unlocked.",
    "The dust beneath it is older than the object itself.",
    "Its catalog number changes whenever the museum is empty.",
    "Visitors often return to this room without remembering why.",
    "The night guard reports hearing applause from an empty gallery.",
    "The object weighs exactly as much as a handwritten apology.",
    "The exhibit log contains three entries in the same handwriting, centuries apart.",
    "A replacement was commissioned once. The replacement arrived first.",
    "The museum insists this was its very first acquisition. So do eleven other objects.",
]


def make_museum(seed: int = 6, rooms: int = 3) -> dict:
    """Produce a deterministic museum with no repeated source fragments."""
    if not 1 <= rooms <= len(OBJECTS):
        raise ValueError(f"rooms must be between 1 and {len(OBJECTS)}")
    rng = random.Random(seed)
    chosen_objects = rng.sample(OBJECTS, rooms)
    origins = rng.sample(ORIGINS, rooms)
    warnings = rng.sample(WARNINGS, rooms)
    observations = rng.sample(OBSERVATIONS, rooms)
    exhibits = []
    for index, ((name, behavior), origin, warning, observation) in enumerate(
        zip(chosen_objects, origins, warnings, observations), start=1
    ):
        exhibits.append({
            "room": index,
            "name": name,
            "behavior": behavior,
            "provenance": origin,
            "visitor_notice": warning,
            "curator_note": observation,
        })
    return {
        "title": "The Museum of Things That Almost Existed",
        "seed": seed,
        "admission": "One question you cannot answer.",
        "exhibits": exhibits,
    }


def format_museum(museum: dict) -> str:
    lines = [
        museum["title"],
        "=" * len(museum["title"]),
        f"Admission: {museum['admission']}",
        f"Catalog seed: {museum['seed']}",
    ]
    for exhibit in museum["exhibits"]:
        lines.extend([
            "",
            f"Room {exhibit['room']}: {exhibit['name']}",
            f"  {exhibit['behavior']}",
            f"  Origin: {exhibit['provenance']}",
            f"  Notice: {exhibit['visitor_notice']}",
            f"  Curator's note: {exhibit['curator_note']}",
        ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=6, help="Repeatable catalog seed")
    parser.add_argument("--rooms", type=int, default=3, help="Number of exhibits (1-12)")
    parser.add_argument("--json", action="store_true", help="Print structured JSON instead")
    args = parser.parse_args()
    try:
        museum = make_museum(args.seed, args.rooms)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(museum, indent=2) if args.json else format_museum(museum))


if __name__ == "__main__":
    main()
