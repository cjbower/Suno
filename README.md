# Suno Studio

**Purpose:** Authoritative repository for Suno Creative Studio – a long-term AI-assisted music, podcast, publishing, and media studio.

**Scope:** Creative direction, artist roster, production standards, source material policy, catalog development, and operational governance.

---

## Project Overview

Suno Studio is a **label-based creative operation** with:

- **12 individual artists** in active development
- **6 bands and ensembles** organized by creative direction
- **2 producer-led projects** (Meridian, Foundry)
- **Catalog-first architecture** emphasizing artist identity persistence and long-term catalog building
- **Source material-driven** creative process (Scripture, poetry, history, literature adapted for contemporary music)
- **Contemporary production standards** comparable to mainstream commercial releases
- **Multi-genre support** with no genre constraints or exclusions

---

## Repository Structure

```
.
├── foundations/               # Manifestos and constitutional principles
├── docs/                      # Governance, decision log, validation reports
├── creative/                  # Production framework, style guides, identity framework
├── artist-roster/             # Solo artists, bands, producer projects
│   ├── solo-artists/
│   ├── bands/
│   └── producer-projects/
├── catalog/                   # Albums, repertoire, metadata
├── operations/                # Roadmap, release calendar, workflow
├── research/                  # Naming, platform, distribution, and AI-artist research
├── archive/                   # Retired artists, superseded concepts
├── CHANGELOG.md               # Version history
├── LICENSE                    # License information
└── README.md                  # This file
```

---

## Key Documents

### Foundational Strategy

- [AI_Music_Project_Manifesto_and_Notes_v2.md](foundations/AI_Music_Project_Manifesto_and_Notes_v2.md) – Complete editorial vision, artist roster strategy, genre portfolio, voice management, and long-term mission
- [Manifesto Delta Report](docs/manifesto-delta-report.md) – Changes from original manifesto to V2
- [Decision Log](docs/decision-log.md) – Recorded architectural and creative decisions
- [Human-Centered Knowledge Preservation Policy](docs/human-centered-knowledge-preservation-policy.md) – Preservation-first governance and founder approval requirements for destructive documentation changes
- [AI Music Platform Thesis](foundations/ai-music-platform-thesis-and-strategic-vision.md) – Foundational intent for a durable music-production and release platform
- [Adaptive Media Strategy and Governance](research/ai-artists/adaptive-media-strategy-and-governance.md) – Approved source-centered direction; companion formats and capabilities remain unactivated
- [Real-Person Voice Consent and Rights Governance](docs/real-voice-consent-and-rights-governance.md) – Explicit authorization and review gates; no voice assignments are created

### Creative Framework

- [Identity Framework](creative/identity-framework.md) – **Authoritative principle:** Source Material → Emotional Objective → Artist Assignment → Genre Selection
- [Artist Development Template](creative/artist-development-template.md) – Framework for documenting artist identity and evolution
- [Genre Portfolio](creative/genre-portfolio.md) – 22 currently enumerated genres with industry context and guidance
- [Production Style Guide](creative/production-style-guide.md) – Production standards and preferences
- [Vocal Style Guide](creative/vocal-style-guide.md) – Vocal recording and performance guidelines

### Research References

