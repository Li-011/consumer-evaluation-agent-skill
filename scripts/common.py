"""Shared deterministic helpers for Consumer Evaluation Agent 1.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DIMENSIONS = ("attention", "relevance", "clarity", "value", "desire")
ANCHOR_TO_SCORE = {1: 20, 2: 40, 3: 60, 4: 80, 5: 100}


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, value: Any) -> None:
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def root_dir() -> Path:
    return Path(__file__).resolve().parents[1]

