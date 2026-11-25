# Suno MCP Capability Matrix

**Captured:** 2026-11-24
**Status:** Point-in-time inventory of the Suno MCP tool registry; read-only discovery
**Scope:** Capabilities advertised by the signed-in Suno MCP connector, not a complete Suno product or API specification

## Purpose and Evidence Labels

This reference inventories the connector operations and their advertised parameters, operation type, and descriptor-level return shape. It does not execute write operations to test them.

- **VERIFIED** — successfully executed and validated in this session or in the prior repository discovery recorded in [Suno Object Model Discovery](suno-object-model-discovery.md).
- **TESTED-FAILED** — executed and returned an error. This label applies to that attempt/input, not necessarily to the whole operation.
- **EXPOSED-NOT-TESTED** — advertised in the connector registry, but not executed and validated.
- **UNKNOWN** — no corresponding operation was found in the complete advertised tool inventory. This means unknown/not exposed by this connector, not necessarily absent from Suno itself.

The connector exposes tool parameter descriptors and descriptions, but not a uniform formal response schema for every operation. “Return shape” below is the shape or fields stated in the descriptor; details not stated there remain unknown. Parameters are grouped by required and optional status as advertised. Conditional requirements and nested parameter properties are called out where material.

## Inventory Summary

The advertised inventory contains **60 operations**. The previously verified operations include listing and retrieving songs, listing workspaces and playlists, creating a workspace, assigning songs to a workspace, and read-only `voices-list` requests. No destructive operation was attempted.

### Songs and Audio

| Tool / capability | Description | Required parameters | Optional parameters | Read or write | Return shape | Status |
|---|---|---|---|---|---|---|
| `account-me` | Read the signed-in Suno user's public profile. | None | None | Read | User profile; exact fields are not specified in the descriptor. | EXPOSED-NOT-TESTED |
| `account-upgrade` | Open the Suno plan/credit upgrade flow; does not itself document a purchase action. | None | None | Account action | Upgrade URL/button flow. | EXPOSED-NOT-TESTED |
| `account-usage` | Read account plan and metered usage. | None | None | Read | Account plan and usage; Suno account includes generation credits. | EXPOSED-NOT-TESTED |
| `audio-analysis` | Generate/read audio description and musical timing analysis; first read can start background analysis. | `id` | None | Read / analysis job | Status; musical beats, tempo, meter, key, sections, terms, and labels when available. | EXPOSED-NOT-TESTED |
| `audio-covers-create` | Generate a cover from a source clip with a new style or voice. | `id` | `controls` (`audio_influence`, `style_influence`, `variety`, `weirdness`), `custom_model_id`, `duration`, `idempotency_key`, `lyrics`, `max_mode`, `model`, `negative_style`, `style`, `title`, `voice_id`, `workspace_id` | Write / credit-spending generation | New clip; creation tools return clip IDs/status for later polling. | EXPOSED-NOT-TESTED |
| `audio-create` | Generate one or more songs in simple-description or custom-lyrics mode; can use reference songs or a MIDI upload. | No unconditional required field. Conditional: `description` for simple mode; custom mode uses `lyrics` and/or `style`; `instrumental: true` allows both to be omitted. | `controls` (`audio_influence`, `style_influence`, `variety`, `weirdness`), `custom_model_id`, `description`, `duration`, `duration_guidance`, `duration_strict`, `idempotency_key`, `instrumental`, `lyrics`, `max_mode`, `midi_upload_id`, `model`, `negative_style`, `reference_audio_ids`, `style`, `title`, `vocal_gender`, `voice_id`, `workspace_id` | Write / credit-spending generation | New clip IDs; a Suno sign-in receives two songs per call. | EXPOSED-NOT-TESTED |
| `audio-download` | Download the signed-in user's own song, subject to Suno download rules and credits. | `id` | `confirm` (default false), `format` (`mp3` or `wav`; default `mp3`) | Read / download; may spend a download credit after confirmation | Download URL or a processing/credit-required response. | EXPOSED-NOT-TESTED |
| `audio-edit` | Change a song's title, lyrics, caption, or any combination; does not change visibility. | `id` | `caption` (max 500 chars), `lyrics`, `title` | Write | Updated song object; exact response fields are not stated in the descriptor. | EXPOSED-NOT-TESTED |
| `audio-extensions-create` | Generate a continuation from a source clip at `continue_at`; resulting clip is only the continuation. | `id`, `continue_at` | `controls` (`audio_influence`, `style_influence`, `variety`, `weirdness`), `custom_model_id`, `duration`, `idempotency_key`, `instrumental`, `lyrics`, `max_mode`, `model`, `negative_style`, `style`, `title`, `voice_id`, `workspace_id` | Write / credit-spending generation | Continuation clip ID(s); use `audio-full-song` to join a chain. | EXPOSED-NOT-TESTED |
| `audio-full-song` | Join a completed extension chain into a whole-song clip. | `id` (last extension) | `idempotency_key` | Write / creates a joined clip; free according to descriptor | Joined clip object/status. | EXPOSED-NOT-TESTED |
| `audio-like` | Like or dislike a song. | `id` | `dislike` (default false) | Write / account preference | Operation result; exact response fields are not stated. | EXPOSED-NOT-TESTED |
| `audio-listen` | Ask Suno's audio model a question about a finished clip. | `id`, `question` | None | Read / analysis job | Listen ID and `processing` status; `audio-listen-wait` retrieves the answer. | EXPOSED-NOT-TESTED |
| `audio-listen-wait` | Read the result of an `audio-listen` request. | `id` | None | Read | Status and, when ready, text answer or error. | EXPOSED-NOT-TESTED |
| `audio-lyrics-alignment` | Read or generate word-level lyric timings. | `id` | None | Read / analysis job | Status and aligned words with audio spans and best-effort success flags. | EXPOSED-NOT-TESTED |
| `audio-mashups-create` | Create a mashup of exactly two source clips. | `id`, `additional_audio_id` | `controls` (`audio_influence`, `style_influence`, `variety`, `weirdness`), `custom_model_id`, `duration`, `idempotency_key`, `lyrics`, `max_mode`, `model`, `negative_style`, `style`, `title`, `workspace_id` | Write / credit-spending generation | New mashup clip ID(s). | EXPOSED-NOT-TESTED |
| `audio-midi` | Transcribe a finished song to a multi-track MIDI file; descriptor states 10 credits unless cached or a generated stem. | `id` | None | Read / paid analysis job | Processing status; on success, MIDI URL and instrument/track note counts. | EXPOSED-NOT-TESTED |
| `audio-retrieve` | Read a clip's current status and metadata. | `id` | None | Read | Audio clip object; may include status, song URL, metadata, engagement counts, and source reference IDs. | VERIFIED |
| `audio-settings` | Change a song's visibility and/or remix permission. | `id`; at least one of `visibility` or `can_remix` to request a change | `can_remix`, `visibility` (`public` or `private`) | Write | Updated setting state or an error; exact response fields are not specified. | EXPOSED-NOT-TESTED |
| `audio-stems-create` | Split a finished song into two or twelve stem parts. | `id`, `mode` (`two` or `twelve`) | `idempotency_key` | Write / paid generation | Stem group identifier and initial status. | EXPOSED-NOT-TESTED |
| `audio-stems-retrieve` | Read the result of a stem split. | `id`, `group_id` | None | Read | Group status (`pending`, `complete`, `partial`, or `error`) and stem clip IDs. | EXPOSED-NOT-TESTED |
| `audio-unlike` | Clear the signed-in user's like/dislike on a song. | `id` | None | Write / account preference | Operation result; exact response fields are not stated. | EXPOSED-NOT-TESTED |
| `audio-upload-complete` | Complete processing of an audio upload session. | `id` (upload-session ID) | `title` | Write / creates library clip | New audio clip object/status. | EXPOSED-NOT-TESTED |
| `audio-upload-create` | Start an audio upload session, optionally with a chat attachment. | No unconditional required field; the user must supply the audio through `file` or the returned upload flow. | `file`, `title` | Write / starts upload | Upload session ID and upload URL/page URL, or resulting clip when an attachment is passed. | EXPOSED-NOT-TESTED |
| `audio-wait` | Wait for generated audio clips to become playable or complete. | One of `id` or `ids` (up to 12) | `until` (`playable` or `complete`; default `playable`) | Read / polling | Audio clip response(s), with multiple results under `clips`. | EXPOSED-NOT-TESTED |
| `library-liked` | List songs liked by the user, including songs by others. | None | `cursor`, `limit` (1-50; default 10) | Read | Paginated song objects and optional `next_cursor`. | EXPOSED-NOT-TESTED |
| `library-list` | List the signed-in user's finished songs; supports paging and filters. | None | `cursor`, `downloaded`, `liked`, `limit` (1-50; default 10), `origin` (`upload`, `cover`, `extension`, `remaster`), `visibility`, `workspace_id` | Read | Paginated audio-retrieve-shaped song objects; lyrics are omitted from this list response. | VERIFIED |
| `library-search` | Search finished songs by title or style, with library-list filters. | None unconditionally; `query` if performing a search | `cursor`, `downloaded`, `liked`, `limit` (1-50; default 10), `origin`, `query` (1-200 chars), `visibility`, `workspace_id` | Read | Paginated song objects and optional `next_cursor`. | EXPOSED-NOT-TESTED |

