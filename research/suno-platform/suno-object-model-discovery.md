# Suno Object Model and Connector Capability Discovery

**Captured:** 2026-11-24
**Status:** Read-only, point-in-time connector observation; not a Suno schema specification
**Authority:** Evidence-bounded reference for fields and operations exposed by the signed-in Suno MCP connector

## Purpose and Evidence Labels

This document records song, workspace, playlist, and sampled voice fields exposed by the connector, based on five retrieved song records, one read-only voice listing, other list responses, tool descriptions, and verified workspace assignments. The earlier object-model sampling was read-only; the separately approved full workspace cleanup is recorded below and in the operations inventory.

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
| F | `aebb54a6-b11c-484c-8f4a-7a2228aa966c` | Showtime in the City | Second song listed in the Kio workspace; compared separately below |

“Replace-titled” and “Untitled Project-titled” describe the returned titles, not verified Suno object classes. The connector returned `metadata.type: generate` for all five samples and no explicit Replace or project relationship field.

## Song Object Field Inventory

The connector's `audio-retrieve` responses had the following top-level shape. Presence codes: **A**, **B**, **C**, **D**, and **E** refer to the baseline sample set above; the additional Kio record **F** is analyzed separately below.

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
| Cover creation with a voice | `audio-covers-create` requires an existing source clip ID and optionally accepts `voice_id`; it creates a new clip. | Advertised | The descriptor does not promise melody/arrangement preservation, automatic lyric carryover, or in-place vocalist replacement. See [Suno MCP Capability Matrix](suno-mcp-capability-matrix.md). |
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

### Full catalog inventory and approved workspace cleanup

On 2026-11-24, a paginated `library-list` inventory returned **438 unique, complete, private records**. All exposed `metadata.type` values were `generate`; this does not distinguish ordinary songs from Replace- or edit-labeled outputs. Model counts were `v6` 151, `v6-mini` 275, `v6-wild` 8, and model absent 4. Style was present on 434 records. The list response did not expose `workspace_id` or `metadata.voice_id`; membership was determined by matching IDs from workspace-filtered listings.

| Workspace | Before | After |
|---|---:|---:|
| Kio | 2 | 2 |
| Patriotism-1776 | 61 | 61 |
| N-Learning | 246 | 8 |
| Virtues-Learning | 24 | 24 |
| Faith | 54 | 54 |
| Challenge-Picture | 4 | 4 |
| First-Mango | 8 | 8 |
| First-Disco | 4 | 4 |
| Nebraska | 0 | 238 |
| EXP-Voice-ID-Validation | 0 | 4 |
| **Total assigned** | **403** | **407** |

The user approved creation of `Nebraska` and `EXP-Voice-ID-Validation`. The connector returned workspace IDs `49763997-c197-4172-bff3-9175b4d5616c` and `9f39af6d-d8b4-43d9-b35d-d9fdf90b1a8e`. A total of 238 Nebraska-themed clips were moved from N-Learning to Nebraska; four voice-test clips were filed in EXP-Voice-ID-Validation. The five Nebraska update batches and the EXP update returned all requested IDs as added, with no skipped or removed IDs. Follow-up filtered listings exactly matched all 238 approved Nebraska IDs and all four EXP IDs; N-Learning retained eight records. A post-move paginated global library refresh returned 438 unique IDs, exactly matching the inventory, with no missing or new IDs.

There were no overlapping workspace IDs in the pre-change membership set. The connector contract states that a song can be in at most one workspace. After reassignment, 407 workspace records plus 31 intentionally unassigned Replace-/Untitled-titled records reconcile to all 438 library records. No songs were deleted or edited. Three `(Edit)`-titled records were not moved. N-Learning's `Under City Lights` (2) and `Maize and Blue` (4), Virtues-Learning's `Dare to Die` (2), First-Mango's `The guy`/`The girl` (8), Patriotism-1776's `Midnight Velocity` (2), and Faith's `Happy Sun Jealous Moon` (1) remain in place because title/style evidence did not establish a confident reassignment.

