# Phase 3.1B - Intake Model Refinement Using DEMO-2026-0001

**Status:** Analysis and recommendations only. This document does not modify schemas, records, taxonomy definitions, or the workbench.

## Purpose and Evidence Boundary

Use the first real intake to evaluate the existing model rather than inventing fields in isolation. Keep these concepts separate:

1. Repository identity
2. Source provenance
3. Creative context
4. Creator intent
5. Source labels
6. Review readiness
7. Governance state

The repository registry remains authoritative. A value shown by a platform, supplied by a user, entered by a submitter, inferred by analysis, and decided during founder review are different evidence types and must retain their origins.

## DEMO-2026-0001 Evidence Snapshot

| Information | Evidence observed | Current repository state |
|---|---|---|
| Repository identity | `DEMO-2026-0001` | Stable demo ID in the canonical registry. |
| Working/source title | `Carillon` | Registry title and public source title. A title can change and is not the repository identity. |
| Source platform and URLs | Suno; original share URL `https://suno.com/s/ZLqsa9pWs6BPXl8T`; canonical page `https://suno.com/song/c7b5dc50-d324-42f5-9611-30fe44e0d1a5` | Both URLs are in the provenance artifact. The canonical page URL is also stored in `audio_location`, even though no local audio file was received. |
| Platform asset identifier | `c7b5dc50-d324-42f5-9611-30fe44e0d1a5` | Stored as `suno_song_id`. |
| Source account and display name | Public page metadata identifies `Christopher Bower (@cjbower)`. | The registry stores `creator: Christopher Bower`; it does not store the account handle. Creator attribution is explicitly not a legal ownership finding. |
| Playlist | `1776`, as supplied in the Phase 3.1B task description | Not represented in the current registry or per-demo artifacts. Preserve as a source-observed value if confirmed against the source view. |
| Model | `V6-MINI`, as supplied in the Phase 3.1B task description | `model_version` remains `UNKNOWN` in the canonical record and provenance artifact. Reconcile and capture the evidence before any future record update. |
| Prompt | The task describes prompt information as available. | `original_prompt` and `exclude_prompt` are `UNKNOWN`; the current intake artifacts contain no prompt text. Capture the exact prompt and its source/version if accessible; do not infer it from lyrics or style labels. |
| Lyrics | Visible on the public Suno page. | `lyrics_available: true`; lyrics are not copied locally. `lyrics_location` points to the public song page, not to a local lyrics artifact. |
| Suno style label(s) | The task calls out source style labels; `Dark Electronic Hip-Hop` is used as an example in the task. | No exact style label is stored in the repository. Treat the example as unverified until its exact source display and label origin are captured. |
| Audio and checksum | Public page exists; no original audio file was received locally. | `audio_downloaded: false`; `audio_sha256: UNKNOWN`. A source page is not a preserved audio asset. |
| Intake and review | Intake is incomplete; `REVIEW-2026-0001` is an AI intake screen, founder review pending, audio not reviewed, audio-dependent grades `N/R`. | `review_status: intake_incomplete`, disposition `hold`; classification and seed designation remain `UNKNOWN`. |
| Source material and rights | No source-material identification or rights evidence was captured. | Source material, ownership assertion, and rights-review status remain `UNKNOWN`. |

The current public page and repository establish the title, creator display name/account handle, song ID, URLs, and visible lyrics. Playlist `1776` and model `V6-MINI` are values supplied in the current task but are not yet in the canonical record. The original prompt and exact source labels are not present in the current repository artifacts; no values are inferred or copied into records in this phase.

## 1. Review of the Current Intake Model

### Useful fields and structures

- `demo_id` provides a stable repository identity independent of the platform ID.
- The original share URL, canonical Suno URL, and Suno song ID together make the source findable.
- `audio_downloaded`, `audio_sha256`, and explicit `UNKNOWN` values expose preservation gaps.
- Prompt and lyric status/reference fields anticipate important evidence, even though their current values are incomplete.
- Rights status, required evidence, risks, owner, next action, and review trigger help explain why intake is blocked.
- The separate review registry records reviewer role, date, `founder_review_status`, audio audition state, criteria, grades, and written evidence.
- The current review's N/R grades and pending founder status correctly avoid turning missing audio into a creative judgment.
- Per-demo profile, provenance, evaluation, and hold-plan files provide human-readable supporting context.

