#!/usr/bin/env python3
# Script name: plan_daily_missal_psalms.py
# Purpose: Build deterministic Psalm production planning queues from The Daily Missal.
# Semantic version: 1.0.0
# Author: Christopher Bower
# Description: Retrieves United States Ordinary Form liturgical metadata and Psalm citations;
#              optionally includes only the source-provided WEB Catholic Edition Psalm text.
# Requirements and dependencies: Python 3.10+; Python standard library only.
# Usage examples:
#   python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25
#   python3 tools/liturgy/plan_daily_missal_psalms.py --start-date 2026-11-25 --days 15
#   python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25 --include-text
# Revision history:
#   2026-11-24 1.0.0 Initial Daily Missal Psalm planning and acquisition prototype.

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import email.utils
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE_URL = "https://thedailymissal.com/api/v1/day"
USER_AGENT = "SunoStudio-DailyMissalPlanner/1.0.0 (read-only planning prototype)"
REQUEST_TIMEOUT_SECONDS = 15
MAX_RESPONSE_BYTES = 5 * 1024 * 1024
MAX_ATTEMPTS = 3
BASE_RETRY_DELAY_SECONDS = 0.5
MAX_RETRY_DELAY_SECONDS = 5.0
MAX_PLANNING_DAYS = 15
WEB_CATHOLIC_EDITION = "World English Bible, Catholic Edition"
NON_TEXT_KEYS = {"text", "content", "html", "body", "fulltext", "textcontent"}


class DailyMissalError(Exception):
    """Expected retrieval, normalization, selection, or output failure."""


