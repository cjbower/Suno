# Suno Studio Durable Handoff

## Purpose

This handoff preserves the current state, governing principles, completed work, known limitations, open decisions, and recommended next phases for the Suno Studio repository.  It is intended to let a future Copilot session, Luna agent run, collaborator, or future maintainer resume the work without relying on conversational memory.

This document reflects the discussion and execution reports available at the time of writing.  Statements about repository contents are based on the reported agent output and reviewed files.  Where the repository was not independently inspected in this session, that limitation is stated explicitly.

## Project Mission

Suno Studio is intended to become a long-term, AI-assisted music, podcast, publishing, and media operation rather than a collection of isolated generated songs.

The studio will adapt enduring source material such as Psalms, Scripture, Revolutionary War poetry, historical documents, virtue literature, and related public-domain or properly licensed texts into contemporary music.  The target is not niche devotional music, conventional church presentation, or historical reenactment.  The production ambition is comparable to contemporary commercial and Billboard-level artists, while remaining faithful to the source material and emotionally authentic.

The studio is deliberately genre-agnostic.  Relevant styles already explored or discussed include rap, alternative hip-hop, country, classic rock, post-punk, grunge, metal, pop, electronic, dance, house, EDM, Latin, Regional Mexican, Christian, Gospel, singer-songwriter, Americana, and multilingual or bilingual work.  No source category is permanently bound to a genre.

The intended audience begins approximately with ages 15 through 25, but the work should not be artificially limited to that demographic.  The guiding cultural objective is to extend the life of enduring texts by translating them faithfully into contemporary listening habits.

## Foundational Creative Principle

The authoritative creative sequence is:

```text
Source Material
    -> Emotional Objective
    -> Artist or Band Assignment
    -> Genre and Production Selection
```

Genre does not lead the process.  The source and intended emotional effect lead.  Artist identity and audience fit also matter when selecting the final genre and production treatment.

## Stable and Variable Identity

Artist and band identities must remain recognizable over time without becoming frozen.

Stable elements generally include:

- Voice character or ensemble vocal identity
- Production DNA
- Core themes and emotional territories
- Recurring motifs and performance signatures
- Audience relationship and artistic positioning

Variable elements generally include:

- Genre
- Tempo
- Instrumentation
- Album direction
- Production techniques
- Language, when consistent with the artist and reviewed appropriately

Evolution should be documented as evolution rather than accidental drift.

## Human and Agent Authority

Human editorial review remains authoritative.

Luna is treated as an execution agent and repository operator, not as the source of creative truth.  The preferred operating pattern is:

```text
Human intent and architecture
    -> Explicit agent instruction
    -> Agent execution
    -> Validation and report
    -> Human review
    -> Commit
```

Manual edits are allowed, but should be disclosed before the next agent phase so that observed repository state and conversational state remain synchronized.

The repository is Git-managed.  Managed deletion, relocation, consolidation, and refactoring are allowed when deliberate, validated, documented, and recoverable.  Prefer one authoritative source of truth over indefinite duplicate structures.

## Repository Architecture

The current conceptual repository domains are:

```text
foundations/       Why the studio exists and the principles it protects

docs/              Governance, decisions, validation, assessment, and policy

creative/          Creative architecture, standards, templates, and identity rules

artist-roster/     Solo artists, bands, and producer projects

catalog/           Repertoire, releases or albums, and canonical metadata

operations/        Workflows, calendars, roadmaps, observability, and automation ideas

research/          Evidence and research corpora such as naming and distribution research

archive/           Retired, superseded, or rejected material preserved for reference
```

The intended authority rule is:

```text
YAML metadata is canonical for machine-readable facts and relationships.
Markdown explains context, rationale, creative direction, and human-readable detail.
```

## Completed Phases

### Phase 0: Vision

Completed through the original manifesto and subsequent discussion.

### Phase 1: Manifesto Reconciliation and Governance

Reported completed artifacts include:

- Original manifesto preserved as historical context
- Manifesto Version 2 created
- Manifesto delta report created
- Validation report created
- Decision log created
- Creative constitution created

### Phase 2A: Repository Scaffolding

Reported completed work includes:

- Core directory structure
- Initial roster scaffolding
- Band scaffolding
- Producer-project scaffolding
- Creative framework documents
- YAML metadata registries
- Operations placeholders
- Archive structure
- Validation reports

### Phase 2A.6: Foundations Refactor

The generic `Documents/` concept was replaced by `foundations/` as the authoritative home for founding material.  The old `Documents/` folder was manually verified and removed before the initial commit.

### Phase 2A.7: Naming Research Corpus

Reported completed research includes:

- First-name datasets by decade and gender for the 1970s through the 2020s
- A top-50 U.S. surname dataset
- Name-trend analysis
- Current artist-name collision analysis
- Current band-name collision analysis
- Name-selection strategy
- Naming validation report

The research corpus exists, but its external collision conclusions must be independently verified before being treated as authoritative.  Earlier public searches found active music usage for several apparently low-risk names.

### Phase 2A.8: Initial Repository Commit

Reported initial commit:

```text
84b325b2fb6e9403a5718cad7f8667967a66af87
```

Reported commit title:

```text
milestone: establish studio foundations and naming research corpus
```

Reported state after commit:

- Branch: `main`
- 176 files added
- Working tree clean
- `.DS_Store` ignored
- Secret-like filenames and common credential patterns checked before commit

### Phase 2B.0: Roster Normalization

Verified normalized structure:

```text
artist-roster/
├── solo-artists/
├── bands/
└── producer-projects/
```

Validation performed:

- 12 solo-artist entities
- 6 band entities
- 2 producer-project entities
- 74 moved files compared with their originals; all were byte-identical
- Entity-specific templates separated
- References and metadata paths updated
- `git diff --check` passed
- See `docs/roster-normalization-report.md` for details

### Phase 2B.1: Name Collision Remediation

The approved replacement names are:

```text
Jordan Mercer
Adrian Santiago
```

Repository evidence confirms the two replacement folders, display names, metadata identifiers, and references are consistent. The former names remain documented in `docs/name-remediation-report.md`. No other artist or band names were changed.

The existing Phase 2A.7 research rated the original Jordan name medium risk and the original Adrian name low risk. Those research references were updated to the replacement names, but their surrounding analysis was not rerun. Treat the results as historical assessments, not collision verification for the replacements.

### Phase 2B.2: Voice Architecture Foundation

Verified artifacts include:

- `creative/voice-architecture.md`
- `docs/voice-governance-principles.md`
- `docs/voice-architecture-assessment.md`
- Creative index updated

Assessment of `catalog/metadata/voices.yaml`:

- Contains a schema reference and 12 artist-linked placeholder entries
- `notes` is described in the schema but absent from the entries
- No lifecycle fields
- No version fields
- No voice assignments or populated voice profiles were added
- The registry was not modified during this phase

## Known Data-Quality Issues

A generation defect was found in some artist documents:

```text
isauella reyes
```

instead of:

```text
Isabella Reyes
```

This should be handled through a repository-wide artist-name normalization audit.  Search all artist Markdown and YAML files for capitalization, display-name, folder-name, and transformation artifacts.

## Current Roster State

The current solo-artist roster is:

```text
Adrian Santiago
Nathan Cross
Isaac Vega
Ethan Navarro
Jordan Mercer
Lucas Reed
Elena Cruz
Sophia Martinez
Maya Bennett
Isabella Reyes
Natalie Vega
Olivia Brooks
```

The approved name replacements are reflected in the roster, metadata, and references. The name-remediation report records the former names and the limits of the collision research.

The original band roster contained:

```text
North Star Revival
Lantern House
Signal Fire
Harbor Lights
Midnight Avenue
City Saints
```

The producer projects were:

```text
Meridian
Foundry
```

All names remain provisional until collision, brand, trademark, domain, platform, and cultural reviews are complete.  Exact-name and near-match searches should include Spotify, Apple Music, YouTube Music, Amazon Music, SoundCloud, Bandcamp, Discogs, performing-rights databases, social handles, domain availability, and relevant trademark records.  Absence from one platform is not sufficient evidence of availability.

## Voice and Identity Problem Statement

The largest unresolved technical problem is reliable identity persistence.

The studio must separate:

```text
Artist identity
Voice implementation
Song performance
Production model
Platform or generator version
```