### Confusing or overloaded fields

| Current field or pattern | Why it is confusing for DEMO-2026-0001 | Recommendation |
|---|---|---|
| `title` | A working/source title can change; it is not the stable identity. | Present as `working_title`; retain the exact source-displayed title separately when needed. |
| `creation_date` | The schema means source creation date, while `demo_id` embeds the intake year and `submitted_at` means receipt date. These are different events. | Rename the source date to `source_created_at`; use a separate repository record timestamp and intake receipt timestamp. |
| `creator` | The page display name is not the account handle, authorized submitter, verified author, or legal owner. | Preserve source display name and source account separately from `submitted_by` and any ownership assertion. |
| `submission_source` | Current value, “User-provided public Suno share URL,” describes how the repository received the link, not the originating platform. | Rename/interpret as `intake_channel`; separately record `source_platform: Suno`. |
| `audio_location` and `suno_url` | `audio_location` contains the canonical web page while `audio_downloaded` is false. A web page is not a local audio asset. The share URL and canonical URL are also different references. | Keep original and resolved source URLs separately; reserve `audio_asset_ref` for an actual preserved audio file. |
| `lyrics_location` | It points to the Suno page, not to copied lyrics. | Rename/interpret as `lyrics_source_ref`; add a separate versioned lyrics artifact reference only if a snapshot is actually preserved. |
| `suno_song_id`, `generator`, `model_version` | Provider-specific fields are mixed into a general demo record; a generic `generator` name does not distinguish platform, model, or version. | Group under provider-scoped source/generation metadata with a generic core and optional provider extension. |
| `original_prompt`, `exclude_prompt` | Current fields do not capture source, capture time, or prompt revisions. A single mutable prompt field loses the history of evolved prompts. | Store immutable prompt revisions/references with source and version; keep the latest/current pointer separate. |
| `source_material` and `source_material_id` | A source reference, source-material type, and creator intent can be conflated. | Keep the exact source reference/provenance separate from creator-stated source-material type and any later interpretation. |
| `approximate_genre` and `approximate_bpm` | The source, method, and stage of estimation are not represented. These could be mistaken for creator intent or founder-reviewed conclusions. | Move to attributed source labels or observed characteristics. Only add an audio-derived observation after analysis/listening; retain source and method. |
| `review_status` vs. `founder_review_status` | `review_status` in the demo registry is a lifecycle state; founder review status lives in the review record and is derived by the workbench. | Use `lifecycle_state` for the demo workflow; continue deriving founder review status from linked review records. |
| `audio_downloaded` | It describes a download action, not whether an approved, usable audio asset is preserved. | Prefer an `audio_asset_ref` plus a derived `audio_received`/preservation state. |
| `classification`, `seed_designation`, `current_disposition` | These fields are adjacent to intake facts but have different authority and gates. | Keep them in Governance State; never populate classification or seed during intake. A documented `hold` may represent an A&R blocker, not a creative conclusion. |

### Missing or insufficiently represented information

- Source account handle, source display name, source playlist/collection, and exact platform style labels.
- Source capture time and a reference to the source metadata snapshot used for intake.
- Generic source platform and provider-scoped asset ID, separate from the intake channel.
- Exact prompt/lyrics revisions and immutable references to their source or preserved artifacts.
- A structured, explicitly attributed Creator Intent object separate from raw prompt and lyrics.
- A raw source-label collection separate from Creator Intent and repository taxonomy mappings.
- A distinction between source-created, submitted/received, observed/captured, and repository-recorded timestamps.
- A clear difference between remote source availability and locally preserved audio.
- A machine-readable explanation of missing evidence and the reason a next stage is blocked. `required_evidence` helps, but does not distinguish present, missing, inaccessible, or not applicable.
- A status model that distinguishes unknown, not captured, inaccessible, and not applicable. This is a future schema question; do not reinterpret existing `UNKNOWN` values silently.

## 2. Recommended Intake Structure

