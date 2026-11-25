# Liturgical Psalm Planning Utilities

## Purpose and source roles

`plan_daily_missal_psalms.py` is the production-oriented, read-only planner. It retrieves U.S. Ordinary Form liturgical metadata and Psalm citations from The Daily Missal API, preserving alternatives, optional memorials, and multiple Mass reading sets for human review. It does not invoke Suno, generate music or lyrics, publish content, or schedule work.

The primary metadata endpoint is `https://thedailymissal.com/api/v1/day/{YYYY-MM-DD}.json?cal=us`. Citation-only plans omit the `text=1` query parameter. Scripture text is requested only when `--include-text` is explicitly supplied; the planner keeps only source-provided Psalm text, identifies the translation as World English Bible, Catholic Edition, and marks its license as public domain. It does not claim to reproduce official USCCB text.

`validate_usccb_psalm.py` is retained as an optional structural validation utility, not as the production source of liturgical dates or content. It retrieves the USCCB RSS feed at <https://bible.usccb.org/readings.rss> and emits selected source text to stdout only. Its output is restricted source material; it has no file-output option.

## Planning commands

Date selection is always explicit. Use one date or an inclusive range of 1–15 days:

```sh
python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25
python3 tools/liturgy/plan_daily_missal_psalms.py --start-date 2026-11-25 --days 15
python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25 --include-text
python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25 \
  --output /tmp/psalm-plan.json
python3 tools/liturgy/plan_daily_missal_psalms.py --date 2026-11-25 \
  --output /tmp/psalm-plan.json --force
```

`--date` conflicts with `--start-date` and `--days`; ranges require both range options. The planner does not silently choose a date. A range includes every calendar date, including days whose API response fails. Failures are retained as explicit `failed` entries, the queue is marked `incomplete`, and the command exits nonzero. Reading or Psalm alternatives and additional Masses are never silently selected; they are retained and flagged for review.

Retrieval uses `urllib.request`, a user agent, a bounded timeout and response size, JSON content-type validation, and bounded retries for transient errors. The planner does not keep a persistent cache. Its metadata-only output removes text-valued fields from source metadata while preserving other unknown source fields where possible.

## Output model

The JSON is deterministic for the same source response: stable insertion order, UTF-8, two-space indentation, and a final newline. No current retrieval time is embedded.

```json
{
  "schema_version": "1.0.0",
  "record_type": "psalm_production_queue",
  "completion_status": "complete",
  "calendar": {"id": "us", "label": "United States"},
  "requested_range": {
    "start_date": "2026-11-25",
    "days": 1,
    "end_date": "2026-11-25"
  },
  "source": {
    "name": "The Daily Missal",
    "role": "primary_liturgical_planning_source",
    "scripture_translation": "World English Bible, Catholic Edition",
    "scripture_license": "public_domain",
    "official_usccb_text_reproduced": false
  },
  "days": [
    {
      "date": "2026-11-25",
      "status": "available",
      "reading_sets": [
        {
          "selection_status": "selected_by_source",
          "psalms": [
            {
              "citation": "Psalm 1:1",
              "alternatives": [],
              "text_source": "World English Bible, Catholic Edition",
              "text_included": false
            }
          ]
        }
      ],
      "attention_required": false,
      "attention_reasons": []
    }
  ],
  "failures": []
}
```

The citation above is illustrative. With `--include-text`, only Psalm text associated with the selected Psalm reading objects is retained; other readings' text is removed. The command still retains multiple valid Masses and Psalm alternatives, so callers must not assume a single unambiguous selection.

## Output and file safety

By default, JSON is written to stdout; status, retry warnings, and errors go to stderr. `--output PATH` is optional and refuses to replace an existing file unless `--force` is supplied. File output is written to a temporary sibling, flushed and fsynced where supported, and atomically published. Failed writes clean up the temporary file where possible. The USCCB validator is stdout-only and prints a copyright warning to stderr before its JSON.

## Optional USCCB validation

The validator requires an explicit selection. It supports the newest feed item or one publication date:

```sh
python3 tools/liturgy/validate_usccb_psalm.py --latest
python3 tools/liturgy/validate_usccb_psalm.py --date 2026-11-24
```

It parses RSS/XML and the selected item's encoded HTML structurally, identifies the Psalm by its heading, and requires exactly one Psalm section. Response choices and source notations are preserved. The output is **not** to be redirected into repository data or otherwise retained without permission.

## Tests

The tests are offline, use Python's standard library `unittest`, and rely on small synthetic JSON/XML fixtures rather than full Lectionary readings:

```sh
python3 -m unittest discover -s tools/liturgy/tests -v
```

## Retrospective USCCB citation comparison

`compare_usccb_daily_missal.py` is an optional after-the-fact check of a Daily Missal Psalm citation against the same date in the rolling USCCB RSS feed. It is separate from production planning, reads the plan without changing it, and does not access USCCB date pages.

The date is explicit. The comparator accepts a plan and optionally a local RSS fixture for offline tests:

```sh
python3 tools/liturgy/compare_usccb_daily_missal.py \
  --date 2026-11-25 --plan /path/to/daily-missal-plan.json
python3 tools/liturgy/compare_usccb_daily_missal.py \
  --date 2026-11-25 --plan /path/to/daily-missal-plan.json \
  --rss-fixture tools/liturgy/tests/fixtures/rss_comparison_match.xml
```

The comparator prints deterministic JSON to stdout and diagnostics to stderr. Its result is `match` when the Psalm citations match after superficial normalization, `difference` when they differ, and `unavailable` when the date is outside the rolling RSS window. A title difference is reported as a boolean and does not change the citation result. No output file is created; Psalm verses, refrain text, HTML, and RSS descriptions are not printed.

The comparator checks only Psalm citations. It does not interpret Lectionary prose, select among optional memorials or Masses, or access date-based USCCB pages. The normalized Daily Missal plan must already exist.

Copyright boundary: the USCCB Lectionary text and Psalm refrain are copyrighted. The comparator emits citation metadata only; do not retain, publish, or commit live USCCB text or live comparison output.

## Limitations, review, and copyright

- The planner depends on the observed, undocumented behavior and availability of The Daily Missal API. It validates response shape, dates, content type, size, and JSON syntax, but does not independently verify every liturgical assignment against an official source.
- The Daily Missal and USCCB names identify the respective sources only; this project is not affiliated with or endorsed by either organization.
- Alternatives, multiple Masses, readings from a common, missing proper readings, and absent Psalm citations require human review. The planner preserves them instead of inferring which option applies.
- The optional USCCB validator depends on the feed's current RSS, publication-date, HTML-heading, and poetry markup. A source change may require fixture and parser updates.
- The API's `text=1` payload shape may change. The planner only requests it on explicit instruction and keeps only Psalm-associated text; it does not persist live results unless a user explicitly requests `--output`.
- USCCB states that Lectionary text and Psalm refrains are copyrighted and may not be reproduced, distributed, performed, or displayed without permission. Treat text retrieved by the validator as restricted source material. Do not commit live USCCB output or synthetic fixtures containing full readings. The planner's optional text mode is limited to the source-identified public-domain World English Bible, Catholic Edition; verify applicable terms and permissions before downstream use.
