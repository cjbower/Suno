# Suno Workspace Assignment Queue

**Captured:** 2026-11-24
**Status:** Full inventory completed; approved Nebraska and EXP workspaces created; 242 song records assigned and verified
**Evidence basis:** 438 unique `library-list` records and workspace-filtered membership listings captured on 2026-11-24. No song content was edited or deleted. See the [per-song inventory](suno-song-workspace-inventory-2026-11-24.csv) for the complete field snapshot.

## Earlier Kio Assignment Snapshot

The earlier same-day Kio assignment snapshot returned **434 unique finished-library objects**. The seven pre-existing workspace counts summed to 401; after creating Kio and assigning the two songs below, 403 records were assigned and 31 remained unassigned. This historical snapshot is superseded by the full inventory and cleanup record that follows.

| Workspace | Clips after the Kio assignment |
|---|---:|
| Patriotism-1776 | 61 |
| N-Learning | 246 |
| Virtues-Learning | 24 |
| Faith | 54 |
| Challenge-Picture | 4 |
| First-Mango | 8 |
| First-Disco | 4 |
| Kio | 2 |
| **Total assigned** | **403** |

At that earlier snapshot, the 31 unassigned records were 30 Replace-titled records and one Untitled Project-titled record. The later 438-record refresh and final state are documented below.

## Full Inventory and Approved Cleanup

The user approved creation of both missing workspaces, reassignment of the Nebraska cohort, and assignment of the four voice-test clips. No ambiguous or excluded records were moved.

The refreshed library contained **438 unique records**, all `status: complete`, `visibility: private`, and `metadata.type: generate`. Models observed were `v6` (151), `v6-mini` (275), `v6-wild` (8), and model absent (4). Style was present on 434 records. `library-list` did not expose a workspace ID or voice ID; workspace membership was joined from workspace-filtered listings. The CSV preserves every returned record's ID, title, URL, creation date, status, workspace, model, type, duration, style, visibility, voice-field evidence, and task-level classification.

### Workspace counts before and after

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
| **Total workspace assignments** | **403** | **407** |

`Virtues-Learning` exists under that hyphenated name; it was preserved rather than renamed. `Nebraska` and `EXP-Voice-ID-Validation` were created with empty descriptions. Their workspace IDs are `49763997-c197-4172-bff3-9175b4d5616c` and `9f39af6d-d8b4-43d9-b35d-d9fdf90b1a8e`, respectively.

### Approved assignments

| Source | Destination | Records | Classification evidence |
|---|---|---:|---|
| N-Learning | Nebraska | 238 | 204 `Scarlet and Cream`, 22 `Nebraska's Good Life`, 10 `Scarlet Cream Saturday`, and 2 `Scarlet Cream Saturday (Remastered)` |
| Unassigned | EXP-Voice-ID-Validation | 4 | The four `Prairie Light - Nebraska Voice Test` control/treatment clips |

The 238 Nebraska clips were added in five batches (50, 50, 50, 50, and 38). Each update returned every requested ID under `added`, with empty `skipped` and `removed` lists. The four experiment clips were added in one call with the same result. Workspace-filtered listings then returned exactly the approved 238 Nebraska IDs, all four experiment IDs, and eight remaining N-Learning records. A post-move, paginated global `library-list` refresh returned 438 unique IDs, matching the inventory exactly with no missing or new IDs. No song was deleted or lost. Workspace assignment is exclusive in the exposed connector contract.

### Ambiguous records retained

These records were left in their existing workspaces because title/style metadata alone did not establish topic or intent. They are reported for later review, not silently classified or moved.

