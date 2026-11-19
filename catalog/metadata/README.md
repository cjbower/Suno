# Metadata

**Purpose:** Maintain authoritative YAML schemas and canonical registries for Suno Studio.

**Scope:** Artists, bands, albums, songs, voices, and motifs.

---

## Registry Files

- `artists.yaml` – Complete artist registry (individuals)
- `bands.yaml` – Band and ensemble registry
- `albums.yaml` – Album registry
- `songs.yaml` – Song registry
- `voices.yaml` – Voice profile registry
- `motifs.yaml` – Recurring motifs and patterns

---

## Organization Principle

Each YAML file contains:

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

---

## Cross-References

- Main catalog README: `../README.md`
- Artist rosters: `artist-roster/`
- Albums: `../albums/`
- Repertoire: `../repertoire/`
