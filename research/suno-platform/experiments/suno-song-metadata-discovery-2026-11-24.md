# Suno Song and Workspace Metadata Discovery

**Captured:** 2026-11-24
**Status:** Observational API snapshot; not a Suno schema specification
**Evidence source:** Signed-in Suno MCP `audio-retrieve`, `library-list`, `workspaces-list`, and tool descriptions
**Scope:** Two unfiled songs titled “Showtime in the City,” one “Replace” item, and one “Untitled Project” item

## Purpose and Limitations

This report records the fields returned for four user-owned Suno clips and what the exposed MCP operations establish about workspace membership and lineage. The records were retrieved read-only. No song, workspace, visibility, or catalog data was changed.

The captured song objects were all present in the library but absent from the returned membership lists for all seven workspaces. That membership comparison is the basis for recording their workspace as unassigned; `audio-retrieve` itself does not return a `workspace_id` or workspace name.

This is a point-in-time API observation. An absent field means it was not returned for these objects, not proof that Suno stores no such information internally.

## Object Snapshots

All four `audio-retrieve` responses included these top-level fields:

| Field | Value |
|---|---|
| `error` | `null` |
| `handle` | `cjbower` |
| `like_count` | `0` |
| `liked` | `false` |
| `comment_count` | `0` |
| `status` | `complete` |
| `visibility` | `private` |

Each also returned `id`, `title`, `created_at`, `song_url`, `play_count`, `cover_image_url`, `cover_image_large_url`, and a `metadata` object. The object-specific values follow.

### Showtime in the City — clip 1

| Field | Returned value |
|---|---|
| `id` | `1e69b69c-4e05-457e-887f-19ffe1982577` |
| `title` | `Showtime in the City` |
| `song_url` | https://suno.com/song/1e69b69c-4e05-457e-887f-19ffe1982577 |
| `created_at` | `2026-11-24T02:19:25.158Z` |
| `play_count` | `10` |
| `cover_image_url` | https://cdn1.suno.ai/image_1e69b69c-4e05-457e-887f-19ffe1982577.jpeg |
| `cover_image_large_url` | https://cdn1.suno.ai/image_large_1e69b69c-4e05-457e-887f-19ffe1982577.jpeg |
| `metadata.description` | `null` |
| `metadata.duration` | `187.56` seconds |
| `metadata.model` | `v6-mini` |
| `metadata.style` | `80s west coast rap style` |
| `metadata.type` | `generate` |
| `metadata.lyrics` | Present; text below |

### Showtime in the City — clip 2

| Field | Returned value |
|---|---|
| `id` | `aebb54a6-b11c-484c-8f4a-7a2228aa966c` |
| `title` | `Showtime in the City` |
| `song_url` | https://suno.com/song/aebb54a6-b11c-484c-8f4a-7a2228aa966c |
| `created_at` | `2026-11-24T02:19:25.158Z` |
| `play_count` | `7` |
| `cover_image_url` | https://cdn1.suno.ai/image_aebb54a6-b11c-484c-8f4a-7a2228aa966c.jpeg |
| `cover_image_large_url` | https://cdn1.suno.ai/image_large_aebb54a6-b11c-484c-8f4a-7a2228aa966c.jpeg |
| `metadata.description` | `null` |
| `metadata.duration` | `181.6` seconds |
| `metadata.model` | `v6-mini` |
| `metadata.style` | `80s west coast rap style` |
| `metadata.type` | `generate` |
| `metadata.lyrics` | Present and identical to clip 1; see the shared text below |

### Replace 03:26-03:30 (11:19 PM Nov 21)

| Field | Returned value |
|---|---|
| `id` | `ea8d8ea5-e574-4480-9b79-f67a42ee585c` |
| `title` | `Replace 03:26-03:30 (11:19 PM Nov 21)` |
| `song_url` | https://suno.com/song/ea8d8ea5-e574-4480-9b79-f67a42ee585c |
| `created_at` | `2026-11-22T07:21:23.588Z` |
| `play_count` | `0` |
| `cover_image_url` | https://cdn1.suno.ai/image_ea8d8ea5-e574-4480-9b79-f67a42ee585c.jpeg |
| `cover_image_large_url` | https://cdn1.suno.ai/image_large_ea8d8ea5-e574-4480-9b79-f67a42ee585c.jpeg |
| `metadata.description` | `null` |
| `metadata.duration` | `34.04` seconds |
| `metadata.model` | `v6` |
| `metadata.style` | `Modern Heartland Rock, Celtic Rock, Pub Anthem, College Rally Song, Nebraska Pride Anthem, Male Lead Vocal, Crowd Gang Vocals, Stadium Chant Intro, Driving Drums, Electric Guitar, Fiddle, Mandolin, Big Singalong Chorus, Emotional Reflection Verse, Powerful Outro, Anthemic, Energetic, Triumphant` |
| `metadata.type` | `generate` |
| `metadata.lyrics` | Present; exact returned excerpt below |