### Workspaces and Playlists

| Tool / capability | Description | Required parameters | Optional parameters | Read or write | Return shape | Status |
|---|---|---|---|---|---|---|
| `playlists-add-clips` | Add songs to a playlist the user owns. | `id` (playlist ID), `clip_ids` (1-100) | None | Write | Added/failed IDs; failed entries include reasons. | EXPOSED-NOT-TESTED |
| `playlists-create` | Create a private playlist by default. | `name` (1-100 chars) | `description` (max 2000 chars), `visibility` (`public` or `private`; default `private`) | Write | New playlist record; list records expose ID, name, URL, visibility, and clip count. | EXPOSED-NOT-TESTED |
| `playlists-list` | List playlists owned by the user, optionally by name query. | None | `cursor`, `limit` (1-50; default 25), `query` (max 200 chars) | Read | Paginated playlist records and optional `next_cursor`. | VERIFIED |
| `playlists-list-clips` | List songs in a playlist in playlist order. | `id` (playlist ID) | `cursor`, `limit` (1-50; default 10) | Read | Paginated song objects; lyrics are omitted through MCP. | VERIFIED |
| `playlists-remove-clips` | Remove songs from a playlist; songs remain in the library. | `id` (playlist ID), `clip_ids` (1-100) | None | Write | Requested IDs under `removed`, including IDs not previously present. | EXPOSED-NOT-TESTED |
| `workspaces-create` | Create a workspace. | `name` (1-100 chars) | `description` (max 2000 chars) | Write | Workspace record; observed fields include ID, name, description, and clip count. | VERIFIED |
| `workspaces-list` | List owned or invited workspaces, optionally by name query. | None | `cursor`, `query` (max 200 chars) | Read | Paginated workspace records and optional `next_cursor`. | VERIFIED |
| `workspaces-update-clips` | Add/remove songs from a workspace; adding moves a song out of its former workspace. A song can be in at most one workspace. | `id` (workspace ID) | `add` (up to 50 clip IDs), `remove` (up to 50 clip IDs) | Write | Added, removed, and skipped IDs; check skipped IDs instead of assuming success. | VERIFIED |

### Visuals, Sequences, Voices, and Other Media

| Tool / capability | Description | Required parameters | Optional parameters | Read or write | Return shape | Status |
|---|---|---|---|---|---|---|
| `characters-list` | List saved characters and optionally Suno preset characters/backgrounds. | None | `presets` (boolean) | Read | Character entries with image references; exact full record shape is not specified. | EXPOSED-NOT-TESTED |
| `characters-save` | Save a ready image as a character. | `id` (image asset ID) | None | Write | Saved character result; exact response fields are not specified. | EXPOSED-NOT-TESTED |
| `custom-models-list` | List own or shared custom models, with optional name query and paging. | None | `collection` (`own` or `shared`; default `own`), `cursor`, `limit` (1-100; default 20), `query` (1-200 chars) | Read | Paginated model records and optional `next_cursor`; includes `can_use` where described. | EXPOSED-NOT-TESTED |
| `image-create` | Generate image assets, optionally as a Sequence shot keyframe; supports price-only dry run. | `prompt` | `aspect` (`1:1`, `9:16`, `16:9`), `dry_run`, `idempotency_key`, `model`, `sequence_id`, `shot_id` | Write / may spend Visuals credits; dry run starts nothing | Generation ID, or a quote for dry run; `visuals-wait` returns assets. | EXPOSED-NOT-TESTED |
| `midi-upload-complete` | Finish processing a MIDI upload. | `id` (MIDI upload ID) | None | Write / completes upload | MIDI upload record, including `midi_upload_id` as described. | EXPOSED-NOT-TESTED |
| `midi-upload-create` | Start a MIDI upload, optionally from an attached MIDI file. | No unconditional required field; user supplies file through attachment or upload flow. | `file` | Write / starts upload | Upload URL/fields or completed upload record; MIDI must be under 256 KB. | EXPOSED-NOT-TESTED |
| `sequence-create` | Create a music-video Sequence with a song timeline, shots, style, characters, and sets. | `shots` (1-200 entries; each requires `duration_s`) | `aspect`, `characters`, `idempotency_key`, `lyrics`, `sets`, `song_id`, `song_start_s`, `style`, `title` | Write / creates Sequence; descriptor says free | Sequence ID, editor URL, and Sequence details. | EXPOSED-NOT-TESTED |
| `sequence-export` | Render a Sequence as an MP4. | `id` (Sequence ID) | None | Write / creates render; descriptor says free | Render ID; wait and download for output. | EXPOSED-NOT-TESTED |
| `sequence-generate` | Generate keyframes or clips for up to eight Sequence shots. | `id` (Sequence ID), `shots` (1-8, each with `shot_id` and `prompt`), `step` (`keyframes` or `clips`) | `aspect`, `dry_run`, `idempotency_key`, `model`, `resolution`; per-shot `continues_shot_id`, `first_frame_asset_id`, `last_frame_asset_id`, `leads_into_shot_id`, `lip_sync`, `prompt`, `shot_id` | Write / may spend Visuals credits; dry run starts nothing | Per-shot status, generation IDs, and take labels; wait for generated assets. | EXPOSED-NOT-TESTED |
| `sequence-get` | Read one Sequence. | `id` (Sequence ID) | `view` (`full` or `summary`; default `full`) | Read | Sequence style, characters, sets, ordered shots, progress, and take details; summary omits descriptive fields. | EXPOSED-NOT-TESTED |
| `sequence-list` | List the user's Sequences with optional title query and paging. | None | `cursor`, `limit` (1-20; default 20), `query` | Read | Sequence entries with title and length, plus optional cursor. | EXPOSED-NOT-TESTED |
| `sequence-update` | Update Sequence style, characters, sets, shot metadata/assets, or timeline. | `id` (Sequence ID) | `characters`, `idempotency_key`, `ops` (up to 49), `sets`, `shots`, `style`, `view` (`full` or `changed`; default `full`) | Write; descriptor states timeline and metadata changes save atomically | Updated Sequence or changed shots/deleted shot IDs/revision in `changed` view. | EXPOSED-NOT-TESTED |
| `sounds-create` | Generate two short sound effects, one-shots, or loops. | `description` (1-500 chars) | `idempotency_key`, `key`, `loop`, `tempo` (1-300), `title` | Write / costs credits | Two clip IDs; poll audio status for each. | EXPOSED-NOT-TESTED |
| `speech-create` | Generate spoken-word audio. Exactly one of `script` or `prompt` is required; `style` is only valid with `script`. | Conditional: exactly one of `script` or `prompt` | `backing_music`, `duration` (15-360), `duration_guidance`, `duration_strict`, `idempotency_key`, `negative_style`, `prompt`, `script`, `style`, `title`, `vocal_gender`, `voice_id`, `workspace_id` | Write / generation | Descriptor says it returns an ordinary audio clip that can be polled by ID; it does not enumerate the full response object. | EXPOSED-NOT-TESTED |
| `video-assemble` | Render an ordered set of ready video clips/stills over a song. | `clips` (1-40 entries; each requires `asset_id`), `song_id` | `aspect`, `idempotency_key`, `lyrics`, `song_start_s`; per-clip `duration_s`, `trim_start_s`, `trim_end_s` | Write / creates render; descriptor says free | Render ID; wait and download the MP4. | EXPOSED-NOT-TESTED |
| `video-create` | Generate a 5-15 second video clip, optionally tied to a song or Sequence shot; supports price-only dry run. | `prompt` | `aspect`, `dry_run`, `duration_s` (5-15), `first_frame_asset_id`, `idempotency_key`, `last_frame_asset_id`, `lip_sync`, `model`, `resolution`, `sequence_id`, `shot_id`, `song_id`, `song_start_s` | Write / may spend Visuals credits; dry run starts nothing | Generation ID; wait for video asset. | EXPOSED-NOT-TESTED |
| `visuals-download` | Obtain a signed URL for an image/video asset. | `id` (asset ID) | None | Read / download | Signed download URL or processing state. | EXPOSED-NOT-TESTED |
| `visuals-library` | List the user's image/video generations, optionally filtered by sequence, song, media type, or liked state. | None | `cursor`, `liked`, `limit` (1-50; default 20), `media_type` (`image` or `video`), `sequence_id`, `song_id` | Read | Paginated generations, prompts, models, and assets. | EXPOSED-NOT-TESTED |
| `visuals-models` | List image/video models, supported sizes/aspects, audio support, defaults, and credit rates. | None | None | Read | Model catalog and defaults. | EXPOSED-NOT-TESTED |
| `visuals-show` | Display ready image/video assets or presets in chat. | None unconditionally; `ids` to select assets | `at` (video frame times), `ids` (up to 10 asset IDs or preset references) | Read / presentation | Displayed image/video frames; URLs may be supplied for Suno assets. | EXPOSED-NOT-TESTED |
| `visuals-upload-complete` | Finish processing a visuals upload. | `id` (asset/upload ID) | None | Write / completes upload processing | Asset ID/status; `visuals-wait` can wait for ready/failed processing. | EXPOSED-NOT-TESTED |
| `visuals-upload-create` | Start an image/video upload. | No unconditional required field; user supplies an attachment or chooses a file in the uploader. | `bytes`, `content_type`, `file` | Write / starts upload | Upload URL and fields, or resulting upload asset when file is attached. | EXPOSED-NOT-TESTED |
| `visuals-wait` | Wait for visual generations or renders. | `ids` (up to 8 generation/render IDs) | `view` (`full` or `summary`; default `full`) | Read / polling | Job statuses and generated assets/takes. | EXPOSED-NOT-TESTED |
| `voices-list` | List own or loved voices, with optional query and paging. | None | `collection` (`own` or `loved`; default `own`), `cursor`, `limit` (1-100; default 20), `query` (1-200 chars) | Read | One live result observed with fields `id`, `name`, `description`, `image_url`, `source`, `is_public`, and `is_owned`; descriptor documents paging with `next_cursor`. | VERIFIED |
| `voices-start` | Start the Suno custom voice setup/verification flow. | None | None | Write / starts external account workflow | Suno URL to create and verify a voice; exact response wrapper is not enumerated. | EXPOSED-NOT-TESTED |