class ApiRequestError(DailyMissalError):
    def __init__(
        self,
        message: str,
        *,
        retryable: bool = False,
        retry_after: str | None = None,
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.retry_after = retry_after


def build_day_url(day: date, calendar: str, include_text: bool) -> str:
    params = {"cal": calendar}
    if include_text:
        params["text"] = "1"
    return f"{API_BASE_URL}/{day.isoformat()}.json?{urlencode(params)}"


def _json_content_type(value: str) -> bool:
    media_type = value.split(";", 1)[0].strip().lower()
    return media_type == "application/json" or media_type.endswith("+json")


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_at = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return None
        if retry_at.tzinfo is None:
            return None
        now = datetime.now(timezone.utc)
        return max(0.0, (retry_at - now).total_seconds())


def _retry_delay(error: ApiRequestError, attempt: int) -> float | None:
    exponential = min(
        BASE_RETRY_DELAY_SECONDS * (2 ** (attempt - 1)),
        MAX_RETRY_DELAY_SECONDS,
    )
    if error.retry_after is None:
        return exponential
    delay = _retry_after_seconds(error.retry_after)
    if delay is None:
        return exponential
    if delay > MAX_RETRY_DELAY_SECONDS:
        return None
    return max(delay, exponential)


def fetch_json(
    url: str,
    *,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
    opener: Callable[..., Any] | None = None,
    sleeper: Callable[[float], None] | None = None,
) -> dict[str, Any]:
    """Fetch one bounded JSON response, retrying only transient failures."""
    open_url = opener or urlopen
    sleep = sleeper or time.sleep
    last_error: ApiRequestError | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with open_url(request, timeout=timeout) as response:
                status = response.getcode()
                if status is None or not 200 <= status < 300:
                    retryable = status == 429 or (status is not None and 500 <= status < 600)
                    raise ApiRequestError(
                        f"Daily Missal API returned HTTP status {status!r}.",
                        retryable=retryable,
                        retry_after=response.headers.get("Retry-After"),
                    )
                content_type = response.headers.get("Content-Type", "")
                if not _json_content_type(content_type):
                    raise ApiRequestError(
                        f"Daily Missal API returned unexpected Content-Type {content_type!r}; "
                        "expected JSON."
                    )
                body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise ApiRequestError(
                        f"Daily Missal API response exceeds the {MAX_RESPONSE_BYTES}-byte limit."
                    )
                try:
                    payload = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ApiRequestError(f"Daily Missal API returned malformed JSON: {exc}.") from exc
                if not isinstance(payload, dict):
                    raise ApiRequestError("Daily Missal API JSON response must be an object.")
                return payload
        except HTTPError as exc:
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            last_error = ApiRequestError(
                f"Daily Missal API request failed with HTTP {exc.code} ({exc.reason})."
                + (f" Retry-After: {retry_after}." if retry_after else ""),
                retryable=exc.code == 429 or 500 <= exc.code < 600,
                retry_after=retry_after,
            )
        except ApiRequestError as exc:
            last_error = exc
        except (TimeoutError, socket.timeout) as exc:
            last_error = ApiRequestError(
                f"Timed out retrieving {url}; retry later.",
                retryable=True,
            )
        except URLError as exc:
            last_error = ApiRequestError(
                f"Network failure retrieving {url}: {exc.reason}.",
                retryable=True,
            )
        except OSError as exc:
            last_error = ApiRequestError(
                f"Network failure retrieving {url}: {exc}.",
                retryable=True,
            )

        assert last_error is not None
        if not last_error.retryable or attempt == MAX_ATTEMPTS:
            raise last_error
        delay = _retry_delay(last_error, attempt)
        if delay is None:
            suffix = (
                f" Retry-After {last_error.retry_after!r} exceeds the "
                f"{MAX_RETRY_DELAY_SECONDS:g}-second retry bound."
            )
            raise ApiRequestError(str(last_error) + suffix, retry_after=last_error.retry_after)
        retry_note = (
            f"; Retry-After={last_error.retry_after}"
            if last_error.retry_after is not None
            else ""
        )
        print(
            f"warning: attempt {attempt}/{MAX_ATTEMPTS} failed{retry_note}; "
            f"retrying in {delay:g}s: {last_error}",
            file=sys.stderr,
        )
        sleep(delay)

    assert last_error is not None
    raise last_error


def _without_text(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_text(child)
            for key, child in value.items()
            if key.casefold().replace("_", "") not in NON_TEXT_KEYS
        }
    if isinstance(value, list):
        return [_without_text(child) for child in value]
    return value


def _source_fields(value: dict[str, Any], known_keys: set[str]) -> dict[str, Any]:
    return _without_text(
        {key: child for key, child in value.items() if key not in known_keys}
    )


def _as_list(value: Any, description: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise DailyMissalError(f"Daily Missal {description} must be an array.")
    return value


def _normalize_alternative(value: Any) -> Any:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return _without_text(value)
    raise DailyMissalError("Daily Missal reading alternatives must be strings or objects.")


def _extract_psalm_text(reading: dict[str, Any]) -> Any:
    for key in ("text", "verses", "scriptureText", "scripture_text"):
        if key in reading:
            return _without_text_value(reading[key])
    return None


def _without_text_value(value: Any) -> Any:
    """Keep the value of the selected Psalm text while recursively removing unrelated fields."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [_without_text_value(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _without_text_value(child)
            for key, child in value.items()
            if key.casefold().replace("_", "") not in {"firstreading", "secondreading", "gospel"}
        }
    return value


def _normalize_reading(reading: Any, include_text: bool) -> dict[str, Any]:
    if not isinstance(reading, dict):
        raise DailyMissalError("Daily Missal readings must be objects.")
    kind = reading.get("kind")
    if not isinstance(kind, str) or not kind:
        raise DailyMissalError("Daily Missal reading is missing its kind.")
    label = reading.get("label")
    citation = reading.get("citation")
    if citation is not None and not isinstance(citation, str):
        raise DailyMissalError(f"Daily Missal {kind} citation must be a string or null.")
    alternatives = [
        _normalize_alternative(item)
        for item in _as_list(reading.get("alternatives"), f"{kind} alternatives")
    ]
    normalized: dict[str, Any] = {
        "kind": kind,
        "label": label if isinstance(label, str) else kind,
        "citation": citation,
        "alternatives": alternatives,
    }
    if "universalLectionary" in reading:
        normalized["universal_lectionary"] = reading["universalLectionary"]
    extras = _source_fields(
        reading,
        {"kind", "label", "citation", "alternatives", "universalLectionary"},
    )
    if extras:
        normalized["source_fields"] = extras
    if kind.casefold() == "psalm":
        normalized["psalm_text"] = _extract_psalm_text(reading) if include_text else None
    return normalized


def _normalize_reading_set(
    raw_set: dict[str, Any],
    *,
    index: int,
    primary: bool,
    include_text: bool,
) -> dict[str, Any]:
    raw_content = raw_set.get("ordinaryForm")
    if isinstance(raw_content, dict):
        content: dict[str, Any] = raw_content
    else:
        content = raw_set
    readings = _as_list(content.get("readings"), "reading set readings")
    normalized_readings = [
        _normalize_reading(reading, include_text=include_text) for reading in readings
    ]
    psalms: list[dict[str, Any]] = []
    reading_alternatives: list[dict[str, Any]] = []
    reading_citations: list[dict[str, Any]] = []
    for reading in normalized_readings:
        reading_citations.append(
            {
                "kind": reading["kind"],
                "label": reading["label"],
                "citation": reading["citation"],
                "alternatives": reading["alternatives"],
            }
        )
        if reading["alternatives"]:
            reading_alternatives.append(
                {
                    "kind": reading["kind"],
                    "label": reading["label"],
                    "citation": reading["citation"],
                    "alternatives": reading["alternatives"],
                }
            )
        if reading["kind"].casefold() == "psalm":
            psalm: dict[str, Any] = {
                "citation": reading["citation"],
                "alternatives": reading["alternatives"],
                "text_source": WEB_CATHOLIC_EDITION,
                "text_included": bool(include_text and reading["psalm_text"] is not None),
            }
            if include_text and reading["psalm_text"] is not None:
                psalm["text"] = reading["psalm_text"]
            psalms.append(psalm)

    label = None
    for key in ("setLabel", "set_label", "massLabel", "label", "name", "title"):
        if isinstance(raw_set.get(key), str) and raw_set[key]:
            label = raw_set[key]
            break
    if label is None:
        label = "Primary Mass" if primary else f"Other Mass {index}"

    readings_source = content.get("readingsSource", content.get("readings_source"))
    if readings_source is not None and not isinstance(readings_source, str):
        readings_source = str(readings_source)
    reading_source_folded = (readings_source or "").casefold()
    missing_proper = bool(
        content.get("missingProperReadings")
        or content.get("missing_proper_readings")
        or reading_source_folded in {"common", "commons", "no-proper"}
    )
    normalized_set: dict[str, Any] = {
        "set_id": (
            str(raw_set.get("id") or content.get("id") or "ordinary_form_primary")
            if primary
            else str(raw_set.get("id") or f"other_mass_{index}")
        ),
        "set_label": label,
        "selection_status": "selected_by_source" if primary else "available_unselected",
        "readings_source": readings_source,
        "readings_from_common": reading_source_folded in {"common", "commons"},
        "missing_proper_readings": missing_proper,
        "reading_citations": reading_citations,
        "reading_alternatives": reading_alternatives,
        "psalms": psalms,
    }
    celebration = raw_set.get("celebration", content.get("celebration"))
    if isinstance(celebration, dict):
        normalized_set["celebration"] = _normalize_celebration(celebration)
    known = {
        "ordinaryForm",
        "id",
        "setId",
        "set_id",
        "setLabel",
        "set_label",
        "massLabel",
        "label",
        "name",
        "title",
        "celebration",
        "readings",
        "readingsSource",
        "readings_source",
        "missingProperReadings",
        "missing_proper_readings",
        "otherMasses",
        "optionalMemorials",
        "season",
        "sundayCycle",
        "weekdayCycle",
        "psalterWeek",
        "translation",
        "officialReadings",
    }
    extras = _source_fields(raw_set, known)
    if extras:
        normalized_set["source_fields"] = extras
    return normalized_set


def _normalize_celebration(celebration: Any) -> dict[str, Any]:
    if not isinstance(celebration, dict):
        raise DailyMissalError("Daily Missal ordinaryForm is missing a celebration object.")
    colors = _as_list(celebration.get("colors"), "celebration colors")
    normalized: dict[str, Any] = {
        "id": celebration.get("id"),
        "name": celebration.get("name", celebration.get("title")),
        "rank": celebration.get("rank", celebration.get("class")),
        "colors": colors,
        "holy_day_of_obligation": celebration.get(
            "holyDayOfObligation",
            celebration.get("holy_day_of_obligation"),
        ),
    }
    extras = _source_fields(
        celebration,
        {"id", "name", "title", "rank", "class", "colors", "holyDayOfObligation", "holy_day_of_obligation"},
    )
    if extras:
        normalized["source_fields"] = extras
    return normalized


def _normalize_memorials(value: Any) -> list[dict[str, Any]]:
    memorials = _as_list(value, "optional memorials")
    normalized: list[dict[str, Any]] = []
    for memorial in memorials:
        if not isinstance(memorial, dict):
            raise DailyMissalError("Daily Missal optional memorials must be objects.")
        record: dict[str, Any] = {
            "id": memorial.get("id"),
            "name": memorial.get("name", memorial.get("title")),
            "colors": _as_list(memorial.get("colors"), "optional memorial colors"),
        }
        extras = _source_fields(memorial, {"id", "name", "title", "colors"})
        if extras:
            record["source_fields"] = extras
        normalized.append(record)
    return normalized


def normalize_day(
    payload: dict[str, Any],
    requested_date: date,
    *,
    calendar: str = "us",
    include_text: bool = False,
) -> dict[str, Any]:
    if payload.get("date") != requested_date.isoformat():
        raise DailyMissalError(
            f"Daily Missal returned date {payload.get('date')!r} for requested "
            f"date {requested_date.isoformat()}."
        )
    calendar_data = payload.get("calendar")
    if calendar_data is not None and not isinstance(calendar_data, dict):
        raise DailyMissalError("Daily Missal calendar metadata must be an object.")
    calendar_data = calendar_data or {}
    returned_calendar = calendar_data.get("id", calendar)
    if returned_calendar != calendar:
        raise DailyMissalError(
            f"Daily Missal returned calendar {returned_calendar!r}; expected {calendar!r}."
        )

    ordinary = payload.get("ordinaryForm")
    if not isinstance(ordinary, dict):
        raise DailyMissalError("Daily Missal response is missing ordinaryForm.")

    primary = _normalize_reading_set(
        ordinary,
        index=1,
        primary=True,
        include_text=include_text,
    )
    other_masses: list[Any] = []
    other_masses.extend(_as_list(payload.get("otherMasses"), "otherMasses"))
    other_masses.extend(_as_list(ordinary.get("otherMasses"), "ordinaryForm.otherMasses"))
    other_masses_present = "otherMasses" in payload or "otherMasses" in ordinary
    reading_sets = [primary]
    for index, mass in enumerate(other_masses, start=1):
        if not isinstance(mass, dict):
            raise DailyMissalError("Daily Missal otherMasses entries must be objects.")
        reading_sets.append(
            _normalize_reading_set(
                mass,
                index=index,
                primary=False,
                include_text=include_text,
            )
        )

    optional_memorials = _normalize_memorials(ordinary.get("optionalMemorials"))
    attention_reasons: list[str] = []
    if optional_memorials:
        attention_reasons.append("optional_memorial_choice")
    if len(reading_sets) > 1:
        attention_reasons.append("multiple_valid_reading_sets")
    if any(
        len(reading["alternatives"]) > 0
        for reading_set in reading_sets
        for reading in reading_set["reading_citations"]
    ):
        attention_reasons.append("reading_alternatives")
    if any(
        len(psalm["alternatives"]) > 0
        for reading_set in reading_sets
        for psalm in reading_set["psalms"]
    ) or sum(len(reading_set["psalms"]) for reading_set in reading_sets) > 1:
        attention_reasons.append("multiple_psalm_options")
    if any(reading_set["missing_proper_readings"] for reading_set in reading_sets):
        attention_reasons.append("missing_proper_readings")
    if not any(reading_set["psalms"] for reading_set in reading_sets):
        attention_reasons.append("psalm_citation_not_provided")

    calendar_label = calendar_data.get("label")
    if calendar_label is not None and not isinstance(calendar_label, str):
        raise DailyMissalError("Daily Missal calendar label must be a string.")
    normalized_day: dict[str, Any] = {
        "date": requested_date.isoformat(),
        "status": "available",
        "celebration": _normalize_celebration(ordinary.get("celebration")),
        "season": ordinary.get("season"),
        "sunday_cycle": ordinary.get("sundayCycle"),
        "weekday_cycle": ordinary.get("weekdayCycle"),
        "psalter_week": ordinary.get("psalterWeek"),
        "optional_memorials": optional_memorials,
        "reading_sets": reading_sets,
        "other_masses_present": other_masses_present,
        "calendar_label": calendar_label or "United States",
        "official_readings_url": ordinary.get("officialReadings"),
        "source_translation": ordinary.get("translation"),
        "attention_required": bool(attention_reasons),
        "attention_reasons": attention_reasons,
        "operator_choice_required": bool(attention_reasons),
    }
    if not any(reading_set["psalms"] for reading_set in reading_sets):
        normalized_day["psalm_source_explanation"] = (
            "The Daily Missal ordinaryForm and otherMasses records contain no reading "
            "with kind 'psalm'."
        )
    source_fields = _source_fields(
        payload,
        {"date", "calendar", "ordinaryForm", "otherMasses"},
    )
    if source_fields:
        normalized_day["source_fields"] = source_fields
    calendar_fields = _source_fields(calendar_data, {"id", "label"})
    if calendar_fields:
        normalized_day["calendar_source_fields"] = calendar_fields
    if include_text:
        if not isinstance(ordinary.get("translation"), str) or "world english bible" not in str(
            ordinary["translation"]
        ).casefold():
            raise DailyMissalError(
                "Requested Scripture text is not identified by the source as the "
                "World English Bible."
            )
        for reading_set in reading_sets:
            for psalm in reading_set["psalms"]:
                if psalm["citation"] and not psalm["text_included"]:
                    raise DailyMissalError(
                        f"Requested WEB Catholic Edition Psalm text was absent for "
                        f"{requested_date.isoformat()} ({psalm['citation']})."
                    )
    return normalized_day


def parse_iso_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise DailyMissalError(f"Invalid date {value!r}; use YYYY-MM-DD.") from exc
    if parsed.isoformat() != value:
        raise DailyMissalError(f"Invalid date {value!r}; use YYYY-MM-DD.")
    return parsed


def resolve_range(
    *,
    single_date: str | None,
    start_date: str | None,
    days: int | None,
) -> tuple[date, int]:
    if single_date is not None:
        if start_date is not None or days is not None:
            raise DailyMissalError("--date conflicts with --start-date and --days.")
        return parse_iso_date(single_date), 1
    if start_date is None or days is None:
        raise DailyMissalError("Provide --date or both --start-date and --days.")
    if days < 1:
        raise DailyMissalError("--days must be at least 1.")
    if days > MAX_PLANNING_DAYS:
        raise DailyMissalError(f"--days cannot exceed {MAX_PLANNING_DAYS}.")
    return parse_iso_date(start_date), days


def generate_queue(
    start_date: date,
    days: int,
    *,
    calendar: str = "us",
    include_text: bool = False,
    fetcher: Callable[[date, str, bool], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if not 1 <= days <= MAX_PLANNING_DAYS:
        raise DailyMissalError(f"Planning days must be between 1 and {MAX_PLANNING_DAYS}.")
    retrieve = fetcher or (
        lambda day, selected_calendar, with_text: fetch_json(
            build_day_url(day, selected_calendar, with_text)
        )
    )
    end_date = date.fromordinal(start_date.toordinal() + days - 1)
    cache: dict[tuple[str, bool, str], dict[str, Any]] = {}
    planned_days: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for offset in range(days):
        requested_day = date.fromordinal(start_date.toordinal() + offset)
        cache_key = (requested_day.isoformat(), include_text, calendar)
        try:
            if cache_key not in cache:
                cache[cache_key] = retrieve(requested_day, calendar, include_text)
            planned_days.append(
                normalize_day(
                    cache[cache_key],
                    requested_day,
                    calendar=calendar,
                    include_text=include_text,
                )
            )
        except DailyMissalError as exc:
            message = str(exc)
            failures.append({"date": requested_day.isoformat(), "error": message})
            planned_days.append(
                {
                    "date": requested_day.isoformat(),
                    "status": "failed",
                    "error": message,
                }
            )
        except (TypeError, ValueError, KeyError) as exc:
            message = f"Could not normalize Daily Missal data: {exc}."
            failures.append({"date": requested_day.isoformat(), "error": message})
            planned_days.append(
                {
                    "date": requested_day.isoformat(),
                    "status": "failed",
                    "error": message,
                }
            )

    complete = not failures
    source_translation = next(
        (
            day["source_translation"]
            for day in planned_days
            if day.get("status") == "available" and day.get("source_translation")
        ),
        "World English Bible (Catholic Edition)",
    )
    calendar_label = next(
        (
            day["calendar_label"]
            for day in planned_days
            if day.get("status") == "available" and day.get("calendar_label")
        ),
        "United States",
    )
    source = {
        "name": "The Daily Missal",
        "role": "primary_liturgical_planning_source",
        "api_base_url": API_BASE_URL,
        "scripture_translation": WEB_CATHOLIC_EDITION,
        "scripture_license": "public_domain",
        "official_usccb_text_reproduced": False,
        "source_translation": source_translation,
    }
    document: dict[str, Any] = {
        "schema_version": "1.0.0",
        "record_type": "psalm_production_queue",
        "completion_status": "complete" if complete else "incomplete",
        "calendar": {"id": calendar, "label": calendar_label},
        "requested_range": {
            "start_date": start_date.isoformat(),
            "days": days,
            "end_date": end_date.isoformat(),
        },
        "source": source,
        "days": planned_days,
        "failures": failures,
    }
    return document


def serialize_queue(document: dict[str, Any]) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def write_atomic(path: Path, content: str, force: bool = False) -> None:
    path = path.expanduser()
    parent = path.parent
    if not parent.is_dir():
        raise DailyMissalError(f"Output directory does not exist: {parent}")
    if path.exists() and not force:
        raise DailyMissalError(f"Output already exists: {path}; pass --force to replace it.")

    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=parent,
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary_path, path)
        else:
            os.link(temporary_path, path)
            temporary_path.unlink()
        temporary_path = None
        try:
            directory_fd = os.open(parent, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(directory_fd)
        except OSError:
            pass
        finally:
            os.close(directory_fd)
    except FileExistsError as exc:
        raise DailyMissalError(
            f"Output already exists: {path}; pass --force to replace it."
        ) from exc
    except OSError as exc:
        raise DailyMissalError(f"Could not atomically write {path}: {exc}") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Daily Missal United States Psalm planning queue. "
            "Date selection is always explicit."
        )
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--date", metavar="YYYY-MM-DD", help="plan one explicit date")
    selection.add_argument(
        "--start-date",
        metavar="YYYY-MM-DD",
        help="first date in an inclusive planning range; requires --days",
    )
    parser.add_argument("--days", type=int, help=f"range length from 1 to {MAX_PLANNING_DAYS}")
    parser.add_argument("--calendar", choices=("us",), default="us", help="liturgical calendar")
    parser.add_argument(
        "--include-text",
        action="store_true",
        help="request WEB Catholic Edition text and retain only Psalm text",
    )
    parser.add_argument("--output", type=Path, help="write JSON here instead of stdout")
    parser.add_argument("--force", action="store_true", help="atomically replace --output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.force and args.output is None:
        parser.error("--force requires --output.")
    if args.output is not None and args.output.exists() and not args.force:
        print(
            f"error: output already exists: {args.output}; pass --force to replace it.",
            file=sys.stderr,
        )
        return 2
    try:
        start_date, days = resolve_range(
            single_date=args.date,
            start_date=args.start_date,
            days=args.days,
        )
        queue = generate_queue(
            start_date,
            days,
            calendar=args.calendar,
            include_text=args.include_text,
        )
        serialized = serialize_queue(queue)
        if args.output is None:
            sys.stdout.write(serialized)
        else:
            write_atomic(args.output, serialized, force=args.force)
        print(
            f"Daily Missal plan {queue['completion_status']}: "
            f"{len(queue['days'])} date(s), {len(queue['failures'])} failure(s).",
            file=sys.stderr,
        )
        return 0 if queue["completion_status"] == "complete" else 1
    except DailyMissalError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
