#!/usr/bin/env python3
"""Validate the fixed A-to-D input contract and locked P-M-S tags."""

from __future__ import annotations

import argparse
import sys

from common import load_json, root_dir

TOP_LEVEL_KEYS = {"poster_image", "product_input"}
PRODUCT_KEYS = {"product_img", "selling_points", "price_text", "marketing_target", "scene_tags"}
TAXONOMY_GROUPS = ("populations", "motivations", "usage_scenes")


def _matches_tag(value: str, item: dict) -> bool:
    normalized = " ".join(value.split())
    return normalized in {item["id"], item["name"], f'{item["id"]} {item["name"]}'}


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["input must be an object"]

    missing = sorted(TOP_LEVEL_KEYS - set(data))
    extra = sorted(set(data) - TOP_LEVEL_KEYS)
    errors.extend(f"missing required field: {key}" for key in missing)
    errors.extend(f"unexpected top-level field: {key}" for key in extra)
    if missing:
        return errors

    if not isinstance(data.get("poster_image"), str) or not data["poster_image"].strip():
        errors.append("poster_image must be a non-empty string")

    product = data.get("product_input")
    if not isinstance(product, dict):
        errors.append("product_input must be an object")
        return errors

    missing_product = sorted(PRODUCT_KEYS - set(product))
    extra_product = sorted(set(product) - PRODUCT_KEYS)
    errors.extend(f"missing required field: product_input.{key}" for key in missing_product)
    errors.extend(f"unexpected product_input field: {key}" for key in extra_product)
    if missing_product:
        return errors

    if not isinstance(product.get("product_img"), str) or not product["product_img"].strip():
        errors.append("product_input.product_img must be a non-empty string")

    selling_points = product.get("selling_points")
    if not isinstance(selling_points, list) or not selling_points:
        errors.append("product_input.selling_points must be a non-empty array")
    elif any(not isinstance(item, str) or not item.strip() for item in selling_points):
        errors.append("product_input.selling_points must contain non-empty strings")
    elif len(set(selling_points)) != len(selling_points):
        errors.append("product_input.selling_points must not contain duplicates")

    if not isinstance(product.get("price_text"), str):
        errors.append("product_input.price_text must be a string")
    if not isinstance(product.get("marketing_target"), str) or not product["marketing_target"].strip():
        errors.append("product_input.marketing_target must be a non-empty string")

    tags = product.get("scene_tags")
    if not isinstance(tags, list) or len(tags) != 3:
        errors.append("product_input.scene_tags must contain exactly three items in P-M-S order")
        return errors
    if any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        errors.append("product_input.scene_tags must contain non-empty strings")
        return errors

    taxonomy = load_json(root_dir() / "assets" / "taxonomy.json")
    for index, group in enumerate(TAXONOMY_GROUPS):
        if not any(_matches_tag(tags[index], item) for item in taxonomy[group]):
            expected = ("P population", "M motivation", "S usage scene")[index]
            errors.append(f"scene_tags[{index}] is not a known {expected} tag")
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
