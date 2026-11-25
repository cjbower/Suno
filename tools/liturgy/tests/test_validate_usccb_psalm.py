from __future__ import annotations

from datetime import date
from email.message import Message
import io
import json
from pathlib import Path
import socket
import unittest
from unittest import mock
import urllib.error

from tools.liturgy import validate_usccb_psalm as ingestion


FIXTURES = Path(__file__).parent / "fixtures"


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def feed_with_description(description: str, *, title: str = "Synthetic liturgical day") -> bytes:
    import html

    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<rss version='2.0'><channel><item>"
        f"<title>{title}</title>"
        "<link>https://example.test/readings/synthetic</link>"
        "<pubDate>Tue, 24 Nov 2026 00:00:00 -0500</pubDate>"
        f"<description>{html.escape(description)}</description>"
        "</item></channel></rss>"
    ).encode()


def selected_item(xml_bytes: bytes, selection_date: str = "2026-11-24") -> ingestion.FeedItem:
    items = ingestion.parse_feed(xml_bytes)
    return ingestion.select_item(items, latest=False, requested_date=selection_date)


class PsalmParsingTests(unittest.TestCase):
    def test_single_response_and_ordered_verse_groups(self) -> None:
        item = selected_item(fixture_bytes("single_response.xml"))
        record = ingestion.build_record(item)

        self.assertEqual(record["source"]["published"], "Tue, 24 Nov 2026 00:00:00 -0500")
        self.assertEqual(record["liturgical_day"]["date"], "2026-11-24")
        self.assertEqual(record["psalm"]["citation"], "Psalm 96:10, 11-12, 13")
        self.assertEqual(
            record["psalm"]["responses"],
            [{"text": "A fictional refrain follows.", "source_notation": "(13b)"}],
        )
        verses = record["psalm"]["verses"]
        self.assertEqual([verse["sequence"] for verse in verses], [1, 2, 3])
        self.assertEqual([verse["source_verse_number"] for verse in verses], [10, 11, 12])
        self.assertEqual(
            verses[0]["lines"],
            ["Fictional voices greet the sunrise.", "Soft bells welcome the morning."],
        )

    def test_alternate_responses_are_retained(self) -> None:
        record = ingestion.build_record(
            selected_item(fixture_bytes("alternate_response.xml"), "2026-11-19")
        )
        self.assertEqual(
            record["psalm"]["responses"],
            [
                {"text": "The fictional dawn brings hope.", "source_notation": "(Rev. 5:10)"},
                {"text": "Alleluia.", "source_notation": None},
            ],
        )

    def test_repeated_refrain_in_one_paragraph_is_not_an_alternate_response(self) -> None:
        record = ingestion.build_record(
            selected_item(fixture_bytes("repeated_response_single_paragraph.xml"))
        )
        self.assertEqual(
            record["psalm"]["responses"],
            [{"text": "A fictional refrain.", "source_notation": "(13b)"}],
        )
        self.assertEqual(
            [verse["lines"] for verse in record["psalm"]["verses"]],
            [
                ["A fictional verse line one.", "A fictional verse line two."],
                ["A second fictional verse line one.", "A second fictional verse line two."],
                ["A third fictional verse line one.", "A third fictional verse line two."],
            ],
        )

    def test_parenthetical_source_notation_is_preserved(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 1:1</p><p>R. (1b) A synthetic refrain.</p>"
                "<p><sup>1</sup>A synthetic verse.</p></div>"
            )
        )
        response = ingestion.build_record(item)["psalm"]["responses"][0]
        self.assertEqual(response["source_notation"], "(1b)")

    def test_distinct_notations_for_same_text_remain_distinct_choices(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 1:1</p><p>R. (1a) A refrain.</p>"
                "<p>R. (1b) A refrain.</p><p>A synthetic verse.</p></div>"
            )
        )
        responses = ingestion.build_record(item)["psalm"]["responses"]
        self.assertEqual(
            responses,
            [
                {"text": "A refrain.", "source_notation": "(1a)"},
                {"text": "A refrain.", "source_notation": "(1b)"},
            ],
        )

    def test_response_spacing_and_nonbreaking_spaces_are_normalized(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 1:1</p><p>R. &nbsp; &nbsp; A&nbsp;synthetic&nbsp;refrain.</p>"
                "<p><sup>1</sup> First&nbsp;line.<br>Second&nbsp;line.</p></div>"
            )
        )
        psalm = ingestion.build_record(item)["psalm"]
        self.assertEqual(psalm["responses"][0]["text"], "A synthetic refrain.")
        self.assertEqual(psalm["verses"][0]["lines"], ["First line.", "Second line."])

    def test_heading_is_selected_by_text_not_section_position(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>First Reading</h4><div>Not a psalm.</div>"
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 3:1</p><p>R. A refrain.</p><p><sup>1</sup>A verse.</p>"
                "</div><h4>Gospel</h4>"
            )
        )
        self.assertEqual(ingestion.build_record(item)["psalm"]["citation"], "Psalm 3:1")

    def test_citation_can_be_outside_poetry_container(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><p>Psalm 4:2-3</p>"
                "<div class='poetry'><p>R. A refrain.</p><p>A synthetic verse.</p></div>"
            )
        )
        self.assertEqual(ingestion.build_record(item)["psalm"]["citation"], "Psalm 4:2-3")

    def test_no_explicit_verse_numbers_are_inferred(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 5:1</p><p>R. A refrain.</p>"
                "<p>First line.<br>Second line.</p><p>Another verse group.</p></div>"
            )
        )
        verses = ingestion.build_record(item)["psalm"]["verses"]
        self.assertEqual([verse["sequence"] for verse in verses], [1, 2])
        self.assertTrue(all("source_verse_number" not in verse for verse in verses))

    def test_multiple_explicit_verse_markers_on_one_line_are_preserved(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 5:1-2</p><p>R. A refrain.</p>"
                "<p><sup>1</sup> First verse. <sup>2</sup> Second verse.</p></div>"
            )
        )
        verses = ingestion.build_record(item)["psalm"]["verses"]
        self.assertEqual([verse["source_verse_number"] for verse in verses], [1, 2])
        self.assertEqual([verse["lines"] for verse in verses], [["First verse."], ["Second verse."]])

    def test_no_psalm_section_fails(self) -> None:
        item = selected_item(feed_with_description("<h4>Gospel</h4><p>No psalm.</p>"))
        with self.assertRaisesRegex(ingestion.IngestionError, "No Responsorial Psalm heading"):
            ingestion.build_record(item)

    def test_multiple_psalm_sections_fail(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'><p>Psalm 1:1</p>"
                "<p>R. First.</p><p>Verse.</p></div>"
                "<h4>Responsorial Psalm</h4><div class='poetry'><p>Psalm 2:1</p>"
                "<p>R. Second.</p><p>Verse.</p></div>"
            )
        )
        with self.assertRaisesRegex(ingestion.IngestionError, "found 2"):
            ingestion.build_record(item)

    def test_missing_citation_fails(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>R. A refrain.</p><p>A verse.</p></div>"
            )
        )
        with self.assertRaisesRegex(ingestion.IngestionError, "no parseable Psalm citation"):
            ingestion.build_record(item)

    def test_missing_response_fails(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 1:1</p><p>A verse.</p></div>"
            )
        )
        with self.assertRaisesRegex(ingestion.IngestionError, "No response marked R"):
            ingestion.build_record(item)

    def test_empty_verse_content_fails(self) -> None:
        item = selected_item(
            feed_with_description(
                "<h4>Responsorial Psalm</h4><div class='poetry'>"
                "<p>Psalm 1:1</p><p>R. A refrain.</p><p><sup>1</sup> &nbsp; </p>"
                "</div>"
            )
        )
        with self.assertRaisesRegex(ingestion.IngestionError, "no non-empty verse content"):
            ingestion.build_record(item)

    def test_malformed_xml_fails_actionably(self) -> None:
        with self.assertRaisesRegex(ingestion.IngestionError, "malformed XML"):
            ingestion.parse_feed(fixture_bytes("malformed.xml"))


class SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.items = ingestion.parse_feed(fixture_bytes("multiple_items.xml"))

    def test_multiple_items_are_parsed(self) -> None:
        self.assertEqual(len(self.items), 2)
        self.assertEqual(self.items[0].calendar_date, date(2026, 11, 24))

    def test_explicit_date_selects_exact_item(self) -> None:
        item = ingestion.select_item(self.items, latest=False, requested_date="2026-11-23")
        self.assertEqual(item.title, "Older synthetic day")

    def test_latest_uses_newest_publication_timestamp(self) -> None:
        item = ingestion.select_item(self.items, latest=True, requested_date=None)
        self.assertEqual(item.title, "Newest synthetic day")

    def test_absent_date_reports_available_dates(self) -> None:
        with self.assertRaisesRegex(
            ingestion.IngestionError,
            r"2026-11-23, 2026-11-24",
        ):
            ingestion.select_item(self.items, latest=False, requested_date="2026-11-22")

    def test_duplicate_date_is_rejected(self) -> None:
        duplicated = [self.items[0], self.items[0]]
        with self.assertRaisesRegex(ingestion.IngestionError, "found 2"):
            ingestion.select_item(duplicated, latest=False, requested_date="2026-11-24")

    def test_latest_and_date_conflict_is_rejected_by_cli(self) -> None:
        with mock.patch("sys.stderr"), self.assertRaises(SystemExit) as raised:
            ingestion.main(["--latest", "--date", "2026-11-24"])
        self.assertEqual(raised.exception.code, 2)

    def test_selection_is_required_by_cli(self) -> None:
        with mock.patch("sys.stderr"), self.assertRaises(SystemExit) as raised:
            ingestion.main([])
        self.assertEqual(raised.exception.code, 2)

    def test_invalid_date_format_is_rejected(self) -> None:
        with self.assertRaisesRegex(ingestion.IngestionError, "use YYYY-MM-DD"):
            ingestion.select_item(self.items, latest=False, requested_date="2026-2-3")


