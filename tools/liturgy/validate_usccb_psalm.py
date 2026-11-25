#!/usr/bin/env python3
"""Validate a USCCB RSS Responsorial Psalm section; output is restricted text."""

from __future__ import annotations

import argparse
import email.utils
from html.parser import HTMLParser
import json
import re
import socket
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable


FEED_URL = "https://bible.usccb.org/readings.rss"
USER_AGENT = "SunoStudio-LiturgyIngestion/0.1 (read-only prototype)"
REQUEST_TIMEOUT_SECONDS = 15
MAX_FEED_BYTES = 5 * 1024 * 1024
XML_CONTENT_TYPES = {
    "application/atom+xml",
    "application/rdf+xml",
    "application/rss+xml",
    "application/xml",
    "text/xml",
}


class IngestionError(Exception):
    """An expected feed, parsing, selection, or output error."""


@dataclass(frozen=True)
class FeedItem:
    title: str
    item_url: str
    published: str
    published_at: datetime
    calendar_date: date
    description: str


@dataclass
class _HtmlNode:
    tag: str
    attrs: dict[str, str]
    children: list[_HtmlNode | str]


class _DescriptionParser(HTMLParser):
    _VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _HtmlNode("root", {}, [])
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = _HtmlNode(tag.lower(), {key.lower(): value or "" for key, value in attrs}, [])
        self.stack[-1].children.append(node)
        if tag.lower() not in self._VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = _HtmlNode(tag.lower(), {key.lower(): value or "" for key, value in attrs}, [])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag.lower():
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _child_text(parent: ET.Element, name: str) -> str:
    for child in parent:
        if _local_name(child.tag) == name.lower():
            return "".join(child.itertext()).strip()
    return ""


def _parse_pub_date(raw: str, item_index: int) -> datetime:
    if not raw:
        raise IngestionError(f"RSS item {item_index} has no pubDate.")
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise IngestionError(f"RSS item {item_index} has an invalid pubDate: {raw!r}.") from exc
    if parsed is None:
        raise IngestionError(f"RSS item {item_index} has an invalid pubDate: {raw!r}.")
    return parsed