## Focused Schema Inspection

The five operations below were inspected from their MCP descriptors. `voices-list` was subsequently invoked read-only for the `own` and `loved` collections and queried once by the observed ID; the returned entry shape is documented below. At that inspection stage, no generation or voice-creation operation was invoked. A later approved music-generation control/treatment test is documented under [Voice Influence Experiment](experiments/voice-influence-test-2026-11-24.md). “Return schema” states exactly what the descriptor supports; where it does not provide a complete JSON shape, that limitation is explicit.

### `speech-create`

**Operation:** Generate spoken-word audio. This is a write/generation operation and requires the plan's speech feature. The result is described as an ordinary audio clip; the descriptor does not provide a complete formal response schema.

| Parameter | Type and constraints | Required? | Descriptor example or usage note |
|---|---|---|---|
| `backing_music` | Boolean; default `false` | No | Keep a music bed under the speech; default is no music. |
| `duration` | Integer, 15-360 seconds | No | Target duration; omitted to let the model choose. |
| `duration_guidance` | Boolean | No | Only meaningful with `duration`; enabled by default when a duration is set. Sizes AI-written words to the target; does not rewrite a supplied `script`. |
| `duration_strict` | Boolean | No | Only meaningful with `duration`; enabled by default when a duration is set. `false` makes the duration a soft target. |
| `idempotency_key` | String, 1-255 bytes, non-whitespace pattern | No | Reuse the same key on a retry to avoid creating a second generation. |
| `negative_style` | String, max 1000 characters | No | Styles to avoid; only valid with caller-supplied tags and not with `prompt`; requires advanced-controls access. |
| `prompt` | String, max 2947 characters, or max 2887 with `backing_music` | One of `prompt` or `script` | Instruction for AI-written spoken words. |
| `script` | String, max 5000 characters | One of `script` or `prompt` | Words to speak verbatim. |
| `style` | String, max 1000 characters | No | Delivery tags; valid only with `script`. When `backing_music` is enabled, may also describe the bed's style. Descriptor example: `"calm narrator, warm"`. |
| `title` | String, max 256 characters | No | Clip title. |
| `vocal_gender` | Enum: `"male"` or `"female"` | No | Force the generated voice gender; requires advanced-controls access. |
| `voice_id` | String | No | Optional ready voice ID; on a Suno sign-in, use a voice from `voices-list`. |
| `workspace_id` | String | No | Workspace in which to file the new clip; Suno sign-in only. |

**Required-field rule:** Exactly one of `script` and `prompt` must be supplied. `style` cannot accompany `prompt`; the descriptor says that combination returns HTTP 400. `duration_guidance` or `duration_strict` without `duration` is invalid.

**Return schema:** The descriptor says the generated result is an ordinary clip and directs callers to poll `GET /v0/audio/{id}`; it does not enumerate the full immediate response keys. The audio retrieval descriptor documents the clip object as exposing fields including ID, status, and (when available) `song_url`. These are descriptor-level references, not a result observed by running `speech-create`.

**Descriptor-grounded example shape (not executed):**

```json
{
  "script": "<spoken words>",
  "style": "calm narrator, warm",
  "backing_music": false
}
```

### `voices-list`

**Operation:** Read/list Suno voices. It is available for a signed-in Suno user; API-key authentication is documented to return HTTP 403.

| Parameter | Type and constraints | Required? | Descriptor example or usage note |
|---|---|---|---|
| `collection` | Enum: `"own"` or `"loved"`; default `"own"` | No | `"loved"` is the set saved or favorited by the user. |
| `cursor` | String | No | Use `next_cursor` from the previous page. |
| `limit` | Integer, 1-100; default 20 | No | Page size. |
| `query` | String, 1-200 characters | No | Search voice name in the selected collection, or supply a voice ID to find the user's own or a public voice they may use. A name search is limited to the selected collection. |

**Return schema:** The descriptor documents a newest-first voice list with pagination via `next_cursor`, but does not enumerate voice-entry keys. Live reads returned a `voices` array with one entry in `own` and an empty array in `loved`; the own entry exposed `id`, `name`, `description`, `image_url`, `source`, `is_public`, and `is_owned`. Neither response contained `next_cursor`. Four requested name variants each returned the same own entry and no loved result. Querying the observed ID returned that same owned/private entry with either collection selected. No alternate or public entry appeared; these searches do not enumerate a public catalog. See “Observed voice-list entry” and “Voice name and ID search correlation” in the [object-model discovery](suno-object-model-discovery.md). The descriptor states that each voice's `id` can be supplied as `voice_id` to `audio-create`, `speech-create`, `audio-covers-create`, and `audio-extensions-create`.

#### Voice catalog enumeration and query scope

| Request | Advertised by descriptor? | Read-only observation / disposition |
|---|---|---|
| `collection: "own"` | Yes; default | Returned one entry. Its observed fields were `id`, `name`, `description`, `image_url`, `source`, `is_public`, and `is_owned`. |
| `collection: "loved"` | Yes | Returned an empty `voices` array. |
| `collection: "public"` | No; enum permits only `"own"` or `"loved"` | Not sent; no runtime rejection or result was captured. |
| `collection: "all"` | No; enum permits only `"own"` or `"loved"` | Not sent; no runtime rejection or result was captured. |
| `query` as a voice name | Yes; descriptor says the name contains the query text, within the selected collection | Partial name fragments and a generic word from the name matched the same own entry; loved searches were empty. One near-typo returned no entries in either collection. |
| `query` as a voice ID | Yes; descriptor says it finds the user's own or a public voice they may use | The full observed ID returned the same owned/private entry with either collection selected; the first UUID segment and last UUID segment alone returned no entries in either collection. |
| `query` as a source value | Not documented | Not attempted; runtime behavior is unknown. |
| `query` as an ownership-state filter | Not documented | Not attempted; runtime behavior is unknown. |

Thus, `public` and `all` are outside the advertised collection schema, but were not submitted to obtain a server-side error. Likewise, the generic string type for `query` is not evidence that source or ownership filters are supported; only name and ID lookup are documented. No public voice appeared in the observed results, which does not establish that no public voice exists.

The observed partial-name matches are consistent with the descriptor's “name contains” behavior, not exact-name-only matching. Fuzzy matching was not observed for the single near-typo tested; this does not establish the behavior for every possible spelling variation.

