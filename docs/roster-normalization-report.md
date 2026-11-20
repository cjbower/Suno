# Roster Normalization Report

## Previous Structure

- Solo-artist folders were directly under `artist-roster/`.
- Bands were already organized under `artist-roster/bands/`.
- Producer projects were under `artist-roster/producers/`.
- The artist development template covered individual artists and band leaders.

## New Structure

- `artist-roster/solo-artists/` contains individual artist identities.
- `artist-roster/bands/` contains group identities and ensemble projects.
- `artist-roster/producer-projects/` contains production-led initiatives that may span multiple artists and genres.
- Creative documentation now has separate solo artist, band, and producer-project templates.

## Folders Moved

The following 12 solo-artist folders moved to `artist-roster/solo-artists/`:

- adrian-santiago
- nathan-cross
- isaac-vega
- ethan-navarro
- jordan-mercer
- lucas-reed
- elena-cruz
- sophia-martinez
- maya-bennett
- isabella-reyes
- natalie-vega
- olivia-brooks

The `meridian/` and `foundry/` project folders moved from `artist-roster/producers/` to `artist-roster/producer-projects/`.

The six existing band folders remain under `artist-roster/bands/`: North Star Revival, Lantern House, Signal Fire, Harbor Lights, Midnight Avenue, and City Saints.

## Files Moved

- 72 solo-artist files moved (six existing documents in each of 12 folders).
- Two producer-project profile files moved (one in each project folder).
- Existing band files were not moved or modified.

## References Updated

- Artist-specific file patterns and links now point to `artist-roster/solo-artists/`.
- Producer-project links now point to `artist-roster/producer-projects/`.
- The repository README documents the normalized structure and links to the new locations.
- Creative guidance, the Phase 2A validation report, and the repertoire README reference the solo-artist paths.
- `creative/README.md` lists the separated development templates.

## Schema Updates

- Paths in `catalog/metadata/artists.yaml` now point to `artist-roster/solo-artists/`.
- `catalog/metadata/bands.yaml` already pointed to `artist-roster/bands/` and required no change.
- No schema fields, registry entries, or metadata values were added or redesigned.

## Validation Performed

- Confirmed all 12 solo-artist folders, six band folders, and two producer-project folders exist in their normalized locations.
- Compared all 74 moved files byte-for-byte with their original repository versions; no mismatches were found.
- Confirmed the old solo-artist and producer source paths are absent.
- Searched active documentation and metadata for stale old-layout paths; the prior producer path appears only in this report's historical structure description.
- Checked relative links in the moved entity folders.
- Confirmed the solo-artist template contains no band, band-leader, or ensemble references.
- Confirmed the band and producer-project templates include their requested sections and use placeholders.
- Ran `git diff --check` successfully.

## Open Issues

- An earlier historical statement in `docs/validation-report.md` describes the repository before its roster structure was created; it was left unchanged as historical context.
- No blocking issues were found for this phase.

## Recommendations

- Keep solo-artist, band, and producer-project documentation under their respective folders and use their matching templates.
- Consider producer-project metadata requirements in a future, explicitly scoped phase; no producer-project registry was introduced here.
