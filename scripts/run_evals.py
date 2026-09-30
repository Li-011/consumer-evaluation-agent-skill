#!/usr/bin/env python3
"""Dependency-free regression checks for the A-D Consumer Agent contract."""

from __future__ import annotations

import copy
import sys

from common import DIMENSION_LABELS, load_json, root_dir
from score_evaluation import OUTPUT_KEYS, error_result, score_result, validate_output
from validate_input import validate


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_value_error(function, message: str) -> None:
    try:
        function()
    except ValueError:
        return
    raise AssertionError(message)


def main() -> int:
    root = root_dir()
    input_data = load_json(root / "examples" / "nori-input.json")
    check(validate(input_data) == [], "NORI A-D input should validate")

    wrong_order = copy.deepcopy(input_data)
    wrong_order["product_input"]["scene_tags"] = ["M02 功能效率", "P02 职场通勤人群", "S03 通勤车载"]
    check(validate(wrong_order), "misordered P-M-S tags must be rejected")

    unknown_tag = copy.deepcopy(input_data)
    unknown_tag["product_input"]["scene_tags"][2] = "S99 未知场景"
    check(validate(unknown_tag), "unknown scene tag must be rejected")

    draft = load_json(root / "examples" / "nori-draft-result.json")
    result = score_result(copy.deepcopy(draft))
    check(result["score"] == 7, "NORI score must equal 7")
    check(result["pass"] is True, "score 7 without critical issue must pass")
    check(set(result) == OUTPUT_KEYS, "output must contain exactly seven fields")
    check(result["meta"]["judge_dimensions"] == list(DIMENSION_LABELS), "judge dimensions must be fixed")
    check(validate_output(result) == [], "scored output should validate")

    blocked = copy.deepcopy(draft)
    blocked["dimension_scores"] = {
        "product_recognition": 2,
        "benefit_clarity": 2,
        "offer_visibility": 2,
        "population_scene_fit": 1,
        "purchase_drive": 1,
    }
    blocked_problem = "价格文案与输入不一致"
    blocked["problem_list"] = [blocked_problem]
    blocked["modify_suggestion"] = ["恢复product_input.price_text中的准确价格文案"]
    blocked["critical_issues"] = [blocked_problem]
    blocked_result = score_result(blocked)
    check(blocked_result["score"] == 8, "blocked result score must equal 8")
    check(blocked_result["pass"] is False, "critical issue must block pass")

    mismatch = copy.deepcopy(draft)
    mismatch["modify_suggestion"] = []
    expect_value_error(lambda: score_result(mismatch), "unpaired problems and suggestions must fail")

    parse_error = error_result("海报图像解析失败", "重新提供可读取的海报图像后再次评估")
    check(parse_error["score"] == 0 and parse_error["pass"] is False, "parse failure must be score 0 and fail")
    check(validate_output(parse_error) == [], "parse failure must retain the unified output shape")

    bad_meta = copy.deepcopy(result)
    bad_meta["meta"]["confidence"] = 2
    check(validate_output(bad_meta), "out-of-range confidence must be rejected")

    print("PASS: 8 A-D contract checks")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