**Descriptor-grounded example shape (not executed):**

```json
{
  "collection": "own",
  "limit": 20,
  "query": "<voice name or ID>"
}
```

### `voices-start`

**Operation:** Start the Suno custom-voice creation and verification flow. The descriptor instructs the caller to invoke this before asking for audio and says not to request recordings or files. It is only for a Suno sign-in; API-key authentication returns HTTP 409.

| Parameter | Type and constraints | Required? | Descriptor example or usage note |
|---|---|---|---|
| None | No input parameters | N/A | Invoke with an empty parameter object. |

**Return schema:** The descriptor guarantees a Suno `url` where the user creates and verifies the voice. It does not enumerate the complete response wrapper. Once ready, the voice appears in `voices-list` and its `id` can be passed as `voice_id`.

**Descriptor-grounded example shape (not executed):**

```json
{}
```

### Full music-generation parameter schemas

The following tables transcribe the advertised top-level parameters for the three music-generation operations in scope. These are descriptor schemas, not execution examples; no generation operation was called. The `speech-create`, `voices-list`, and `voices-start` schemas are recorded above.

#### `audio-create`

No top-level parameter is unconditionally required. The request has conditional mode rules: simple mode uses `description`; custom mode uses `lyrics` and/or `style`; `instrumental: true` allows both to be omitted. Sending `description` with `lyrics` or `style` is invalid except that `lyrics` may accompany description when instrumental.

| Parameter | Type and constraints | Required? | Descriptor meaning / constraint |
|---|---|---|---|
| `controls` | Object; nested fields below | No | Advanced controls; requires plan grant. |
| `custom_model_id` | String | No | Account's own/shared custom model; cannot be combined with `model` or `midi_upload_id`. |
| `description` | String, max 3000 chars | Conditional | Simple-mode natural-language instruction; AI writes lyrics and style. |
| `duration` | Integer, 15-360 | No | Target seconds; result may vary unless strict duration is enabled. |
| `duration_guidance` | Boolean | No | Only valid with `duration`; sizes AI-written lyrics to target duration. |
| `duration_strict` | Boolean | No | Only valid with `duration`; true hard-caps output at the target. |
| `idempotency_key` | String, 1-255 bytes, non-whitespace | No | Retry key for idempotent creation. |
| `instrumental` | Boolean; default `false` | No | Requests no vocals, but a `voice_id` takes precedence and sings. |
| `lyrics` | String, max 5000 chars | Conditional | Custom-mode lyrics; incompatible with `description` unless instrumental. |
| `max_mode` | Boolean | No | Higher-compute mode; requires lyrics or style and plan support. |
| `midi_upload_id` | String | No | MIDI score upload; Suno sign-in only, requires `v6-wild`, and uses simple mode. |
| `model` | String | No | Generation model label; cannot be combined with `custom_model_id`. |
| `negative_style` | String, max 1000 chars | No | Styles to avoid; requires caller-supplied style tags, not `description`. |
| `reference_audio_ids` | Array of unique strings, max 10 items | No | Finished source song IDs for reference-based generation or edits. |
| `style` | String, max 1000 chars | Conditional | Custom-mode style/genre tags; incompatible with `description`. |
| `title` | String, max 256 chars | No | Output title. |
| `vocal_gender` | Enum: `"male"` or `"female"` | No | Vocal gender; a supplied `voice_id` takes precedence. |
| `voice_id` | String | No | Ready voice ID from the account's voice catalog; a voice always sings and overrides `instrumental`. |
| `workspace_id` | String | No | Workspace for the resulting clip; Suno sign-in only. |

#### `audio-extensions-create`

| Parameter | Type and constraints | Required? | Descriptor meaning / constraint |
|---|---|---|---|
| `id` | String | Yes | Source clip ID; source must be complete. |
| `continue_at` | Number, minimum 0.4 | Yes | Seconds into the source clip from which to continue. |
| `controls` | Object; nested fields below | No | Advanced controls; requires plan grant. |
| `custom_model_id` | String | No | Account's own/shared custom model; cannot be combined with `model`. |
| `duration` | Integer, 15-360 | No | Target continuation duration. |
| `idempotency_key` | String, 1-255 bytes, non-whitespace | No | Retry key for idempotent creation. |
| `instrumental` | Boolean | No | Vocal-free continuation; a `voice_id` takes precedence. |
| `lyrics` | String, max 5000 chars | No | Lyrics for the continuation; omitted lyrics continue the source lyrics. |
| `max_mode` | Boolean | No | Higher-compute mode; Suno sign-in and plan support required. |
| `model` | String | No | Generation model label; cannot be combined with `custom_model_id`. |
| `negative_style` | String, max 1000 chars | No | Styles to avoid; requires advanced-controls access. |
| `style` | String, max 1000 chars | No | Style/genre tags for the continuation. |
| `title` | String, max 256 chars | No | Defaults to source title. |
| `voice_id` | String | No | Ready account voice ID; implies vocals and overrides an instrumental source. |
| `workspace_id` | String | No | Workspace for the new continuation; Suno sign-in only. |

#### `audio-covers-create`

| Parameter | Type and constraints | Required? | Descriptor meaning / constraint |
|---|---|---|---|
| `id` | String | Yes | Source clip ID; source must be complete. |
| `controls` | Object; nested fields below | No | Advanced controls; requires plan grant. |
| `custom_model_id` | String | No | Account's own/shared custom model; cannot be combined with `model`. |
| `duration` | Integer, 15-360 | No | Target output duration. |
| `idempotency_key` | String, 1-255 bytes, non-whitespace | No | Retry key for idempotent creation. |
| `lyrics` | String, max 5000 chars | No | Lyrics to sing; omitted lyrics make the cover instrumental unless `voice_id` is set. |
| `max_mode` | Boolean | No | Higher-compute mode; Suno sign-in and plan support required. |
| `model` | String | No | Generation model label; cannot be combined with `custom_model_id`. |
| `negative_style` | String, max 1000 chars | No | Styles to avoid; requires advanced-controls access. |
| `style` | String, max 1000 chars | No | New style/genre tags. |
| `title` | String, max 256 chars | No | Defaults to source title. |
| `voice_id` | String | No | Ready account voice ID; a supplied voice always sings, even without lyrics. |
| `workspace_id` | String | No | Workspace for the new clip; Suno sign-in only. |

#### Shared nested `controls` schema

| Nested field | Type and constraints | Descriptor meaning |
|---|---|---|
| `audio_influence` | Number, 0-1 | Music generation: resemblance to the supplied voice; only valid with `voice_id`. On covers/extensions, source-audio influence. |
| `style_influence` | Number, 0-1 | How strongly the supplied style tags are followed. |
| `variety` | Integer, 0-4 | Style reinterpretation level. |
| `weirdness` | Number, 0-1 | Amount of deviation from expected results. |

#### Descriptor-described return shapes

| Operation | Return information advertised | Schema limitation |
|---|---|---|
| `audio-create` | New clip IDs; a signed-in Suno user receives two songs per call. Poll audio by ID. | Full immediate response object is not enumerated. |
| `audio-extensions-create` | `clip_ids`; one continuation per supplied ID. Join the desired chain with `audio-full-song`. | Full immediate response wrapper is not enumerated. |
| `audio-covers-create` | New audio clip; creation tools return clip IDs/status for later polling. | Full immediate response object is not enumerated. |
| `speech-create` | Ordinary audio clip; poll `GET /v0/audio/{id}`. | Full immediate response object is not enumerated. |
| `voices-list` | Observed `voices` array entry fields are listed below; descriptor documents `next_cursor` pagination. | Formal response schema and all variants are not enumerated. |
| `voices-start` | Advertised Suno `url` to create/verify a voice. | Exact response wrapper and additional fields are not enumerated; operation was not invoked. |

### `characters-list`

**Operation:** Read the user's saved characters and optionally include Suno preset characters and backgrounds. It requires a Suno user token granting `visuals`; otherwise the descriptor documents HTTP 404.

| Parameter | Type and constraints | Required? | Descriptor example or usage note |
|---|---|---|---|
| `presets` | Boolean | No | `presets=true` adds Suno's preset characters and preset backgrounds. |

**Return schema:** The descriptor says the result lists saved character images, most recently used first, at most 60. With presets enabled it includes Suno presets/backgrounds. It refers to saved image `asset_id` and preset `ref` values, including the `preset:<id>` form, but does not enumerate the complete entry or response wrapper. It recommends `visuals-show` to display an image rather than using `thumbnail_url`.

**Descriptor-grounded example shape (not executed):**

```json
{
  "presets": true
}
```