The detailed row-level inventory, including title, ID, date, model, type, style, visibility, derived workspace membership, and voice-field evidence, is preserved in [the workspace inventory CSV](../../operations/suno-song-workspace-inventory-2026-11-24.csv). The change sequence and remaining ambiguities are documented in the [workspace assignment record](../../operations/suno-workspace-assignment-queue-2026-11-24.md).

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
| Move song between workspaces | **Verified** | The approved cleanup moved 238 clips from N-Learning to Nebraska. All requested IDs were returned as added with no skipped IDs, and the filtered destination listing exactly matched the approved set. |
| Assign one song to multiple workspaces | **Not supported by the connector contract** | The update tool states a song is in at most one workspace. |
| Delete song | **Unknown / not exposed** | No delete-song operation appeared in the inspected connector tools; no delete was attempted. |
| Archive song | **Unknown / not exposed** | No archive operation appeared; no archive was attempted. |
| Rename workspace | **Unknown / not exposed** | No workspace-rename operation appeared; no rename was attempted. |
| Tags | **Unknown / not exposed** | No tag fields or tag operations appeared in the inspected tool set. |

“Not exposed” describes the inspected MCP connector, not necessarily the Suno website or underlying service.

## Replace Artifact Observations

For sample C, the connector returned an ordinary song-shaped record: ID, title, URL, creation date, status, visibility, counts, cover URLs, and `metadata` including duration, lyrics, model, style, and `type: generate`. Its title begins with `Replace`, but no Replace-specific relationship, parent ID, project ID, or edit-state field was returned. This verifies the title and returned fields only; it does **not** establish whether the record is a song, edit artifact, or child of another song.

The earlier [song metadata snapshot](experiments/suno-song-metadata-discovery-2026-11-24.md) preserves the prior four-object observations and limitations. No Replace object was changed in this discovery.

## Kio Voice Provenance Investigation

**Captured:** 2026-11-24. **Evidence:** Direct `audio-retrieve` responses for Kio samples E and F. Read-only; no generation or Suno edits were made.

### Retrieved Record Comparison

| Field | Sample E: `1e69b69c-4e05-457e-887f-19ffe1982577` | Sample F: `aebb54a6-b11c-484c-8f4a-7a2228aa966c` |
|---|---|---|
| `title` | `Showtime in the City` | `Showtime in the City` |
| `song_url` | `https://suno.com/song/1e69b69c-4e05-457e-887f-19ffe1982577` | `https://suno.com/song/aebb54a6-b11c-484c-8f4a-7a2228aa966c` |
| `created_at` | `2026-11-24T02:19:25.158Z` | `2026-11-24T02:19:25.158Z` |
| `status` / `visibility` | `complete` / `private` | `complete` / `private` |
| `handle` / `error` | `cjbower` / `null` | `cjbower` / `null` |
| `cover_image_url` | `https://cdn1.suno.ai/image_1e69b69c-4e05-457e-887f-19ffe1982577.jpeg` | `https://cdn1.suno.ai/image_aebb54a6-b11c-484c-8f4a-7a2228aa966c.jpeg` |
| `cover_image_large_url` | `https://cdn1.suno.ai/image_large_1e69b69c-4e05-457e-887f-19ffe1982577.jpeg` | `https://cdn1.suno.ai/image_large_aebb54a6-b11c-484c-8f4a-7a2228aa966c.jpeg` |
| `play_count` | `10` | `7` |
| `like_count` / `liked` / `comment_count` | `0` / `false` / `0` | `0` / `false` / `0` |
| `metadata.description` | `null` | `null` |
| `metadata.duration` | `187.56` seconds | `181.6` seconds |
| `metadata.lyrics` | Present; same returned lyrics as F | Present; same returned lyrics as E |
| `metadata.model` | `v6-mini` | `v6-mini` |
| `metadata.style` | `80s west coast rap style` | `80s west coast rap style` |
| `metadata.type` | `generate` | `generate` |

The complete returned top-level keys for both records were `id`, `title`, `song_url`, `created_at`, `status`, `visibility`, `handle`, `error`, `cover_image_url`, `cover_image_large_url`, `play_count`, `like_count`, `liked`, `comment_count`, and `metadata`. The complete nested `metadata` keys were `description`, `duration`, `lyrics`, `model`, `style`, and `type`. `metadata.controls` and `metadata.negative_style` were absent from both. Lyrics are noted as present and identical but are not duplicated here.

### Voice and Generation Identity Fields

| Field checked in either record | Result |
|---|---|
| `voice_id`, `voice`, `singer`, `vocalist`, `voice_name`, `voice_reference`, `generation_voice`, `model_voice` | Absent from both top-level records and `metadata` |
| `persona`, `character` | Absent from both top-level records and `metadata` |
| `generation_parameters` | Absent from both records |
| `updated_at`, `workspace_id`, `workspace_name` | Absent from both retrieved song records |

### Findings and Evidence Boundaries

