from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import date
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from urllib.request import Request

from tools.liturgy import compare_usccb_daily_missal as comparator
from tools.liturgy import validate_usccb_psalm as usccb


FIXTURES = Path(__file__).parent / "fixtures"
REQUESTED_DATE = date(2026, 11, 25)


def load_plan() -> dict:
    return json.loads(
        (FIXTURES / "daily_missal_plan.json").read_text(encoding="utf-8")
    )


def load_feed() -> list[usccb.FeedItem]:
    return usccb.parse_feed((FIXTURES / "rss_comparison_match.xml").read_bytes())


class ComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_plan()
        self.feed_items = load_feed()

    def test_exact_match(self) -> None:
        result = comparator.compare_plan_to_feed(
            self.plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        self.assertEqual(result["result"], "match")
        self.assertEqual(
            result["daily_missal"]["psalm_citations"],
            result["usccb"]["psalm_citations"],
        )

    def test_normalized_equivalent_match(self) -> None:
        plan = deepcopy(self.plan)
        plan["days"][0]["reading_sets"][0]["psalms"][0]["citation"] = (
            "Psalms 98: 1, 2 – 3ab, 7-8, 9"
        )
        result = comparator.compare_plan_to_feed(
            plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        self.assertEqual(result["result"], "match")

    def test_different_psalm_citation(self) -> None:
        plan = deepcopy(self.plan)
        plan["days"][0]["reading_sets"][0]["psalms"][0]["citation"] = (
            "Psalm 97:1-3"
        )
        result = comparator.compare_plan_to_feed(
            plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        self.assertEqual(result["result"], "difference")

    def test_date_unavailable_from_rss(self) -> None:
        result = comparator.compare_plan_to_feed(
            self.plan,
            REQUESTED_DATE,
            [],
        )
        self.assertEqual(result["result"], "unavailable")
        self.assertIsNone(result["usccb"]["item_url"])
        self.assertEqual(result["usccb"]["psalm_citations"], [])

    def test_title_difference_does_not_change_match(self) -> None:
        plan = deepcopy(self.plan)
        plan["days"][0]["celebration"]["name"] = "Another synthetic title"
        result = comparator.compare_plan_to_feed(
            plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        self.assertEqual(result["result"], "match")
        self.assertTrue(result["title_difference"])

    def test_deterministic_json(self) -> None:
        result = comparator.compare_plan_to_feed(
            self.plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        serialized = comparator._serialize_result(result)
        self.assertEqual(serialized, comparator._serialize_result(result))
        self.assertTrue(serialized.endswith("\n"))

    def test_plan_remains_unchanged(self) -> None:
        plan = deepcopy(self.plan)
        original = deepcopy(plan)
        comparator.compare_plan_to_feed(plan, REQUESTED_DATE, self.feed_items)
        self.assertEqual(plan, original)

    def test_output_contains_no_usccb_verses_refrains_html_or_description(self) -> None:
        result = comparator.compare_plan_to_feed(
            self.plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        output = comparator._serialize_result(result)
        self.assertNotIn("Synthetic refrain", output)
        self.assertNotIn("Synthetic verse line", output)
        self.assertNotIn("<h4>", output)
        self.assertNotIn("description", output)
        self.assertEqual(
            set(result),
            {
                "schema_version",
                "record_type",
                "comparison_date",
                "result",
                "daily_missal",
                "usccb",
                "title_difference",
                "full_usccb_text_persisted",
                "production_record_modified",
            },
        )

    def test_result_records_no_production_modification(self) -> None:
        result = comparator.compare_plan_to_feed(
            self.plan,
            REQUESTED_DATE,
            self.feed_items,
        )
        self.assertFalse(result["production_record_modified"])
        self.assertFalse(result["full_usccb_text_persisted"])


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.directory = Path(self.temporary_directory.name)
        self.plan_path = self.directory / "plan.json"
        self.plan_path.write_bytes((FIXTURES / "daily_missal_plan.json").read_bytes())
        self.fixture_path = FIXTURES / "rss_comparison_match.xml"

    def invoke(self, *, fixture: bool = True) -> tuple[int, str, str]:
        args = [
            "--date",
            REQUESTED_DATE.isoformat(),
            "--plan",
            str(self.plan_path),
        ]
        if fixture:
            args.extend(["--rss-fixture", str(self.fixture_path)])
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = comparator.main(args)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_difference_exits_nonzero(self) -> None:
        plan = load_plan()
        plan["days"][0]["reading_sets"][0]["psalms"][0]["citation"] = "Psalm 97:1-3"
        self.plan_path.write_text(json.dumps(plan), encoding="utf-8")
        exit_code, stdout, _ = self.invoke()
        self.assertEqual(exit_code, 1)
        self.assertEqual(json.loads(stdout)["result"], "difference")

    def test_match_exits_zero(self) -> None:
        exit_code, stdout, stderr = self.invoke()
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout)["result"], "match")
        self.assertIn("match", stderr)
        self.assertEqual(sorted(path.name for path in self.directory.iterdir()), ["plan.json"])

    def test_unavailable_exits_zero_with_notice(self) -> None:
        rss_outside_window = self.fixture_path.read_bytes().replace(
            b"Wed, 25 Nov 2026 00:00:00 -0500",
            b"Thu, 26 Nov 2026 00:00:00 -0500",
        )
        with mock.patch.object(
            comparator.usccb,
            "fetch_feed",
            return_value=rss_outside_window,
        ):
            exit_code, stdout, stderr = self.invoke(fixture=False)
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout)["result"], "unavailable")
        self.assertIn("outside the current rolling USCCB RSS window", stderr)
        self.assertEqual(sorted(path.name for path in self.directory.iterdir()), ["plan.json"])

    def test_help_has_no_output_file_options(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            comparator.main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        help_text = stdout.getvalue()
        self.assertNotIn("--signal-output", help_text)
        self.assertNotIn("--force", help_text)
        self.assertNotIn("--output", help_text)

    def test_live_mode_requests_only_the_fixed_rss_feed(self) -> None:
        feed_bytes = self.fixture_path.read_bytes()
        requests: list[Request] = []

        class FakeResponse:
            headers = {"Content-Type": "application/rss+xml; charset=utf-8"}

            def __enter__(self) -> FakeResponse:
                return self

            def __exit__(self, *_: object) -> None:
                return None

            def getcode(self) -> int:
                return 200

            def read(self, size: int = -1) -> bytes:
                return feed_bytes[:size]

        def fake_urlopen(request: Request, **kwargs: object) -> FakeResponse:
            requests.append(request)
            self.assertIn("timeout", kwargs)
            return FakeResponse()

        with mock.patch(
            "tools.liturgy.validate_usccb_psalm.urllib.request.urlopen",
            side_effect=fake_urlopen,
        ):
            exit_code, stdout, _ = self.invoke(fixture=False)
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout)["result"], "match")
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].full_url, usccb.FEED_URL)
        self.assertNotIn(REQUESTED_DATE.isoformat(), requests[0].full_url)


if __name__ == "__main__":
    unittest.main()
