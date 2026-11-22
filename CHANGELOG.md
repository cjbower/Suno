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