### Untitled Project [01:00 - 02:30]

| Field | Returned value |
|---|---|
| `id` | `9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b` |
| `title` | `Untitled Project [01:00 - 02:30]` |
| `song_url` | https://suno.com/song/9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b |
| `created_at` | `2026-11-18T06:28:08.061Z` |
| `play_count` | `0` |
| `cover_image_url` | https://cdn1.suno.ai/image_9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b.jpeg |
| `cover_image_large_url` | https://cdn1.suno.ai/image_large_9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b.jpeg |
| `metadata.description` | `null` |
| `metadata.duration` | `90` seconds |
| `metadata.model` | Not returned |
| `metadata.style` | `Dark Electronic Hip-Hop` |
| `metadata.type` | `generate` |
| `metadata.lyrics` | Present; text below |

## Fields Not Returned for These Objects

| Requested field or relationship | Finding |
|---|---|
| Updated date | No `updated_at` field was returned. |
| Workspace ID/name | No workspace fields were returned on the song objects. Comparing their IDs with all seven workspace song listings found no membership; all four were unassigned at capture time. |
| Parent song ID / source song ID | No `parent_song_id` or `source_song_id` field was returned. |
| Edit / Replace relationship | No edit or Replace operation/relationship field was returned. |
| Project relationship | No project ID or project name was returned. |
| Source-reference fields | These objects did not return `cover_audio_id`, `extend_audio_id`, `mashup_clip_ids`, or `reference_audio_ids`. |
| Separate prompt field | No `prompt` field was returned. `metadata.description` was `null`; `metadata.style` held the visible style prompt. |
| Hidden / archived / deleted state | No such state fields were returned. |

Suno's retrieve operation can expose source fields such as `cover_audio_id`, `extend_audio_id`, `mashup_clip_ids`, or `reference_audio_ids` for other objects. Their absence here means no source relationship is exposed in these snapshots; it does not prove that no internal relationship exists.

## Lyrics Returned

The two “Showtime in the City” objects returned identical lyrics:

```text
[Showtime in the City]

[Verse 1]
Black and red, got the gym alive,
Fast-break thunder, watch the whole crowd rise.
Lights in the school, pride on the floor,
Griffin Middle heartbeat when the Grizzlies score.

Grizzlies with the vision, see the pass before it's made,
Running through defenders like they're standing in the shade.
Big-game energy, spotlight glow,
Everybody in the building knows it's Showtime, go!

[Pre-Chorus]
The crowd gets loud, hear the sneakers sing,
Every fast break feels like a championship ring.
From the hallways to the top of the charts,
Black and red got the school by the heart.

[Chorus]
Showtime, Showtime, light it up tonight,
Black and red shining bright under the gymnasium lights.
Showtime, Showtime, hear the people say,
The Grizzlies got the rhythm and they're running away.
[
Verse 2]
No-look pass, whole arena shakes,
One more bucket and the pressure breaks.
Students and families in the front-row seats,
But the loudest sound is victory's beat.

Clock winding down, crowd on their feet,
Defense locked in, can't handle the heat.
Banners in the rafters, spirit in the air,
Everybody knows there's history there.

[Bridge] [Spoken Announcer Style]
"This game's in the refrigerator.
The door's closed, the light's out, the eggs are cooling,
the butter's getting hard, and the Jell-O's jiggling."

[Rap Breakdown]
That's the signal, that's the call,
Means the black and red conquered all.
Grizzlies swagger, eighties style,
Got the whole league chasing mile after mile.

From the tip to the finish, from the paint to the break,
Every move electric, every highlight great.
School of champions, hear the crowd roar,
When the Grizzlies are rolling, everybody wants more.

[Final Chorus]
Showtime, Showtime, light it up tonight,
Black and red shining bright under the gymnasium lights.
Showtime, Showtime, hear the people say,
The Grizzlies got the rhythm and they're running away.

[Outro]
Griffin nights and the dreams never fade,
Legends live forever in the plays they made.
Black and red till the final light's low,
Grizzlies forever, let the whole world know.
```

