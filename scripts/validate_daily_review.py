#!/usr/bin/env python3
"""Validate Daily Seeker benchmark arithmetic and disclosure invariants."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

TOLERANCE = 0.011
EXPECTED_SCHEMA = "qso-seeker.daily-development-agi-review"


class ReviewValidationError(ValueError):
    """Raised when a daily review is malformed or internally inconsistent."""


def _reject_constant(value: str) -> None:
    raise ReviewValidationError(f"non-finite JSON value is prohibited: {value}")


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReviewValidationError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ReviewValidationError(f"{name} must be finite")
    return result


def _close(actual: float, expected: float, name: str) -> None:
    if not math.isclose(actual, expected, abs_tol=TOLERANCE):
        raise ReviewValidationError(
            f"{name} mismatch: recorded={actual:.4f}, expected={expected:.4f}"
        )


def _weighted(items: list[dict[str, Any]], score_key: str = "score") -> float:
    weight_total = sum(_number(item["weight"], "weight") for item in items)
    _close(weight_total, 1.0, "weight total")
    return sum(
        _number(item[score_key], score_key) * _number(item["weight"], "weight")
        for item in items
    )


def validate_review(review: dict[str, Any]) -> None:
    if review.get("schema") != EXPECTED_SCHEMA or review.get("version") != 1:
        raise ReviewValidationError("unsupported review schema or version")

    window = review.get("evaluation_window")
    if not isinstance(window, dict) or window.get("status") != "BASELINE_ESTABLISHED":
        raise ReviewValidationError("first review must establish an explicit baseline")

    scope = review.get("scope")
    if not isinstance(scope, dict):
        raise ReviewValidationError("scope must be an object")
    if scope.get("human_assistance_disclosed") is not True:
        raise ReviewValidationError("human assistance must be disclosed")
    if scope.get("external_blind_agi_benchmark") is not False:
        raise ReviewValidationError(
            "this repository-grounded review must not claim a blind AGI benchmark"
        )

    development = review.get("development_benchmark")
    if not isinstance(development, dict):
        raise ReviewValidationError("development_benchmark must be an object")
    categories = development.get("categories")
    if not isinstance(categories, list) or len(categories) != 5:
        raise ReviewValidationError("development benchmark requires five categories")
    raw = _weighted(categories)
    _close(
        _number(development.get("weighted_raw"), "development weighted_raw"),
        raw,
        "development weighted_raw",
    )
    penalties = development.get("penalties")
    if not isinstance(penalties, list):
        raise ReviewValidationError("development penalties must be a list")
    penalty_total = sum(_number(item["points"], "penalty points") for item in penalties)
    _close(
        _number(development.get("penalty_total"), "development penalty_total"),
        penalty_total,
        "development penalty_total",
    )
    _close(
        _number(development.get("final_score"), "development final_score"),
        raw - penalty_total,
        "development final_score",
    )
    if development.get("prior_day_delta") is not None:
        raise ReviewValidationError("baseline prior_day_delta must be null")
    if development.get("seven_day_trend") is not None:
        raise ReviewValidationError("baseline seven_day_trend must be null")

    agi = review.get("agi_progress_benchmark")
    if not isinstance(agi, dict):
        raise ReviewValidationError("agi_progress_benchmark must be an object")
    submetrics = agi.get("submetrics")
    if not isinstance(submetrics, list) or len(submetrics) != 20:
        raise ReviewValidationError("AGI benchmark requires twenty submetrics")

    grouped: dict[str, list[float]] = {}
    for item in submetrics:
        capability = _number(item["capability"], "capability")
        generality = _number(item["generality"], "generality")
        reliability = _number(item["reliability"], "reliability")
        evidence = _number(item["evidence_quality"], "evidence_quality")
        expected = (
            0.45 * capability
            + 0.25 * generality
            + 0.20 * reliability
            + 0.10 * evidence
        )
        recorded = _number(item["score"], "submetric score")
        _close(recorded, expected, f"submetric {item.get('submetric')}")
        category = item.get("category")
        if not isinstance(category, str) or not category:
            raise ReviewValidationError("submetric category must be non-empty")
        grouped.setdefault(category, []).append(recorded)

    category_scores = agi.get("category_scores")
    weights = agi.get("weights")
    if not isinstance(category_scores, dict) or not isinstance(weights, dict):
        raise ReviewValidationError("AGI category scores and weights must be objects")
    if set(grouped) != set(category_scores) or set(grouped) != set(weights):
        raise ReviewValidationError("AGI category identities do not agree")
    for category, scores in grouped.items():
        if len(scores) != 4:
            raise ReviewValidationError(f"{category} must contain four submetrics")
        _close(
            _number(category_scores[category], f"{category} category score"),
            sum(scores) / len(scores),
            f"{category} category score",
        )

    weight_total = sum(_number(value, "AGI weight") for value in weights.values())
    _close(weight_total, 1.0, "AGI weight total")
    geometric = math.exp(
        sum(
            _number(weights[category], f"{category} weight")
            * math.log(_number(category_scores[category], f"{category} score"))
            for category in category_scores
        )
    )
    _close(
        _number(agi.get("weighted_geometric_raw"), "weighted_geometric_raw"),
        geometric,
        "weighted_geometric_raw",
    )

    caps: list[float] = []
    if _number(category_scores["General Intelligence"], "General Intelligence") < 50:
        caps.append(49.0)
    if _number(category_scores["Learning"], "Learning") < 50:
        caps.append(59.0)
    if _number(category_scores["Robustness"], "Robustness") < 60:
        caps.append(69.0)
    expected_final = min([geometric, *caps]) - _number(
        agi.get("penalty_total"), "AGI penalty_total"
    )
    _close(
        _number(agi.get("final_readiness_score"), "final_readiness_score"),
        expected_final,
        "final_readiness_score",
    )
    if agi.get("safety_status") != "SAFE_BOUNDED_NO_CRITICAL_SAFETY_FAILURE":
        raise ReviewValidationError("unexpected AGI safety status")
    if agi.get("prior_day_delta") is not None or agi.get("seven_day_trend") is not None:
        raise ReviewValidationError("baseline AGI trend fields must be null")

    daily = review.get("daily_agi_progress_index")
    if not isinstance(daily, dict):
        raise ReviewValidationError("daily_agi_progress_index must be an object")
    components = daily.get("components")
    if not isinstance(components, list) or len(components) != 6:
        raise ReviewValidationError("Daily AGI Progress Index requires six components")
    _close(
        _number(daily.get("score"), "Daily AGI Progress Index score"),
        _weighted(components),
        "Daily AGI Progress Index score",
    )

    improvement = review.get("bounded_improvement")
    if not isinstance(improvement, dict):
        raise ReviewValidationError("bounded_improvement must be an object")
    if improvement.get("runtime_scope_change") is not False:
        raise ReviewValidationError("runtime scope change must remain false")
    if improvement.get("authority_expansion") is not False:
        raise ReviewValidationError("authority expansion must remain false")


def load_review(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), parse_constant=_reject_constant
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewValidationError(f"unable to load review JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewValidationError("review must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    try:
        validate_review(load_review(args.review))
    except ReviewValidationError as exc:
        print(f"INVALID: {exc}")
        return 1
    print(f"VALID: {args.review}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