| Section | Purpose and ownership | Recommended contents |
|---|---|---|
| **1. Repository Identity** | Catalog/repository owner controls stable identity and lifecycle. | `demo_id`, record-created timestamp, lifecycle state, intake submission type. Keep working title out of identity. |
| **2. Source Provenance** | Intake records exactly where the artifact and observed metadata came from. | Source kind/platform, original and resolved URLs, provider-scoped asset ID, source account/display name, source collection/playlist, source/model metadata, source creation date, intake channel/submitter/received date, capture timestamp, snapshot reference. |
| **3. Creative Context** | Preserve the creative artifacts and their revisions without turning them into outcomes. | Source-displayed title, current working title, prompt/exclusion-prompt revisions, lyrics revisions/references, creator notes, language when known. |
| **4. Creator Intent** | Preserve creator-authored intent as stated, attributed, and immutable. | Source-material type, genre/style/voice/tempo targets, project purpose, evidence source and revision/capture context. Keep inferred analysis elsewhere. |
| **5. Source Labels** | Preserve exact labels emitted or displayed by the source platform or supplied by another named source. | Raw label text, label origin, capture timestamp, source reference; optional separately versioned taxonomy mapping. |
| **6. Review Readiness** | Intake/A&R identifies evidence available, missing, and blocking the next authorized stage. | Audio asset/preservation state, checksum when available, rights-review state, linked founder-review state, required/missing evidence, blocker explanation, derived eligibility. |
| **7. Governance State** | Authorized A&R/founder decisions remain separate from intake facts and retain evidence/rationale. | Classification and seed designation (review-gated), disposition and rationale, review references, any later authorized assignment. |

### Field classification key

- **Required (R):** Required for the record or for the specific subrecord when one exists.
- **Optional (O):** Capture when relevant and available; its absence alone does not invalidate intake.
- **Derived (D):** Calculated from source evidence or governed workflow state, not manually asserted.
- **Unknown Allowed (U):** An explicit `UNKNOWN` is permitted while evidence is missing. Do not replace it with a guess or silently omit it.
- **Review Gated (G):** Set only after the specified review/authorization; this does not mean every value must eventually be known.

Tags may be combined. “Required” does not mean a source-specific value can be invented; where evidence is unavailable, record `UNKNOWN` and the blocker.

### 1. Repository Identity

| Field | Classification | Rationale |
|---|---|---|
| `demo_id` | R | Repository-assigned immutable key; never derive it from a title or platform ID. |
| `record_created_at` | R, D | Repository event time; distinct from source creation or submission time. |
| `lifecycle_state` | R, D | Derived from intake/review workflow events. It replaces ambiguous use of `review_status` for the demo lifecycle. |
| `submission_type` | R, U | Required intake classification under current policy; `UNKNOWN` only if intake class cannot yet be established. It is not a project type or source platform. |

`creation_date` belongs in Source Provenance as `source_created_at` and is O/U. It is not the demo's identity or repository record creation time.

### 2. Source Provenance

| Field | Classification | Rationale |
|---|---|---|
| `source_kind` | R, U | Identifies the general origin category when known; preserve `UNKNOWN` until established. Do not hard-code a Suno-only model. |
| `source_platform` | O, U | Provider name such as Suno when applicable; absent for a direct local-file source. |
| `source_url_original` | O, U | Preserve the exact URL submitted or observed, including a share URL. Never overwrite it with a redirect. |
| `source_url_resolved` | O, D, U | Capture the canonical destination separately when resolution is observed. |
| `source_asset_id` | O, U | Provider-scoped identifier, e.g. Suno song ID; store its provider/namespace with the value. |
| `source_account_handle` | O, U | Exact public account handle when available. It is not the submitter identity or proof of ownership. |
| `source_display_name` | O, U | Exact source-displayed creator/name attribution; not a legal authorship finding. |
| `source_collection_labels` | O, U | Exact playlist/collection value(s), including `1776` if confirmed; preserve original spelling and capture context. |
| `source_material_ref` | O, U | Reference to the exact source text/item if identified; do not infer it from the demo title or lyrics. |
| `source_material_description` | O, U | Attributed descriptive context for a source reference; not the source identity or rights conclusion. |
| `source_created_at` | O, U | Date asserted by the source; do not infer it from repository ID or retrieval time. |
| `generation_model` | O, U | Exact source-reported model/version, e.g. task-supplied `V6-MINI`; retain the evidence origin. |
| `intake_channel` | R, U | How the repository received the item/link, distinct from the original source platform. |
| `submitted_by` | O, U | Authorized repository submitter, distinct from the source account and credited creator. |
| `ownership_assertion` | O, U | Preserve any submitter assertion as an assertion only; never treat it as verified ownership. |
| `external_contributors` | O, U | Capture attributed contributors when known; do not infer contributor identity from a public account. |
| `intake_received_at` | R, D | Time the repository received the intake. |
| `source_observed_at` | R, D | Time the source metadata was captured; needed to interpret mutable platform fields. |
| `source_metadata_snapshot_ref` | O, U | Link or identifier for a preserved metadata snapshot, when one is actually retained. |