- **Verified:** Both IDs returned complete, private, song-shaped records with `metadata.type: generate`.
- **Observed:** Both expose the same `model` (`v6-mini`) and `style` (`80s west coast rap style`), with null `description`; neither exposes any of the checked voice/persona/character/generation-parameter fields.
- **Unknown:** Whether the same voice was used for both songs. A shared model, style, creation timestamp, or lyrics is not evidence that the underlying voice was the same.
- **Advertised:** The `audio-create` schema accepts an optional `voice_id` to select a ready voice for future generation. See [Suno MCP Capability Matrix](suno-mcp-capability-matrix.md).
- **Unknown:** Whether either song's generating voice can be identified and selected for reuse. The records provide no `voice_id` to carry forward; future reuse of a particular voice requires obtaining its ID independently.
- **Observed:** The generation metadata includes model, type, style, duration, lyrics, and a null description, not only prompts/styles. It does not expose a voice identity or a `generation_parameters` object in these two responses.

Workspace membership is not a field in either retrieved song record; Kio membership is established separately by the workspace-filtered listing documented above. This is a point-in-time sample of two records, not evidence that other Suno songs have identical field coverage.

## Try, Try Again Voice-Usage Comparison

**Captured:** 2026-11-24. **Evidence:** Read-only `library-search` for `Try, Try Again` returned 22 exact-title matches with no next cursor. Full `audio-retrieve` responses were inspected for two representatives: one with null style and one whose style text describes a solo vocal. The shared browser tab at capture time showed the Founder Review Workspace, not a Suno song list; the 22-item cohort is therefore defined by the connector search, not claimed to be an exact UI selection.

### Metadata comparison

| Cohort | Search/retrieval evidence | Metadata fields observed | Voice-related result |
|---|---|---|---|
| `Try, Try Again` | 22 complete, private search results; all `metadata.type: generate`, model `v6-mini`, duration 23.56-59.96 seconds, and `metadata.description: null`. `metadata.style` is null for some records and contains vocal-performance wording in others. | Base: `description`, `duration`, `model`, `style`, `type`; `controls` occurs on some results. Full retrieval adds `lyrics`, which search/list responses omit. | No `voice_id`, voice name, singer, vocalist, persona, or generation-voice field appeared in the search objects or either full retrieval. |
| Kio | Two `Showtime in the City` songs, retrieved directly in the prior comparison. | `description`, `duration`, `lyrics`, `model`, `style`, `type`. | No voice identity field. |
| Nebraska search cohort | Read-only `library-search` for `Nebraska` returned 23 title/style matches; a workspace-name search for `Nebraska` returned none. A full retrieval of `Nebraska's Good Life` confirmed the listing shape. | Base fields plus optional `controls`; model values include `v6` and `v6-wild`; some styles contain vocal descriptions. Full retrieval includes `lyrics`. | No voice ID or identity field in the listing or retrieved representative. |
| Ordinary controls | Baseline samples A and B (`The River Remembers`, `Carillon`) retrieved in the earlier object-model discovery. | Base fields; `controls` is present on B and absent on A. Full retrieval includes `lyrics`. | No voice identity field in either sample. |

The two fully retrieved `Try, Try Again` examples were `e47eb16a-ff90-4514-9162-a767c7888978` (`metadata.style: null`) and `7f61d122-d0bd-492d-a13d-1a5e4e628d66` (`metadata.style` contains “lead vocal only / solo singer / unaccompanied vocal performance”). Both returned ordinary song-shaped records. The style wording describes requested vocal content; it is not a voice identity or proof that `voice_id` was supplied.

### Identity, model, and source-type fields

| Field/concept | Finding across the searched/retrieved samples |
|---|---|
| `voice_id`, `voice`, `voice_name`, `singer`, `vocalist`, `persona`, `generation_voice` | Not present in the `Try, Try Again` search records or the two full retrievals; also absent from the previously sampled Kio, Nebraska representative, and ordinary records. |
| `custom_model_id` | Not present as a returned song field in the searched records or retrieved representatives. `metadata.model` is present and contains model labels; it is not a custom-model identity association. |
| `source`, `source_type`, `origin` | No per-song source-type field appeared in these objects. The listing operation accepts `origin` as a filter, but that does not make `origin` a returned song field. |
| `metadata.type` | Present as `generate` in the Try cohort and inspected comparison records. It describes generation type, not source provenance or voice use. |
| `metadata.controls` | Present on some Try and Nebraska results and on ordinary sample B; these are generation-control values, not voice identifiers. The Try examples inspected show style/variety/weirdness controls, not `audio_influence`. |

### Voice-use identification conclusion

