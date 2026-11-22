# Founder Review Workbench Refinement - DEMO-2026-0001

**Phase:** 3.1B.1
**Status:** Workflow recommendation only; no workbench or repository behavior is changed by this document.

## 1. Evidence and Observations

### DEMO-2026-0001 evidence

| Evidence source | Observed facts | Limits |
|---|---|---|
| [Canonical demo registry](../../catalog/metadata/demos.yaml) | Repository identity `DEMO-2026-0001`; title `Carillon`; source platform `Suno`; Suno song ID `c7b5dc50-d324-42f5-9611-30fe44e0d1a5`; original share URL; creator display attribution `Christopher Bower`; no local audio; prompt, excluded prompt, model version, source material, and checksum are `UNKNOWN`. | The record does not store a source account handle, playlist, source labels, creator-intent fields, or revisions of creative material. |
| [Provenance record](../../catalog/demos/internal/intake/DEMO-2026-0001/provenance.md) and [demo profile](../../catalog/demos/internal/intake/DEMO-2026-0001/demo-profile.md) | The public page displays the title, credited creator, and lyrics. Lyrics are not preserved locally. Rights, source material, prompt, model, and original audio are unresolved. | A live public page is not an immutable source snapshot, local audio preservation, or a rights determination. |
| [Review record](../../catalog/metadata/demo-reviews.yaml) and [evaluation notes](../../catalog/demos/internal/intake/DEMO-2026-0001/evaluation.md) | `REVIEW-2026-0001` is an AI intake screen, founder review is pending, audio was not reviewed, and audio-dependent grades are `N/R`. | This is not an observed founder listening or completed review session. |
| Public [Suno source page](https://suno.com/song/c7b5dc50-d324-42f5-9611-30fe44e0d1a5) | Provides a source-page reference and visible lyrics. The song ID is also present in the canonical page URL. | The page content retrieved for this analysis did not provide a preserved prompt, excluded styles, playlist, or model value. |
| Founder workflow observation supplied for this phase | The founder sought source context, prompt, lyrics, creator intent, playlist, model, and source labels before repository governance details. | Qualitative evidence from the first demo; no task timing, click log, or multi-demo usability study is available. |
| Phase 3.1B intake description | Identifies playlist `1776` and model `V6-MINI` as observed intake information and names `Dark Electronic Hip-Hop` as a label to evaluate for preservation. | These values are not in the canonical demo record or local provenance. Preserve them as reported candidate evidence until the original source capture confirms them; do not imply they have been independently verified. |

### Current workbench observation

The shared read-only workbench was inspected in its Overview and `Carillon` detail views. The detail header shows `DEMO-2026-0001`, `Carillon`, the display attribution `Christopher Bower`, and review-state badges. It then leads with a **Canonical demo record** panel containing review status, disposition, submission type, submitted date, creator attribution, classification, seed designation, rights status, and checksum. The linked review follows. Source provenance and per-demo files are links near the bottom; prompt, lyrics, creator intent, playlist, model, and source labels are not displayed in the detail view.

No saved screenshot files were found in the repository. The active browser view provided a live visual check, but no screenshot or interaction log is treated as a durable research artifact.

The founder-reported ordering need and the live screen inspection support moving source and creative context ahead of governance metadata. They do not establish that every founder will use the same order; test the recommendation in subsequent real reviews.

## 2. Recommended Display Hierarchy

Use a persistent identity header, followed by the information needed to understand and assess the creative artifact, then readiness and governance:

1. **Repository identity header:** `Carillon` as the working-title heading; `DEMO-2026-0001` continuously visible as the authoritative, stable ID; review/intake state as a compact status indicator.
2. **Source context:** platform, source title/attribution, account, collection or playlist, model, source ID, and prominent source link. Visually distinguish source-reported facts from repository values.
3. **Creative context:** original prompt and exclusions, lyrics, creator notes, and available artwork, with exact source and revision shown.
4. **Creator intent:** explicit targets and constraints extracted or stated by the creator, with provenance and a clear separation between creator statements and analysis.
5. **Source labels:** verbatim platform- or creator-supplied labels, followed by optional, visibly separate taxonomy mappings.
6. **Review readiness:** whether audio and evidence are available, what remains unknown or missing, why review is blocked, and the next required action.
7. **Governance state:** founder review outcome, classification, seed designation, disposition, and rationale. Keep these lower in the reading order and clearly gated.
8. **Preservation details:** compact preservation status in readiness; full technical metadata in an expandable advanced section.

This keeps `DEMO-2026-0001` authoritative without making repository administration the first substantive content. It also avoids letting source labels or creator intent appear to be founder conclusions.

### Above-the-fold and content behavior

| Placement | Recommended content |
|---|---|
| **Above the fold** | Working title and stable demo ID; compact source strip with platform, credited display name/account if known, playlist/collection, model, and source link; prompt and excluded-style summary; visible source-label chips; a clear audio/evidence readiness indicator and blocker. |
| **Visible in the initial creative section** | Creator-intent summary with its evidence source. Keep prompt-derived analysis visually distinct from explicit creator intent. |
| **Expandable, initially open when evidence exists** | Full original prompt and creative constraints. Allow collapse for long text, but do not hide the fact that the source prompt is missing or require opening repository YAML to see it. |
| **Expandable** | Full lyrics, creator notes, artwork and its attribution, complete taxonomy mappings, and long evidence lists. Keep an obvious preview or availability indicator so their presence is discoverable. |
| **Below the fold** | Detailed review history, rights workflow, classification and seed rationales, disposition plan, and full repository metadata. Preserve direct links to canonical records. |
| **Linked, not duplicated as authority** | Original source page, preserved audio asset when available, source metadata snapshot, lyrics/prompt artifact when separately stored, review record, provenance record, and repository record. Always identify which view is canonical. |

“Above the fold” is a prioritization target, not a requirement to squeeze every value into one viewport. On narrow screens, keep the same semantic order and use responsive sections rather than moving governance before creative context.

## 3. Source Context Model

The values below should be source-attributed, not inferred from the repository title or assigned artist. `Required` is conditional on the source type; sources without a platform equivalent should not be blocked for lacking a Suno-shaped field.

| Display field | Requirement and unknown handling | DEMO-2026-0001 / future-source guidance |
|---|---|---|
| `source_platform` | Required when a platform is identified; `UNKNOWN` is allowed while unresolved. Can be derived provisionally from a verified URL host, but mark it as derived and preserve the URL evidence. | `Suno` is in the registry. Do not make a platform name a global enum that excludes local or historical material. |
| `source_song_id` | Optional and source-specific; `UNKNOWN` allowed. It may be parsed from a verified source URL, but retain the raw URL and the derivation provenance. | The Suno ID is recorded and appears in the canonical page URL. For future neutral modeling, prefer a generic `source_item_id` plus the original provider field/key. |
| `source_url` | Required when an online source URL is available; optional for a local file, physical/historical source, or offline contributor handoff; `UNKNOWN` allowed if no reliable reference exists. Preserve submitted and canonical URLs separately with link type. | Both share and canonical Suno URLs are recorded. The current `audio_location` value is a page URL, not a preserved audio file; display it as a source link, not an audio asset. |
| `source_display_name` | Optional; exact source-displayed attribution. `UNKNOWN` allowed. Do not derive it from a handle or promote it to legal authorship. | `Christopher Bower` is shown as source attribution and in the current `creator` field. |
| `source_account` | Optional; preserve exact handle, account URI, or account identifier as observed. `UNKNOWN` allowed. Never infer it from a display name. | The public profile was observed as `@cjbower`, but this is not stored in the canonical record. It identifies a source account, not ownership or assignment. |
| `source_playlist` | Optional; `UNKNOWN` allowed when no source collection exists or it was not captured. Preserve the exact observed label and, when available, a separate collection ID and URL. Do not normalize the displayed label. | `1776` is reported in the Phase 3.1B intake description but not stored in the demo record; preserve as reported until its source context is captured. |
| `source_generation_model` | Optional; `UNKNOWN` allowed. Record only the exact source-reported model/version and capture context. It is not derived from the source URL, creation date, or output sound. | `V6-MINI` is reported in the intake description but the canonical record says `UNKNOWN`; retain the discrepancy until verified. |

### Source-neutral compatibility

- Separate source type/origin from provider-specific fields. Suno and Udio may provide platform item IDs, links, accounts, collections, labels, and generation metadata; capture only the values each source actually exposes.
- A local audio file may have no platform, account, song ID, playlist, or model. Represent its file/asset reference and preservation data without inventing those values.
- A historical recording may have archival references, catalog numbers, source publication, dates, and attribution rather than a creator account or generation model.
- An external contributor may provide files and attribution through a private handoff. Preserve submitter identity separately from public creator attribution and project/rights ownership.
- Keep original source fields extensible and optional. A common source model may provide generic item/link/collection references while retaining exact provider-specific metadata as attributed evidence.
- The current registries define `UNKNOWN`; they do not establish a general `NOT_APPLICABLE` value. Do not silently use empty strings to mean either. A future schema should distinguish unknown, unavailable, and not applicable before making source fields mandatory.

## 4. Creative Context Model

| Field | Display recommendation |
|---|---|
| `working_title` | Show as the human-readable heading. Preserve a separate source-displayed title and title history if they differ or change. Optional/unknown is valid; the demo ID is still required. |
| `prompt` | Show the preserved original prompt prominently, with exact text, source, capture time, and revision. If it is long, place it in an initially expanded or clearly previewed block. Do not replace it with a cleaned or interpreted summary. |
| `creative_constraints.exclude_styles` | Show beside the prompt as explicit creative constraints, preserving the creator's exact phrases and order. Do not imply the generated work obeyed them. |
| `lyrics` | Make availability and source obvious. Provide a readable, expandable full text view; show a useful preview without replacing the complete preserved text. Link to the canonical artifact if policy or storage requires it to remain elsewhere. Do not copy lyrics into a new store solely for display. |
| `creator_notes` | Optional, attributed, versioned notes. Show a short preview in creative context; expand for full notes. Keep them distinct from reviewer notes. |
| `artwork` | Optional source-linked thumbnail when available and appropriate, with attribution/provenance and rights context. Expand or link to the original asset; never require artwork for intake. |

For `Carillon`, the public page makes lyrics available, but the repository intentionally does not copy them locally. The repository records `original_prompt` and `exclude_prompt` as `UNKNOWN`. The interface should show that state explicitly rather than render an empty prompt panel as if no prompt existed.

## 5. Creator Intent and Creative Constraints

Present creator intent as an attributed, append-only set of statements. Preserve the raw phrase, evidence source (prompt, creator note, intake answer, or other source), capture time, and any separate analysis/mapping. The creator's original intent is immutable historical evidence: a clarification or revision creates a new version and never overwrites the earlier statement.

| Intent field | Governance and display |
|---|---|
| `source_material_type` | Preserve what the creator says the work draws on. Keep material identity/reference separate from the type and from a review of fidelity. |
| `genre_target` | Preserve the creator's phrase(s); an optional taxonomy mapping is separate and versioned. Do not turn a prompt-analysis guess into a creator target. |
| `style_target` | Preserve stated musical influences, arrangement, vocal, and production directions as distinct facets when possible. Keep raw input available. |
| `voice_target` | Preserve the requested voice qualities or role. Do not treat it as a roster assignment, performer credit, or voice identity. |
| `tempo_target` | Preserve the stated tempo/range and units when provided. An analyzed tempo from audio is a separate observation. |
| `project_purpose` | Preserve the creator's stated purpose. Do not infer it from the source material, lyrics, genre, or intended release channel. |
| `creative_constraints` | Add as a first-class intent group for positive and negative requirements. Include `exclude_styles` as a verbatim list; keep other exclusions/constraints separately attributed rather than compressing them into free text. |

Prompt analysis may identify explicit targets and infer likely intent, but these must remain distinct fields/perspectives. The [Music Taxonomy and Intent Framework](../../foundations/music-taxonomy-and-intent-framework.md) governs the boundary between creator intent, prompt analysis, founder review, and audience perception. Missing or conflicting values remain visible as `UNKNOWN` or conflicting evidence; they are not silently completed by the workbench.

## 6. Source Labels and Taxonomy Mappings

Treat source labels as evidence, not as the repository's verdict. `source_labels` should preserve the exact raw label, origin (platform, creator, or other source), source record/link, capture time, and any available source context. Do not normalize case, punctuation, spelling, or a hybrid expression in the preserved value.

`Dark Electronic Hip-Hop` is named in the Phase 3.1B.1 request as a label to evaluate. It is not present in the current registry or provenance record, and the page content captured for this analysis does not confirm it as a Suno label. If the original source shows it, retain that exact value as a raw source label; until then, mark it as a reported/unverified candidate rather than a confirmed platform label.

Any mapping belongs in a separate, optional structure containing taxonomy/version, mapped term(s), mapping relationship, rationale, status, and mapper. The displayed source label must remain visible alongside the mapping. A creator label, platform style label, prompt-derived intent, and founder classification are separate perspectives; a controlled vocabulary supports repository organization but does not replace them. One label may map to multiple concepts or remain unmapped.

## 7. Creator, Project Owner, Source Account, Artist, and Performer

The current `creator` field and the portal's `Creator attribution` label are too broad to carry all these meanings. For this demo, `Christopher Bower` is a public-page creator attribution; it is not evidence that the person is the legal rights owner, repository submitter, assigned artist, or performer.

Display and preserve separate concepts:

- **Source-displayed creator attribution:** exact name/credit shown by the source (`Christopher Bower` for this record).
- **Source account:** platform handle or account reference (`@cjbower` was observed but is not in the registry).
- **Repository submitter:** who supplied/registered the item; current `submitted_by` is `UNKNOWN`.
- **Project owner / rights party:** an explicitly established project or rights relationship; current ownership assertion and rights status are `UNKNOWN`. Do not infer legal ownership.
- **Assigned artist or project:** a roster entity selected through a separate human decision; current assigned-entity fields are `UNKNOWN`.
- **Performer / voice implementation:** who or what performed the recording, and any associated voice identity; not established by a creator credit or source account.

Until evidence supports a stronger role, label the UI value **Source attribution** or **Credited creator (source)** rather than an unqualified **Creator**. Keep the source name and account link separate.

## 8. Repository ID and Working Title

`DEMO-2026-0001` is the permanent repository identity and join key. `Carillon` is a working/source title, not an identity. Recommended header: **Carillon** as the readable title with **DEMO-2026-0001** always visible as the stable identifier. Keep external source IDs in the source section, never as repository IDs.

If the working title changes, update the current display title through an authorized record change while retaining the prior title and source-displayed title in attributable history. A title change must not create a new demo or break review, provenance, asset, or disposition links.

## 9. Preservation Metadata Placement

Do not remove preservation data; change only its presentation priority:

- In the first-screen readiness summary, show operationally important state such as **Original audio not received** and **Preservation incomplete**. This is a review blocker and should not be buried.
- Put full checksum, immutable asset URI, file format, file size, ingest/capture dates, storage/archive identifiers, preservation-copy status, and derivative lineage in an expandable **Preservation Details** or **Advanced Metadata** section.
- Show a checksum as a derived value tied to a specific preserved file and algorithm. `UNKNOWN` is appropriate when no file exists; never substitute a page URL or source ID for an audio asset/checksum.
- Keep source links and preserved-asset links visually distinct. A URL to the Suno page is source provenance, not a locally preserved audio location.

The current detail view puts `Audio checksum: UNKNOWN` among canonical repository facts. Keep an at-a-glance audio/preservation status near review readiness, but move the technical checksum and archive inventory into the advanced section.

## 10. Write-Back Readiness

**Assessment: NOT READY.** The current workbench is explicitly read-only, and the requested refinement is design-only. Do not implement write-back from this evidence.

### Blocking risks and missing foundations

- The current workbench is a static, build-time read model over YAML. It has no authenticated write path, backend, permission model, or safe repository-change workflow.
- A stale build can present data different from the current repository unless source revision and build time are identified.
- The current record lacks structured source account, playlist, model, prompt revisions, excluded styles, creator intent, source labels, and a distinct source-attribution field. Some values reported by the intake description are not recorded or independently captured.
- `creator` and `audio_location` conflate concepts; source-page availability is not asset preservation or rights evidence.
- There is no approved representation for append-only creator-intent revisions, source-label provenance, source metadata snapshots, or title history.
- Write-back would need repository-side schema/semantic validation, cross-reference checks, conflict handling, reviewable diffs, audit history, least-privilege authorization, and human approval. None is established by the current prototype.
- Governance and rights-sensitive actions must remain separate. Editable UI controls must not make review eligibility, classification, seed, disposition, ownership, or development approval look like routine intake fields.

### Remaining workflow uncertainty

- Confirm where the original prompt, excluded styles, playlist, model, and exact source labels can be captured, with what provenance, and whether values can change after generation.
- Decide how to preserve prompt/lyrics/artwork revisions and source-page snapshots without copying material into an unauthorized location.
- Validate the proposed ordering with more than one real founder review, including whether the full lyrics should default open and which source metadata is consistently used.
- Define roles and authority for source attribution, rights review, creator-intent correction, founder review, and repository submission before permitting edits.

The [workbench architecture](./founder-review-workbench.md) already documents the prototype's read-only boundary and future PR-based write-model direction. Revisit write-back only after the field model and workflow are approved, source discrepancies are resolved, and repository-side validation and authorization are designed.

## Validation and Scope

- Analysis uses the current demo/review records, per-demo provenance and evaluation artifacts, intake/evaluation/disposition standards, taxonomy governance, workbench documentation and code, the shared live workbench, the public Suno page, and the founder-reported first-use observation.
- No demo or review record, schema, demo metadata, taxonomy definition, workbench code, write-back, or GitHub Actions was changed.
- Playlist/model/style-label observations that are not in the canonical record are identified as reported or unverified rather than promoted to repository facts.
- This document recommends display and governance behavior only; it does not authorize implementation.
