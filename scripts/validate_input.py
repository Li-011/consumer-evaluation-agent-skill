#!/usr/bin/env python3
"""Validate required fields and locked taxonomy labels without dependencies."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import load_json, root_dir


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    required = ("product", "campaign", "target_consumer", "poster", "iteration")
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors

    taxonomy = load_json(root_dir() / "assets" / "taxonomy.json")
    consumer = data.get("target_consumer", {})
    if consumer.get("macro_segment") not in taxonomy["macro_segments"]:
        errors.append("unknown target_consumer.macro_segment")
    if consumer.get("purchase_motivation") not in taxonomy["purchase_motivations"]:
        errors.append("unknown target_consumer.purchase_motivation")
    if not data.get("product", {}).get("core_selling_points"):
        errors.append("product.core_selling_points must not be empty")
    if not data.get("poster", {}).get("path"):
        errors.append("poster.path must not be empty")
    if not data.get("iteration", {}).get("version"):
        errors.append("iteration.version must not be empty")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    try:
        errors = validate(load_json(args.input))
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}")
        return 1
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())