### `characters-save`

**Operation:** Save a ready image as a character. A video asset returns HTTP 400; an upload that is still processing returns HTTP 409. It requires a Suno user token granting `visuals`; otherwise the descriptor documents HTTP 404.

| Parameter | Type and constraints | Required? | Descriptor example or usage note |
|---|---|---|---|
| `id` | String; the ready image's `asset_id` | Yes | The descriptor calls this the image's `asset_id`; the resulting character appears first in `characters-list` and in Suno's character picker. |

**Return schema:** The descriptor does not enumerate response keys or a formal JSON schema. It specifies the side effect: the image is saved as a character, and saving it again marks it used now. It instructs callers to retain the character name/role in the Sequence's `characters`.

**Descriptor-grounded example shape (not executed):**

```json
{
  "id": "<ready-image-asset-id>"
}
```

## Voice, Character, and Speech Findings

### Evidence Vocabulary and Scope

These findings are based on the five MCP tool descriptors listed above, plus read-only `voices-list` calls. **Verified** and **Observed** apply only to successful list/query calls and their returned entry; all generation and voice-creation operations remain **Untested** at runtime for this investigation. Descriptor-backed features are **Advertised**; absent or unspecified features remain **Unknown**. **Inferred** is used only for cautious conclusions from the fields and operation descriptions.

| Area | Question / conclusion | Evidence class | Descriptor evidence and boundary |
|---|---|---|---|
| Speech | Spoken-word generation is exposed. | Advertised | `speech-create` describes spoken-word audio, accepts exactly one of a verbatim `script` or AI-worded `prompt`, and optionally adds backing music. |
| Speech | Explicit single-speaker support is specified. | Unknown | The descriptor does not state a supported speaker count. It exposes one optional scalar `voice_id`; that is not proof of a one-speaker limit. |
| Speech | Multiple-speaker support is exposed. | Unknown | No speaker list, speaker count, or multi-voice input is in the `speech-create` schema. Absence from the descriptor does not prove the Suno product cannot support it elsewhere. |
| Speech | Speaker assignment or speaker roles are exposed. | Unknown | There are no speaker IDs, per-segment voice selectors, role labels, or speaker-to-line mappings. |
| Speech | Script segmentation is exposed. | Unknown | `script` is a single string (max 5000 chars); no segments, turns, SSML, or timing fields are advertised. |
| Speech | A specific voice can be selected. | Advertised | Optional `voice_id` selects a ready voice; the descriptor refers signed-in users to `voices-list`. A voice that is unknown or still processing is rejected. |
| Speech | Voice consistency across segments or separate calls is guaranteed. | Unknown | A `voice_id` selector is advertised, but no seed, speaker-continuity, cross-segment, or consistency guarantee is described. |
| Speech | Podcast-specific production workflow is exposed. | Unknown | The tool describes speech with optional backing music, not podcast projects, episodes, tracks, editing, or publishing. |
| Speech | A narration-specific mode is exposed. | Unknown | The tool advertises general spoken-word generation using a script or prompt but no separately named narration mode. Generic use as narration is recorded as an inference below. |
| Voices | Voice records/catalog entries exist. | Advertised | `voices-list` lists the user's own or loved voices and supports paginated lookup. The full voice-entry response schema is not supplied. |
| Voices | Voice IDs exist and can be selected. | Advertised | The descriptor refers to each listed voice's `id`, used as `voice_id` by audio and speech generation tools. |
| Voices | A live voice-list result includes an ID and name. | Observed | One signed-in `voices-list` call returned one entry with `id`, `name`, `description`, `image_url`, `source`, `is_public`, and `is_owned`. Account-specific ID/name/image values are omitted from this repository. |
| Voices | Ownership and public-state indicators are returned. | Observed | That entry had `is_owned: true` and `is_public: false`; one record does not establish all possible combinations or their access rules. |
| Voices | A voice object has a `source` field. | Observed | The sample returned `source: "recording"`. The descriptor does not define this field's full enum or prove a specific training/cloning mechanism. |
| Voices | The observed ID is UUID-shaped. | Observed | The one returned ID has UUID form; the descriptor does not constrain the ID format. |
| Voices | Multiple voice records were returned. | Observed: no | The `own` query returned one entry and `loved` returned none; neither response had a `next_cursor`. This is not a complete inventory of public voices searchable by a known ID. |
| Voices | `source` values vary across records. | Unknown | Only `recording` was observed; no second record/source value was returned. |
| Voices | Ownership values vary across records. | Unknown | Only `is_owned: true` was observed; `loved` returned no entries, so no contrasting ownership value was available. |
| Voices | A voice `type`, lifecycle status, or creation timestamp is exposed. | Unknown | These fields were not present in the observed entry; one response does not establish the complete schema for every voice kind. |
| Voices | Voices are reusable. | Advertised | A ready voice ID can be passed to `speech-create`, `audio-create`, `audio-covers-create`, and `audio-extensions-create`. This does not promise a voice's availability duration. |
| Voices | Own and loved voice collections are available. | Advertised | `voices-list.collection` accepts `own` or `loved`; default is `own`. Name search is scoped to the selected collection. |
| Voices | Voice creation/setup is available. | Advertised | `voices-start` returns a Suno URL where the user creates and verifies a voice. It does not expose a recording upload or training operation through this tool. |
| Voices | User-created/recording-origin voice support exists. | Advertised / Observed | `speech-create` describes selecting one of the user's own voices when the plan includes voice cloning; the one observed list record had `source: "recording"`. Neither establishes how voice creation or training works. |
| Voices | Preset/system-provided speech voices exist. | Advertised | `speech-create` refers to preset voices listed in the Quickstart. This connector does not expose their full catalog or object schema here. |
| Voices | Voice IDs represent artist identities. | Unknown | The schema exposes a voice `name` and opaque `id`, but no artist/profile identity, rights, or attribution fields. A voice selector is not evidence of an artist identity. |
| Voices | Voice training details or controls are exposed. | Unknown | No training examples, dataset controls, model parameters, progress schema, or training operation are advertised. A creation-and-verification URL alone does not establish how training works. |
| Voices | A ready voice appears in the voice list. | Advertised | `voices-start` says a created and verified voice appears in `voices-list` when ready. |
| Voices | Voice retention period, deletion, and lifecycle guarantees are specified. | Unknown | The descriptors provide no retention period or voice deletion operation/lifecycle contract. |
| Voices | A ready voice ID can be reused for later songs and speech clips. | Advertised | The same `voice_id` input is documented on the music and speech creation operations. Availability duration, output fidelity, and cross-call consistency are not guaranteed by the descriptors. |
| Voices | Voice persistence across workspaces/projects is specified. | Unknown | Generation operations can file clips into workspaces, but no voice-to-workspace/project relationship or persistence scope is described. |
| Characters | Character records exist. | Advertised | `characters-list` lists images saved as characters; `characters-save` saves a ready image as a character. |
| Characters | Character identifiers are distinct from image asset IDs. | Unknown | `characters-save` takes the image's `asset_id`, and the list descriptor refers to saved image assets and preset `ref` values. No distinct character-ID schema is documented. |
| Characters | Character persistence is exposed. | Advertised | A saved image appears in `characters-list` and Suno's character picker. How long it persists, and whether it can be deleted through this connector, are unspecified. |
| Characters | Character assets can be reused. | Advertised | The descriptors say saved `asset_id`s and preset `ref` values can be used as Sequence character/set references or video first-frame assets. |
| Integration | Speech can reference a voice. | Advertised | `speech-create.voice_id` selects an optional ready voice. |
| Integration | Speech can reference a character. | Unknown | No character ID, image asset, or character field appears in `speech-create`. |
| Integration | Characters can reference voices. | Unknown | Character descriptors expose image assets/references and name/role guidance for Sequences, not voice IDs or speech settings. |
| Integration | Multi-speaker or dialogue workflows are exposed. | Unknown | No multi-speaker fields, turn/line arrays, dialogue roles, or per-turn voice assignment are advertised. |
| Integration | Generic speech generation may be used for narration. | Inferred | `speech-create` advertises prompt/script spoken-word generation and optional backing music, but has no narration-specific mode, narrator role, or episode workflow. |

### Exposed Objects, Limits, and Follow-up

**Advertised object types:** spoken-word audio clip; voice entries/voice IDs; saved character images; preset character/background references. The speech tool can also accept a `workspace_id` to file its resulting clip. The descriptors do not define a speaker, dialogue-turn, podcast-episode, or distinct character-ID object.