An artist may persist while an underlying voice implementation changes.  The repository must preserve sufficient evidence to compare outputs, detect drift, reproduce acceptable behavior when possible, and deliberately approve replacement or evolution.

Future voice metadata should likely address, after review:

- Stable voice ID
- Artist ID
- Voice implementation version
- Source generation or reference asset
- Generator and model version
- Persona or Voice identifier when available
- Prompt fingerprint
- Languages and pronunciation notes
- Vocal range and delivery characteristics
- Known drift
- Approved use cases
- Evaluation evidence
- Status and lifecycle
- Replacement and retirement lineage
- Rights and consent evidence where relevant

Do not populate invented voice characteristics merely to complete the schema.

## Production Principles Learned Through Experimentation

The following are evidence-based preferences from actual Suno experimentation:

- Clean recording aesthetic
- Close, natural vocal presence
- Minimal reverb and delay
- Transparent rather than obvious compression
- Minimal vocal stacking and doubling
- Breath and human pauses may be preserved
- Rap cadence should not be accidentally converted into strained or theatrical singing
- Large instrumental and bass impact can coexist with a dry, human lead vocal
- Deep sub-bass should come from the production, not an unnaturally low narrator voice
- Instrumental gaps between stanzas or narrative sections are valuable
- Strategic repetition can create hooks without rewriting source material
- Avoid Broadway, musical theater, trailer narration, choir wash, excessive auto-tune, and robotic delivery unless deliberately selected for a specific identity
- Contemporary commercial quality is the target, but imitation of a specific living artist is not the governing method

## Source-Material Governance

The studio intends to prioritize public-domain material and properly licensed or permitted sources.

Potential sources include:

- Psalms and Scripture
- Daily readings
- Revolutionary War poetry
- Historical letters, speeches, and documents
- Virtue literature
- Saints' lives
- Poetry

For each source, preserve:

- Stable source ID
- Title
- Author or originating tradition
- Edition or translation
- Language
- Publication date when known
- Public-domain or rights status
- Source URL or repository path
- Attribution requirement
- Adaptation notes
- Lyrics derived from the source
- Human editorial decisions

Modern Bible translations may be copyrighted even when the underlying Scriptural material is ancient.  Do not assume permission based on mission alignment or institutional goodwill.  Verify the actual translation terms.

## Separate Editorial Initiatives

Two editorial missions should remain cleanly separated even if they share infrastructure.

### Psalms, Scripture, and Catholic Tradition

Purpose: provide contemporary, meaningful music and companion media that can fit commuting, exercise, reflection, or ordinary listening habits without being confined to traditional church production.

### History, Patriotism, and Civic Memory

Purpose: make historical poetry, documents, stories, sacrifice, courage, duty, and civic memory emotionally immediate to a contemporary audience.

The musical roster may serve either initiative when the source, emotional objective, and artist identity naturally align.  Branding, feeds, channels, and audience promises may remain distinct.

## Release and Album Model

Weekly releases may accumulate before album formation.

The expected model is:

```text
Weekly or recurring singles
    -> Catalog accumulation
    -> Thematic and sonic clustering
    -> Curated playlist, EP, or album
```

Albums do not need to be planned first.  They may emerge through intentional curation of strong releases, provided the resulting collection has a coherent artistic purpose.

## Distribution and Audience Development

A proposed Phase 2B.3 instruction was drafted to research and document global distribution, audience development, and podcast architecture.

The intended operating layers are:

```text
Canonical Master and Metadata
    -> Distributor of Record
    -> Streaming and Music Platforms
    -> Platform-Specific Artist Portals
    -> Discovery Content
    -> Owned Audience
    -> Analytics and Review
    -> Next Release Decision
```

Key platform roles under consideration:

- Spotify for streaming and playlist discovery
- Apple Music for streaming, Shazam, radio, and global audience analytics
- YouTube and YouTube Music for visual storytelling, long-form discovery, Shorts, lyric videos, visualizers, and podcasts
- TikTok for hook discovery, creator engagement, and campaign analytics
- SoundCloud for early community, experimentation, direct uploads, and possible distribution
- Amazon Music for streaming, territory reporting, programming pitches, and Alexa discovery
- Podcast directories through one canonical RSS feed

Target markets under consideration include:

- United States
- Canada
- Mexico
- United Kingdom
- Ireland
- European Union markets treated individually rather than as one audience
- Australia
- New Zealand
- Other Latin American markets
- Additional markets selected from observed data

No distributor, podcast host, advertising platform, or international rollout has been approved.

## Recommended Operational Model for Distribution

Use one authoritative distributor for each master recording unless an approved exception exists.  Avoid duplicate deliveries.

Maintain direct access to each platform's artist portal for profile management, editorial pitching where available, analytics, and issue resolution.

Use an owned website and email list as portable audience assets.  Streaming platforms should not be the only relationship with listeners.

Treat each release as a campaign with pre-release, release-week, and post-release phases.  Derivative assets may include the master, lyric video, visualizer, official video when justified, short vertical clips, source-text context, podcast episode, podcast shorts, email features, and localized metadata.  Not every release requires every asset.

Reject purchased streams, bots, guaranteed playlist-placement services, and opaque traffic sources.

## Podcast Architecture

The podcast is intended to complement the music rather than exist as unrelated content.

Possible relationships include:

- Song as emotional encounter; podcast as historical, theological, literary, or production context
- Podcast as primary discovery; song as a companion work
- Shared source material expressed through different media

The preferred technical model is one canonical RSS feed controlled through a selected podcast host, then submitted to podcast directories.  YouTube should be treated as an additional discovery and video platform, not as the distributor of the RSS feed to other directories.

The podcast-host decision remains open.

## Immediate Next Actions

### 1. Human review of local commits

Review `docs/local-commit-report.md` and the local commits before authorizing any push. The current branch is `main`; Git reports its configured `origin/main` upstream as gone. Do not change upstream tracking as part of this handoff. Verify branch and remote state before any future push.

### 2. Perform Artist-Name Data Quality Audit

Correct `isauella reyes` and scan all entity files for similar artifacts.

### 3. Review Naming-Collision Evidence

Reassess the replacement names against current sources before treating their collision risk as verified. Do not accept generated LOW or MEDIUM labels without checking the underlying sources and search methodology.

### 4. Review Voice Architecture

Have a human review the voice-architecture and governance documents before changing the YAML schema or making voice assignments.

### 5. Run Phase 2B.3 Distribution Research

Use the previously drafted documentation-only instruction.  Require official sources, retrieval dates, explicit uncertainty, and no account creation or purchasing.

### 6. Add Source Registry Design

Consider a future canonical `sources.yaml` because the entire creative sequence begins with source material.

## Explicitly Deferred Work

Do not yet assume approval for:

- Distributor selection
- Podcast-host selection
- Artist voice assignments
- Detailed artist biographies
- Band membership
- Album titles or track lists
- Release dates
- Paid campaigns
- International localization spend
- Full automation
- API integration
- Trademark clearance
- Legal clearance

## Agent Execution Standards

Future Luna or Copilot instructions should generally include:

- Objective
- Scope
- Non-goals
- Authoritative sources
- Allowed mutations
- Prohibited actions
- Validation steps
- Evidence requirements
- Report artifact
- Stop condition
- Git instructions stated separately

For repository changes:

- Inspect current state first
- Preserve unknown records
- Do not fabricate missing values
- Make small, reviewable changes
- Validate references and paths
- Run whitespace or syntax checks
- Scan for secrets before commits
- Report unexpected files and stop when appropriate
- Prefer clean, atomic commits

## Suggested Status Summary

```text
Vision and mission                 Complete
Governance and constitution        Complete
Repository architecture            Complete
Naming research corpus             Complete, evidence review pending
Foundations refactor               Complete
Initial baseline commit            Complete
Roster entity normalization        Complete, repository-verified
Known artist-name remediation      Complete, repository-verified; replacement research pending
Voice architecture foundation      Complete, repository-verified; human review pending
Local commit workflow              Complete locally; human review required
Artist identity population         Not started
Voice profile population           Not started
Source registry population         Not started
Catalog content development        Not started
Distribution research              Instruction drafted, not yet executed
Podcast platform selection         Not started
Publishing and release operations  Not started
```

## Final Continuity Note

The repository is intended to function as the studio's institutional memory and creative constitution.  Future work should preserve not only what the studio creates, but why decisions were made, what evidence supports them, what remains unknown, and what should not change casually.
