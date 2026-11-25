# Metadata

**Purpose:** Maintain authoritative YAML schemas and canonical registries for Suno Studio.

**Scope:** Artists, bands, albums, songs, voices, motifs, demos, development projects, and audience-research schemas.

---

## Registry Files

- `artists.yaml` – Complete artist registry (individuals)
- `bands.yaml` – Band and ensemble registry
- `albums.yaml` – Album registry
- `songs.yaml` – Song registry
- `voices.yaml` – Voice profile registry
- `motifs.yaml` – Recurring motifs and patterns
- `demos.yaml` – Canonical demo registry; one intake-incomplete record
- `demo-reviews.yaml` – Canonical A&R review registry; one initial intake screen
- `voice-experiments.yaml` – Structured Voice-ID experiment evidence and evaluation answers; not joined to demo review state
- `development-projects.yaml` – Development handoff schema example; no project records
- `audience-research-sessions.yaml` – Research session schema example; no session records
- `audience-responses.yaml` – Response schema example; no response or participant records

---

## Organization Principle

Registry files contain canonical records where present. The demo and review files retain their `schema_reference` and `schema_example` sections and now also contain the first provisional demo and intake-screen records. Development-project and audience-research files remain schema-only.

Registry files generally contain:

1. **Schema Reference** – Structure and field definitions
2. **Current Registry** – All current entries
3. **Notes** – Organization and usage guidelines

---

## Usage Guidelines

- Metadata files are **canonical** – they are the authoritative source of truth
- Individual artist/band/album folders contain detailed documentation; metadata files contain summary information
- Cross-references connect individual folders to canonical metadata
- Changes to artist status, genre, or core identity should be reflected in metadata
- New artists, bands, or albums should be added to metadata before detailed documentation is created
- Demo intake records document evidence and disposition; they do not automatically authorize development, artist assignment, audience research, or release
- Voice experiment records document controlled-generation evidence separately from demo intake and founder review; the Voice-ID-001 local writeback proof-of-concept appends audited submissions, while other workflows remain read-only
- Unknown scalar values remain the literal `UNKNOWN`

---

## Cross-References

- Main catalog README: `../README.md`
- Artist rosters: `artist-roster/`
- Albums: `../albums/`
- Repertoire: `../repertoire/`
- Demo assets: `../demos/`
- Demo Intake and A&R: `../../operations/demo-intake/`
- Audience Research Operations: `../../operations/audience-research/`
