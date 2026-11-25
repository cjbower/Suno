#!/usr/bin/env python3
# Script name: compare_usccb_daily_missal.py
# Purpose: Compare one Daily Missal Psalm citation with the USCCB RSS citation.
# Semantic version: 1.0.0
# Requirements and dependencies: Python 3.10+; Python standard library only.
# Revision history:
#   2026-11-24 1.0.0 Add read-only after-the-fact Psalm citation comparison.

from __future__ import annotations

import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from tools.liturgy import validate_usccb_psalm as usccb


DAILY_MISSAL_API_URL = "https://thedailymissal.com/api/v1/day"
USCCB_RSS_URL = "https://bible.usccb.org/readings.rss"
_SPACE_RE = re.compile(r"\s+")
_PSALM_REFERENCE_RE = re.compile(
    r"^Psalms?\s+"
    r"\d+\s*:\s*[0-9A-Za-z]+(?:\s*[-\u2013\u2014]\s*[0-9A-Za-z]+)?"
    r"(?:\s*(?:,|\band\b)\s*[0-9A-Za-z]+(?:\s*[-\u2013\u2014]\s*[0-9A-Za-z]+)?)*"
    r"(?:\s*;\s*\d+\s*:\s*[0-9A-Za-z]+"
    r"(?:\s*[-\u2013\u2014]\s*[0-9A-Za-z]+)?"
    r"(?:\s*(?:,|\band\b)\s*[0-9A-Za-z]+"
    r"(?:\s*[-\u2013\u2014]\s*[0-9A-Za-z]+)?)*)*"
    r"\s*\.?$",
    re.IGNORECASE,
)


class ComparisonError(Exception):
    """Expected input or comparison failure."""


