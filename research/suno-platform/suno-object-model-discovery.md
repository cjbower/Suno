# Suno Object Model and Connector Capability Discovery

**Captured:** 2026-11-24
**Status:** Read-only, point-in-time connector observation; not a Suno schema specification
**Authority:** Evidence-bounded reference for fields and operations exposed by the signed-in Suno MCP connector

## Purpose and Evidence Labels

This document records song, workspace, and playlist fields exposed by the connector, based on five retrieved song records, list responses, tool descriptions, and the previously executed Kio workspace assignment. No song, workspace, playlist, project, or visibility state was changed for this discovery.

- **Verified:** Returned in a connector response or confirmed by a completed connector operation.
- **Observed:** Present or absent in the sampled response. Absence from a sample does not prove Suno stores no such value.
- **Inferred:** Derived by matching IDs across separate connector listings; not a field on the song object.
- **Unknown:** Not exposed or not tested. This does not prove the Suno website or underlying service lacks the capability.

### Sample Set

| Sample | ID | Observed title | Sample role |
|---|---|---|---|
| A | `282b6ef1-16e7-451b-b5b5-00b5dbb5d166` | The River Remembers | Normal song |
| B | `96dc1426-93af-4f7c-a089-a5a99498a1fb` | Carillon | Second normal song |
| C | `ea8d8ea5-e574-4480-9b79-f67a42ee585c` | Replace 03:26-03:30 (11:19 PM Nov 21) | Replace-titled record |
| D | `9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b` | Untitled Project [01:00 - 02:30] | Untitled Project-titled record |
| E | `1e69b69c-4e05-457e-887f-19ffe1982577` | Showtime in the City | Song listed in the Kio workspace |

“Replace-titled” and “Untitled Project-titled” describe the returned titles, not verified Suno object classes. The connector returned `metadata.type: generate` for all five samples and no explicit Replace or project relationship field.

## Song Object Field Inventory

The connector's `audio-retrieve` responses had the following top-level shape. Presence codes: **A**, **B**, **C**, **D**, and **E** refer to the sample set above.

| Field | Example value | Present / absent in samples | Notes | Reliability | Classification usefulness |
|---|---|---|---|---|---|
| `id` | `282b6ef1-16e7-451b-b5b5-00b5dbb5d166` | Present A-E | Stable-looking clip identifier; use as the join key across listings. | High: returned directly | High for identity; none for semantic class |
| `title` | `The River Remembers`; `Replace ...`; `Untitled Project [...]` | Present A-E | A Replace or project label appears as ordinary title text. | High: returned directly | Moderate clue only; not proof of object type |
| `song_url` | `https://suno.com/song/<id>` | Present A-E | Direct URL for the song page. | High: returned directly | Low |
| `created_at` | `2026-11-23T17:45:51.627Z` (A); `2026-11-24T02:19:25.158Z` (E) | Present A-E | ISO timestamp. No `updated_at` was returned. | High for returned value; lifecycle completeness unknown | Low |
| `status` | `complete` | Present A-E | All five were complete. | High: returned directly | Low; does not distinguish ordinary song from edit/project-labeled records |
| `visibility` | `private` | Present A-E | All five were private at capture time. | High: returned directly | Low |
| `handle` | `cjbower` | Present A-E | Creator/account handle in these samples. | High: returned directly | Low |
| `error` | `null` | Present A-E | Error field was present and null in these completed records. | High: returned directly | None |
| `cover_image_url` | `https://cdn1.suno.ai/image_<id>.jpeg` | Present A-E | Small cover-image URL. | High: returned directly | Low |
| `cover_image_large_url` | `https://cdn1.suno.ai/image_large_<id>.jpeg` | Present A-E | Large cover-image URL. | High: returned directly | Low |
| `play_count` | `5` (A); `16` (B); `0` (C/D); `10` (E) | Present A-E | Engagement counter; may change over time. | High at retrieval time | None |
| `like_count` | `1` (A/B); `0` (C/D/E) | Present A-E | Engagement counter; may change over time. | High at retrieval time | None |
| `liked` | `true` (A/B); `false` (C/D/E) | Present A-E | Whether the signed-in user liked the record. | High at retrieval time | None |
| `comment_count` | `0` | Present A-E | Engagement counter; may change over time. | High at retrieval time | None |
| `metadata` | Object | Present A-E | Nested generation and audio details; keys vary between records. | High: returned directly | Some nested fields are useful |
| `metadata.description` | `null` | Present A-E, null in all five | No non-null description was present in these samples. `description` is also the generation input for simple mode, but this does not establish a separate saved prompt field. | High for sample values | Low |
| `metadata.duration` | `314.76` (A); `284.36` (B); `34.04` (C); `90` (D); `187.56` (E) | Present A-E | Duration in seconds. | High: returned directly | Moderate for triage, not a definitive object classifier |
| `metadata.lyrics` | Non-empty text | Present A-E | `audio-retrieve` returned lyrics. `library-list` and playlist clip listings omit `metadata.lyrics` through MCP. Lyrics are intentionally not duplicated here. | High for presence in retrieval; content may be truncated by tool output | High for content/catalog review, not for relationship proof |
| `metadata.model` | `v6-mini` (A/B/E); `v6` (C) | Present A/B/C/E; absent D | Model is missing from the Untitled Project-titled sample. | High: returned directly | Low |
| `metadata.style` | `Heavy metal...` (A); `Dark Electronic Hip-Hop...` (B/D); `80s west coast rap style` (E) | Present A-E | Style prompt/tags as returned by Suno. Long values omitted here. | High: returned directly | Moderate for creative cataloging |
| `metadata.type` | `generate` | Present A-E | Same value across ordinary, Replace-titled, and Untitled Project-titled samples. | High: returned directly | Low; does not distinguish the observed title categories |
| `metadata.origin` | No sample value | Absent A-E | `library-list` accepts an `origin` filter (`upload`, `cover`, `extension`, or `remaster`); no per-record `origin` key appeared in these responses. | Filter is tool-described; field absence is sample-observed | Potentially useful if a record field is returned; not available directly here |
| `metadata.controls` | `{"variety": 0}` (B) | Present B; absent A/C/D/E | Optional generation-control object. The audio-retrieve tool description also names controls as a returned settings group. | High when present; optionality observed | Low |
| `metadata.negative_style` | Non-empty text (B) | Present B; absent A/C/D/E | Optional negative-style prompt. | High when present; optionality observed | Moderate for creative cataloging |
| `metadata.max_mode` | No sample value | Absent A-E; named in tool description | The audio-retrieve tool description says metadata carries this setting; not observed in these five responses. | Tool-described, not sample-verified | Low |

