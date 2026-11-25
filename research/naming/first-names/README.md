# First Names – Decade Datasets

**Purpose**

This folder contains static decade-labeled first-name lists. The source labels (for example, male/female) must not be interpreted as an individual's gender identity or as evidence of audience familiarity.

**Contents**

- 1970s-male.md / 1970s-female.md
- 1980s-male.md / 1980s-female.md
- 1990s-male.md / 1990s-female.md
- 2000s-male.md / 2000s-female.md
- 2010s-male.md / 2010s-female.md
- 2020s-male.md / 2020s-female.md

**Methodology**

Each file presents a historical top-20 list for its stated decade and source category. The local files do not retain the annual counts or a reproducible extraction needed to verify a decade aggregation.

Each entry includes:
- Rank (1-20)
- Name
- Source reference

**Sources**

The [SSA Popular Baby Names page](https://www.ssa.gov/oact/babynames/) is the intended primary source for national and state/territory rankings. The page and data endpoints returned HTTP 403 during the 2026-11-25 review, so current coverage and source methodology were not independently rechecked. The California and Washington state sources are evaluated separately in the [official source review](../reports/official-name-data-source-review.md); they are not merged into these files.

**How to Use**

1. Confirm the exact source, period, geographic scope, categories, and aggregation method.
2. Treat the lists as historical context only until underlying counts and extraction are verified.
3. Use current, documented searches of relevant music services, identifiers, domains, social accounts, and trademark sources for collision assessment.
4. Do not infer age, gender identity, cultural identity, audience familiarity, or genre from a name's frequency.

**Limitations**

- Reflects primarily U.S. naming patterns
- Skewed toward English-language databases
- Does not capture regional, cultural, or ethnic variations
- The 2020s files cover 2020-2024 only and are partial, not a complete decade or current-year update
- A top-N list omits names outside its threshold
- Popularity does not establish collision risk or availability
- Do not combine data sources with different categories, time ranges, geographies, or transformations without documenting differences

**Research Gaps**

- International naming patterns not comprehensively covered
- Ethnic/cultural naming traditions under-represented
- Surname-first naming patterns (common in many cultures) not included in first-name datasets
- Regional variation within U.S. not fully captured

**Next Steps**

Review the evidence and limitations in:
- [Official Baby-Name Data Source Review](../reports/official-name-data-source-review.md)
- [Name Trends Analysis](../reports/name-trends-analysis.md)
- [Name Selection Strategy](../reports/name-selection-strategy.md)
- [Current Artist Review](../industry-collision-analysis/current-artist-review.md)
