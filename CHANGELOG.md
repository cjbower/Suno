# Changelog

All notable changes to Suno Studio repository are documented in this file.

---

## [Unreleased] – 2026-11-20

### Phase 2B.0 – Roster Normalization

- Separated solo artists, bands, and producer projects into distinct roster locations.
- Added entity-specific development templates and updated affected paths and metadata references.
- Added the roster-normalization report.

### Phase 2B.1 – Artist Name Remediation

- Applied the two approved artist-name replacements to roster folders, metadata identifiers, and references.
- Added the name-remediation report; collision evidence for the replacements was not independently rerun.

### Phase 2B.2 – Voice Architecture Foundation

- Added the voice architecture framework, governance principles, and registry assessment.
- Documented existing voice-registry gaps without modifying voice metadata or assigning voices.

### Phase 2B.4 – Demo Intake and Audience Research Operations

- Added documentation-only demo intake, A&R evaluation, disposition, and development-handoff standards, with schema examples and no demo records.
- Added audience-research governance, survey and session standards, privacy guidance, and response/session schema examples, with no participants or responses.
- Defined cross-domain authority boundaries and updated repository indexes and the durable handoff.
- No audio, artist assignments, surveys, recruitment, external submissions, contracts, or releases were created or activated.

### Phase 2B.5 – Strategic and Platform Research Integration

- Integrated the platform thesis, Suno research, AI-artist strategy, and Spotify for Artists operations references in their authoritative domains with explicit authority and verification metadata.
- Added domain indexes, recorded the approved platform decision, and updated the durable handoff and intake report.
- Kept the proposed AI-artist operating model and all operational recommendations unapproved; no roadmap actions, accounts, contracts, releases, commits, or pushes were created.

### Phase 3.0 – Initial Demo Intake

- Added a provisional intake and review record for the first user-supplied Suno demo link, with unknown evidence preserved explicitly and audio-dependent criteria marked N/R.
- Recorded a hold disposition pending original audio, provenance, and founder listening review; no development, artist assignment, audience research, or release was authorized.
- Additional demos and local audio files remain pending; Phase 3.0 inventory is incomplete.

### Suno Object Model Discovery (2026-11-24)

- Added a read-only inventory of song, workspace, and playlist fields exposed through the Suno MCP connector.
- Documented tested capabilities, tool-advertised behavior, and unverified operations while preserving uncertainty about Replace and project relationships.
- No Suno songs, workspaces, playlists, projects, or visibility settings were changed during this discovery.

### Voice-ID-Validation Experiment Registry (2026-11-24)

- Formalized the existing four-clip control/treatment test as Voice-ID-001 in a dedicated experiment registry.
- Recorded verified generation metadata findings separately from pending human listening evidence; the audible effect remains undetermined.
- Added a human-evaluation placeholder and backlog entries for a v6-mini replication, speech comparison, Nebraska anthem comparison, and cover comparison.
- This documentation-only update generated no audio, modified no songs, and ran no new experiment.
### Voice Experiment Export and Persistence Validation (2026-11-24)

- Validated the saved Voice-ID-001 JSON export against the serializer: valid JSON, four `context.assets` array entries, ID-consistent Suno URL paths, and explicit `null` values for unanswered fields.
- Preserved the export as an unchanged timestamped snapshot and set the canonical human-evidence status to `Recorded`; the exact observation remains “The output is obvious.”
- Documented that the browser initiates a Blob download but does not write to repository sources, and that the immediate UI success message does not confirm the browser saved the file.
- Added current persistence findings, a repository-first recommendation, and a shared-envelope/workflow-specific schema recommendation. No write-back, schema validator, new experiment, or Suno operation was implemented.
### Voice-ID-001 Repository Writeback Proof-of-Concept (2026-11-24)

- Added free-form listener-name entry with type-ahead suggestions from the existing listener and prior Voice-ID-001 submissions; names remain evaluation metadata, not authenticated identity.
- Added local, loopback-only Vite development writeback, limited to the Voice-ID-001 YAML record and its registry/report.
- Recorded each submission's timestamp, listener name (`user`), modified fields, previous/new values, and complete answer snapshot; generated a unique JSON snapshot without overwriting the earlier export.
- Kept founder reviews, A/B/focus-group workflows, discovery intake, and production builds outside the writeback scope. No evaluation was submitted during implementation.
### Evaluation Platform Design Principles (2026-11-24)

- Accepted Voice-ID-001 as an alpha repository-backed evaluation proof-of-concept, not as the final persistence model.
- Documented that future workflows should distinguish current evaluation state, append-only audit history, and evidence snapshots.
- Deferred broader persistence decisions until Founder Review writeback, A/B Testing, Focus Groups, or Discovery Intake require them.
### Voice-ID-001 Human Evaluation Workflow (2026-11-24)