def parse_feed(xml_bytes: bytes) -> list[FeedItem]:
    """Parse RSS item metadata without interpreting any description as XML."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise IngestionError(f"The RSS response contains malformed XML: {exc}.") from exc

    if _local_name(root.tag) != "rss":
        raise IngestionError("The XML root is not an RSS <rss> document.")
    channel = next((child for child in root if _local_name(child.tag) == "channel"), None)
    if channel is None:
        raise IngestionError("The RSS document has no <channel> element.")

    items: list[FeedItem] = []
    for index, element in enumerate(
        (child for child in channel if _local_name(child.tag) == "item"),
        start=1,
    ):
        title = _child_text(element, "title")
        item_url = _child_text(element, "link")
        published = _child_text(element, "pubDate")
        description = _child_text(element, "description")
        if not title:
            raise IngestionError(f"RSS item {index} has no title.")
        if not item_url:
            raise IngestionError(f"RSS item {index} has no canonical item link.")
        published_at = _parse_pub_date(published, index)
        items.append(
            FeedItem(
                title=title,
                item_url=item_url,
                published=published,
                published_at=published_at,
                calendar_date=published_at.date(),
                description=description,
            )
        )

    if not items:
        raise IngestionError("The RSS channel contains no <item> elements.")
    return items


def _xml_content_type(content_type: str) -> bool:
    normalized = content_type.split(";", 1)[0].strip().lower()
    return normalized in XML_CONTENT_TYPES or normalized.endswith("+xml")


def fetch_feed(url: str = FEED_URL, timeout: int = REQUEST_TIMEOUT_SECONDS) -> bytes:
    """Retrieve a bounded RSS response with explicit request headers and validation."""
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            if status is None or not 200 <= status < 300:
                raise IngestionError(f"USCCB feed request returned HTTP status {status!r}.")
            content_type = response.headers.get("Content-Type", "")
            if not _xml_content_type(content_type):
                raise IngestionError(
                    "USCCB feed returned an unexpected Content-Type "
                    f"{content_type!r}; expected RSS/XML."
                )
            body = response.read(MAX_FEED_BYTES + 1)
            if len(body) > MAX_FEED_BYTES:
                raise IngestionError(
                    f"USCCB feed response exceeds the {MAX_FEED_BYTES}-byte size limit."
                )
            return body
    except urllib.error.HTTPError as exc:
        raise IngestionError(f"USCCB feed request failed with HTTP {exc.code} ({exc.reason}).") from exc
    except (TimeoutError, socket.timeout) as exc:
        raise IngestionError(
            f"Timed out retrieving the USCCB feed after {timeout} seconds; retry later."
        ) from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            raise IngestionError(
                f"Timed out retrieving the USCCB feed after {timeout} seconds; retry later."
            ) from exc
        if isinstance(reason, socket.gaierror):
            raise IngestionError(
                f"DNS lookup failed for the USCCB feed host: {reason}; check network or DNS."
            ) from exc
        raise IngestionError(
            f"Network failure retrieving the USCCB feed: {reason}; check connectivity and retry."
        ) from exc
    except OSError as exc:
        if isinstance(exc, socket.gaierror):
            raise IngestionError(
                f"DNS lookup failed for the USCCB feed host: {exc}; check network or DNS."
            ) from exc
        raise IngestionError(
            f"Network failure retrieving the USCCB feed: {exc}; check connectivity and retry."
        ) from exc


def _walk(node: _HtmlNode) -> Iterable[_HtmlNode]:
    for child in node.children:
        if isinstance(child, _HtmlNode):
            yield child
            yield from _walk(child)


def _plain_text(node: _HtmlNode, line_breaks: bool = False) -> str:
    pieces: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            pieces.append(child)
        elif child.tag == "br" and line_breaks:
            pieces.append("\n")
        else:
            pieces.append(_plain_text(child, line_breaks=line_breaks))
    return "".join(pieces).replace("\u00a0", " ")


def _normalized_lines(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", line).strip()
        for line in text.replace("\u00a0", " ").splitlines()
        if re.sub(r"\s+", " ", line).strip()
    ]


def _is_responsorial_heading(node: _HtmlNode) -> bool:
    if node.tag not in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        return False
    heading = re.sub(r"\s+", " ", _plain_text(node)).strip().casefold()
    return re.match(r"^responsorial\s+psalm(?:\b|$)", heading) is not None


def _heading_sections(root: _HtmlNode) -> list[tuple[_HtmlNode, list[_HtmlNode]]]:
    nodes = list(_walk(root))
    result: list[tuple[_HtmlNode, list[_HtmlNode]]] = []
    heading_indexes = [
        index
        for index, node in enumerate(nodes)
        if node.tag in {"h1", "h2", "h3", "h4", "h5", "h6"}
    ]
    for index, heading in enumerate(nodes):
        if not _is_responsorial_heading(heading):
            continue
        following_heading = next((position for position in heading_indexes if position > index), len(nodes))
        result.append((heading, nodes[index + 1 : following_heading]))
    return result


_CITATION_RE = re.compile(
    r"^(?:Psalm|Ps(?:alm)?)\.?\s+(\d+(?::[\dA-Za-z,\s\u2013\u2014-]+)?)\.?$",
    re.IGNORECASE,
)
_VERSE_MARKER_RE = re.compile(r"\[\[VERSE:(\d+)]]")
_RESPONSE_RE = re.compile(r"^R\s*\.\s*(.*)$", re.IGNORECASE)
_LEADING_NOTATION_RE = re.compile(r"^(\([^()]+\))\s*(.*)$")


def _paragraph_lines(node: _HtmlNode) -> list[tuple[str | None, str]]:
    pieces: list[str] = []

    def collect(current: _HtmlNode) -> None:
        for child in current.children:
            if isinstance(child, str):
                pieces.append(child)
            elif child.tag == "br":
                pieces.append("\n")
            elif child.tag == "sup":
                marker = re.sub(r"\s+", "", _plain_text(child))
                if marker.isdigit():
                    pieces.append(f"[[VERSE:{marker}]]")
                else:
                    collect(child)
            else:
                collect(child)

    collect(node)
    text = "".join(pieces).replace("\u00a0", " ")
    lines: list[tuple[str | None, str]] = []
    for raw_line in text.splitlines() or [text]:
        markers = list(_VERSE_MARKER_RE.finditer(raw_line))
        if not markers:
            line = re.sub(r"\s+", " ", raw_line).strip()
            if line:
                lines.append((None, line))
            continue
        prefix = re.sub(r"\s+", " ", raw_line[: markers[0].start()]).strip()
        if prefix:
            lines.append((None, prefix))
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else len(raw_line)
            line = re.sub(r"\s+", " ", raw_line[marker.end() : end]).strip()
            lines.append((marker.group(1), line))
    return lines


def _extract_psalm(item: FeedItem) -> dict[str, object]:
    parser = _DescriptionParser()
    try:
        parser.feed(item.description)
        parser.close()
    except (AssertionError, ValueError) as exc:
        raise IngestionError(
            f"Could not parse HTML in the description for {item.calendar_date.isoformat()}: {exc}."
        ) from exc

    sections = _heading_sections(parser.root)
    if not sections:
        raise IngestionError(
            f"No Responsorial Psalm heading was found for {item.calendar_date.isoformat()}."
        )
    if len(sections) != 1:
        raise IngestionError(
            f"Expected exactly one Responsorial Psalm section for "
            f"{item.calendar_date.isoformat()}, found {len(sections)}."
        )

    _, section_nodes = sections[0]
    poetry_nodes = [
        node
        for node in section_nodes
        if node.tag == "div" and "poetry" in node.attrs.get("class", "").split()
    ]
    if not poetry_nodes:
        raise IngestionError(
            f"The Responsorial Psalm section for {item.calendar_date.isoformat()} "
            "has no div.poetry content."
        )

    citation: str | None = None
    citation_node: _HtmlNode | None = None
    heading_text = re.sub(r"\s+", " ", _plain_text(sections[0][0])).strip()
    heading_citation = re.sub(
        r"^responsorial\s+psalm\s*",
        "",
        heading_text,
        flags=re.IGNORECASE,
    ).strip()
    if heading_citation:
        heading_match = _CITATION_RE.fullmatch(heading_citation)
        if heading_match:
            citation = heading_citation.rstrip(".")
    for node in section_nodes:
        if citation:
            break
        for line in _normalized_lines(_plain_text(node, line_breaks=True)):
            match = _CITATION_RE.fullmatch(line)
            if match:
                citation = line.rstrip(".")
                citation_node = node
                break
        if citation:
            break
    if citation is None:
        raise IngestionError(
            f"The Responsorial Psalm section for {item.calendar_date.isoformat()} "
            "has no parseable Psalm citation."
        )

    paragraphs = [
        descendant
        for poetry in poetry_nodes
        for descendant in _walk(poetry)
        if descendant.tag == "p" and descendant is not citation_node
    ]
    responses: list[dict[str, str | None]] = []
    verse_paragraphs: list[list[tuple[str | None, str]]] = []
    for paragraph in paragraphs:
        lines = _paragraph_lines(paragraph)
        if lines:
            verse_paragraphs.append(lines)

    has_explicit_verse_numbers = any(
        marker is not None for paragraph in verse_paragraphs for marker, _ in paragraph
    )
    verse_groups: list[dict[str, object]] = []
    seen_responses: dict[str, set[str | None]] = {}
    current_group: dict[str, object] | None = None

    def start_group(source_verse_number: str | None = None) -> dict[str, object]:
        group: dict[str, object] = {
            "sequence": len(verse_groups) + 1,
            "lines": [],
        }
        if source_verse_number is not None:
            group["source_verse_number"] = int(source_verse_number)
        verse_groups.append(group)
        return group

    def append_line(group: dict[str, object], line: str) -> None:
        lines = group["lines"]
        assert isinstance(lines, list)
        lines.append(line)

    # Responses and verse lines share paragraph blocks on the live feed.
    # Process the source stream in order so repeated refrains delimit verse
    # groups without being mistaken for additional response choices.
    for paragraph in verse_paragraphs:
        if (
            not has_explicit_verse_numbers
            and current_group is not None
            and current_group["lines"]
        ):
            current_group = None
        for marker, line in paragraph:
            response_match = _RESPONSE_RE.match(line) if marker is None else None
            if response_match:
                response_text = response_match.group(1).strip()
                source_notation: str | None = None
                notation_match = _LEADING_NOTATION_RE.match(response_text)
                if notation_match:
                    source_notation = notation_match.group(1)
                    response_text = notation_match.group(2).strip()
                if not response_text:
                    raise IngestionError(
                        f"Found an empty Responsorial Psalm response for "
                        f"{item.calendar_date.isoformat()}."
                    )
                prior_notations = seen_responses.setdefault(response_text, set())
                if not prior_notations or (
                    source_notation is not None and source_notation not in prior_notations
                ):
                    prior_notations.add(source_notation)
                    responses.append(
                        {"text": response_text, "source_notation": source_notation}
                    )
                if current_group is not None and current_group["lines"]:
                    current_group = None
                continue
            if marker is not None:
                current_group = start_group(marker)
                if line:
                    append_line(current_group, line)
                continue
            if line:
                if current_group is None:
                    current_group = start_group()
                append_line(current_group, line)

    if not responses:
        raise IngestionError(
            f"No response marked R. was found in the Responsorial Psalm for "
            f"{item.calendar_date.isoformat()}."
        )

    verse_groups = [group for group in verse_groups if group["lines"]]
    for sequence, group in enumerate(verse_groups, start=1):
        group["sequence"] = sequence
    if not verse_groups:
        raise IngestionError(
            f"The Responsorial Psalm for {item.calendar_date.isoformat()} "
            "has no non-empty verse content."
        )

    return {
        "citation": citation,
        "responses": responses,
        "verses": verse_groups,
    }


def build_record(item: FeedItem) -> dict[str, Any]:
    """Build the deterministic, versioned record for one already-selected item."""
    return {
        "schema_version": "1.0.0",
        "record_type": "responsorial_psalm",
        "source": {
            "feed_url": FEED_URL,
            "item_url": item.item_url,
            "published": item.published,
            "publisher": "USCCB",
        },
        "liturgical_day": {
            "date": item.calendar_date.isoformat(),
            "title": item.title,
        },
        "psalm": _extract_psalm(item),
    }


def serialize_record(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, indent=2) + "\n"


def select_item(items: list[FeedItem], latest: bool, requested_date: str | None) -> FeedItem:
    if latest == (requested_date is not None):
        raise IngestionError("Select exactly one of --latest or --date YYYY-MM-DD.")
    if latest:
        return max(items, key=lambda item: item.published_at)

    assert requested_date is not None
    try:
        parsed_date = date.fromisoformat(requested_date)
    except ValueError as exc:
        raise IngestionError(f"Invalid date {requested_date!r}; use YYYY-MM-DD.") from exc
    if parsed_date.isoformat() != requested_date:
        raise IngestionError(f"Invalid date {requested_date!r}; use YYYY-MM-DD.")
    matches = [item for item in items if item.calendar_date == parsed_date]
    if len(matches) == 1:
        return matches[0]
    available = ", ".join(sorted({item.calendar_date.isoformat() for item in items}))
    if not matches:
        raise IngestionError(
            f"No feed item exists for {requested_date}. Available feed dates: {available}."
        )
    raise IngestionError(
        f"Expected exactly one feed item for {requested_date}, found {len(matches)}. "
        f"Available feed dates: {available}."
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate one USCCB Daily Readings RSS Responsorial Psalm section and "
            "emit restricted source material to stdout."
        ),
        epilog=(
            "Retrieved Lectionary text and Psalm refrains are copyrighted source material. "
            "Use the output only as permitted by the USCCB."
        ),
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--latest",
        action="store_true",
        help="select the feed item with the newest publication timestamp",
    )
    selection.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="select exactly one item by the calendar date in its pubDate",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        items = parse_feed(fetch_feed())
        item = select_item(items, latest=args.latest, requested_date=args.date)
        record = build_record(item)
        serialized = serialize_record(record)
        print(
            "warning: USCCB Lectionary text and Psalm refrains are copyrighted; "
            "stdout contains restricted source material.",
            file=sys.stderr,
        )
        sys.stdout.write(serialized)
        response_count = len(record["psalm"]["responses"])  # type: ignore[index]
        print(
            f"Selected {item.calendar_date.isoformat()} "
            f"({record['psalm']['citation']}); retained {response_count} response(s).",  # type: ignore[index]
            file=sys.stderr,
        )
        return 0
    except IngestionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
