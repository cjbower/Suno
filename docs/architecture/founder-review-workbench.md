# Temporary Founder Review Workbench

**Status:** Phase 3.1A workflow-discovery artifact. The existing browser prototype remains under [`portal/`](../../portal/) and is reclassified as a temporary, read-only workbench. It is not the final portal, is not deployed, and may be discarded after workflow learning.

## Purpose

Use the existing portal prototype to observe demo intake and founder review work against real repository records. The goal is to learn which information and actions are useful, where manual work is repeated, which fields are missing, and which future automation merits investment.

The repository remains the sole source of truth. This workbench is an experimental interface layer over the existing YAML registries; it does not own approvals or records.

## Goals and Discovery Questions

During real use, capture evidence for:

1. What information does the founder open or consult repeatedly while reviewing a demo?
2. Which fields are difficult to find, interpret, or update in the repository?
3. Which actions are repeated across YAML and Markdown records?
4. Which choices are ambiguous, and what decision rules are missing?
5. What interruptions, rework, or validation errors occur?
6. Which future automation would remove mechanical work without replacing editorial judgment?

The first DEMO-2026-0001 use exposed a source-first information need: the founder sought source and creative context before repository governance. Screenshot-observed source attributes include a playlist, generation model, source label, style description, lyrics, and creation timestamp; these observations are not all present in the canonical demo record. This is one qualitative workflow observation, not a measured multi-demo usability study, and no completed founder listening review is recorded.

## Current Prototype

The workbench reuses the existing source under `portal/`; no separate `workbench/` copy is needed or created.

| Area | Current capability |
|---|---|
| Dashboard | Counts canonical demos, pending reviews, complete reviews, and classification-eligible records |
| Demo intake | Read-only summary of source, intake state, and required evidence |
| Demo queue | Search and filter records by review state |
| Demo detail | Presents source context, creative material, creator intent, constraints, source labels, readiness blockers, governance, and advanced metadata in founder review order |
| Review state | Derived from linked review data; no state is written back |
| Classification and seed | Displays current values and gate state; does not decide or edit them |
| Disposition | Displays the current disposition; does not recommend or change it |

The current registry contains `DEMO-2026-0001` (`Carillon`) with `current_disposition: hold`, `review_status: intake_incomplete`, and primary classification and seed values `UNKNOWN`. Its linked `REVIEW-2026-0001` is an AI intake screen, `founder_review_status: pending`, `audio_reviewed: false`, and its audio-dependent grades are N/R. The UI therefore shows Review Pending and zero Review Complete or Classification Eligible records. Source metadata not captured in canonical YAML is shown as `UNKNOWN` with a clear not-captured explanation; screenshot observations are not hardcoded into the UI.

The application imports the canonical `demos.yaml` and `demo-reviews.yaml` as raw build inputs, parses them with `js-yaml`, and derives the interface state in memory. A built bundle is a disposable snapshot; it is not an editable record. The current review gate is intentionally conservative: complete founder status, founder reviewer role, known reviewer ID, parseable review date, audio reviewed, at least one rateable grade, and written non-N/R category evidence. `Classification Eligible` means only that this prerequisite gate is met; it does not assign a value.

Current code and operating instructions are in [`portal/README.md`](../../portal/README.md), [`portal/src/main.js`](../../portal/src/main.js), and [`portal/src/review-state.js`](../../portal/src/review-state.js). The prototype is local-development software. It has no authentication, backend, database, write-back, deployment workflow, or production hosting configuration.

## Review Modes and Workflow Boundaries

| Mode | Purpose | Status and boundary |
|---|---|---|
| Demo Intake | Record source facts, provenance, identifiers, and missing evidence | Existing read-only view; does not evaluate creative quality or approve submissions |
| Founder Review | Evaluate an eligible demo using the approved review standard | Existing queue/detail workflow; separate from experiment evaluation and gated classification |
| Voice Experiment Review | Capture structured human evidence for a controlled generation experiment | Voice-ID-001 has a local writeback exception; no other experiment or review workflow can write |
| A/B Focus Group Evaluation | Conduct blind comparisons, collect preference rankings, and aggregate results statistically | Future placeholder only; no participants, sessions, or aggregation are implemented |
| New Music Discovery Intake | Maintain a personal review queue, categorize music, recommend a workspace, and record Archive / Reject / Promote triage | Future placeholder only; does not replace demo intake or change catalog membership |
| Founder Triage Workflow | Prioritize and route work for founder attention | Future placeholder only; not a formal demo review, experiment evaluation, or approval gate |

