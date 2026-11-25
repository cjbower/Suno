from __future__ import annotations

from datetime import date
from typing import Any
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest import mock
import urllib.error
from urllib.request import Request

from tools.liturgy import plan_daily_missal_psalms as planner


FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class FixtureFetcher:
    def __init__(self, fixtures: dict[str, dict[str, Any]]) -> None:
        self.fixtures = fixtures
        self.calls: list[tuple[date, str, bool]] = []

    def __call__(self, requested_date: date, calendar: str, include_text: bool) -> dict[str, Any]:
        self.calls.append((requested_date, calendar, include_text))
        value = self.fixtures.get(requested_date.isoformat())
        if value is None:
            raise planner.DailyMissalError("synthetic date unavailable")
        return value


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        status: int = 200,
        content_type: str = "application/json; charset=utf-8",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.body = body
        self.status = status
        self.headers = {"Content-Type": content_type, **(headers or {})}

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> bool:
        return exc_type is None and exc_value is None and traceback is None

    def getcode(self) -> int:
        return self.status

    def read(self, size: int = -1) -> bytes:
        return self.body[:size]


def response_opener(response: FakeResponse):
    def open_response(request: Request, **kwargs: Any) -> FakeResponse:
        if not isinstance(request, Request):
            raise AssertionError("fetch_json must use urllib.request.Request")
        if "timeout" not in kwargs:
            raise AssertionError("fetch_json must set a bounded timeout")
        return response

    return open_response


class RangeTests(unittest.TestCase):
    def test_explicit_single_date(self) -> None:
        self.assertEqual(
            planner.resolve_range(single_date="2026-11-25", start_date=None, days=None),
            (date(2026, 11, 25), 1),
        )

    def test_explicit_date_range(self) -> None:
        self.assertEqual(
            planner.resolve_range(single_date=None, start_date="2026-11-25", days=15),
            (date(2026, 11, 25), 15),
        )

    def test_selection_is_required(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "Provide --date"):
            planner.resolve_range(single_date=None, start_date=None, days=None)

    def test_date_conflicts_with_range(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "conflicts"):
            planner.resolve_range(single_date="2026-11-25", start_date="2026-11-25", days=2)

    def test_range_requires_both_start_and_days(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "both --start-date and --days"):
            planner.resolve_range(single_date=None, start_date="2026-11-25", days=None)

    def test_range_rejects_zero_days(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "at least 1"):
            planner.resolve_range(single_date=None, start_date="2026-11-25", days=0)

    def test_range_rejects_more_than_fifteen_days(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "cannot exceed 15"):
            planner.resolve_range(single_date=None, start_date="2026-11-25", days=16)

    def test_date_must_be_iso_format(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "YYYY-MM-DD"):
            planner.parse_iso_date("2026-2-5")

    def test_cli_requires_explicit_selection(self) -> None:
        with mock.patch("sys.stderr"):
            self.assertEqual(planner.main([]), 1)

    def test_cli_rejects_date_and_range_conflict(self) -> None:
        with mock.patch("sys.stderr"), self.assertRaises(SystemExit) as raised:
            planner.main(["--date", "2026-11-25", "--start-date", "2026-11-25", "--days", "1"])
        self.assertEqual(raised.exception.code, 2)