The Replace object's lyrics field was returned as:

```text
we leave in others is the part that's here to stay

[Final Chorus]
Raise the scarlet, raise the cream
Let the whole world hear the dream
Greatest fans all of football, standing hand in hand
Still together across the land
Across the prairie, through the years
Through victories and through tears
From Lincoln town we'll always sing
Nebras
```

The Untitled Project lyrics field was returned as:

```text
 the banner of Britain,
And whispering to the trees
Of the swift gliding boats on the waters
That are nearing the fog-shrouded land,
With the old Green Mountain Lion,
And his daring patriot band.

[Verse]
[Pre-Chorus]
Flushed with pride, the whole eastern heavens
With crimson and gold are ablaze[Chorus]
[Verse]
But the sentinel at the postern
Heard not the whisper low;
He is dreaming of the banks of the Shannon
As he walks on his beat to and fro,
Of the starry eyes in Green Erin
That were dim when he marched away,
And a tear down his bronzed cheek courses,
’T is the first for many a day.
```

Line wrapping and trailing whitespace are normalized for Markdown; the text values otherwise reflect the returned fields.

## Findings

### Are Replace items songs or edit artifacts?

The selected Replace item is returned as a completed audio object with its own clip ID, `song_url`, duration, and `metadata.type: generate`. In the exposed response it is a song/clip record, not a separately typed edit-artifact record. Its title and 34.04-second duration are consistent with a segment replacement, but they do not prove which Suno operation created it.

### Is there a parent-child relationship?

No parent, source, edit, or Replace relationship was returned for the selected item. The response provides no basis to assert that the Replace item is linked to a parent song, nor to assert that no such relation exists internally.

### Can Replace items be assigned to workspaces?

The exposed `workspaces-update-clips` operation accepts song IDs to add to or remove from a workspace; adding moves a song from its prior workspace, and the tool can report skipped IDs. Generation can also accept a `workspace_id`. The selected Replace item was not moved as part of this read-only investigation, so its individual eligibility is not confirmed. No workspace change was made.

### Can they be hidden, archived, or deleted independently?

- `audio-settings` exposes per-song `visibility: private|public`; setting `private` unpublishes a song. This is a public-visibility control, not evidence that the song is hidden from its owner's library.
- Workspace membership can be changed independently through `workspaces-update-clips`; removing a clip from a workspace is not deletion from the library.
- No archive or delete operation was exposed by the MCP tools examined. The available metadata does not establish whether Suno's website offers additional hide, archive, or delete controls.

### Are fields suitable for catalog management?

Useful observed or conditionally available fields include:

- Stable external clip ID, title, URL, and source creation timestamp.
- Duration, status, visibility, model, style prompt, and lyrics.
- Workspace membership, joined from a workspace listing rather than embedded in these song objects.
- Source/lineage IDs when returned (`cover_audio_id`, `extend_audio_id`, `mashup_clip_ids`, `reference_audio_ids`).
- Play, like, and comment counts as time-sensitive observations, not durable identity or editorial classifications.

`updated_at`, a separate prompt value, project relationship, and explicit edit/Replace lineage were not available in these snapshots. The existing [song registry schema](../../../catalog/metadata/songs.yaml) has generic title, status, source-material, duration, and creation fields, but does not currently define provider IDs, provider prompts/models, workspace membership, or source-clip lineage. This report recommends evaluating those as optional catalog fields; it does not change the schema or register these Suno clips.

## Provenance and Reproduction Notes

- Four songs were retrieved individually by clip ID through `audio-retrieve`.
- Workspace absence was checked against all seven returned workspaces using workspace-filtered library listings.
- Tool operations were read-only during this capture. No edit, visibility change, workspace assignment, archive, or deletion was attempted.
- Recheck fields against Suno before using them for release, rights, or catalog decisions; this is a snapshot of the exposed MCP interface, not a guarantee of Suno's complete internal data model.