Voice Experiment Review is an evidence-capture workflow, not a music discovery queue or audience study. Focus group testing would require a separately designed participant process, blinding method, preference instrument, privacy handling, and statistical plan before implementation.

## Workflow Analysis

For each workflow, the manual activities are drawn from existing standards and current records. Repetition and pain points remain hypotheses until the founder uses the workbench and records observations. Automation candidates below are ideas for later prioritization only.

### 1. Demo Intake

- **Current manual activities:** Receive a source reference; confirm the active submission class; identify title, creator attribution, platform ID, and source URL; preserve provenance and known unknowns; assign an immutable demo ID; create/update YAML and supporting Markdown records; record missing audio and rights evidence.
- **Pain points to validate:** Source facts, provenance, review status, and next actions are split across registries and per-demo files. YAML structure and manual links require repository editing. Public-page data may be mistaken for rights or creative evidence.
- **Repetitive actions:** Copy identifiers and URLs into multiple records, preserve exact `UNKNOWN` values, check the next unique ID, and verify cross-links.
- **Automation candidates:** Guided intake checklist, duplicate-ID detection, URL/identifier consistency checks, completeness summary, and template generation that leaves unknowns unknown.
- **Future validation opportunities:** Required field presence, unique stable IDs, valid submission types, source URL integrity, linked record existence, and explicit evidence for non-UNKNOWN facts. Keep the classification/seed gate closed at intake.

### 2. Founder Review

- **Current manual activities:** Locate and audition the original audio, review source and rights context, grade criteria using the review standard, write evidence for each grade, preserve N/R when evaluation is not fair, identify strongest/weakest elements, and record reviewer, date, and completion state.
- **Pain points to validate:** The review template and canonical review registry are YAML-shaped; audio and provenance are separate from the review form; the current AI intake record is not a founder review and has no auditioned audio.
- **Repetitive actions:** Reopen the same source and provenance links, enter grades and evidence criterion by criterion, and repeat reviewer/date/ID fields.
- **Automation candidates:** Evidence-focused worksheet, missing-field checklist, N/R reason prompts, links to audio and provenance, and a queue of pending reviews.
- **Future validation opportunities:** Allowed grades only, written evidence for every grade, reviewer identity/date, explicit founder completion, and evidence-backed handling of N/R. Automated checks must not grade creative quality.

### 3. Classification

- **Current manual activities:** After a documented founder review, choose supported primary/secondary classification values and record a written rationale. The current demo remains `UNKNOWN`.
- **Pain points to validate:** The registry describes classification fields but does not publish an explicit allowed-value taxonomy or link a classification rationale to a specific review record.
- **Repetitive actions:** Recheck review completion, reread evidence, copy rationale into the demo registry, and confirm the value is consistent with the decision.
- **Automation candidates:** A post-review worksheet that presents evidence and controlled values, records rationale, and shows a proposed YAML diff.
- **Future validation opportunities:** Block non-UNKNOWN classification before qualifying review; validate chosen values against an approved taxonomy; require a rationale and evidence reference. Do not infer a value from a title, lyrics, or score.

### 4. Seed Qualification

- **Current manual activities:** Separately assess reusable strategic value and development potential after review, then record `seed_designation` and `seed_rationale` when evidence supports them. Current values remain `UNKNOWN`.
- **Pain points to validate:** The metadata fields exist, but the registry does not define an explicit seed-value taxonomy, criteria, threshold, or distinct evidence schema.
- **Repetitive actions:** Revisit the demo and review evidence, distinguish seed value from song classification, and preserve a separate rationale.
- **Automation candidates:** A worksheet with approved criteria, evidence references, and a reasoned result; side-by-side comparison may be considered only after the method is approved.
- **Future validation opportunities:** Require completed founder review, explicit seed criteria and controlled values, evidence and rationale; keep a negative or unresolved result distinct from `UNKNOWN`.

### 5. Disposition

- **Current manual activities:** Select a disposition from the A&R standard, document rationale, owner, bounded next action, required evidence, review trigger, and risks. The current demo is on hold pending original audio and provenance.
- **Pain points to validate:** Disposition, next action, risks, and required evidence live in the registry while the bounded hold plan is a separate Markdown artifact.
- **Repetitive actions:** Keep the plan and registry synchronized, copy the trigger and required evidence, and check that a nonterminal outcome has an owner.
- **Automation candidates:** Disposition worksheet, required-field checks, consistency check against the per-demo plan, and a concise handoff summary.
- **Future validation opportunities:** Restrict values to the approved disposition list; require the nonterminal fields; distinguish recommendation from approval; prevent a disposition from implicitly authorizing development, assignment, research, or release.

### 6. Future Artist Assignment

