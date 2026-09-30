#!/usr/bin/env python3
"""Convert an internal five-dimension draft into the fixed D-to-A JSON."""

from __future__ import annotations

import argparse
import json
import sys

from common import DIMENSION_LABELS, DIMENSIONS, load_json, write_json

OUTPUT_KEYS = {
    "agent_name",
    "score",
    "pass",
    "problem_list",
    "modify_suggestion",
    "protected_content",
    "meta",
}


def _string_list(value: object, field: str, maximum: int | None = None) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{field} must be an array of non-empty strings")
    if maximum is not None and len(value) > maximum:
        raise ValueError(f"{field} must contain at most {maximum} items")
    return value


def score_result(data: dict) -> dict:
    dimensions = data.get("dimension_scores")
    if not isinstance(dimensions, dict):
        raise ValueError("missing dimension_scores")
    if set(dimensions) != set(DIMENSIONS):
        raise ValueError("dimension_scores must contain exactly the five fixed dimensions")

    scores: list[int] = []
    for name in DIMENSIONS:
        value = dimensions[name]
        if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1, 2):
            raise ValueError(f"dimension_scores.{name} must be 0, 1, or 2")
        scores.append(value)

    problems = _string_list(data.get("problem_list"), "problem_list", maximum=3)
    suggestions = _string_list(data.get("modify_suggestion"), "modify_suggestion", maximum=3)
    if len(problems) != len(suggestions):
        raise ValueError("problem_list and modify_suggestion must have the same length")

    protected = _string_list(data.get("protected_content"), "protected_content")
    if len(set(protected)) != len(protected):
        raise ValueError("protected_content must not contain duplicates")

    critical = _string_list(data.get("critical_issues", []), "critical_issues", maximum=3)
    if any(item not in problems for item in critical):
        raise ValueError("every critical issue must also appear in problem_list")

    confidence = data.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be a number from 0 to 1")

    total = sum(scores)
    return {
        "agent_name": "consumer_agent",
        "score": total,
        "pass": total >= 7 and not critical,
        "problem_list": problems,
        "modify_suggestion": suggestions,
        "protected_content": protected,
        "meta": {
            "judge_dimensions": list(DIMENSION_LABELS),
            "confidence": confidence,
        },
    }


def error_result(problem: str, suggestion: str) -> dict:
    return {
        "agent_name": "consumer_agent",
        "score": 0,
        "pass": False,
        "problem_list": [problem],
        "modify_suggestion": [suggestion],
        "protected_content": [],
        "meta": {"judge_dimensions": [], "confidence": 0},
    }


def validate_output(data: dict) -> list[str]:
    errors: list[str] = []
    if set(data) != OUTPUT_KEYS:
        errors.append("output must contain exactly the seven A-D fields")
        return errors
    if data.get("agent_name") != "consumer_agent":
        errors.append("agent_name must be consumer_agent")
    score = data.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 10:
        errors.append("score must be an integer from 0 to 10")
    if not isinstance(data.get("pass"), bool):
        errors.append("pass must be boolean")
    try:
        problems = _string_list(data.get("problem_list"), "problem_list", maximum=3)
        suggestions = _string_list(data.get("modify_suggestion"), "modify_suggestion", maximum=3)
        if len(problems) != len(suggestions):
            errors.append("problem_list and modify_suggestion must have the same length")
        protected = _string_list(data.get("protected_content"), "protected_content")
        if len(set(protected)) != len(protected):
            errors.append("protected_content must not contain duplicates")
    except ValueError as exc:
        errors.append(str(exc))
    meta = data.get("meta")
    if not isinstance(meta, dict) or set(meta) != {"judge_dimensions", "confidence"}:
        errors.append("meta must contain exactly judge_dimensions and confidence")
    else:
        try:
            dimensions = _string_list(meta.get("judge_dimensions"), "meta.judge_dimensions")
            if len(set(dimensions)) != len(dimensions):
                errors.append("meta.judge_dimensions must not contain duplicates")
        except ValueError as exc:
            errors.append(str(exc))
        confidence = meta.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append("meta.confidence must be a number from 0 to 1")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = score_result(load_json(args.input))
        output_errors = validate_output(result)
        if output_errors:
            raise ValueError("; ".join(output_errors))
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    if args.output:
        write_json(args.output, result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
