#!/usr/bin/env python3
"""Compare two scored evaluations while enforcing a locked context."""

from __future__ import annotations

import argparse
import json
import sys

from common import DIMENSIONS, load_json


def compare(old: dict, new: dict) -> dict:
    if old.get("consumer_profile") != new.get("consumer_profile"):
        raise ValueError("consumer profile changed; start a separate benchmark track")
    deltas = {name: new["scores"][name] - old["scores"][name] for name in DIMENSIONS}
    largest = max(deltas, key=deltas.get) if max(deltas.values()) > 0 else None
    regressions = [name for name, delta in deltas.items() if delta < 0]
    return {
        "from": old.get("poster_version"),
        "to": new.get("poster_version"),
        "CES": round(new["CES"] - old["CES"], 1),
        "dimensions": deltas,
        "largest_improvement": largest,
        "regressions": regressions,
        "remaining_below_threshold": [name for name in DIMENSIONS if new["scores"][name] < 65]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("old")
    parser.add_argument("new")
    args = parser.parse_args()
    try:
        result = compare(load_json(args.old), load_json(args.new))
    except (OSError, ValueError, KeyError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