- [Suno Research Reference](research/suno-platform/suno-research-reference.md) – Primary consolidated, mixed-evidence Suno reference; preserve classifications and revalidate time-sensitive claims
- [Suno Object Model Discovery](research/suno-platform/suno-object-model-discovery.md) – Connector-exposed song, workspace, playlist metadata and capability evidence
- [Suno MCP Capability Matrix](research/suno-platform/suno-mcp-capability-matrix.md) – Point-in-time inventory of every advertised connector operation, parameters, evidence status, and unknowns
- [Suno Prompt Behavior Research](research/suno-platform/prompt-behavior.md) – Prompt findings, evidence limits, and links to preserved experiments; not a deterministic prompt standard
- [Suno Song and Workspace Metadata Discovery](research/suno-platform/experiments/suno-song-metadata-discovery-2026-11-24.md) – Read-only snapshot of Suno song metadata and workspace/Replace relationships
- [Suno Experiment Index](research/suno-platform/experiments/README.md) – Index of Suno platform experiments and registries
- [EXP-Voice-ID-Validation Registry](research/suno-platform/experiments/voice-id-validation-registry.md) – Voice-ID-001 experiment record, recorded human evidence, and planned follow-ups
- [Voice Experiment Metadata](catalog/metadata/voice-experiments.yaml) – Structured experiment and human-listening evidence source
- [Suno Voice Influence Experiment](research/suno-platform/experiments/voice-influence-test-2026-11-24.md) – Four approved voice-ID control/treatment clips and Christopher's recorded observation
- [AI Artist Strategy and Governance](research/ai-artists/ai-artist-strategy-and-governance.md) – Research synthesis and recommendations, not approved policy
- [Official Baby-Name Data Source Evaluation](docs/strategic-direction-voice-and-adaptive-media-validation-report.md#official-name-data-source-evaluation) – Evaluation of SSA, California CDPH, Washington DOH, and CDC/NCHS sources
- [Name Trends Analysis](research/naming/reports/name-trends-analysis.md) – Evidence-limited naming research; no demographic or cultural conclusions
- [Spotify for Artists Access and Roster Operations](research/distribution/platforms/spotify-for-artists-access-and-roster-operations.md) – Operational research reference; current Spotify documentation remains authoritative

### Operational Guidance

- [Roadmap](operations/roadmap.md) – Long-term strategic vision
- [Release Calendar](operations/release-calendar.md) – Planned releases and timeline
- [Automation Opportunities](operations/automation-opportunities.md) – Future workflow improvements
- [Suno Workspace Inventory and Assignment Record](operations/suno-workspace-assignment-queue-2026-11-24.md) – Full inventory, workspace counts, approved assignments, and ambiguous classifications
- [Suno Song Workspace Inventory CSV](operations/suno-song-workspace-inventory-2026-11-24.csv) – Row-level metadata and derived workspace memberships for 438 library records
- [Demo Intake and A&R](operations/demo-intake/README.md) – Governed intake, evaluation, and development handoff
- [Temporary Founder Review Workbench](portal/README.md) – Local demo review and Voice-ID-001 repository-writeback alpha
- [Workbench Architecture and Workflow Analysis](docs/architecture/founder-review-workbench.md) – Demo and experiment review boundaries plus future workflow placeholders
- [Workbench Wireframes](docs/architecture/founder-review-workbench-wireframes.md)
- [Audience Research Operations](operations/audience-research/README.md) – Research governance, privacy, and reporting framework
- [Demo and Audience Research Governance](docs/demo-and-audience-research-governance.md) – Cross-domain decision boundaries

---

## Artist Roster

### Individual Artists (12)

**Men:** Adrian Santiago, Nathan Cross, Isaac Vega, Ethan Navarro, Jordan Mercer, Lucas Reed

**Women:** Elena Cruz, Sophia Martinez, Maya Bennett, Isabella Reyes, Natalie Vega, Olivia Brooks

Each solo artist has detailed documentation in [artist-roster/solo-artists/](artist-roster/solo-artists/):
- Artist profile
- Development plan and strategic direction
- Production DNA and sonic identity
- Core themes and intellectual framework
- Discography and album history

### Bands (6)

North Star Revival, Lantern House, Signal Fire, Harbor Lights, Midnight Avenue, City Saints

Each band has [documentation](artist-roster/bands/) including creative direction, production philosophy, and ensemble identity.

### Producer Projects (2)

**Meridian** and **Foundry** – Producer-led project entities with documentation in [artist-roster/producer-projects/](artist-roster/producer-projects/).

---

## Metadata Registry

Canonical metadata maintained in [catalog/metadata/](catalog/metadata/) as YAML files:

- `artists.yaml` – Individual artist registry
- `bands.yaml` – Band registry
- `albums.yaml` – Album registry (with reserved albums: Fortress, Republic, Watchman Vol. 1)
- `songs.yaml` – Song registry
- `voices.yaml` – Voice profile registry
- `motifs.yaml` – Recurring motifs and patterns
- `demos.yaml` – Canonical demo registry; one intake-incomplete demo record
- `demo-reviews.yaml` – Canonical A&R review registry; one initial intake screen, founder review pending
- `development-projects.yaml` – Development handoff schema example; no projects registered
- `audience-research-sessions.yaml` – Research session schema example; no sessions registered
- `audience-responses.yaml` – Audience response schema example; no responses registered

---

## Creative Governance Principles

1. **Source Material is Foundational**
   - Every song begins with source material (Scripture, poetry, history, literature)
   - Source material determines emotional objective
   - Emotional objective determines artist assignment
   - Artist characteristics and emotions determine genre selection

2. **Artist Identity Persistence**
   - Voice character, production DNA, and themes remain stable
   - Artists are recognizable across their entire catalog
   - Catalog continuity is more important than any individual song
   - Genre evolution is natural; identity remains constant

3. **Genre Freedom**
   - No genre is excluded or privileged
   - Genre is selected to serve source material and emotional objective
   - Artists may work across multiple genres
   - Contemporary production is prioritized over traditional or theatrical approaches

4. **Emotional Authenticity**
   - Emotional truth matters more than technical perfection
   - Conversational vocal delivery preferred
   - Minimal processing preserves voice character
   - Clean, modern production supports emotional connection

5. **Label Structure**
   - Studio operates as a creative label, not a single-artist operation
   - Multiple artists, bands, and producer projects coexist
   - Each artist maintains distinct identity within unified framework
   - Catalog development supports long-term artist growth

---

## Source Material Repertoire

Studio draws source material from:

- **Psalms** – Scriptural Psalms and Psalm-inspired adaptations
- **Daily Readings** – Scripture readings and devotional material
- **Revolutionary War** – American historical documents and narratives
- **Historical Documents** – Primary sources from various periods and cultures
- **Virtue Literature** – Character studies and moral philosophy
- **Saints' Lives** – Hagiography and spiritual narratives
- **Poetry** – Literary works and verse

See [catalog/repertoire/](catalog/repertoire/) for organization and content.

---

## Validation and Quality

- [Phase 2A Validation Report](docs/phase-2a-validation-report.md) – Repository structure validation
- [Release Standards](creative/release-standards.md) – Quality checkpoints for release-ready work
- [Production Philosophy](docs/production-philosophy.md) – Overall production approach (framework)

---

## Archives

Retired, superseded, and rejected materials are preserved in [archive/](archive/):
- Retired artists
- Superseded prompts
- Rejected concepts

---

## Getting Started

1. **Understand the Manifesto:** Start with [Manifesto V2](foundations/AI_Music_Project_Manifesto_and_Notes_v2.md)
2. **Review Creative Framework:** Study [Identity Framework](creative/identity-framework.md) for the core principle
3. **Explore Artist Rosters:** Browse [artist-roster/](artist-roster/) to understand individual artist documentation
4. **Check Governance:** See [Decision Log](docs/decision-log.md) for major decisions and rationale
5. **Review Standards:** Consult [Production Style Guide](creative/production-style-guide.md) and [Vocal Style Guide](creative/vocal-style-guide.md) for quality standards

---

## Contributing

[PLACEHOLDER: Contribution guidelines and workflow]

---

## Status

**Phase 2A (Repository Scaffolding):** ✅ Complete

**Current Development:** Phase 3.1A uses the existing read-only portal prototype as a temporary Founder Review Workbench. It is for local workflow discovery only; it is not deployed or the final portal. One Suno demo remains intake-incomplete with founder review pending; original audio and additional demos are pending. No artist assignments, audience research, releases, accounts, or contracts are activated.

---

## License

[LICENSE file information]

---

## Contact and Support

[PLACEHOLDER: Contact information for studio coordination]

---

**Last Updated:** 2026-11-25

**Canonical Repository:** This document is authoritative for Suno Studio structure and governance.
