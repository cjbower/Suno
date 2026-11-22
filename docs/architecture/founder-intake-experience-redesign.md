# Founder Intake Experience Redesign

**Phase:** 3.1C
**Status:** Practical single-operator recommendation; analysis only.

## Findings

DEMO-2026-0001 exposed a display-order problem: the current read-only workbench leads with repository status, disposition, classification, seed, rights, and checksum, while the founder first sought the source and creative material needed to understand the demo. The [live workbench](./workbench-refinement-demo-0001.md) confirms that prompt, lyrics, style description, playlist, model, creator intent, and source labels are not presented in the detail view.

The founder's screenshots establish the following as **Observed Source Metadata**:

| Observed source attribute | Observed value or state | Current canonical intake |
|---|---|---|
| Playlist | `1776` | Not captured |
| Generation model | `V6-MINI` | `model_version: UNKNOWN` |
| Source label | `Dark Electronic Hip-Hop` | Not captured |
| Style description | Present as a distinct source item | Not captured |
| Lyrics | Present as a distinct source item | Availability is recorded; content is not preserved locally |
| Creation timestamp | Present on the source | `creation_date: UNKNOWN` |
| Creator display name | `Christopher Bower` | Stored as the broad `creator` field |

These are direct source observations, not hypothetical values. Their absence from [demos.yaml](../../catalog/metadata/demos.yaml) and the [provenance record](../../catalog/demos/internal/intake/DEMO-2026-0001/provenance.md) means **not yet captured in canonical intake**, not unverified. Preserve source values as observed; do not silently infer, normalize, or reinterpret them.

This phase supersedes earlier analysis wording that treated the screenshot-observed playlist, model, and source label as unverified. It does not retroactively update the canonical record.

The existing canonical record remains unchanged in this phase. Its source/platform ID and URLs are recorded, but prompt and excluded styles are `UNKNOWN`, audio and checksum are absent, and the review is still pending. The [review record](../../catalog/metadata/demo-reviews.yaml) is an AI intake screen, not a founder listening review. The [taxonomy framework](../../foundations/music-taxonomy-and-intent-framework.md) continues to govern classification; this redesign does not assign a taxonomy mapping or review outcome.

**Operator model:** For the near term, Christopher is the founder, intake operator, reviewer, and curator. The experience should support one person moving quickly through intake and review. It should not ask the operator to select among artificial roles or build public-submission, external-contributor, or multi-user workflows.

## What the Demo 0002 Intake Screen Should Look Like

Start with one simple **Add Demo** screen, not an enterprise workflow:

1. **Create identity:** assign the next `demo_id` automatically. Show it as permanent; treat the title as a mutable working title.
2. **Point to the source:** accept a source URL or a local/archive asset reference. A platform name and item ID can be recorded when available. Capture `observed_at` automatically.
3. **Capture what the source shows:** provide a compact **Observed Source Metadata** section for creator/display attribution, account, playlist/collection, creation timestamp, model, source labels, and artwork reference. Copy exact values; allow unknowns.
4. **Capture creative material separately:** keep prompt, style description, lyrics, and excluded styles in distinct fields or asset references. Do not bury all of them in one prompt box.
5. **Record creator intent and constraints:** capture only what is explicit; leave missing fields `UNKNOWN`.
6. **Save as intake:** keep intake separate from review and governance. The new record may be intake-incomplete while the operator gathers evidence.

For a single operator, the default screen should be a straightforward vertical form with a persistent demo ID and clear source/evidence states. Do not require assignment, multi-person approval, audience research, taxonomy mapping, or rights conclusions merely to register the demo.

## Field Recommendations

### Required to register a demo

| Field | Recommendation |
|---|---|
| `demo_id` | Required and system-assigned; stable and never reused. |
| Source reference | Require at least one practical locator: source URL, local asset reference, archive/catalog reference, or a clearly marked pending-source note for a draft. Do not require a platform URL for a local or historical recording. |
| `observed_at` | Required for a source snapshot and automatically captured at intake; retain timezone/precision where available. |
| Intake state | Required operationally, but default it from whether the source/reference and evidence are complete. Do not ask the founder to choose a governance outcome during intake. |

