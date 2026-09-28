#!/usr/bin/env python3
"""Dependency-free regression checks for protocol 1.0."""

from __future__ import annotations

import copy
import sys

from common import load_json, root_dir
from compare_versions import compare
from score_evaluation import score_result
from validate_input import validate


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    root = root_dir()
    input_data = load_json(root / "examples" / "nori-input.json")
    check(validate(input_data) == [], "NORI input should validate")

    draft = load_json(root / "examples" / "nori-draft-result.json")
    scored = score_result(copy.deepcopy(draft))
    check(scored["CES"] == 68.0, "V1 CES must equal 68")
    check(scored["decision"] == "ITERATE", "V1 must iterate")

    passing = copy.deepcopy(draft)
    passing["poster_version"] = "V2"
    passing["failure_codes"] = []
    passing["revision_actions"] = []
    for item in passing["dimensions"].values():
        item["anchor"] = 4
        item["score"] = 80
    passing = score_result(passing)
    check(passing["CES"] == 80.0, "V2 CES must equal 80")
    check(passing["decision"] == "PASS", "V2 must pass")

    delta = compare(load_json(root / "examples" / "nori-v1-result.json"), load_json(root / "examples" / "nori-v2-result.json"))
    check(delta["CES"] == 12.0, "CES delta must equal 12")

    drift = load_json(root / "examples" / "nori-v2-result.json")
    drift["consumer_profile"]["macro_segment"] = "Z世代"
    try:
        compare(load_json(root / "examples" / "nori-v1-result.json"), drift)
    except ValueError:
        pass
    else:
        raise AssertionError("profile drift must be rejected")

    print("PASS: 4 golden cases, 6 protocol checks")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)