class RetrievalTests(unittest.TestCase):
    class FakeResponse:
        def __init__(self, body: bytes, content_type: str, status: int = 200) -> None:
            self.body = body
            self.headers = {"Content-Type": content_type}
            self.status = status

        def __enter__(self) -> RetrievalTests.FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def getcode(self) -> int:
            return self.status

        def read(self, size: int = -1) -> bytes:
            return self.body[:size]

    def test_fetch_sends_user_agent_timeout_and_accepts_rss_content_type(self) -> None:
        response = self.FakeResponse(b"<rss/>", "application/rss+xml; charset=utf-8")
        with mock.patch.object(ingestion.urllib.request, "urlopen", return_value=response) as open_url:
            self.assertEqual(ingestion.fetch_feed(timeout=7), b"<rss/>")
        request = open_url.call_args.args[0]
        timeout = open_url.call_args.kwargs["timeout"]
        self.assertEqual(request.get_header("User-agent"), ingestion.USER_AGENT)
        self.assertEqual(timeout, 7)

    def test_unexpected_content_type_fails(self) -> None:
        response = self.FakeResponse(b"<rss/>", "text/html")
        with mock.patch.object(ingestion.urllib.request, "urlopen", return_value=response):
            with self.assertRaisesRegex(ingestion.IngestionError, "unexpected Content-Type"):
                ingestion.fetch_feed()

    def test_non_success_http_response_fails(self) -> None:
        error = urllib.error.HTTPError(
            ingestion.FEED_URL,
            503,
            "Unavailable",
            Message(),
            None,
        )
        with mock.patch.object(ingestion.urllib.request, "urlopen", side_effect=error):
            try:
                with self.assertRaisesRegex(ingestion.IngestionError, "HTTP 503"):
                    ingestion.fetch_feed()
            finally:
                error.close()

    def test_returned_non_success_status_fails(self) -> None:
        response = self.FakeResponse(b"<rss/>", "application/rss+xml", status=503)
        with mock.patch.object(ingestion.urllib.request, "urlopen", return_value=response):
            with self.assertRaisesRegex(ingestion.IngestionError, "HTTP status 503"):
                ingestion.fetch_feed()

    def test_timeout_has_actionable_error(self) -> None:
        with mock.patch.object(
            ingestion.urllib.request, "urlopen", side_effect=socket.timeout()
        ):
            with self.assertRaisesRegex(ingestion.IngestionError, "Timed out"):
                ingestion.fetch_feed(timeout=3)

    def test_dns_failure_has_actionable_error(self) -> None:
        error = urllib.error.URLError(socket.gaierror("name resolution failed"))
        with mock.patch.object(ingestion.urllib.request, "urlopen", side_effect=error):
            with self.assertRaisesRegex(ingestion.IngestionError, "DNS lookup failed"):
                ingestion.fetch_feed()

    def test_network_failure_has_actionable_error(self) -> None:
        error = urllib.error.URLError("connection refused")
        with mock.patch.object(ingestion.urllib.request, "urlopen", side_effect=error):
            with self.assertRaisesRegex(ingestion.IngestionError, "Network failure"):
                ingestion.fetch_feed()


class SerializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.item = selected_item(fixture_bytes("single_response.xml"))
        self.serialized = ingestion.serialize_record(ingestion.build_record(self.item))

    def test_repeated_serialization_is_deterministic(self) -> None:
        first = ingestion.serialize_record(ingestion.build_record(self.item))
        second = ingestion.serialize_record(ingestion.build_record(self.item))
        self.assertEqual(first, second)
        self.assertTrue(first.endswith("\n"))
        self.assertEqual(json.loads(first)["schema_version"], "1.0.0")

    def test_cli_warns_and_emits_restricted_material_only_to_stdout(self) -> None:
        with (
            mock.patch.object(
                ingestion,
                "fetch_feed",
                return_value=fixture_bytes("multiple_items.xml"),
            ),
            mock.patch("sys.stdout", new_callable=io.StringIO) as stdout,
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            result = ingestion.main(["--date", "2026-11-24"])
        self.assertEqual(result, 0)
        self.assertIn('"record_type": "responsorial_psalm"', stdout.getvalue())
        self.assertIn("restricted source material", stderr.getvalue())

    def test_cli_has_no_file_output_option(self) -> None:
        with mock.patch("sys.stderr"), self.assertRaises(SystemExit) as raised:
            ingestion.main(["--latest", "--output", "/tmp/restricted-psalm.json"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