**Limitations and risks:** The return schemas for voices and characters are not fully enumerated as formal schemas. The single observed voice entry is a point-in-time account-specific sample, not the complete schema for all voice types; its ID, name, and image URL are deliberately not copied here. Do not equate one `voice_id` input with a guaranteed single-speaker output, infer multiple speakers from script content, or assume a character can determine a speech voice. No voice-creation, speech-generation, or character operation was invoked. The later music-generation test captured connector metadata; a separate human listening submission is recorded in the [Voice-ID-001 registry](experiments/voice-id-validation-registry.md), but these sources do not establish a causal effect of `voice_id` on the rendered audio.

**Open questions:** Does Suno speech generation support multiple speakers through an undocumented or web-only interface? Are script markup, line-level speaker assignment, or dialogue workflows available outside this connector? What are the exact voice and character response objects and lifecycle/deletion rules? Are voice-consistency settings available beyond selecting a `voice_id`?

### Voice Object Discovery and Music/Speech Comparison

#### Observed voice-list entry

The read-only `voices-list` call using the default `own` collection returned one voice entry. A second call using `collection: loved` returned an empty `voices` array. Neither response included `next_cursor`. Account-specific values are redacted; the field names and non-identifying values below are what the connector returned:

| Field | Observed value/shape | Evidence class | Interpretation and limits |
|---|---|---|---|
| `id` | UUID-shaped value, redacted | Observed | Opaque voice identifier; this one value has UUID form, but the schema does not require that format. Descriptors say to supply it as `voice_id`. |
| `name` | Non-empty account-specific name, redacted | Observed | A display label, not evidence that it is an artist identity. |
| `description` | Empty string | Observed | Description field exists; its semantics and optionality are not fully specified. |
| `image_url` | URL, redacted | Observed | Image associated with the voice record; the descriptor does not say it is the voice/audio itself. |
| `source` | `"recording"` | Observed | Indicates a recording source for this sample; not a documented voice-type enum or training recipe. No other source value was observed, so variability is unknown. |
| `is_public` | `false` | Observed | Public-state indicator for this sample only. |
| `is_owned` | `true` | Observed | Ownership indicator for this sample only. Variability is unknown; the loved collection was empty. |
| `type`, `status`, `created_at`, `updated_at` | Not returned | Observed absent in this entry | The complete schema may vary; lifecycle and retention remain unknown. |

The response wrapper exposed `voices`; `next_cursor` was absent from both observed responses. The observed queries returned one own voice and no loved voices, so they show one accessible record, not multiple records. The descriptor supports searching for a known public voice ID, but the queries did not enumerate public voices. The live record supports the existence of an owned, non-public voice entry with recording provenance; it does not establish whether the voice is cloned, how it was trained, whether source/ownership values vary, or how long it persists.

#### Music voice versus speech voice

| Aspect | Music generation | Speech generation |
|---|---|---|
| Output | Sung music; `audio-create.voice_id` selects a ready voice, which always sings and takes precedence over `instrumental`. | Spoken-word clip; `speech-create.voice_id` selects an optional ready voice. |
| Voice catalog | The `voices-list` descriptor says listed voice IDs can be passed to `audio-create`, covers, extensions, and speech. | The same descriptor says listed voice IDs can be passed to `speech-create`; speech also advertises preset voices listed in the Quickstart. |
| Generation controls | Music tools expose `model` and optional `custom_model_id`; the selected voice can be combined with music style/lyrics and, on `audio-create`, voice-related `audio_influence`. | Speech always uses the default model; there is no `model` parameter. It takes exactly one `script` or `prompt`, with optional delivery `style`, `backing_music`, and `vocal_gender`. |
| Reuse conclusion | **Advertised:** a ready voice ID is an input to subsequent music-generation calls. | **Advertised:** a ready voice ID is an input to speech-generation calls. |
| Model identity conclusion | **Unknown:** the descriptor does not expose voice model internals or promise identical rendering across calls. | **Unknown:** the default speech model is not named, and the descriptors do not establish whether its voice representation/model is identical to music generation. |

**Evidence-bounded conclusions**

- **Verified:** `voices-list` successfully returned a `voices` array with one entry.
- **Observed:** The `own` query returned one entry and the `loved` query returned none. The entry exposes `id`, `name`, `description`, `image_url`, `source`, `is_public`, and `is_owned`; its ID is UUID-shaped, its source was `recording`, it was owned, and it was not public.
- **Unknown:** Whether other records use different `source` values or `is_owned` values. No alternate source or ownership value was observed.
- **Advertised:** `voice_id` is a reusable selector on the music and speech creation schemas. Speech also refers to preset voices; the connector does not expose a complete preset catalog in these descriptors.
- **Inferred:** The connector models a voice as a reusable voice resource/input, rather than as an artist-profile object. The inference follows from the opaque ID, display name, ownership/public flags, and reuse parameters; there is no explicit formal voice object type specification.
- **Unknown:** Whether the recorded voice is a voice clone; how it is trained or verified; whether voice rendering is consistent across songs/calls; the voice resource's retention/deletion lifecycle; and any persistence relationship to workspaces or projects.

#### Voice-ID eligibility and lifecycle constraints

| Operation | `voice_id` constraint advertised | Other voice-specific behavior |
|---|---|---|
| `audio-create` | Optional string; voice must belong to the account and be `ready`. Unknown ID returns 404; processing voice returns 400. For Suno sign-in, use one of the user's Suno voices from `GET /v0/voices`. | Voice always sings and overrides `instrumental`. `controls.audio_influence` is only valid with `voice_id`. |
| `audio-covers-create` | Optional string; voice must belong to the account and be `ready`. Unknown ID returns 404; processing voice returns 400. For Suno sign-in, use one of the user's Suno voices from `GET /v0/voices`. | Supplied voice always sings, even with no lyrics, and keeps vocals in the new cover. |
| `audio-extensions-create` | Optional string; voice must belong to the account and be `ready`. Unknown ID returns 404; processing voice returns 400. For Suno sign-in, use one of the user's Suno voices from `GET /v0/voices`. | Supplying it implies vocals and overrides an instrumental source. |
| `speech-create` | Optional string; the descriptor describes preset voices or, when the plan includes voice cloning, a user's own voice. It also says a voice must belong to the account and be `ready`; for Suno sign-in, use one of the user's Suno voices from `GET /v0/voices`. Unknown ID returns 404; processing voice returns 400. | Spoken-word output; no model selector. Preset and custom-voice authorization details are not fully reconciled by the wording. |

| Question | Finding | Evidence boundary |
|---|---|---|
| Must the voice be owned? | **Advertised for Suno sign-in:** all four descriptors direct users to their own Suno voices, and the shared constraint says the voice must belong to the account. | `speech-create` also mentions preset voices; the descriptors do not fully distinguish ownership rules for presets from cloned/account voices. |
| Can the voice be public? | **Possible to discover, not confirmed usable:** `voices-list.query` can find an owned voice or any public voice the user may sing in. | Generation descriptors say account-owned/one of the user's Suno voices; they do not explicitly confirm that a public, non-owned voice ID is accepted. |
| Can it belong to someone else? | A private voice belonging to another account is **not advertised as usable**. A public voice belonging to another account remains **unknown** because public lookup language and account-ownership constraints are not reconciled. | No non-owned public voice was observed or submitted. |
| Must `source` equal `recording`? | **No such requirement is advertised.** | The four schemas constrain the ID, ownership/authorization, and readiness, but do not mention `source`. The one observed entry had `source: "recording"` only. |
| Is the observed voice eligible? | **Advertised candidate for all four operations:** it was returned from the `own` collection and had `is_owned: true`, matching the account-ownership wording. | Its object has no `status`/`ready` field. `voices-start` says ready voices appear in `voices-list`, but no generation was attempted; runtime acceptance and readiness are not verified. |

#### Voice object details, lifecycle, and usage references

The current 60-operation MCP inventory exposes only `voices-list` and `voices-start` as voice-specific operations. `voices-start` opens an external creation/verification workflow; it does not return a voice record or verification/readiness status. No dedicated voice-details, voice-retrieve, voice-status, voice-metadata, readiness-check, or verification-status operation is advertised.