The working title is useful but need not block intake. When it is unknown, the demo ID is still the identity.

### Optional but capture when present

| Field or asset | Capture rule |
|---|---|
| `working_title` | Preserve the current human-readable title. Keep source-displayed title separately if it differs. |
| Source snapshot fields | Capture exact platform, URL, item ID, source display name, creator credit, account, playlist, generation model, labels, source creation timestamp, and artwork reference when visible. |
| `prompt` | Preserve the original prompt verbatim as its own source artifact. Do not replace it with a summary or inferred intent. |
| `style_description` | Preserve the source's reusable style description separately from the generation prompt and source labels. |
| `lyrics` | Preserve or reference the source lyrics separately. Keep the exact source text/revision and source location; do not make a second copy solely for UI convenience. |
| `creative_constraints.exclude_styles` | Preserve excluded styles verbatim as constraints, not as the desired style or source label. |
| Creator intent | Capture explicit `source_material_type`, `genre_target`, `style_target`, `voice_target`, `tempo_target`, and `project_purpose`; each can remain unknown independently. |
| Artwork | Keep a source reference and attribution if present. It is optional and should not block intake. |
| Audio and preservation data | Record the original asset reference, checksum, integrity, and archive metadata when the audio is received/preserved. |

### Remain `UNKNOWN` when evidence is missing

Do not fill unknowns by guesswork. In particular, keep source account, source timestamp, prompt, excluded styles, style description, source labels, model, source material, rights, checksum, creator/owner relationship, assigned artist, performer, classification, seed, and disposition unknown when the evidence is not available. If a value is visible in the source screenshot, record it as an observed source fact even if it has not yet been copied into the canonical record.

### Defer until later

- Taxonomy mapping and any genre/classification decision.
- Seed designation, disposition, artist assignment, and development authorization.
- Rights conclusions or assumptions from a creator display name.
- Advanced archive metadata until an asset is preserved.
- External contributor intake, public submission, multi-user roles, and approval routing.
- Automation beyond a fast source capture and repository-backed record.

Missing prompt, lyrics, playlist, model, artwork, or a taxonomy match should not by itself prevent creation of the intake record. Missing or inaccessible audio should still be shown as a blocker to audio-dependent founder evaluation, in line with the [evaluation standard](../../operations/demo-intake/evaluation-standard.md).

## Source Snapshot Recommendation

Add a lightweight, append-only `source_snapshot` concept to future intake. It records **what the operator observed from the source at a particular time**; it is not repository identity, creator intent, taxonomy, rights approval, or founder classification.

```yaml
source_snapshot:
  source_title: UNKNOWN
  source_platform: UNKNOWN
  source_url: UNKNOWN
  source_song_id: UNKNOWN
  source_display_name: UNKNOWN
  source_creator_display: UNKNOWN
  source_account: UNKNOWN
  source_playlist: UNKNOWN
  source_generation_model: UNKNOWN
  source_labels: UNKNOWN
  source_created_timestamp: UNKNOWN
  style_description_ref: UNKNOWN
  lyrics_ref: UNKNOWN
  artwork_reference: UNKNOWN
  observed_at: REQUIRED_CAPTURE_TIME
```

Guidance:

- Keep exact observed strings and identifiers; do not normalize labels or convert a display name into an account or legal-owner field.
- `source_display_name` is the account/profile display name; `source_creator_display` is the credit shown for the specific work. They may match but are not interchangeable.
- `source_playlist` preserves the displayed value `1776` as observed. Do not coerce it to a number or treat it as a repository classification.
- Preserve `source_created_timestamp` as shown, including timezone/precision if available. Keep `observed_at` separate: source creation time and repository observation time answer different questions.
- Keep the source's style description and lyrics as separately addressable assets/references. The snapshot can retain their source references and capture metadata without embedding all text in the snapshot object.
- A later observation or correction should append a new snapshot/observation with its own time and source, not silently rewrite the earlier snapshot.
- For a practical first version, keep the snapshot in the existing provenance artifact or the same canonical record boundary after the model is approved. Do not create a database or a proliferation of files just for this workflow.