**Not generally identifiable from library song metadata.** Some `Try, Try Again` style strings explicitly request a solo or human-sounding vocal, and Nebraska styles include vocalist descriptions. Those strings can be searched as prompt intent, but they do not prove use of a saved voice resource. In a later approved four-clip control/treatment test, `audio-wait` metadata exposed `voice_id` for the two treatment outputs and not for controls, while `library-list` omitted the field for all four. This makes request/response metadata correlation possible for those generated outputs, but does not establish audible influence or provide a general voice-usage reference for existing library songs. See the [voice influence experiment record](experiments/voice-influence-test-2026-11-24.md).

## Voice Object Discovery

**Captured:** 2026-11-24. **Evidence:** Descriptors for `voices-list`, `voices-start`, `audio-create`, `audio-extensions-create`, `audio-covers-create`, and `speech-create`; read-only `voices-list` calls for `own`, `loved`, four requested name variants, and the observed ID. No voice or speech clip was created. A later music voice-ID test is recorded in the [EXP-Voice-ID-Validation registry](experiments/voice-id-validation-registry.md).

### Observed voice-list entry

The read-only `voices-list` call with the `own` collection returned one entry; `collection: loved` returned an empty array. Neither response included `next_cursor`. Account-specific values are redacted here; field names and non-identifying values are preserved.

| Field | Observation | Evidence class | Limits |
|---|---|---|---|
| `id` | UUID-shaped voice identifier; redacted | Observed | This value has UUID form, but the descriptor does not constrain the format. Opaque ID; descriptors say it is used as `voice_id`. |
| `name` | Non-empty, account-specific display name; redacted | Observed | Does not establish an artist identity. |
| `description` | Empty string | Observed | Semantics and optionality are undocumented. |
| `image_url` | URL; redacted | Observed | Image associated with the voice entry, not documented as voice audio. |
| `source` | `recording` | Observed | Field semantics/enum and creation mechanism are not defined by the descriptor; no other source value was observed. |
| `is_owned` | `true` | Observed | Ownership indicator for this single entry; no contrasting value was observed. |
| `is_public` | `false` | Observed | Public-state indicator for this single entry. |
| `type`, `status`, `created_at`, `updated_at` | Not returned | Observed absent in this entry | A single response does not establish the complete schema for all voice types. |

The descriptor describes `voices-list` as newest-first, with `own` or `loved` collections, optional name/ID search, and cursor pagination. The observed calls returned one own entry and zero loved entries, with no `next_cursor`; thus multiple records were not observed in the available collections. Public voices may be searched by known ID, but the connector does not expose a complete public catalog through these queries. One entry with `source: recording` is evidence of recording provenance for that sample, not proof of voice cloning, how training works, whether other source/ownership values are possible, or how long the entry persists.

### Voice name and ID search correlation

**Observed:** Each of the four requested name variants (two name fragments, a full-name phrase, and a possessive voice-label phrase) returned one result from `own`, and all four results had the same UUID as the previously observed voice. The same four name searches returned no results from `loved`. A direct query using that UUID returned the same entry with either `collection: own` or `collection: loved`.

The matching entry remained owned and private (`is_owned: true`, `is_public: false`); no alternate or public voice record appeared in these searches. This demonstrates that the tested name queries follow the selected collection, while the tested ID lookup returned the owned record regardless of collection selection. It does **not** show that no other public voices exist: the descriptor only advertises ID lookup for public voices the user may use, and these reads did not enumerate a public catalog or test a known public ID.

The account-specific name, UUID, and image URL are deliberately not repeated here. This is a point-in-time result for the signed-in account; it does not establish whether other accounts or other names have additional records.

### Voice catalog query boundaries

The `voices-list` descriptor permits only `collection: "own"` and `"loved"`; it does not advertise `"public"` or `"all"`. Those unsupported enum values were not submitted, so there is no runtime rejection response to report. Its `query` parameter is documented for voice-name and voice-ID lookup only. Source-value and ownership-state queries were not attempted because the descriptor does not define them. The generic string parameter type does not establish support for those filters. The observed `own` listing contained the seven fields listed above; `loved` returned no entries. See the [capability matrix](suno-mcp-capability-matrix.md) for the request-by-request evidence table.

### Voice search matching behavior

**Observed, read-only:** Queries for the first UUID segment and last UUID segment alone returned no entries in either `own` or `loved`; the previously tested complete ID returned the voice. Partial name searches (two prefixes and a generic word from the display name) each returned the same entry in `own` and no entries in `loved`. A one-character-deletion near-typo returned no entries in either collection.