### Prompt, Persona, and Relationship Fields

| Requested field | Finding | Evidence class | Reliability and classification usefulness |
|---|---|---|---|
| Separate `prompt` field | No separate `prompt` key appeared in the five retrieved song objects. `metadata.description` was null in all five; `metadata.style` held the visible style text. | Observed | High for these responses; a null description does not prove no prompt was used |
| Persona | No `persona` field appeared in the five objects. `voice_id` is an audio-generation input, not a returned persona field in these samples. | Observed | High for samples; persona association remains unknown |
| Parent / child song IDs | No explicit `parent_song_id` or `child_song_id` appeared. | Observed | High for samples; not evidence that Suno has no internal lineage |
| Cover / extension / mashup / source references | The `audio-retrieve` tool description says a song may name its source through `cover_audio_id`, `extend_audio_id`, `mashup_clip_ids`, or `reference_audio_ids`. None appeared in A-E. | Tool-described; absent in samples | Useful if returned; not observed here |
| Replace relationship | No `replace_audio_id` or explicit Replace relationship appeared. Sample C's title contains `Replace`, while its `metadata.type` is `generate`. | Observed | The title is not reliable proof of a Replace/edit lineage |
| Extend relationship | No `extend_audio_id` appeared in A-E. The connector description identifies it as a possible source field. | Tool-described; absent in samples | Could establish a source link if populated; not observed |
| Remaster relationship | No explicit remaster-parent field appeared. `reference_audio_ids` is described as a possible source-reference field, but its presence alone would not prove a specific remaster relationship. | Observed / tool-described | Unknown for these samples |
| Project relationship | No project ID, project name, or project relationship appeared for sample D. | Observed | `Untitled Project` is title text only; project classification/lineage is unverified |

### Organization and Classification Fields

| Field or concept | Finding | Evidence class | Reliability and classification usefulness |
|---|---|---|---|
| `workspace_id` / `workspace_name` on song | Neither appeared on A-E. | Observed | High for direct response shape; workspace membership can be derived separately |
| Workspace membership | `library-list` accepts a `workspace_id`; `workspaces-list` returns workspace records. Matching the song ID in a workspace-filtered listing establishes membership at query time. A was listed in Patriotism-1776; E was listed in Kio. | Inferred from separate listings | Strong for point-in-time membership; not an intrinsic song metadata field |
| Playlist membership | No playlist ID or name appeared on song objects. Membership is discoverable by matching IDs from `playlists-list-clips` responses. A was listed in `1776~2026`; E was listed in the separate playlist also named `Kio`. | Inferred from separate listings | Strong for visible playlist contents at query time; do not confuse a playlist named Kio with workspace Kio |
| Tags, categories, labels | No such fields appeared in A-E, and no corresponding tag operation was found in the exposed connector tool set. | Observed / tool inventory | Unknown whether the Suno product stores or supports these elsewhere |
| Custom metadata | No `custom_metadata` object or comparable custom-field operation was exposed. | Observed / tool inventory | Unknown beyond the connector |
| Archive / deletion state | No archived/deleted flag or timestamp appeared on A-E. | Observed | High for sample response shape; lifecycle state remains unknown |
| Object classification | All five returned `metadata.type: generate`; the Replace and Untitled labels were in `title`. | Verified | `type` is not sufficient to classify Replace artifacts or projects |