| Requested detail | Evidence from the observed object/descriptors | Finding |
|---|---|---|
| Creation timestamp | No `created_at` field in the voice entry. | **Unknown / not exposed in sample.** |
| Readiness | No `ready`, `status`, or processing field in the entry. `voices-start` says a voice appears in the list once ready. | **Advertised indirectly; not directly observable.** Presence in the list suggests readiness but does not prove a status value. |
| Verification status | No verification field or verification-status operation. `voices-start` sends the user to an external create/verify flow. | **Unknown after setup.** |
| Source details | `source: "recording"` only. No recording ID, file reference, URL, duration, or provenance detail. | **Observed value; details unknown.** |
| Ownership/public state | `is_owned: true`, `is_public: false`. | **Observed for this entry.** No update/control operation was exposed for changing these values. |
| Voice usage references | No song, speech clip, cover, extension, or usage-history IDs on the voice entry. | **Not exposed in the object.** |
| Training metadata | No training source data, examples, parameters, progress, or model fields. | **Not exposed in the object.** |
| Processing state | No processing/status field. | **Not exposed in the object.** |
| Model association | No model/custom-model association on the voice. `custom_model_id` is a separate generation input. | **Not exposed; no voice-to-model relation established.** |

| Correlation target | What the connector proves | What remains unknown |
|---|---|---|
| Speech generation | `speech-create` accepts `voice_id`; `voices-list` IDs are documented as selectable. | No speech clip was generated/retrieved with this ID; no usage reference links a speech clip to the voice. |
| Music generation | `audio-create` accepts `voice_id`; a voice always sings and takes precedence over instrumental mode. | An approved four-clip control/treatment test used this voice ID. `audio-wait` metadata exposed `voice_id` for both treatment outputs and not for controls; `library-list` omitted it for all four. Christopher's original statement, “The output is obvious,” is preserved separately from a later structured submission recorded in the [Voice-ID-001 registry](experiments/voice-id-validation-registry.md) and [detailed experiment record](experiments/voice-influence-test-2026-11-24.md). The original sentence alone does not identify clips or properties, and the metadata plus human report do not establish that `voice_id` caused the perceived change. Kio, Nebraska, ordinary-song, and 22 `Try, Try Again` samples expose no voice ID; vocal wording in `metadata.style` remains prompt text, not proof of voice selection. |
| Covers | `audio-covers-create` accepts `voice_id` for a new cover. | No cover was generated with this ID; no cover/voice usage relation is present on the voice object. |
| Extensions | `audio-extensions-create` accepts `voice_id` for a continuation. | No extension was generated with this ID; no extension/voice usage relation is present on the voice object. |

For the four test outputs, the treatment `voice_id` can be correlated with the `audio-wait` response metadata; the voice object itself still exposes no usage references. This establishes request/response metadata association, not audible influence or voice identity in the rendered audio. The existing song samples above remain without a voice ID or voice-object link.

## Audio Generation Voice-Field Audit

**Evidence:** The advertised MCP parameter schemas and descriptions for `audio-create`, `audio-edit`, `audio-extensions-create`, and `audio-covers-create` were inspected. No operation was invoked; all four remain **EXPOSED-NOT-TESTED** as operations. Presence below refers only to the exact field names in these four descriptors.

| Exact field name | `audio-create` | `audio-edit` | `audio-extensions-create` | `audio-covers-create` | Finding |
|---|---|---|---|---|---|
| `seed` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |
| `random_seed` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |
| `singer` | Absent | Absent | Absent | Absent | Not advertised as a parameter. |
| `vocalist` | Absent | Absent | Absent | Absent | Not advertised as a parameter. |
| `voice_id` | Present, optional | Absent | Present, optional | Present, optional | The only requested voice-selection field; descriptor-specific behavior below. |
| `persona_id` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |
| `character_id` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |
| `model_voice` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |
| `reuse_voice` | Absent | Absent | Absent | Absent | Not advertised in these schemas. |

### Advertised `voice_id` Semantics

| Operation | Descriptor statement |
|---|---|
| `audio-create` | Optional voice ID for generation. The voice must belong to the account and be ready; signed-in Suno users select from Suno voices. A supplied voice always sings and takes precedence over `instrumental`. |
| `audio-edit` | No `voice_id` field. The operation changes title, lyrics, caption, or any combination; it does not advertise audio-generation or voice-selection parameters. |
| `audio-extensions-create` | Optional voice ID for singing the continuation. Supplying it implies vocals and overrides an instrumental source; the voice must belong to the account and be ready. |
| `audio-covers-create` | Optional voice ID. A supplied voice always sings, even with no lyrics, and keeps vocals in the cover; the voice must belong to the account and be ready. |

`audio-create` also advertises `vocal_gender` (`male` or `female`), but this is a gender setting, not a singer/persona/character identifier. Its `model` and `custom_model_id` parameters select generation models; neither is described as a voice identity. The absence of the requested fields is bounded to these four MCP descriptors and does not establish what Suno may support through other interfaces.

### Cover and Voice Relationship Investigation

**Evidence:** The advertised `audio-covers-create` descriptor was inspected read-only. The operation was not invoked; no cover was generated.

#### Explicit descriptor claims

| Topic | What the descriptor explicitly says | Evidence boundary |
|---|---|---|
| Cover operation | Creates a **new audio clip** by covering an existing clip with a new style or voice. | A source `id` is required; the source must have status `complete`, or the request returns HTTP 400. |
| Eligible source | A signed-in Suno user may use a Suno song they are allowed to remix. | Descriptor documents 404 if the user cannot see it, 403 if they cannot remix it, and 503 while the source is still finishing. |
| Source lyrics | The source's lyrics are **not carried over**. The descriptor says to pass the source lyrics to keep its vocals. | This is an explicit lyric-handling statement; it does not promise melody or arrangement preservation. |
| Omitted lyrics | Without `lyrics`, the cover is instrumental unless `voice_id` is set. | The descriptor does not say what words, if any, are sung when `voice_id` is supplied without lyrics. |
| `voice_id` | Optional ID of a voice to use. It must be an account voice and be `ready`; an unknown voice returns 404 and a still-processing voice returns 400. For a signed-in Suno user, it is one of their Suno voices from `GET /v0/voices`. | A supplied voice always sings, even with no lyrics, and keeps vocals in the cover. |
| Audio resemblance | `controls.audio_influence` ranges 0-1: low reinterprets freely; high stays near the source. | This describes overall source-audio resemblance, not a specific melody, arrangement, or vocal-isolation guarantee. |
| Style controls | `style` supplies new style/genre tags; `controls.style_influence` controls how strongly they are followed. `negative_style` specifies styles to avoid and requires advanced-controls access. | The descriptor doesn't promise which musical features remain invariant while style changes. |
| Other controls | `variety` is an integer 0-4 for reinterpretation of style tags; `weirdness` is 0-1 for how far the result may drift from expected results. Advanced controls require the relevant plan grant. | These are generation controls, not preservation guarantees. |
| Duration | Optional target duration is an integer from 15 to 360 seconds. | It is a target, not a guaranteed exact duration. |
| Title | The cover takes the source title unless `title` is supplied. | A title default does not establish source/parent metadata on the generated result. |

#### Answers to preservation and replacement questions

| Question | Descriptor-grounded answer |
|---|---|
| Does it promise to preserve the melody? | **No explicit claim.** `audio_influence` can keep the result closer to the source overall, but the descriptor does not guarantee melody retention. |
| Does it preserve lyrics automatically? | **No.** Source lyrics are expressly not carried over; the descriptor instructs the caller to supply them to keep the source's lyrics/vocals. |
| Does it promise to preserve arrangement? | **No explicit claim.** Audio resemblance controls are described, but no arrangement-preservation behavior is specified. |
| Does it replace the vocalist? | **Not explicitly as a replacement operation.** It says a new cover can use a new voice and that a supplied voice always sings. It does not promise removal/isolation of the original vocalist or describe an in-place vocalist swap. |
| Can `voice_id` be applied to an existing song? | **Yes, as input to a new cover generation.** The required source `id` identifies the existing clip and optional `voice_id` selects the voice for the generated cover. The descriptor says this creates a new clip, not that it edits the source clip in place. |

The complete typed parameter table for `audio-covers-create` appears in “Full music-generation parameter schemas.” No inference about exact melody, arrangement, source-vocal removal, or output lineage should be promoted to a descriptor fact.

### Nested Parameter Shapes

The parameter tables list every top-level parameter. The following nested fields are also present in the advertised schemas:

| Parameter | Nested fields and constraints |
|---|---|
| `controls` on audio generation tools | `audio_influence`, `style_influence`, and `weirdness` are numbers from 0 to 1; `variety` is an integer from 0 to 4. |
| `reference_audio_ids` on `audio-create` | Up to 10 unique song IDs. |
| `file` on `audio-upload-create`, `midi-upload-create`, and `visuals-upload-create` | Attachment reference with `download_url` and `file_id`; optional `file_name` and `mime_type`. |
| `characters` / `sets` on `sequence-create` and `sequence-update` | Entries have a required `name`; `asset_ids` has 1-3 references when required for a non-delete entry; optional `description` (up to 500 chars) or `delete`. |
| `shots` on `sequence-create` | Each has required `duration_s` (greater than 0 and at most 15); optional `characters`, `notes` (up to 1000 chars), and `set`. The array schema permits up to 200 shots. |
| `shots` on `sequence-generate` | Each has required `shot_id` and `prompt`; optional `continues_shot_id`, `first_frame_asset_id`, `last_frame_asset_id`, `leads_into_shot_id`, and `lip_sync`. Up to 8 per call. |
| `shots` on `sequence-update` | Each has required `shot_id`; optional `asset_id`, `characters`, `notes`, and `set`. |
| `ops` on `sequence-update` | Each has required `action` (`move`, `delete`, `trim`, `split`, or `add`); optional `after_shot_id`, `asset_id`, `at_s`, `duration_s`, `notes`, `shot_id`, `trim_start_s`, and `trim_end_s`. Up to 49 operations. |
| `clips` on `video-assemble` | Each has required `asset_id`; optional `duration_s`, `trim_start_s`, and `trim_end_s`. Up to 40 clips. |

## Capability Questions

“Unknown” means no corresponding tool is present in the complete 60-operation inventory. A related feature may still exist in Suno's website or an API outside this connector.

| Requested capability | Finding | Evidence/status |
|---|---|---|
| List songs | Exposed; successfully paged/read in prior discovery. | VERIFIED (`library-list`) |
| Retrieve song | Exposed; several songs retrieved in prior discovery. | VERIFIED (`audio-retrieve`) |
| Retrieve audio file | Exposed as a song download; download was not exercised in this task. | EXPOSED-NOT-TESTED (`audio-download`) |
| Create song | Exposed as paid/credit-spending generation; not executed here. | EXPOSED-NOT-TESTED (`audio-create`) |
| Extend song | Exposed as continuation generation; not executed here. | EXPOSED-NOT-TESTED (`audio-extensions-create`, `audio-full-song`) |
| Replace section | No dedicated replace-section tool. `audio-create` describes reference-based edits, including changing time ranges or sections; this is not evidence that a specific Replace artifact type or relationship exists. | No dedicated operation; related generation is EXPOSED-NOT-TESTED |
| Remaster song | No dedicated remaster operation; the `audio-create` descriptor says reference-based generation can remaster. `library-list` can filter `origin=remaster`. | Related feature exposed; creation untested |
| Delete song | No delete-song operation in the inventory. | UNKNOWN |
| Archive song | No archive-song operation in the inventory. | UNKNOWN |
| List workspaces | Exposed and successfully read in prior discovery. | VERIFIED (`workspaces-list`) |
| Create workspace | Exposed and successfully used to create Kio in prior work. | VERIFIED (`workspaces-create`) |
| Rename workspace | No rename operation; only create/list and song membership update are exposed. | UNKNOWN |
| Delete workspace | No delete-workspace operation. | UNKNOWN |
| Move song | No standalone move operation. `workspaces-update-clips` adds to one workspace and moves a song out of its prior workspace. An approved cleanup moved 238 clips from N-Learning to Nebraska; all requested IDs were added without skips and verified in the destination listing. | VERIFIED |
| Multi-workspace assignment | Connector contract says a song can be in at most one workspace. | Not supported by the exposed contract |
| List playlists | Exposed and successfully read in prior discovery. | VERIFIED (`playlists-list`) |
| Create playlist | Exposed; not tested. | EXPOSED-NOT-TESTED (`playlists-create`) |
| Add/remove playlist songs | Exposed; not tested. | EXPOSED-NOT-TESTED (`playlists-add-clips`, `playlists-remove-clips`) |
| Delete playlist | No delete-playlist operation. | UNKNOWN |
| Tags, labels, categories, custom metadata | No dedicated operations or such fields were found in the inspected object sample; no corresponding tool appears in the complete inventory. | UNKNOWN |
| Search | Song title/style search and playlist/workspace name filters are exposed. General metadata or arbitrary-field search is not. | EXPOSED-NOT-TESTED (`library-search`; list filters) |

## Capability Status Evidence

Prior repository discovery records successful read and write results for these operations:

- `library-list`: paginated completed-song library retrieval; a request with a malformed manually supplied cursor failed with an invalid-cursor error. Later page requests succeeded. The failure is input-specific and does not mean listing is unsupported.
- `audio-retrieve`: five sample song-shaped records were retrieved.
- `workspaces-list`: workspaces were listed, including Kio.
- `workspaces-create`: Kio was created; its returned ID, name, description, and clip count were recorded.
- `workspaces-update-clips`: two Showtime songs were reported added and verified in a workspace-filtered library listing.
- An approved workspace cleanup created Nebraska and EXP-Voice-ID-Validation, moved 238 clips from N-Learning to Nebraska in five batches, and assigned four unfiled voice-test clips to EXP. All update responses had empty `skipped` and `removed` lists; filtered membership verified the 238/4 destination sets and the eight clips remaining in N-Learning. A post-move global library refresh matched all 438 inventory IDs with no missing or new IDs.
- `playlists-list` and `playlists-list-clips`: playlist records and contents were read and matched by song ID.
- `voices-list`: read-only requests for `own`, `loved`, and the observed ID returned one own voice, no loved voices, and the same voice entry; its personal ID, name, and image URL are redacted in repository documentation.

All other operations in the matrix are **EXPOSED-NOT-TESTED**, except where their status is otherwise recorded above. No generation operation was executed for this capability inventory; the later voice-influence experiment is documented separately. The `library-list` cursor failure is recorded as **TESTED-FAILED** for that malformed request only; the capability itself is also **VERIFIED** by successful page reads.

## Additional Object Types

Beyond songs, workspaces, playlists, projects, and Replace-titled records, the connector advertises operations involving:

- **Sequences**: named music-video timelines, shots, style, characters, sets, and renders.
- **Visual assets**: generated/uploaded images and videos, frames, takes, and renders.
- **Characters and sets**: named Sequence reference groups that use image asset IDs.
- **Voices**: custom/loved voice records used as generation inputs.
- **Custom models**: own/shared generation model records.
- **MIDI uploads and transcriptions**: uploaded score IDs and generated MIDI files.
- **Stems**: stem groups and their resulting audio clip IDs.
- **Speech clips**: spoken-word audio generated through `speech-create`.
- **Sound effects/loops**: short clips generated by `sounds-create`.
- **Analysis and alignment jobs**: asynchronous results associated with audio IDs.
- **Upload sessions and render jobs**: intermediate processing objects returned by audio/visual upload and rendering flows.

These are connector-level resource concepts inferred from tool descriptions and response fields. Their complete Suno-side object schemas and lifecycle guarantees have not been independently established. The five sampled song records previously called Replace-titled or Untitled Project-titled were still song-shaped `audio-retrieve` responses; no dedicated Replace-artifact or Project API type was exposed in the inventory.

## Known Limitations and Open Questions

- The inventory is the 60 tools advertised to this session on 2026-11-24. Tools, schemas, account permissions, and plan gates can change.
- Tool descriptors are not a complete formal API specification. Where a descriptor does not enumerate response fields, the response schema is marked as unspecified rather than inferred.
- Exposed does not mean the signed-in account is authorized or that an operation will succeed; several tools require specific token scopes, plan features, or credits.
- Creation, editing, privacy, upload, playlist-membership, workspace-membership, and Sequence-update operations can change account state. They were not invoked merely to validate exposure.
- The connector exposes `audio-edit` for song title, lyrics, and caption, and `audio-settings` for visibility/remix permission. Neither offers archive/delete semantics.
- There is no dedicated Replace-section operation, and no exposed delete/archive song, delete playlist/workspace, workspace rename, tagging, labels, categories, or custom metadata operation.
- Whether a Replace-titled item is a song, edit artifact, or child of another song remains unresolved; its title alone does not establish object type or lineage. See [Suno Object Model Discovery](suno-object-model-discovery.md).
- Whether the Suno website exposes capabilities not present in this connector remains outside this inventory.

## Evidence References

- Connector tool registry and individual parameter descriptions returned by MCP tool search during this discovery.
- [Suno Object Model Discovery](suno-object-model-discovery.md) for prior sampled song records, workspace/playlist observations, and verified connector actions.
- [Song and Workspace Metadata Discovery](experiments/suno-song-metadata-discovery-2026-11-24.md) for the read-only sample snapshot and classification cautions.
- [EXP-Voice-ID-Validation Registry](experiments/voice-id-validation-registry.md) and [Voice-ID-001 results](experiments/voice-influence-test-2026-11-24.md) for the approved music-generation metadata test and its untested audible outcome.
