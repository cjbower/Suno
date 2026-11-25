# Official Baby-Name Data Source Review

**Review date:** 2026-11-25
**Purpose:** Evaluate official, aggregated name sources for cautious naming research. This is not a name recommendation, collision report, or demographic profile.

## Source Evaluation

| Source | What the source provides | Assessment and limits |
|---|---|---|
| [U.S. Social Security Administration (SSA) Popular Baby Names](https://www.ssa.gov/oact/babynames/) | National and state/territory name rankings by birth year are the intended primary U.S. reference for the existing first-name corpus. | Keep as the primary source. The official page and data endpoints returned HTTP 403 during this review, so current year coverage, release date, category definitions, and the exact ranking methodology were not independently rechecked here. Existing local decade lists are static summaries, not a reproducible extraction. Recheck the official documentation and underlying data before refreshing or citing specific ranks. |
| [California CDPH Most Popular Baby Names](https://data.chhs.ca.gov/dataset/most-popular-baby-names) | State-level annual top-25 names by source-reported sex category, for 1960-2024; counts and ranks are derived from California birth-certificate data. | Useful aggregated state supplement, not a replacement for SSA's national series. The official data dictionary says `Sex` is the sex recorded on the birth certificate and includes `Female` and `Male`; nonbinary and unknown-sex records are excluded because of small counts. `Name` removes spaces and special characters; some older names may be truncated and marked with `*`. Counts and rankings are not complete name registries. Portal access returned HTTP 502 in this review, but the [official data dictionary CSV](https://data.chhs.ca.gov/dataset/4a8cb74f-c4fa-458a-8ab1-5f2c0b2e22e3/resource/c2f005e6-fc0e-4594-8297-d23b59f9b0ad/download/data-dictionary-baby-names.csv) was retrieved successfully. |
| [Washington State DOH Baby Names](https://doh.wa.gov/data-and-statistical-reports/health-statistics/birth/baby-names) | An official Washington DOH page links to an interactive All Births dashboard with the top 50 names given to babies born to Washington residents; its controls use the source labels `boy` and `girl` and allow year selection. | Relevant regional comparison candidate. The public page does not state the complete year range or define the displayed categories beyond those labels, and this review did not validate a reproducible downloadable name table. Do not merge it into the corpus until coverage, definitions, and extraction are confirmed from the dashboard or a documented export. |
| [CDC/NCHS Vital Statistics Online](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) and CDC WONDER natality documentation | Official natality statistics and access to aggregate vital-statistics products. The reviewed documentation covers natality statistics, not given-name rankings; WONDER suppresses small cells under its published rules. | Useful for birth-statistics context, not as a substitute source for name rankings. General natality totals do not establish a name's popularity, identity, culture, or collision risk. |

## Use Rules

- Treat SSA as the primary national ranking source and state sources as geographically bounded supplements. Record source, retrieval date, covered birth years, category labels, extraction method, and any source revision date for each future refresh.
- Keep rankings and counts at the aggregate level. Do not obtain, store, or seek individual birth records.
- Preserve the source's own category labels; do not convert `sex`, `boy`, or `girl` into claims about an individual person's gender identity.
- A birth-name frequency is not evidence of an artist's age, audience recognition, ethnicity, language, cultural identity, authenticity, or suitability for a genre.
- Popularity is not collision or availability evidence. Artist and band collision checks require current, direct searches of relevant music services, identifiers, domains, social accounts, and trademark sources, with methods and dates recorded.
- A top-N table omits names outside its threshold; absence from the table does not mean a name was unused.
- Do not combine source data with different geography, periods, category definitions, normalization, or coverage without documenting the incompatibility.

## Existing Corpus Status

The existing decade files are retained as historical working material, not revalidated as a reproducible source dataset. The 2020s files state a 2020-2024 window and are therefore partial; they do not represent a complete decade or a current-year update. They should not be used to support current popularity, age-cohort, cultural, gender, or collision claims.

No new name ranking or row-level source data was downloaded or added in this review. The California data dictionary was read to verify field definitions and transformation notes. SSA retrieval failed with HTTP 403; California portal retrieval failed with HTTP 502. These limitations are evidence gaps, not grounds to substitute unverified third-party copies.

## Reproducible Refresh Checklist

Before refreshing a dataset:

1. Retrieve the current official source and its documentation.
2. Record the page/resource URL, retrieval date, source revision date, and checksum for any retained aggregate extract.
3. Confirm year coverage, geographic basis, source categories, inclusion rules, suppression, ties, name normalization, and top-N limits.
4. Use birth-year counts to calculate a multi-year ranking; do not average ordinal ranks as if they were counts.
5. Keep source records and the aggregation script or method traceable, and verify totals against the official published output.
6. Document limitations; do not infer audience behavior, identity, or collision availability from popularity.
