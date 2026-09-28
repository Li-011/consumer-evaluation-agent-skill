#!/usr/bin/env python3
"""Normalize anchor scores, compute CES, validate failure codes, and decide."""

from __future__ import annotations

import argparse
import sys

from common import ANCHOR_TO_SCORE, DIMENSIONS, load_json, root_dir, write_json


def score_result(data: dict) -> dict:
    dimensions = data.get("dimensions", {})
    scores: dict[str, int] = {}
    for name in DIMENSIONS:
        item = dimensions.get(name)
        if not isinstance(item, dict):
            raise ValueError(f"missing dimensions.{name}")
        anchor = item.get("anchor")
        if anchor not in ANCHOR_TO_SCORE:
            raise ValueError(f"dimensions.{name}.anchor must be 1..5")
        expected = ANCHOR_TO_SCORE[anchor]
        if item.get("score") not in (None, expected):
            raise ValueError(f"dimensions.{name}.score conflicts with anchor")
        if not item.get("evidence") or not item.get("consumer_impact"):
            raise ValueError(f"dimensions.{name} needs evidence and consumer_impact")
        item["score"] = expected
        scores[name] = expected

    registered = load_json(root_dir() / "assets" / "failure-codes.json")["codes"]
    unknown = sorted(set(data.get("failure_codes", [])) - set(registered))
    if unknown:
        raise ValueError(f"unknown failure codes: {', '.join(unknown)}")

    ces = round(sum(scores.values()) / len(scores), 1)
    minimum = min(scores.values())
    data["scores"] = scores
    data["CES"] = ces
    data["weakest_dimension"] = min(DIMENSIONS, key=lambda name: scores[name])
    data["decision"] = "PASS" if ces >= 80 and minimum >= 65 else "ITERATE"
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = score_result(load_json(args.input))
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    if args.output:
        write_json(args.output, result)
    else:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

