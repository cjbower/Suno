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
- `demos.yaml` – Demo schema example; no demo records
- `demo-reviews.yaml` – A&R review schema example; no review records
- `development-projects.yaml` – Development handoff schema example; no project records
- `audience-research-sessions.yaml` – Research session schema example; no session records
- `audience-responses.yaml` – Response schema example; no response or participant records

---

## Organization Principle

Existing registries and the new schema-only files have different roles. Registry files contain canonical records where present; the five demo/research files contain only `schema_reference` and `schema_example` structures and are not populated registries.

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
- Demo and audience-research examples must not be treated as actual records or assignments

---

## Cross-References

- Main catalog README: `../README.md`
- Artist rosters: `artist-roster/`
- Albums: `../albums/`
- Repertoire: `../repertoire/`
- Demo assets: `../demos/`
- Demo Intake and A&R: `../../operations/demo-intake/`
- Audience Research Operations: `../../operations/audience-research/`