The screenshot-visible **Reuse Styles** and **Reuse Lyrics** affordances are evidence that style description and lyrics are separate source items. They are not permission to overwrite source evidence, and they do not make either item equivalent to the prompt.

## Creator Intent and Creative Constraints

Keep the two groups separate:

| Creator Intent | Creative Constraints |
|---|---|
| What the creator wants to make or communicate: `source_material_type`, `genre_target`, `style_target`, `voice_target`, `tempo_target`, and `project_purpose`. | Requirements or exclusions that shape generation: for example, `creative_constraints.exclude_styles`. |

Preserve the creator's exact wording, source, and capture time. Treat intent as immutable historical evidence: a clarification or revision is a new attributed statement, not an overwrite. Prompt analysis can propose an interpretation separately, but must not turn its inference into a creator-authored target. Source `style_description` and `source_labels` are source metadata, not automatically creator intent.

## Source Labels

Store `Dark Electronic Hip-Hop` exactly as observed in the screenshots under raw `source_labels`. Do not normalize its spelling, replace it with taxonomy terms, or automatically classify it. Any later taxonomy mapping should be optional, separately attributed, versioned, and displayed beside—not instead of—the original label.

Apply the same rule to future platform or creator labels. Keep the label's origin clear (source platform, creator, or other source). A label does not prove that the generated audio matches it and is not a founder review conclusion.

## Creator, Project Owner, Source Account, Artist, and Performer

The current `creator` field is ambiguous. `Christopher Bower` is shown as a creator display name on the Suno source, but that one string should not stand for several relationships:

- **Creator display/credit:** the exact work-level attribution shown by the source.
- **Project owner:** the explicitly established owner of the repository project or rights; not inferred from a source profile.
- **Source account:** the platform account/profile that published the work.
- **Assigned artist:** a separate roster assignment made by a curator; it may be absent.
- **Performer:** the person or voice that performed the recording; not established by a creator credit.

Christopher may act as founder, operator, reviewer, and curator in this single-operator workflow. Capture those actions under one operator identity where needed; do not reuse the work's creator field to record the operator role. The same person may occupy multiple roles, but the roles remain conceptually separate.

## Repository Identity and Title

`demo_id` is the authoritative repository identity and stable link key. `Carillon` is a mutable working/source title. Present the working title prominently for readability and keep `DEMO-2026-0001` visible nearby at all times. Store source-displayed title separately if it differs. A title change updates the current working title while preserving history and must not create a new demo or break review/provenance links.

## Workbench Layout Recommendations

Recommended display sequence:

1. **Repository Identity:** working title, persistent demo ID, compact intake/review state.
2. **Source Context:** source platform, URLs/item ID, creator display/account, playlist, source creation timestamp, model, and artwork reference.
3. **Creative Context:** prompt, style description, and lyrics as separate assets; put prompt and exclusions near the top because they guide review.
4. **Creator Intent:** explicit positive targets and purpose, with evidence/source labels.
5. **Creative Constraints:** excluded styles and other negative requirements, visibly distinct from intent.
6. **Source Labels:** exact raw source labels, then optional separate mappings.
7. **Review Readiness:** audio received/access status, evidence present/missing, why review is blocked, and next founder action.
8. **Governance State:** review result, classification, seed, disposition, and rationale; do not lead with these.
9. **Preservation Metadata:** an at-a-glance audio/preservation status near readiness, with checksum, integrity, and archive details under expandable **Preservation Details**.

The first screen should make source and creative context available without opening repository YAML. Long prompt/lyrics can be expandable, but show an obvious preview and availability state. Checksum, archive metadata, and integrity details remain accessible but should not displace the creative material needed for initial review.

## Founder Workflow Recommendations