| Current workspace | Records | Reason and recommendation |
|---|---:|---|
| N-Learning | 2 `Under City Lights` | Style is generic; retain in N-Learning pending context. |
| N-Learning | 4 `Maize and Blue` | Title may indicate Michigan, while two style fields contain unrelated city-light lyrics and the others are generic; consider a Michigan workspace only if the intended topic is confirmed. |
| Virtues-Learning | 2 `Dare to Die` | Style describes production, not topic; retain pending context. |
| First-Mango | 4 `The guy`; 4 `The girl` | Vocal-character descriptors vary, but no voice ID is exposed in the listing; move to EXP only if confirmed as voice-comparison tests. |
| Patriotism-1776 | 2 `Midnight Velocity` | Dark electronic hip-hop style does not establish a patriotic topic; retain pending context. |
| Faith | 1 `Happy Sun Jealous Moon` | Soul-jazz style and title do not establish a faith topic; retain pending context. |

The two `Scarlet Cream Saturday (Edit)` records in N-Learning and the `Carillon (Edit)` record in Patriotism-1776 were also left untouched under the edit-artifact exclusion. The other existing workspaces were preserved.

### Inventory and experiment records

- [Per-song inventory CSV](suno-song-workspace-inventory-2026-11-24.csv)
- [Voice influence experiment record](../research/suno-platform/experiments/voice-influence-test-2026-11-24.md)

The four experiment clips were generated in a separately approved test before the v6-mini cost-control instruction. Their audio was not downloaded or auditioned; the test establishes parameter/metadata behavior, not an audible voice effect.

## Song Assignment Completed

The user clarified that both songs belong to the Kio project. A read-only workspace-name search returned no Kio workspace, so a dedicated workspace was created and both song IDs were filed there.

