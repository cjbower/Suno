# Demo Catalog

## Purpose

Preserve demos as first-class creative and operational assets, including ideas that are never promoted to a released work.

## Scope and Ownership Boundary

This catalog records demo identity, provenance, review state, and lineage. Demo Intake and A&R evaluate opportunities; they do not own internal production, audience-research administration, catalog promotion, or release operations. The original demo is immutable. Derived versions retain explicit lineage.

The current active intake class is `internal_founder_demo`. All other classes are future-compatible design values. External submissions are not active or accepted.

## Authoritative Metadata

The proposed schema example is in [`../metadata/demos.yaml`](../metadata/demos.yaml). It contains no registered demo records. Future audio assets should be stored in an approved asset location and referenced by metadata; no audio is stored here by this phase.

Use the literal `UNKNOWN` for unknown future scalar values rather than silently omitting them. An asserted ownership statement is not rights approval.

## Lifecycle

The demo lifecycle and internal queue locations are documented in [`internal/README.md`](internal/README.md) and the [intake workflow](../../operations/demo-intake/triage-workflow.md). Promotion does not remove or overwrite the original demo.

## Asset Distinctions

- **Demo:** An exploratory creative asset, preserved in its original form.
- **Work:** A separately identified composition or song concept derived from creative material.
- **Recording:** A performance capture of a work.
- **Master:** The approved final audio asset for distribution.
- **Release:** The catalog and distribution event that makes an approved master available.

These are related by lineage, not interchangeable records. A future work/composition registry should be designed before overloading `songs.yaml`.

## Known Limitations

This phase creates no demo records, audio, assignments, or development projects. Rights, translations, samples, provenance, generator terms, and ownership claims require review; none are verified by this structure alone.

## Future External Submissions

The external area is reserved only. Before accepting submissions, the studio must separately review submission terms, rights and provenance, contributor consent, privacy, security, response obligations, licensing, and any needed contract workflow. No submission form or active intake path exists.