- **Current manual activities:** No assignment is currently authorized. A future review would compare source and emotional fit, repeated creative characteristics, voice/production continuity, rights conditions, and reproducibility against existing solo artists, bands, or producer projects. Human approval and any later Development Brief remain separate.
- **Pain points to validate:** Fit evidence is distributed across artist profiles and creative frameworks; there is no approved matching taxonomy or single view of candidate evidence. One demo cannot establish repeatability.
- **Repetitive actions:** Search artist profiles, compare documented traits, return to source material, and record counter-evidence and limitations.
- **Automation candidates:** Searchable reference links and side-by-side evidence presentation. Do not auto-rank or assign artists without an approved decision method.
- **Future validation opportunities:** Ensure the selected entity exists, require written fit and counter-evidence, record explicit human approval, and keep `assigned_entity_*` unknown until authorized. Assignment must not create an artist or start development.

## Workflow Observation Method

Record observations during actual work without adding a second application database. A temporary session note can capture:

| Observation | What to record |
|---|---|
| Workflow and demo ID | Which task was being performed |
| Information used | Repository fields and linked documents actually opened |
| Actions and repetition | Copying, searching, switching files, and repeated entry |
| Friction | Confusion, missing fields, invalid values, or rework |
| Time and outcome | Approximate duration and whether the task completed |
| Automation candidate | Mechanical action that could be reduced, not editorial judgment to be delegated |
| Confidence | Observed fact or unverified hypothesis |

Do not add personal listening notes or sensitive material to an unapproved telemetry or analytics service. The goal is qualitative workflow learning; no tracking is implemented.

## Data Integration

### Current Structure

| Registry | Current shape | Workbench use |
|---|---|---|
| `catalog/metadata/demos.yaml` | `schema_reference`, `schema_example`, and `demo_records`; each demo includes identifiers, provenance pointers, lifecycle/disposition, classification/seed fields, required evidence, risks, and next action | Supplies demo identity, intake state, current values, and links |
| `catalog/metadata/demo-reviews.yaml` | `schema_reference`, `schema_example`, and `review_records`; reviews link by `demo_id` and include reviewer fields, letter grades, N/R evidence, category evidence, and founder-review status | Supplies linked review state and written evaluation evidence |
| Per-demo Markdown | Profile, evaluation, provenance, and bounded disposition plan | Supporting records opened by repository links; not parsed as a second index |

### Strengths

- YAML is already the canonical registry and is versioned with the source repository.
- Stable IDs and explicit `UNKNOWN` values make incomplete evidence visible.
- Demo and review records are separated while linked by `demo_id`.
- The existing review fields carry category evidence and distinguish an AI intake screen from founder review.
- Repository diffs provide an inspectable history of source changes.

### Weaknesses and Missing Structure

- YAML shape is documented but not enforced by a schema validator in the current workflow.
- Cross-file links and parallel Markdown records require manual consistency checks.
- Classification and seed fields have no published controlled-value lists or explicit decision criteria.
- Classification/seed rationale is on the demo record, without a direct review ID/evidence reference.
- Review completion and classification eligibility are derived in UI code rather than a canonical field; that is appropriate for a read model but the rule must stay documented and tested.
- The portal currently embeds a build-time snapshot; users can mistake stale displayed data for current repository state.
- Current data is too small to establish frequent actions or a stable queue design.

### Future Read Model

Keep a derived, in-memory read model rather than a second persistent registry. It should join demos to reviews by immutable IDs and expose source provenance, current disposition, outstanding evidence, latest founder-review status, and the reason a gate is pending or open. Future builds should identify the source commit or generation time so stale snapshots are detectable. Controlled taxonomies and validation rules need approval before being encoded.

### Future Write Model

No write capability is implemented. A future write model should draft changes to the existing YAML and required Markdown records, validate them, and submit a reviewable repository change rather than maintaining a parallel database. It should use least-privilege GitHub identity, a non-main branch, and a pull request; never place a personal access token or app secret in browser code. Repository validation and human approval remain authoritative.

## Current Persistence Architecture

The canonical structured experiment record is `catalog/metadata/voice-experiments.yaml`. The browser reads it as a Vite raw input. For Voice-ID-001 only, a local development-server endpoint validates and writes submissions to that YAML and the two corresponding Markdown records. All other views remain read-only.

```text
voice-experiments.yaml
        │ Vite import + js-yaml parse
        ▼
Voice-ID-001 view + listener-name suggestions
        │ validate form + source revision
        ▼
Loopback-only Vite endpoint
        │ update YAML + registry + experiment report
        ▼
Append-only audit + unique JSON snapshot → success status
```