The name results support substring matching rather than exact-name-only matching, consistent with the descriptor's “name contains” wording. No fuzzy match was observed in the one near-typo probe, but this is insufficient to establish that fuzzy matching never occurs. Collection behavior was consistent across the probes: the match was present only in `own`, while `loved` was empty. Search terms and account-specific identifiers remain redacted.

### Advertised voice model and modality comparison

| Topic | Evidence-bounded finding |
|---|---|
| Music voice selection | **Advertised:** `audio-create`, `audio-extensions-create`, and `audio-covers-create` accept an optional ready `voice_id`. The descriptors describe it as a voice that sings; supplying it overrides instrumental settings on the create/extension routes. |
| Speech voice selection | **Advertised:** `speech-create` accepts an optional ready `voice_id`; it generates spoken-word audio, always on a default model, with no model selector. |
| Shared selector | **Advertised:** The `voices-list` descriptor explicitly says its listed IDs can be used by both music and speech routes. |
| Preset and user voices | **Advertised:** The speech descriptor mentions preset voices listed in the Quickstart and the user's own voices when the plan includes voice cloning. The connector does not expose a complete preset catalog or its object schema here. |
| Artist identity | **Unknown:** Voice entries expose a name and opaque ID, but no artist/profile identity, attribution, or rights fields. |
| Reuse across songs/calls | **Advertised:** The same ready voice ID is an input on later supported music/speech requests. This does not guarantee identical rendering, consistency, or availability duration. |
| Reuse across workspaces/projects | **Unknown:** Generation routes can file resulting clips into workspaces, but no voice-to-workspace/project relationship or persistence scope is described. |
| Cloning/training | **Advertised, not characterized:** The speech descriptor refers to plans that include voice cloning, and one observed entry has recording provenance. No training recipe, data handling, validation rules, or lifecycle is exposed by the inspected schemas. |
| Persistence/deletion | **Partially advertised:** `voices-start` says a created and verified voice appears in `voices-list` once ready. No retention period, deletion operation, or durable persistence guarantee is documented. |

The connector therefore models `voice_id` as a reusable voice resource selector, not as a documented artist identity. The available evidence does not establish whether speech and music use the same underlying voice model or representation.

### Voice-ID eligibility

**Advertised:** `audio-create`, `audio-covers-create`, `audio-extensions-create`, and `speech-create` accept an optional `voice_id`. Their descriptors require a ready voice and direct signed-in Suno users to their own Suno voices; the observed record was owned and private. The record does not expose a readiness field, so its runtime acceptance was not tested.

**Unknown / ambiguous:** `voices-list` can search by ID for an owned voice or a public voice the user may sing in, but the four generation descriptors describe account-owned/own voices and do not clearly confirm acceptance of a public voice belonging to someone else. A private voice from another account is not advertised as usable. None of the four generation schemas requires `source: recording`; that value was observed only in this one record. See [Suno MCP Capability Matrix](suno-mcp-capability-matrix.md) for per-operation constraints.

### Voice lifecycle and usage correlation

The complete advertised inventory contains only `voices-list` and `voices-start` as voice-specific operations. The observed entry has no creation timestamp, readiness/processing status, verification result, training metadata, recording reference, model/custom-model association, or song/speech usage-reference field. `source: recording`, `is_owned: true`, and `is_public: false` are the only observed source/ownership details. `voices-start` opens an external creation/verification flow and says a voice appears in the list once ready, but it does not expose a status or verification-result operation.

The four generation descriptors establish that a voice ID can be supplied as an input to speech, music, cover, and extension generation. They do not provide a way to determine which existing clips used a voice; sampled song objects contain no `voice_id`, and the voice object contains no usage history. No generation was attempted, so no output was correlated with this voice.

## Known Limitations and Open Questions

- This is a point-in-time sample of five records and the connector tools available to the signed-in account; it is not a complete Suno API specification.
- Voice-object fields above come from one `voices-list` result and may not cover preset, loved, public, or processing voices; account-specific IDs, names, and image URLs were redacted.
- A field absent from these responses may be present on other songs or in Suno's own UI/API.
- Song lists and playlist clip lists omit lyrics through MCP; `audio-retrieve` returned lyrics for the user's own songs.
- The connector's workspace-filtered library listing excludes collaborators' songs in shared workspaces, per its tool description.
- The sample does not establish whether `metadata.max_mode` or source-reference fields are populated for other generation types.
- The connector does not expose a verified Replace-parent, project, remaster-parent, archive, deletion, or workspace-rename relationship/operation in this evidence set.
- Tagging, categories, labels, custom metadata, and persona association remain unverified.
- The Replace-titled and Untitled Project-titled records need additional evidence before either title is promoted into a semantic object classification.
