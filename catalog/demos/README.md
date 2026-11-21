# Demo Catalog

## Purpose

Preserve demos as first-class creative and operational assets, including ideas that are never promoted to a released work.

## Scope and Ownership Boundary

This catalog records demo identity, provenance, review state, and lineage. Demo Intake and A&R evaluate opportunities; they do not own internal production, audience-research administration, catalog promotion, or release operations. The original demo is immutable. Derived versions retain explicit lineage.

The current active intake class is `internal_founder_demo`. All other classes are future-compatible design values. External submissions are not active or accepted.

## Authoritative Metadata

The canonical registry is [`../metadata/demos.yaml`](../metadata/demos.yaml). One record (`DEMO-2026-0001`) points to a user-provided public Suno page; no local audio has been received or stored. The record remains intake-incomplete, and classification and seed designation remain `UNKNOWN` until a completed founder review supports them.

Use the literal `UNKNOWN` for unknown scalar values rather than silently omitting them. The identifier format is `DEMO-YYYY-NNNN`, where `YYYY` is the intake year; identifiers are immutable and existing identifiers must never be renumbered. An asserted ownership statement is not rights approval.

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

The first intake record is provisional and does not include local audio, rights verification, artist assignments, or authorized development. Rights, translations, samples, provenance, generator terms, and ownership claims require review; none are verified by this structure alone.

## Future External Submissions

The external area is reserved only. Before accepting submissions, the studio must separately review submission terms, rights and provenance, contributor consent, privacy, security, response obligations, licensing, and any needed contract workflow. No submission form or active intake path exists.