1. Open **Add Demo** and receive an automatically assigned `demo_id`.
2. Add one source locator (URL, local file, or archival reference); capture `observed_at` automatically.
3. Record the visible source metadata into `source_snapshot`, preserving exact strings. If copying every field would slow intake, capture the source URL and the high-value source fields first, then mark the remaining values `UNKNOWN` for follow-up.
4. Store prompt, style description, lyrics, and constraints separately or link to their source assets. Do not transcribe unavailable content or create duplicates without a preservation need.
5. Save the demo as intake-incomplete if any important evidence is missing. Show a short checklist of missing audio/source material and the next action.
6. Review the audio when available. Keep audio-dependent grades `N/R` until listened to; do not treat source metadata as an audio evaluation.
7. Leave classification, seed, and disposition for their existing review gates. Do not make the intake form a decision form.

For one founder-operator, keep the routine to one capture pass and one review pass. Prefill stable repository context and avoid repeated operator-role selection, multi-stage approval, public-submission controls, and automation that adds more work than it removes.

## Write-Back Assessment

**NOT READY for workbench write-back.** This does not mean Demo 0002 must wait for an enterprise system; a founder can use a simple repository-backed manual intake while the workbench remains read-only.

| Readiness area | Current assessment |
|---|---|
| Field ownership | Not yet encoded. This proposal separates repository identity/governance, observed source metadata, creative assets, creator intent/constraints, and founder review. |
| Canonical vs observed metadata | Not represented cleanly. The screenshot observations are absent from canonical intake, and the current `creator`/`audio_location` fields are ambiguous. |
| Source snapshot | Concept only; no immutable snapshot field/file format or capture rule exists yet. |
| Validation | No approved schema or validation rules for the proposed fields, asset references, required source locator, or append-only observations. |
| Audit | Git history exists, but no enforced actor/time capture or protection against overwriting source observations is in place. |
| Write path | The prototype is read-only and has no authentication or repository update mechanism. |

Before any UI write-back, approve the small field model, decide where the source snapshot and separate assets live, validate references and required values, preserve an inspectable change history, and require a human-reviewed repository diff. Do not add a multi-tenant backend or workflow engine to meet this bar.

## Simplification Opportunities

- Use one founder intake form and a single operator context.
- Generate the stable ID automatically; avoid asking for classification or disposition on intake.
- Make source/creative metadata optional where sources do not provide it; make unknowns explicit.
- Store one small snapshot and link to source assets rather than copying the same text into multiple records.
- Keep source and creative material ahead of review/governance fields in the workbench.
- Defer taxonomy mappings, advanced archive detail, external-contributor processing, public intake, roles/permissions, GitHub Actions, and automated writes.
- Keep the existing repository as the system of record and the workbench read-only until the minimal field model and validation are agreed.

## Demo 0002: Practical Defaults

| Question | Recommendation |
|---|---|
| What should the intake screen look like? | One source-first form with auto-assigned demo ID, source locator, compact source snapshot, separate prompt/style description/lyrics/constraints, and a clear save-as-incomplete path. |
| What is required? | Stable `demo_id`, one source locator or explicitly pending-source draft, and automatically captured `observed_at`. |
| What is optional? | Title, platform IDs/account/playlist/model, prompt, style description, lyrics, creator intent, constraints, labels, artwork, and asset preservation data when the source does not provide them. |
| What should be captured? | Every useful observed source value verbatim, its source, capture time, and separate references for reusable creative assets. |
| What can wait? | Audio checksum/archive details until preservation; rights conclusions until review; taxonomy mapping, classification, seed, disposition, assignment, and development decisions until their governed stages. |
| What can remain `UNKNOWN`? | Any source or intent field not evidenced, plus ownership/rights, performer/artist assignment, review outcomes, and preservation values for assets not received. |

## Scope and Validation

This is a documentation-only recommendation based on the founder's screenshot observations, the current DEMO-2026-0001 records, the [workbench refinement](./workbench-refinement-demo-0001.md), and existing intake/review governance. It does not update the canonical record to add screenshot values and does not modify schemas, taxonomy, workbench code, or write-back behavior.