| Title | Suno ID | URL | Classification | Workspace | Status |
|---|---|---|---|---|---|
| Showtime in the City | `1e69b69c-4e05-457e-887f-19ffe1982577` | [Open in Suno](https://suno.com/song/1e69b69c-4e05-457e-887f-19ffe1982577) | Song | Kio | Assigned |
| Showtime in the City | `aebb54a6-b11c-484c-8f4a-7a2228aa966c` | [Open in Suno](https://suno.com/song/aebb54a6-b11c-484c-8f4a-7a2228aa966c) | Song | Kio | Assigned |

**Kio workspace ID:** `79a47b93-9ba1-4efb-95e0-a060676ae5c9`

## Workspace Creation Support and Connector Evidence

Workspace creation is supported by the exposed Suno MCP connector:

- The `workspaces-create` operation accepts a required `name` and optional `description`.
- With `name: Kio` and no description, it returned `id: 79a47b93-9ba1-4efb-95e0-a060676ae5c9`, `name: Kio`, `description: ""`, and `clip_count: 0`.
- The `workspaces-update-clips` operation accepts a workspace ID and song IDs to add. It returned both requested IDs under `added`, with `skipped: []` and `removed: []`.
- Verification with `workspaces-list` returned the Kio workspace with `clip_count: 2`. A workspace-filtered `library-list` returned both “Showtime in the City” IDs.

The workspace metadata exposed by the connector is **ID, name, description, and clip count**. The responses did not expose workspace creation/update timestamps, owner fields, or project relationships.

## Currently Unassigned Excluded Records

These 31 records remain unassigned and were excluded from reassignment: 30 Replace-titled records and one Untitled Project-titled record. Their IDs and metadata are included in the per-song inventory. No Replace-titled record or Untitled Project record was changed.

### Replace artifacts — 30

| Existing title | IDs |
|---|---|
| `Replace 03:26-03:30 (11:19 PM Nov 21)` | `ea8d8ea5-e574-4480-9b79-f67a42ee585c`, `2e1d5512-9c5d-430b-a11b-f736812208b2`, `3f021847-3d62-41a6-b607-9d9ac1d60ce4`, `72cd8ab8-3087-4446-b1cd-f18508cae664`, `cbbcd169-bae6-475f-8c43-d955ad695d14`, `ae457d70-b57a-4e72-9df2-156141c071ef` |
| `Replace 03:18-03:51 (11:00 PM Nov 21)` | `bcc72b5e-1084-4618-b78c-9d87747d9c81`, `3b973a13-ea41-4924-8634-e46beef2b502` |
| `Replace 03:18-03:51 (10:53 PM Nov 21)` | `f4a290aa-f1d3-4814-af65-b3a45fec3a5d`, `0e825ca0-f82c-4bef-a375-d173d472c089`, `529ef04b-cdea-4581-976f-997f5be5f0bc`, `5b8f399a-5560-4c62-a8b4-70c11af383f2` |
| `Replace 02:56-02:58 (10:23 PM Nov 21)` | `058462d9-5f97-4fd5-8f6a-088afc328ae3`, `04309b53-5caf-43cf-9916-4ab8be56081a` |
| `Replace 02:25-02:56 (10:16 PM Nov 21)` | `ff866dd1-028b-41a0-a890-8941509f31f5`, `07f0b881-a0cd-49ce-8deb-6c07396bf72c` |
| `Replace 02:56-02:58 (10:12 PM Nov 21)` | `c7df33cb-474f-4e35-8835-503cb823cf05`, `ceb297ea-34a7-4713-8baa-02636021366d`, `749b9419-6858-4ad9-8b66-65a303c64b43`, `ccb3e652-a35a-4e9f-a0ee-9210ea1f2bcc` |
| `Replace 02:56-02:58 (10:02 PM Nov 21)` | `13839889-ee16-4910-8466-046bd736237c`, `2f20e1e7-45ac-4360-922f-7d9e2a5cb352` |
| `Replace 02:56-02:58 (10:01 PM Nov 21)` | `b4fd4371-05e9-4043-946b-c5864c937f17`, `e685a7ba-7af1-44c2-b52b-6ddbb4a6583c`, `880ffec3-00a6-4f01-913d-b565aac92007`, `f907d2e4-afd4-47f6-b860-b41e75366db9` |
| `Replace 02:56-02:58 (09:59 PM Nov 21)` | `7947c42e-3f3e-4297-9a47-96f7cd411191`, `390dcece-937c-4ec6-b618-23421755e3ee` |
| `Replace 01:30-02:00 (10:28 PM Nov 17)` | `aafb9a19-fe07-49d7-84ce-8fed0047a1a3`, `797aeb7f-885e-4b1a-94a5-3fa22b3fab16` |

### Untitled Project — 1

| Existing title | Suno ID | Classification | Queue status |
|---|---|---|---|
| `Untitled Project [01:00 - 02:30]` | `9e7ef13a-a8c4-4730-88a8-47ecc7d98f6b` | Untitled Project | Excluded; untouched |

## Initial Kio Queue Classification Rationale

- **Song (2):** The two `Showtime in the City` entries are distinct finished-library records with regular song titles and their own IDs and song URLs. Their previously captured lyrics identify them as school basketball anthems. Both remain assigned to Kio.
- **Replace Artifact (30):** The existing titles begin with `Replace`; this task explicitly excludes Replace artifacts. This is a task-level queue classification only, not a new finding about Suno's internal lineage or edit implementation.
- **Untitled Project (1):** The existing title explicitly identifies an untitled project segment; excluded as requested.
- **Unknown (0) in that earlier queue:** This does not describe the later full inventory; ambiguous records from the 438-record review are listed above.

## Completion Gate

- **Records reviewed:** 438 unique library records.
- **In-scope songs assigned:** 404, including 238 reassigned from N-Learning and four previously unassigned voice-test clips.
- **Workspace memberships after cleanup:** 407, including three edit-labeled records retained in their prior workspaces.
- **Unassigned excluded records:** 30 Replace-titled records and one Untitled Project-titled record; none were edited, hidden, archived, or deleted.
- **Unclassified candidates:** 19 records retained in their existing workspaces pending context.
- **Validation:** Workspace counts reconcile to 407 assigned records; together with the 31 intentionally unassigned excluded records, they reconcile to all 438 library records. A post-move global library refresh confirmed all 438 inventory IDs remain present, with no missing or new IDs.
- **Next action:** No approved assignment remains queued. Review ambiguous records only with additional project context.