The listener field is free-form with datalist suggestions derived from the initial listener and previous Voice-ID-001 submissions. Its value is evaluation metadata only; it is not authenticated, authorized, or linked to an account. Each submission stores a timestamp, listener name (`user`), modified field names, previous values, new values, and the complete structured-answer snapshot.

The endpoint accepts only the literal experiment ID `Voice-ID-001`, uses fixed repository paths, rejects stale revisions, invalid values, non-loopback requests, and cross-origin POSTs, and is registered only with Vite's development server. The endpoint is not included in production builds. Repository writes are in the working tree; a Git commit remains necessary for durable version-control history.

### Historical Export Validation (2026-11-24)

- The saved [Voice-ID-001 evaluation export](../../research/suno-platform/experiments/voice-id-001-evaluation-2026-11-24.json) parses as JSON and exactly matches serializer output reconstructed with its captured form values, `exported_at`, and export-time status (`Completed`).
- `context.assets` is an array containing four asset objects. Each `song_url` is syntactically valid, uses `https://suno.com/song/`, and ends with the corresponding `song_id`. This validates structure and URL/ID consistency, not live Suno availability or access.
- Unanswered choice and comment fields are serialized as JSON `null`; the one-sentence conclusion preserves exactly “The output is obvious.” The observation itself is included separately. No additional evaluation answer is present.
- The export is a timestamped snapshot. It recorded `listening_status: Completed`; the canonical status is now `Recorded`. The historical export remains unchanged, and the observation and unanswered fields were left intact.
- No standalone JSON Schema is published. Conformance was checked against the producer function and canonical YAML shape; schema-version validation is therefore application-contract validation, not validation against an independent formal schema.

### Historical Save Dialog and Download Evidence

The prior export-only page created an `application/json` Blob, created an object URL, placed it on an anchor with the `download` filename `voice-id-001-evaluation-2026-11-24.json`, clicked the anchor, and revoked the object URL on a zero-delay timer. It did not call `showSaveFilePicker`, a native dialog API, or a repository filesystem API. A macOS Save dialog was therefore browser/host download handling, commonly shown when the browser is configured to ask where downloads should be saved; this workspace's browser preference was not independently inspected.

The exported file exists under the repository's experiment directory. Its filesystem modification time (`2026-11-24 16:24:17 PST`) matches the export timestamp (`2026-11-25T00:24:17.657Z`) to the same displayed second, which is evidence that a download was saved at that time. The file is currently untracked, so it is in the working tree but not yet part of Git history. The app itself did not update repository sources before or during export. Source YAML and experiment docs predate the export and supplied the persisted context; no new structured listening answer was added by this export.

The previous UI wrote “Assessment JSON downloaded” immediately after `link.click()`. That reported initiation, not confirmation that the browser saved a file. The earlier Playwright download-event check timed out, so that attempt alone could not establish success or failure; Playwright download handling requires observing the browser download event and saving/inspecting its artifact, and it does not reliably expose a native macOS Save dialog as a page element. The file and timestamp evidence provide separate confirmation for this export. The browser may either prompt for a destination or save to its configured download location; if download handling is blocked, the old UI's immediate success text could still appear.

## Repository-First Evaluation Workflow

The Voice-ID-001 proof-of-concept implements the repository-first sequence below. The previously saved dated export remains unchanged; every new writeback creates a unique snapshot.

```text
Voice Experiment Review
        ↓
Validate inputs and source revision
        ↓
Update Voice-ID-001 YAML + Markdown
        ↓
Generate unique JSON snapshot
        ↓
Show success status
```

The form submits to the local API; it does not write files from browser code. There is no generalized repository writer, authentication, or deployment. This exception does not enable writes for founder reviews, focus groups, A/B tests, or discovery intake.

## Evaluation Persistence Design Principles

**Status: Accepted**

Voice-ID-001 is the first repository-backed evaluation workflow and is accepted as an alpha proof-of-concept. It validates repository writeback, evaluation capture, listener tracking, and evidence preservation; it does not establish the final persistence model.

Future evaluation workflows should distinguish:

1. **Current Evaluation State** - the active answers and status for an evaluation.
2. **Audit History** - an append-only history of evaluation events and their provenance.
3. **Evidence Snapshots** - preserved snapshots of the evaluation and supporting evidence.

This separation is a design principle for future workflows, not a claim that the current Voice-ID-001 implementation stores these as independent models. Its current save behavior remains alpha behavior and may be redesigned before broader adoption.

Review persistence semantics when Founder Review uses writeback, A/B Testing is implemented, Focus Groups are introduced, or Discovery Intake stores evaluations. Do not generalize the Voice-ID-001 proof-of-concept to those workflows without that review.