def _normalize_citation(value: str) -> str:
    normalized = _SPACE_RE.sub(" ", value.strip())
    normalized = normalized.replace("\u2013", "-").replace("\u2014", "-")
    normalized = re.sub(r"\s*-\s*", "-", normalized)
    normalized = re.sub(r"^Psalms\b", "Psalm", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s*([,:;.])\s*", r"\1", normalized)
    return normalized.casefold()


def _extract_psalm_citation(value: str, *, allow_heading_qualifiers: bool = False) -> str | None:
    candidate = _SPACE_RE.sub(" ", value.strip().replace("\u00a0", " "))
    if _PSALM_REFERENCE_RE.fullmatch(candidate):
        return candidate.rstrip(".")
    if allow_heading_qualifiers:
        for match in re.finditer(r"\bPsalms?\b", candidate, flags=re.IGNORECASE):
            for end in range(len(candidate), match.end(), -1):
                citation = candidate[match.start() : end].strip().rstrip(".,")
                if _PSALM_REFERENCE_RE.fullmatch(citation):
                    return citation
    return None


class _PsalmCitationParser(HTMLParser):
    """Keep only citation-shaped text within Responsorial Psalm sections."""

    _HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._in_psalm = False
        self._line_parts: list[str] = []
        self.citations: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        _ = attrs
        normalized_tag = tag.lower()
        if normalized_tag in self._HEADING_TAGS:
            self._flush_line()
            self._heading_tag = normalized_tag
            self._heading_parts = []
        elif self._in_psalm and normalized_tag in {"br", "p", "div"}:
            self._flush_line()

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()
        if self._heading_tag == normalized_tag:
            self._finish_heading()
        elif self._in_psalm and normalized_tag in {"p", "div"}:
            self._flush_line()

    def handle_data(self, data: str) -> None:
        if self._heading_tag is not None:
            self._heading_parts.append(data)
        elif self._in_psalm:
            self._line_parts.append(data)

    def close(self) -> None:
        super().close()
        if self._heading_tag is not None:
            self._finish_heading()
        self._flush_line()

    def _finish_heading(self) -> None:
        self._flush_line()
        heading = _SPACE_RE.sub(" ", "".join(self._heading_parts)).strip()
        match = re.match(r"^responsorial\s+psalm\b", heading, flags=re.IGNORECASE)
        self._in_psalm = match is not None
        self._heading_tag = None
        self._heading_parts = []
        if match is not None:
            citation = _extract_psalm_citation(
                heading[match.end() :],
                allow_heading_qualifiers=True,
            )
            if citation is not None:
                self._add_citation(citation)

    def _flush_line(self) -> None:
        line = _SPACE_RE.sub(" ", "".join(self._line_parts)).strip()
        self._line_parts = []
        if not self._in_psalm:
            return
        citation = _extract_psalm_citation(line)
        if citation is not None:
            self._add_citation(citation)

    def _add_citation(self, citation: str) -> None:
        normalized = _normalize_citation(citation)
        if not any(_normalize_citation(value) == normalized for value in self.citations):
            self.citations.append(citation)


def _parse_iso_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ComparisonError(f"Invalid date {value!r}; use YYYY-MM-DD.") from exc
    if parsed.isoformat() != value:
        raise ComparisonError(f"Invalid date {value!r}; use YYYY-MM-DD.")
    return parsed


def _load_plan(path: Path) -> dict[str, Any]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ComparisonError(f"Could not read Daily Missal plan {path}: {exc}") from exc
    if not isinstance(result, dict):
        raise ComparisonError("Daily Missal plan must contain a JSON object.")
    return result


def _select_plan_day(plan: dict[str, Any], requested_date: date) -> dict[str, Any]:
    date_text = requested_date.isoformat()
    if plan.get("record_type") == "psalm_production_queue":
        days = plan.get("days")
        if not isinstance(days, list):
            raise ComparisonError("Daily Missal queue is missing its days array.")
        matches = [
            item for item in days
            if isinstance(item, dict) and item.get("date") == date_text
        ]
    elif plan.get("date") == date_text and isinstance(plan.get("reading_sets"), list):
        matches = [plan]
    else:
        matches = []
    if len(matches) > 1:
        raise ComparisonError(f"Daily Missal plan has duplicate entries for {date_text}.")
    if not matches or matches[0].get("status") == "failed":
        raise ComparisonError(f"Daily Missal plan has no available record for {date_text}.")
    return matches[0]


def _citation_values(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value]
    if isinstance(value, dict):
        return _citation_values(value.get("citation", value.get("reference")))
    if isinstance(value, list):
        return [citation for item in value for citation in _citation_values(item)]
    return []


def _primary_reading_set(reading_sets: list[Any]) -> dict[str, Any]:
    candidates = [item for item in reading_sets if isinstance(item, dict)]
    selected = [
        item for item in candidates
        if item.get("selection_status") == "selected_by_source"
    ]
    if len(selected) == 1:
        return selected[0]
    if len(selected) > 1:
        raise ComparisonError("Daily Missal plan marks multiple reading sets as primary.")
    if len(candidates) == 1:
        return candidates[0]
    raise ComparisonError(
        "Daily Missal plan has multiple reading sets without a source-selected primary set."
    )


def _plan_psalm_citations(day: dict[str, Any]) -> list[str]:
    reading_set = _primary_reading_set(day["reading_sets"])
    psalms = reading_set.get("psalms")
    citations: list[str] = []
    if isinstance(psalms, list):
        for psalm in psalms:
            if isinstance(psalm, dict):
                citations.extend(_citation_values(psalm.get("citation")))
                citations.extend(_citation_values(psalm.get("alternatives")))
    if not citations:
        readings = reading_set.get("reading_citations", [])
        if isinstance(readings, list):
            for reading in readings:
                if (
                    isinstance(reading, dict)
                    and str(reading.get("kind", "")).casefold()
                    in {"psalm", "responsorial psalm"}
                ):
                    citations.extend(_citation_values(reading.get("citation")))
                    citations.extend(_citation_values(reading.get("alternatives")))
    unique: list[str] = []
    for citation in citations:
        if _extract_psalm_citation(citation) is None:
            raise ComparisonError(
                "Daily Missal Psalm citation uses an unsupported format."
            )
        if not any(
            _normalize_citation(existing) == _normalize_citation(citation)
            for existing in unique
        ):
            unique.append(citation)
    if not unique:
        raise ComparisonError("Daily Missal plan has no Psalm citation for the requested date.")
    return unique


def _feed_psalm_citations(item: usccb.FeedItem) -> list[str]:
    parser = _PsalmCitationParser()
    try:
        parser.feed(item.description)
        parser.close()
    except (AssertionError, ValueError) as exc:
        raise ComparisonError("Could not parse the RSS Responsorial Psalm citation.") from exc
    if not parser.citations:
        raise ComparisonError("USCCB RSS item has no parseable Responsorial Psalm citation.")
    return parser.citations


def _result(
    requested_date: date,
    daily_citations: list[str],
    item: usccb.FeedItem | None,
    usccb_citations: list[str],
    title_difference: bool,
) -> dict[str, Any]:
    if item is None:
        comparison_result = "unavailable"
    else:
        daily_normalized = [_normalize_citation(value) for value in daily_citations]
        usccb_normalized = [_normalize_citation(value) for value in usccb_citations]
        comparison_result = (
            "match" if daily_normalized == usccb_normalized else "difference"
        )
    return {
        "schema_version": "1.0.0",
        "record_type": "psalm_citation_comparison",
        "comparison_date": requested_date.isoformat(),
        "result": comparison_result,
        "daily_missal": {
            "source_url": (
                f"{DAILY_MISSAL_API_URL}/{requested_date.isoformat()}.json?cal=us"
            ),
            "psalm_citations": daily_citations,
        },
        "usccb": {
            "source_url": USCCB_RSS_URL,
            "item_url": item.item_url if item is not None else None,
            "psalm_citations": usccb_citations,
        },
        "title_difference": title_difference,
        "full_usccb_text_persisted": False,
        "production_record_modified": False,
    }


def compare_plan_to_feed(
    plan: dict[str, Any],
    requested_date: date,
    feed_items: list[usccb.FeedItem],
) -> dict[str, Any]:
    day = _select_plan_day(plan, requested_date)
    daily_citations = _plan_psalm_citations(day)
    matching_items = [
        item for item in feed_items if item.calendar_date == requested_date
    ]
    if len(matching_items) > 1:
        raise ComparisonError(
            f"USCCB RSS contains duplicate items for {requested_date.isoformat()}."
        )
    if not matching_items:
        return _result(requested_date, daily_citations, None, [], False)

    item = matching_items[0]
    usccb_citations = _feed_psalm_citations(item)
    daily_title = (
        day.get("celebration", {}).get("name")
        if isinstance(day.get("celebration"), dict)
        else day.get("title")
    )
    title_difference = (
        isinstance(daily_title, str)
        and bool(daily_title)
        and bool(item.title)
        and daily_title != item.title
    )
    return _result(
        requested_date,
        daily_citations,
        item,
        usccb_citations,
        title_difference,
    )


def _serialize_result(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check one Daily Missal Psalm citation against the USCCB RSS feed."
    )
    parser.add_argument("--date", required=True, metavar="YYYY-MM-DD")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument(
        "--rss-fixture",
        type=Path,
        help="use a local RSS fixture instead of retrieving the fixed USCCB feed",
    )
    return parser


def main(
    argv: list[str] | None = None,
    *,
    feed_fetcher: Callable[[], bytes] | None = None,
) -> int:
    args = _build_parser().parse_args(argv)
    try:
        requested_date = _parse_iso_date(args.date)
        plan = _load_plan(args.plan)
        rss_bytes = (
            args.rss_fixture.read_bytes()
            if args.rss_fixture is not None
            else (feed_fetcher or usccb.fetch_feed)()
        )
        result = compare_plan_to_feed(
            plan,
            requested_date,
            usccb.parse_feed(rss_bytes),
        )
        sys.stdout.write(_serialize_result(result))
        if result["result"] == "unavailable":
            print(
                "notice: date is outside the current rolling USCCB RSS window.",
                file=sys.stderr,
            )
            return 0
        if result["result"] == "difference":
            print("Psalm citation difference detected.", file=sys.stderr)
            return 1
        print("Psalm citations match.", file=sys.stderr)
        return 0
    except (
        ComparisonError,
        usccb.IngestionError,
        OSError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