## Workspace and Playlist Schemas

### Workspace records

`workspaces-list` returned these fields for Kio after its creation:

| Field | Example | Present | Notes |
|---|---|---|---|
| `id` | `79a47b93-9ba1-4efb-95e0-a060676ae5c9` | Yes | Workspace ID |
| `name` | `Kio` | Yes | Workspace name |
| `description` | Empty string | Yes | Optional on creation; empty for Kio |
| `clip_count` | `2` | Yes | Count was zero at creation and two after assignment |

No workspace creation/update timestamp or owner field appeared in these responses. The workspace listing is a list/query operation; no separate single-workspace GET operation was exposed.

### Playlist records

`playlists-list` returned `id`, `name`, `playlist_url`, `visibility`, and `clip_count`. `playlists-list-clips` returns song objects (without `metadata.lyrics` through MCP); membership is determined by matching their `id` values. At capture time, the distinct playlist named `Kio` had ID `9ddbb9e2-692b-42fe-b4f7-e76012b866f3`, while the Kio workspace ID was `79a47b93-9ba1-4efb-95e0-a060676ae5c9`.

## Connector Capability Matrix

| Capability | Finding | Evidence and limits |
|---|---|---|
| List songs | **Verified** | `library-list` returned paginated finished-library records and supports workspace and other filters. Through MCP, list results omit `metadata.lyrics`. |
| Retrieve song | **Verified** | `audio-retrieve` returned the five sample objects, including lyrics for the signed-in user's own songs. |
| Retrieve/list workspaces | **Verified, list-based** | `workspaces-list` returned workspace IDs, names, descriptions, and clip counts; it supports name filtering. No separate get-by-ID operation was exposed. |
| Read playlist membership | **Verified, separate listings** | `playlists-list` and `playlists-list-clips` allowed ID matching across the user's visible playlists. This is not a song-object field. |
| Create workspace | **Verified** | `workspaces-create` accepts `name` and optional `description`. The prior authorized Kio creation returned its ID, name, empty description, and initial zero clip count. |
| Assign song to workspace | **Verified** | `workspaces-update-clips` returned both requested Showtime IDs in `added`, with no skipped or removed IDs; a subsequent workspace-filtered listing returned both songs. |
| Move song between workspaces | **Advertised; not exercised here** | The update tool says adding a song takes it out of its previous workspace. This discovery did not move an already-filed song. |
| Assign one song to multiple workspaces | **Not supported by the connector contract** | The update tool states a song is in at most one workspace. |
| Delete song | **Unknown / not exposed** | No delete-song operation appeared in the inspected connector tools; no delete was attempted. |
| Archive song | **Unknown / not exposed** | No archive operation appeared; no archive was attempted. |
| Rename workspace | **Unknown / not exposed** | No workspace-rename operation appeared; no rename was attempted. |
| Tags | **Unknown / not exposed** | No tag fields or tag operations appeared in the inspected tool set. |

“Not exposed” describes the inspected MCP connector, not necessarily the Suno website or underlying service.

## Replace Artifact Observations

For sample C, the connector returned an ordinary song-shaped record: ID, title, URL, creation date, status, visibility, counts, cover URLs, and `metadata` including duration, lyrics, model, style, and `type: generate`. Its title begins with `Replace`, but no Replace-specific relationship, parent ID, project ID, or edit-state field was returned. This verifies the title and returned fields only; it does **not** establish whether the record is a song, edit artifact, or child of another song.

The earlier [song metadata snapshot](experiments/suno-song-metadata-discovery-2026-11-24.md) preserves the prior four-object observations and limitations. No Replace object was changed in this discovery.

## Known Limitations and Open Questions

- This is a point-in-time sample of five records and the connector tools available to the signed-in account; it is not a complete Suno API specification.
- A field absent from these responses may be present on other songs or in Suno's own UI/API.
- Song lists and playlist clip lists omit lyrics through MCP; `audio-retrieve` returned lyrics for the user's own songs.
- The connector's workspace-filtered library listing excludes collaborators' songs in shared workspaces, per its tool description.
- The sample does not establish whether `metadata.max_mode` or source-reference fields are populated for other generation types.
- The connector does not expose a verified Replace-parent, project, remaster-parent, archive, deletion, or workspace-rename relationship/operation in this evidence set.
- Tagging, categories, labels, custom metadata, and persona association remain unverified.
- The Replace-titled and Untitled Project-titled records need additional evidence before either title is promoted into a semantic object classification.