## Reusable Evaluation Schema Recommendation

Use a small shared envelope with a workflow discriminator and separate versioned payload schemas. Do not force all evaluation types into one flat record.

| Workflow | Shared envelope fields | Workflow-specific fields |
|---|---|---|
| Voice experiment | Stable evaluation ID, schema version, workflow type, experiment reference, evaluator/source, date, status, evidence/asset references, responses, provenance | Control/treatment assignment, generation model/settings, voice parameter presence, per-criterion vocal observations |
| A/B song testing | Stable evaluation ID, schema version, workflow type, study/trial reference, participant pseudonym, date, status, evidence references, responses | Blind stimulus labels, randomized presentation order, preference choice/ranking, confidence, repeated-trial data |
| Focus group | Stable session/evaluation ID, schema version, workflow type, study/session reference, date, moderator, evidence references, status | Participant pseudonyms, consent state/reference, individual response attribution, discussion notes, aggregation method and cohort results |
| New music discovery intake | Stable evaluation ID, schema version, workflow type, asset reference, reviewer, date, status, evidence/provenance, responses | Categorization, workspace recommendation, Archive / Reject / Promote disposition, rationale, follow-up owner |

Common response records should retain a stable question/criterion ID, typed answer, optional comments, and explicit unanswered/null semantics. Workflow payloads should own their controlled choices and validation rules. Focus-group identity and consent material require a separate privacy decision and should not be placed in a public repository by default. This schema family remains a design recommendation only; no shared platform, schema validator, focus group, or discovery intake is implemented.

## Technology Recommendation

Keep Option A for this temporary exercise: plain HTML, CSS, and JavaScript with the existing Vite local server/build and `js-yaml` parser. Modify the existing prototype rather than scaffolding a new `workbench/` application.

| Option | Complexity | Maintainability | Cost | Repository friendliness | Temporary-workbench tradeoff |
|---|---|---|---|---|---|
| A. Static HTML/CSS/JavaScript (existing prototype) | Lowest incremental cost; code already exists | Easy to change in small files | Free local use | Reads canonical YAML directly | Best fit; discardable without framework migration |
| B. React static app | Adds component framework and conventions | Strong for a larger interactive product | Free local use; hosting depends on later choice | Needs build and package structure beyond this prototype | Premature; adds setup without improving workflow discovery |
| C. Markdown/YAML templates plus a small local script | Minimal UI dependencies | Easy for batch summaries, weak for interactive queue/detail work | Free local use | Naturally repository-oriented | Alternative if browser interaction proves unnecessary; not as useful for observing navigation and task flow |

Avoid further visual polish, mobile optimization, authentication, deployment, or write-back in this phase. The prototype exists to test a workflow, not to establish a long-term product stack.

## Evolution Toward Founder Review Portal v1

1. **Phase 3.1A - temporary workbench:** Run locally against repository data; observe actual use; record friction and field gaps. Do not publish or write.
2. **Phase 3.1B - workflow findings and product boundary:** Review observations across several demos; approve a stable review worksheet, classification/seed taxonomies, gate definitions, and the minimum useful read model. Decide whether this prototype should be discarded or retained.
3. **Portal v1 design:** Define identity and authorization, public/private data exposure, stale-snapshot handling, accessible review queues, auditability, PR-based writes, and repository-side validation before selecting production architecture.
4. **Future implementation (not approved here):** GitHub Pages could host static assets; GitHub Actions could build, validate, and publish them. Validation workflows could check YAML schemas, IDs, references, allowed values, and governance gates. Review queues and automated reports could be derived from canonical records. Classification and seed workflows must remain gated and evidence-based. Write-back should propose pull requests, not commit directly to `main`.

No Pages configuration, GitHub Actions, deployment workflow, validation automation, authentication, API, database, or write-back is created by this phase.

## Validation Summary

- The existing portal source remains in `portal/`; this phase adds no second UI codebase or metadata source.
- The portal remains read-only. Source registries and demo/review records are not modified.
- No GitHub Actions, deployment configuration, or authentication implementation is added.
- The prototype's existing focused tests and build were previously validated; this documentation-only phase does not rebuild deployment output.
- The workflow analysis distinguishes repository-backed current facts from unconfirmed user-workflow hypotheses.

## Recommended Phase 3.1B

Conduct guided, time-boxed founder sessions with several real demos. Capture task sequence, information accessed, repeated entry, missing data, friction, and validation mistakes using the observation table above. At the end, approve or revise the workflows, field set, classification/seed criteria, and whether a permanent Portal v1 is justified. Do not begin write-back or deployment until that evidence and security design are reviewed.