- Added a distinct Voice Experiment Review view to the local Founder Review workbench with control/treatment Suno links, metadata evidence, human observation provenance, and structured evaluation questions.
- Added an export-only JSON form; it does not write to repository files or a backend. The existing observation is prefilled exactly, while unreported answers remain empty.
- Preserved “The output is obvious.” as completed human listening evidence from Christopher Bower without inferring answers about identification, pronunciation, pacing, realism, timbre, strength, or reuse.
- Added a canonical structured voice-experiment YAML source and updated the registry, indexes, and architecture documentation.
- Documented A/B Focus Group Evaluation, New Music Discovery Intake, and Founder Triage as future-only workflows; none were implemented.
- No audio was generated, no songs were modified, and no new experiments were run.

## [2.0.0] – 2026-11-18

### Added (Phase 2A – Repository Scaffolding)

#### Artist Roster Framework
- 12 individual artist profiles with complete documentation scaffolding
- 6 band profiles with creative direction documentation
- 2 producer projects (Meridian, Foundry)
- Each artist: 6-document framework (profile, development plan, production DNA, themes, discography, album history)
- Each band: 5-document framework (profile, creative direction, production DNA, themes, discography)

#### Metadata Schemas
- 6 YAML canonical registries created
  - `artists.yaml` – All 12 artists registered
  - `bands.yaml` – All 6 bands registered
  - `albums.yaml` – Album registry with 3 reserved albums (Fortress, Republic, Watchman Vol. 1)
  - `songs.yaml` – Song registry (framework)
  - `voices.yaml` – 12 voice profiles with schema
  - `motifs.yaml` – Motif registry (framework)

#### Creative Governance
- `creative/identity-framework.md` – **Core principle:** Source Material → Emotional Objective → Artist Assignment → Genre Selection
- `creative/artist-development-template.md` – Artist documentation framework
- `creative/genre-portfolio.md` – 23 genres documented with industry context (historical count; the portfolio currently enumerates 22)
- `creative/production-style-guide.md` – Production standards
- `creative/vocal-style-guide.md` – Vocal production guidelines
- `creative/motif-library.md` – Motif catalog framework
- `creative/release-standards.md` – Quality checkpoints

#### Catalog Organization
- `catalog/albums/` – Album project structure
- `catalog/repertoire/` – 7 source material categories
  - Psalms
  - Daily readings
  - Revolutionary War documents
  - Historical documents
  - Virtue literature
  - Saints' lives
  - Poetry

#### Operations Framework
- `operations/roadmap.md` – Strategic planning
- `operations/release-calendar.md` – Release scheduling
- `operations/workflow-notes.md` – Workflow documentation
- `operations/automation-opportunities.md` – Automation planning

#### Governance
- `docs/decision-log.md` – Decision recording framework with foundational decisions
- `docs/phase-2a-validation-report.md` – Comprehensive validation and structure verification

#### Archive Structure
- `archive/retired-artists/` – Retired artist preservation
- `archive/superseded-prompts/` – Old prompts archive
- `archive/rejected-concepts/` – Rejected ideas archive

#### Documentation
- Updated `README.md` – Complete repository overview
- Updated `CHANGELOG.md` – This file

### Documentation Notes

- All 108 files created with structure and placeholders
- **Zero fictional content** – All unknown information marked [PLACEHOLDER]
- **No existing files modified** – Original manifesto and V2 preserved
- **All cross-references verified** – Relative paths consistent throughout
- **Consistent naming** – Artist folders use kebab-case; YAML uses snake_case

### Validation Results

- ✅ 40 directories created
- ✅ 102 markdown files created
- ✅ 6 YAML schemas created
- ✅ All artist scaffolding complete (12 artists × 6 files = 72)
- ✅ All band scaffolding complete (6 bands × 5 files = 30)
- ✅ All cross-references verified
- ✅ Internal consistency verified

---

## [1.0.0] – 2026-11-18

### Added (Phase 1 – Manifesto Reconciliation)

- `foundations/AI_Music_Project_Manifesto_and_Notes_v2.md` – Expanded, reconciled manifesto with 16 documented sections
- `docs/manifesto-delta-report.md` – Report of preserved, expanded, and new concepts
- `docs/validation-report.md` – Internal consistency review

---

## Prior History

- Original repository established with initial manifesto (AI_Music_Project_Manifesto_and_Notes.md)
- Phase 1 completed with Manifesto V2 and delta report
- Ready for Phase 2B content population

---

**Version:** 2.0.0 (Phase 2B changes documented as unreleased)

**Status:** Phases 2B.0–2B.2 are committed locally; human review is required before any push.

**Next Phase:** Follow the future work and open decisions in `docs/durable-handoff.md`.