For DEMO-2026-0001, retain the original share URL and canonical Suno page separately; represent the public account handle and display name separately; and keep the playlist/model as source observations rather than creator intent. The Suno-specific fields can remain as a provider extension during a future migration, but the generic model should not require them.

### 3. Creative Context

| Field | Classification | Rationale |
|---|---|---|
| `source_display_title` | O, U | Exact title shown by the source; immutable as a captured source fact. |
| `working_title` | O, U | Editable project-facing title; not the repository identity and not a replacement for the source title. |
| `prompt_revision_ref` | O, U | Reference to exact original/current prompt revision; record version and origin. |
| `exclude_prompt_revision_ref` | O, U | Reference to exact exclusion/negative-prompt revision when one exists. |
| `lyrics_revision_ref` | O, U | Reference to lyrics as observed or preserved, with source/version. The current public page can be cited without copying the lyrics into YAML. |
| `creator_notes` | O, U | Creator-provided context with author/source and timestamp. |
| `language` | O, U | Record if explicitly supplied or verified; if derived, record that method rather than presenting it as creator intent. |

Prompt and lyric changes create new revisions; they do not overwrite source text. For this demo, the title and public lyrics are available at the [canonical Suno page](https://suno.com/song/c7b5dc50-d324-42f5-9611-30fe44e0d1a5), but the prompt is not captured in the current repository. The task identifies prompt information as available; preserve the exact text/reference when it is collected, otherwise leave it `UNKNOWN`.

### 4. Creator Intent

Every intent value is O/U and must preserve its source wording. It is not review-gated, but any populated value must be attributable. A prompt may contain explicit creator intent; a model/analyst's interpretation of the prompt is not itself creator-authored intent.

| Field | Classification | Rationale |
|---|---|---|
| `source_material_type` | O, U | Creator-stated source class; keep distinct from a verified source ID and rights/provenance record. |
| `genre_target` | O, U | Creator's intended genre terms, not source-platform labels, observed audio, or founder classification. |
| `style_target` | O, U | Creator's intended style/influence/production language, preserved verbatim. |
| `voice_target` | O, U | Requested voice or delivery, not a voice assignment or observed voice characteristic. |
| `tempo_target` | O, U | Creator-stated tempo target; preserve phrase and units before any normalized BPM. |
| `project_purpose` | O, U | Creator-stated purpose, distinct from release/medium and later outcome. |
| `intent_evidence_ref` | R for each populated value; U when none is available | Links each intent statement to prompt, note, intake metadata, or direct clarification. |
| `intent_recorded_at` | R for each captured statement; D | Capture time supports immutable history and distinguishes later clarifications. |

The original Creator Intent record must never be overwritten. Later clarification is an additional attributed statement/version. Keep Prompt Analysis and Founder Review in their own perspectives as defined in the [Music Taxonomy and Intent Framework](../../foundations/music-taxonomy-and-intent-framework.md).

### 5. Source Labels

| Field | Classification | Rationale |
|---|---|---|
| `source_label_text` | O, U | Exact raw string, capitalization, punctuation, and order as supplied/displayed; do not substitute a taxonomy term. |
| `source_label_origin` | R when a label exists; U if its origin cannot be determined | Distinguishes platform label, creator label, analyst label, or audience term. |
| `source_label_observed_at` | R when captured; D | Timestamp and source snapshot make mutable labels auditable. |
| `taxonomy_mapping` | O, U | Separate optional mapping with rationale/version and mapping status. It never replaces raw text and is not silently inferred. |

The request's `Dark Electronic Hip-Hop` example is not present in the current demo record or saved source snapshot. If it is confirmed as a Suno-displayed label, preserve that exact value and identify it as a source-platform label; do not treat it as creator intent or a repository classification.

### 6. Review Readiness

| Field | Classification | Rationale |
|---|---|---|
| `audio_asset_ref` | O, U; required before a completed listening review unless an approved alternative exists | Points to an actually preserved/accessible audio asset, not a web page. |
| `audio_received` | R, D | Derived from the approved asset reference and preservation state; false for the current local-file state. |
| `audio_sha256` | O, D, U | Derived from the preserved file; unknown until a file is available. |
| `rights_review_status` | O, U, G | Set by the rights-review process, not inferred from creator attribution or platform availability. |
| `contract_required` | O, U, G | Set only under the applicable contributor/rights process; do not infer it from source type or ownership assertion. |
| `founder_review_status` | R for review state display; D, G | Derived from the linked review record. Only a documented founder review can be complete for the classification gate. |
| `required_evidence` | O, U; required while a decision is blocked | Owner-maintained list of evidence needed to proceed; preserve evidence-specific reasons. |
| `missing_evidence` | D, U | Computed by comparing requirements with captured evidence; do not confuse inaccessible with absent. |
| `stage_block_reason` | D, U | Explains why the next stage cannot proceed, based on the applicable gate and missing evidence. |
| `classification_eligible` | D, G | Workbench/read-model indicator only. It is derived from qualifying review evidence and never writes a classification value. |
| `audio_observed_genre`, `audio_observed_tempo` | O, D, U, G | Optional observations derived from accessible audio and reviewed evidence; distinct from source labels and creator targets. |
| `owner`, `next_action`, `review_trigger` | O, U; required for a nonterminal disposition | Human-owned next-step commitments; not automatic creative evaluation. |
| `risks` | O, U; required when a material blocker/risk is known | Evidence-backed readiness or decision risk, not a generic replacement for missing fields. |

For this example, the immediate audio-dependent review blocker is the absent local original (or an explicitly approved preservation alternative). Source material/rights context and the exact prompt/model evidence are also unresolved. The UI should explain each blocker rather than presenting a bare “pending” badge.

### 7. Governance State

| Field | Classification | Rationale |
|---|---|---|
| `classification.primary/secondary` | G, U | Keep `UNKNOWN` until documented founder review supplies evidence and an approved value set exists. |
| `classification_rationale` | G, U | Requires review evidence and a reference to the supporting review. |
| `seed_designation.primary/secondary` | G, U | Keep `UNKNOWN` until the separate seed review gate and evidence are satisfied. |
| `seed_rationale` | G, U | Requires distinct evidence/rationale; never infer it from genre or disposition. |
| `disposition` | O, U, G | An A&R decision, not an intake fact. An evidence-based `hold` may be recorded to block progression; development dispositions require the existing review/brief authority. |
| `disposition_rationale` | G, U | Record the evidence and authority for a disposition; required when a disposition is assigned. |
| `review_ref` | O, D, U | Link to review records by their IDs; do not duplicate review grades into intake. |
| `assigned_entity_ref` | O, U, G | Keep unassigned until a separate human decision authorizes assignment. |

Do not move evaluations into intake. Preserve the existing `UNKNOWN` classification/seed values, pending founder review, and `hold` disposition for DEMO-2026-0001.

## 3. Field Movement and Naming Recommendations

| Existing field(s) | Recommended destination/action |
|---|---|
| `demo_id` | Keep in Repository Identity; remain immutable. |
| `title` | Treat as `working_title`; preserve `source_display_title` separately. |
| `creation_date` | Clarify as `source_created_at`; add distinct `record_created_at` and `intake_received_at`. |
| `review_status` | Rename/interpret as `lifecycle_state`; do not use it as founder review status. |
| `submission_source` | Rename/interpret as `intake_channel`; add separate `source_platform`. |
| `creator`, `submitted_by` | Split into source display name, source account handle, and authorized repository submitter. |
| `suno_url`, `audio_location` | Preserve original share URL and resolved page URL separately; reserve audio asset location for a preserved file. |
| `suno_song_id`, `generator`, `model_version` | Move under generic source/provider metadata; keep provider-specific identifiers namespaced. |
| `original_prompt`, `exclude_prompt`, `lyrics_status`, `lyrics_location` | Group under Creative Context as immutable, versioned artifacts/references; do not put their text in Creator Intent fields. |
| `source_material`, `source_material_id` | Separate verified source reference/type from creator-stated intent and rights provenance. |
| `approximate_genre`, `approximate_bpm` | Do not treat as intent or reviewed classification. Capture as source labels or attributed observations; derive audio observations only after appropriate analysis/listening. |
| `audio_downloaded`, `audio_sha256` | Use an asset reference and derived preservation/received state; checksum only exists when a file exists. |
| `rights_review_status`, `contract_required`, `required_evidence`, `risks` | Group under Review Readiness; keep ownership assertions in Source Provenance and rights conclusions under authorized rights review. |
| `classification`, `seed_designation`, rationales, `current_disposition` | Group under Governance State with existing evidence and authorization gates unchanged. |
| `source_account`, playlist, source labels, intent fields, prompt/lyrics revisions, metadata snapshot reference | Add to a future structure only after schema review; do not create duplicate stores or records in this phase. |

## 4. Workbench Recommendations

### Current presentation

The read-only workbench imports the canonical demo/review YAML. The intake card presents title/creator and repository intake facts (submission date/type/source, audio, checksum, rights, founder-review state) before its required-evidence list and links. The detail screen shows repository identity and governance fields first, then the linked review; it does not display prompt, lyrics, source account/playlist, source labels, or structured Creator Intent. Queue columns emphasize review/gate and disposition states.

This matches the current implementation in [`portal/src/main.js`](../../portal/src/main.js). The workbench documentation states that no end-to-end founder listening session has yet been observed; ordering recommendations below are hypotheses to validate, not measured founder behavior.

### Recommended detail-screen order

Keep the repository ID and compact workflow badges in the header, then present:

1. **Source Context:** source platform, source account/display name, playlist, original and canonical URLs, provider asset ID, captured source labels, model/version, and observation timestamp.
2. **Creative Context:** working title, prompt revisions, lyrics reference/preview, and creator notes. Keep long text collapsible; the queue should not reproduce full lyrics.
3. **Creator Intent:** source material, genre/style/voice/tempo targets, and purpose exactly as attributed to the creator. Separate any Prompt Analysis from these fields.
4. **Review Readiness:** local audio/preservation status, rights review, founder review status, missing evidence, and a concise explanation of the next-stage blocker.
5. **Governance State:** classification, seed, and disposition with rationale/evidence references and visible review gates.
6. **Repository/technical details:** immutable demo ID, lifecycle state, record timestamps, paths, checksums, and linked YAML/Markdown records.

This puts source context, prompt, and intent ahead of administrative metadata while keeping identity and governance visible. Keep compact review status in the queue, but include the next blocking evidence so “Review Pending” is actionable. Validate this order during actual founder sessions before changing the workbench.

## 5. Future Source Compatibility

| Source | How the structure fits |
|---|---|
| Suno | Provider `Suno`; exact share URL, resolved page, song ID, public account/display name, playlist, prompt/lyrics references, source labels, and generation model are optional provider metadata. |
| Udio | Same generic source fields; capture Udio-specific URL/asset/account/model values as a provider namespace without requiring Suno fields. |
| Local audio file | `source_kind` and local asset reference identify the file; checksum is derived. Platform URL, platform account, playlist, and model may be absent/unknown. |
| Historical recording | Preserve archive/catalog identifiers, source creator/performer/recordist attribution, recording/publication dates, source location, and rights evidence. Prompt/model/playlist fields are not required. |
| External contributor | Keep submitter, credited source creator, account, and ownership assertion distinct; external intake remains disabled until separately authorized. |
| Future source | Generic origin kind, source reference, stable provider-scoped asset ID, observed metadata snapshot, and optional source-specific fields prevent provider lock-in. |

Do not create fake empty Suno fields for non-Suno sources. A future schema should distinguish unknown from not applicable when required, but no new enum or status behavior is implemented here.

## 6. Migration Impact

- No registry or record changes are made in Phase 3.1B. DEMO-2026-0001 keeps its ID, URLs, review link, `hold` disposition, and current `UNKNOWN` values.
- A future migration should be additive and preserve original field values/URLs. Map `suno_url` to the original source URL and the current `audio_location` page reference to a resolved source URL only after documenting the mapping; do not treat either as a local audio asset.
- Preserve `suno_song_id` as a provider-namespaced asset ID. Do not replace it with `demo_id`.
- Keep current task-supplied `1776` and `V6-MINI` separate from canonical data until their source observations are evidenced and an approved record update is made.
- Keep original prompt, prompt revisions, and lyrics references separate from parsed intent. Do not normalize source labels into taxonomy fields during migration.
- Move lifecycle and review-state presentation into a derived read model; do not duplicate `founder_review_status` or `classification_eligible` as manually editable demo fields.
- Retain all `UNKNOWN` classification/seed values and existing review evidence. No taxonomy, seed, or classification vocabulary is changed by this proposal.

## Validation and Limitations

- Reviewed the canonical demo registry, review registry, DEMO-2026-0001 profile/provenance/evaluation/hold plan, intake/review standards and templates, taxonomy framework, portal code/tests, and workbench architecture/wireframes.
- Confirmed the review is AI-assisted intake only: pending founder review, no audio audition, and audio-dependent N/R grades.
- Confirmed the public Suno page exposes title, creator display name/account handle, song ID, and lyrics; the repository does not preserve the lyrics or original audio.
- Playlist `1776` and model `V6-MINI` are in the task description but absent from canonical records; prompt text and exact source style-label values are not in the current repository artifacts.
- Workbench order recommendations are based on current code and repository evidence, not a completed founder usability session.
- No schema, demo record, review record, taxonomy definition, seed/classification definition, or workbench code was changed.

## Repository Sources Reviewed

| Source | Evidence used |
|---|---|
| [demos.yaml](../../catalog/metadata/demos.yaml) | Canonical demo schema, DEMO-2026-0001 values, and current field names. |
| [demo-reviews.yaml](../../catalog/metadata/demo-reviews.yaml) | Linked AI intake screen, pending founder status, N/R grades, and review evidence fields. |
| [Demo profile](../../catalog/demos/internal/intake/DEMO-2026-0001/demo-profile.md), [provenance](../../catalog/demos/internal/intake/DEMO-2026-0001/provenance.md), [evaluation](../../catalog/demos/internal/intake/DEMO-2026-0001/evaluation.md), and [hold plan](../../catalog/demos/internal/intake/DEMO-2026-0001/development-plan.md) | Human-readable source facts, unknowns, review status, blockers, and disposition. |
| [Demo intake template](../../operations/demo-intake/demo-intake-template.md), [intake standard](../../operations/demo-intake/intake-standard.md), [triage workflow](../../operations/demo-intake/triage-workflow.md), and [evaluation standard](../../operations/demo-intake/evaluation-standard.md) | Current field worksheet, intake boundaries, lifecycle ordering, and review gates. |
| [Disposition standard](../../operations/demo-intake/disposition-standard.md) | A&R disposition authority and conditional next-step requirements. |
| [Music Taxonomy and Intent Framework](../../foundations/music-taxonomy-and-intent-framework.md) | Separation of creator intent, analysis, founder review, source labels, and controlled vocabulary. |
| [Workbench architecture](./founder-review-workbench.md), [wireframes](./founder-review-workbench-wireframes.md), [portal README](../../portal/README.md), [portal index](../../portal/index.html), [portal main.js](../../portal/src/main.js), and [review-state.js](../../portal/src/review-state.js) | Current read-only screens, data ordering, derived review state, and explicitly unobserved workflow assumptions. |
| [Phase 3.0 intake validation report](../phase-3-0-demo-intake-validation-report.md) | Intake provenance, known unknowns, review status, and historical correction context. |

## Recommendation

Approve this as a conceptual field model first. Before schema migration or UI changes, reconcile the source-side prompt, playlist, model, and exact style-label observations; decide the minimal immutable artifact/history representation; then validate the proposed field order with actual founder reviews. Make schema or workbench implementation a separate phase after those decisions.
