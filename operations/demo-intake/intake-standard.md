# Demo Intake Standard

## Purpose

Create a consistent boundary for receiving a demo, validating its minimum provenance and rights context, and deciding whether it is ready for triage.

## Submission Classes

| Class | Current status |
|---|---|
| `internal_founder_demo` | Active now |
| `roster_artist_demo` | Future-compatible; inactive |
| `band_demo` | Future-compatible; inactive |
| `producer_project_demo` | Future-compatible; inactive |
| `collaboration_demo` | Future-compatible; inactive |
| `external_submission` | Future-compatible; inactive |
| `acquired_concept` | Future-compatible; inactive |
| `inbound_pitch` | Future-compatible; inactive |
| `organic_discovery` | Future-compatible; inactive |

These are schema design values, not permission to accept a submission. External intake remains disabled.

## Intake Requirements

Future records should identify the source, submitter assertion, received date, original audio location and checksum, generator/model context when available, prompt and lyric status, source material, language, known defects, and current rights-review status. Unknown values must be written explicitly as `UNKNOWN`.

An ownership assertion is not a verified ownership or rights decision. Verify source-material rights, translation terms, samples, provenance, and generator rights before development or release. No contributor contract process is required for internal founder-created demos under the approved decision; that does not waive rights review.

## Preservation

The original demo is immutable. Store it in an approved asset location and record a checksum; do not overwrite or modify it during intake. Revisions become derived versions with explicit lineage.

## Incomplete Intake

Missing or inaccessible material is `intake_incomplete` or `N/R` as appropriate, not a negative creative grade. Record the missing evidence, responsible owner, and review trigger. Do not start production or imply approval while required intake evidence is unresolved.

## Classification Gate

Intake records existence, identifiers, provenance, and source references only. Classification and seed designation are evaluative conclusions and must remain `UNKNOWN` during intake. Do not assign either value until a completed, documented founder review exists and provides written evidence supporting the conclusion. An AI intake screen, an N/R-only review, a title, lyrics, or public-page metadata does not satisfy this gate.

The required order is:

```text
Demo Exists
    -> Intake
    -> UNKNOWN
    -> Founder Review
    -> Classification
    -> Seed Qualification
    -> Disposition
    -> Development Decision
```

Intake never determines value; review determines value. A development decision remains separately authorized.

## Boundary

Validated intake permits triage only. Internal production requires a separate Approved Development Brief. Catalog registration, release approval, and audience research remain separate processes.