class NormalizationTests(unittest.TestCase):
    def test_normalizes_psalm_metadata_and_strips_unrelated_text(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        normalized = planner.normalize_day(source, date(2026, 11, 25))
        self.assertEqual(normalized["date"], "2026-11-25")
        self.assertEqual(normalized["status"], "available")
        self.assertEqual(normalized["source_translation"], "World English Bible (Catholic Edition)")
        primary = normalized["reading_sets"][0]
        self.assertEqual(primary["psalms"][0]["citation"], "Psalm 98:1, 2-3ab, 7-8, 9")
        serialized = planner.serialize_queue(
            planner.generate_queue(
                date(2026, 11, 25),
                1,
                fetcher=FixtureFetcher({"2026-11-25": source}),
            )
        )
        self.assertNotIn("Synthetic non-Psalm text", serialized)
        self.assertNotIn("must be filtered from metadata", serialized)
        document = json.loads(serialized)
        fields = document["days"][0]["reading_sets"][0]["source_fields"]
        self.assertEqual(fields["newApiField"], {"retained": True})
        self.assertIn("missal1962", document["days"][0]["source_fields"])

    def test_preserves_reading_and_psalm_alternatives_without_selecting(self) -> None:
        source = fixture("daily_missal_alternate_reading.json")
        normalized = planner.normalize_day(source, date(2026, 11, 29))
        primary = normalized["reading_sets"][0]
        gospel = next(item for item in primary["reading_citations"] if item["kind"] == "gospel")
        self.assertEqual(gospel["alternatives"], ["Synthetic 3:1-2"])
        self.assertIn("reading_alternatives", normalized["attention_reasons"])
        self.assertEqual(primary["selection_status"], "selected_by_source")

    def test_preserves_other_masses_and_psalm_alternatives(self) -> None:
        source = fixture("daily_missal_other_masses.json")
        normalized = planner.normalize_day(source, date(2026, 12, 1))
        self.assertEqual(len(normalized["reading_sets"]), 2)
        self.assertTrue(normalized["other_masses_present"])
        other = normalized["reading_sets"][1]
        self.assertEqual(other["set_label"], "Mass for a Synthetic Intention")
        self.assertEqual(other["selection_status"], "available_unselected")
        self.assertEqual(other["psalms"][0]["alternatives"], ["Psalm 34:2-3"])
        self.assertTrue(other["missing_proper_readings"])
        self.assertIn("multiple_valid_reading_sets", normalized["attention_reasons"])
        self.assertIn("multiple_psalm_options", normalized["attention_reasons"])
        self.assertEqual(other["source_fields"]["apiVersionTwoField"], "preserve this")

    def test_marks_common_readings_and_missing_proper_readings(self) -> None:
        source = fixture("daily_missal_other_masses.json")
        normalized = planner.normalize_day(source, date(2026, 12, 1))
        other = normalized["reading_sets"][1]
        self.assertTrue(other["readings_from_common"])
        self.assertIn("missing_proper_readings", normalized["attention_reasons"])

    def test_preserves_optional_memorial(self) -> None:
        source = fixture("daily_missal_optional_memorial.json")
        normalized = planner.normalize_day(source, date(2026, 12, 2))
        self.assertEqual(
            normalized["optional_memorials"][0]["name"],
            "Synthetic Optional Memorial",
        )
        self.assertIn("optional_memorial_choice", normalized["attention_reasons"])
        self.assertTrue(normalized["operator_choice_required"])

    def test_missing_ordinary_form_is_rejected(self) -> None:
        with self.assertRaisesRegex(planner.DailyMissalError, "missing ordinaryForm"):
            planner.normalize_day({"date": "2026-11-25"}, date(2026, 11, 25))

    def test_mismatched_response_date_is_rejected(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        with self.assertRaisesRegex(planner.DailyMissalError, "returned date"):
            planner.normalize_day(source, date(2026, 11, 26))

    def test_mismatched_calendar_is_rejected(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        source["calendar"]["id"] = "ca"
        with self.assertRaisesRegex(planner.DailyMissalError, "expected 'us'"):
            planner.normalize_day(source, date(2026, 11, 25))

    def test_missing_psalm_is_explicitly_flagged(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        source["ordinaryForm"]["readings"] = []
        normalized = planner.normalize_day(source, date(2026, 11, 25))
        self.assertTrue(normalized["attention_required"])
        self.assertIn("psalm_citation_not_provided", normalized["attention_reasons"])
        self.assertIn("psalm_source_explanation", normalized)

    def test_text_is_included_only_for_psalm_when_requested(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        normalized = planner.normalize_day(
            source,
            date(2026, 11, 25),
            include_text=True,
        )
        psalm = normalized["reading_sets"][0]["psalms"][0]
        self.assertTrue(psalm["text_included"])
        self.assertEqual(
            psalm["text"]["verses"][0]["text"],
            "A wholly synthetic public-domain test line.",
        )
        source_fields = normalized["reading_sets"][0]["source_fields"]
        self.assertNotIn("text", source_fields.get("newApiField", {}))

    def test_text_request_requires_web_translation_identification(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        source["ordinaryForm"]["translation"] = None
        with self.assertRaisesRegex(planner.DailyMissalError, "not identified"):
            planner.normalize_day(source, date(2026, 11, 25), include_text=True)

    def test_source_field_nested_text_is_removed(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        source["calendar"]["newCalendarField"] = {
            "region": "synthetic",
            "text": "must not be copied",
        }
        source["unexpectedMetadata"] = {
            "supported": True,
            "text": "must not be copied",
            "nested": {"body": "must also not be copied"},
        }
        normalized = planner.normalize_day(source, date(2026, 11, 25))
        self.assertEqual(
            normalized["source_fields"]["unexpectedMetadata"],
            {"supported": True, "nested": {}},
        )
        self.assertEqual(
            normalized["calendar_source_fields"]["newCalendarField"],
            {"region": "synthetic"},
        )


class QueueTests(unittest.TestCase):
    def test_builds_deterministic_queue_without_retrieval_time(self) -> None:
        source = fixture("daily_missal_single_psalm.json")
        fetcher = FixtureFetcher({"2026-11-25": source})
        queue = planner.generate_queue(date(2026, 11, 25), 1, fetcher=fetcher)
        first = planner.serialize_queue(queue)
        second = planner.serialize_queue(queue)
        self.assertEqual(first, second)
        self.assertTrue(first.endswith("\n"))
        self.assertNotIn("retrieved_at", first)
        self.assertEqual(queue["completion_status"], "complete")
        self.assertFalse(queue["source"]["official_usccb_text_reproduced"])
        self.assertEqual(len(fetcher.calls), 1)

    def test_builds_incomplete_queue_with_explicit_date_failure(self) -> None:
        first = fixture("daily_missal_single_psalm.json")
        fetcher = FixtureFetcher({"2026-11-25": first})
        queue = planner.generate_queue(date(2026, 11, 25), 2, fetcher=fetcher)
        self.assertEqual(queue["completion_status"], "incomplete")
        self.assertEqual([day["status"] for day in queue["days"]], ["available", "failed"])
        self.assertEqual(queue["failures"][0]["date"], "2026-11-26")

    def test_fails_normalization_for_malformed_payload(self) -> None:
        with self.assertRaises(json.JSONDecodeError):
            json.loads((FIXTURES / "daily_missal_malformed.json").read_text(encoding="utf-8"))

    def test_day_url_only_requests_text_when_explicit(self) -> None:
        day = date(2026, 11, 25)
        self.assertNotIn("text=1", planner.build_day_url(day, "us", False))
        self.assertIn("text=1", planner.build_day_url(day, "us", True))

    def test_output_refuses_overwrite_without_force(self) -> None:
        queue = planner.generate_queue(
            date(2026, 11, 25),
            1,
            fetcher=FixtureFetcher(
                {"2026-11-25": fixture("daily_missal_single_psalm.json")}
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "queue.json"
            output.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(planner.DailyMissalError, "pass --force"):
                planner.write_atomic(output, planner.serialize_queue(queue))
            self.assertEqual(output.read_text(encoding="utf-8"), "existing")

    def test_force_atomically_replaces_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "queue.json"
            output.write_text("old", encoding="utf-8")
            planner.write_atomic(output, '{"new": true}\n', force=True)
            self.assertEqual(output.read_text(encoding="utf-8"), '{"new": true}\n')
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_atomic_write_failure_cleans_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "queue.json"
            with mock.patch.object(planner.os, "replace", side_effect=OSError("simulated")):
                with self.assertRaisesRegex(planner.DailyMissalError, "Could not atomically write"):
                    planner.write_atomic(output, '{"new": true}\n', force=True)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_atomic_write_requires_existing_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "missing" / "queue.json"
            with self.assertRaisesRegex(planner.DailyMissalError, "directory does not exist"):
                planner.write_atomic(output, "{}\n")


class RetrievalTests(unittest.TestCase):
    def test_fetch_sends_user_agent_timeout_and_json_accept(self) -> None:
        requests: list[tuple[Request, int]] = []

        def opener(request: Request, timeout: int) -> FakeResponse:
            requests.append((request, timeout))
            return FakeResponse(b'{"date":"2026-11-25"}')

        result = planner.fetch_json("https://example.test/day.json", opener=opener)
        self.assertEqual(result["date"], "2026-11-25")
        request, timeout = requests[0]
        self.assertEqual(timeout, planner.REQUEST_TIMEOUT_SECONDS)
        self.assertEqual(request.get_header("User-agent"), planner.USER_AGENT)
        self.assertEqual(request.get_header("Accept"), "application/json")

    def test_rejects_unexpected_content_type(self) -> None:
        with self.assertRaisesRegex(planner.ApiRequestError, "unexpected Content-Type"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=response_opener(FakeResponse(
                    b"{}",
                    content_type="text/html",
                )),
                sleeper=lambda _: None,
            )

    def test_rejects_malformed_json(self) -> None:
        with self.assertRaisesRegex(planner.ApiRequestError, "malformed JSON"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=response_opener(FakeResponse(b"{")),
                sleeper=lambda _: None,
            )

    def test_rejects_non_object_json(self) -> None:
        with self.assertRaisesRegex(planner.ApiRequestError, "must be an object"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=response_opener(FakeResponse(b"[]")),
                sleeper=lambda _: None,
            )

    def test_rejects_oversized_response(self) -> None:
        with mock.patch.object(planner, "MAX_RESPONSE_BYTES", 3):
            with self.assertRaisesRegex(planner.ApiRequestError, "exceeds"):
                planner.fetch_json(
                    "https://example.test/day.json",
                    opener=response_opener(FakeResponse(b'{"date":1}')),
                    sleeper=lambda _: None,
                )

    def test_retries_transient_http_failure_with_bounded_attempts(self) -> None:
        attempts: list[int] = []
        sleeps: list[float] = []

        def opener(request: Request, **kwargs: Any) -> FakeResponse:
            self.assertIsInstance(request, Request)
            self.assertIn("timeout", kwargs)
            attempts.append(1)
            if len(attempts) < 3:
                return FakeResponse(
                    b"",
                    status=503,
                    headers={"Retry-After": "0"},
                )
            return FakeResponse(b'{"date":"2026-11-25"}')

        result = planner.fetch_json(
            "https://example.test/day.json",
            opener=opener,
            sleeper=sleeps.append,
        )
        self.assertEqual(result["date"], "2026-11-25")
        self.assertEqual(len(attempts), 3)
        self.assertEqual(sleeps, [0.5, 1.0])

    def test_does_not_retry_permanent_http_failure(self) -> None:
        attempts: list[int] = []

        def opener(request: Request, **kwargs: Any) -> FakeResponse:
            self.assertIsInstance(request, Request)
            self.assertIn("timeout", kwargs)
            attempts.append(1)
            return FakeResponse(b"", status=404)

        with self.assertRaisesRegex(planner.ApiRequestError, "HTTP status 404"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=opener,
                sleeper=lambda _: None,
            )
        self.assertEqual(len(attempts), 1)

    def test_retries_timeout_and_surfaces_actionable_error(self) -> None:
        attempts: list[int] = []
        sleeps: list[float] = []

        def opener(request: Request, **kwargs: Any) -> FakeResponse:
            self.assertIsInstance(request, Request)
            self.assertIn("timeout", kwargs)
            attempts.append(1)
            raise socket.timeout("slow")

        with self.assertRaisesRegex(planner.ApiRequestError, "Timed out"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=opener,
                sleeper=sleeps.append,
            )
        self.assertEqual(len(attempts), planner.MAX_ATTEMPTS)
        self.assertEqual(len(sleeps), planner.MAX_ATTEMPTS - 1)

    def test_network_failure_is_actionable(self) -> None:
        error = urllib.error.URLError("connection refused")
        with self.assertRaisesRegex(planner.ApiRequestError, "Network failure"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=mock.Mock(side_effect=error),
                sleeper=lambda _: None,
            )

    def test_rejects_retry_after_beyond_delay_bound(self) -> None:
        with self.assertRaisesRegex(planner.ApiRequestError, "exceeds the 5-second retry bound"):
            planner.fetch_json(
                "https://example.test/day.json",
                opener=response_opener(FakeResponse(
                    b"",
                    status=503,
                    headers={"Retry-After": "30"},
                )),
                sleeper=lambda _: None,
            )


if __name__ == "__main__":
    unittest.main()
