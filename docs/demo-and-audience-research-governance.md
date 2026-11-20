# Demo and Audience Research Governance

## Purpose

Define authority boundaries across Demo Intake and A&R, Internal Studio Development, Audience Research Operations, editorial review, catalog, release operations, and marketing.

## Authority and Ownership

| Domain | Owns | Does not own |
|---|---|---|
| Demo Intake and A&R | Intake validation, opportunity evaluation, repertoire recommendations, approved Development Brief | Audio engineering, audience-research administration, canonical catalog metadata, release operations |
| Internal Studio Development | Authorized creative execution, revision, production, version lineage, candidate freeze | Intake approval, participant recruitment, research decisions, release approval |
| Audience Research Operations | Participant process, survey administration, instrument versions, session integrity, privacy handling, analysis, reporting | Artist assignment, rights approval, technical acceptance, final creative revision, release approval, catalog promotion |
| A&R and Human Editorial Review | Human decisions to revise, hold, assign, promote, hand off, or archive | Rewriting research findings, bypassing rights or technical review |
| Catalog | Authoritative work, recording, master, and release relationships after the required approval | Intake evaluation or audience-study administration |
| Release Operations | Release readiness, distribution, and release execution after approval | Creative approval or research interpretation |
| Marketing | Consume approved listener language, emotional associations, segment and positioning evidence | Control the research record, alter findings, or approve creative/release decisions |

## Decision Boundaries

- A demo is a persistent asset, not a disposable version.
- A demo does not enter internal production until an authorized human approves a Development Brief.
- A demo may remain unassigned; assignment is never inferred from a positive review.
- Research provides evidence and limitations. It does not replace artistic judgment, source fidelity, rights review, technical validation, or human editorial authority.
- A research report does not approve a release or promote an item into the catalog.
- Promotion creates separate work and downstream records while preserving the original demo and lineage.

## Data Ownership

Demo metadata, research instrument definitions, aggregate reports, and decision records are studio-governed records. `ownership_assertion` records a claim or provenance statement; it does not establish legal ownership. Participant responses require privacy review and should not be stored individually in Git by default.

The approved internal founder-demo class does not require a contributor-contract workflow for those demos. Source-material rights, translations, samples, provenance, and generator rights still require review.

## Escalation Points

- Missing source provenance, rights uncertainty, translations, or samples: pause the affected use for rights review.
- Missing, corrupted, or inaccessible audio: intake/technical review; use N/R rather than F.
- Voice, production, or arrangement defects: route to the responsible internal development reviewer without changing the original demo.
- Conflicting or polarized audience evidence: preserve the disagreement and escalate interpretation to A&R and human editorial review.
- Privacy, consent, minors, disclosure, or audio redistribution concern: stop the study and escalate to the designated human authority before further processing.
- Assignment, new identity, licensing, handoff, catalog promotion, or release: obtain the distinct approval required for that boundary.

## Known Limitations

This phase creates schema examples and operating documentation only. No demo, audio, development project, research session, response, participant, artist assignment, or release is created. No external submissions, surveys, recruitment, contracts, platform, or database are activated or selected.

## Future External-Submission Requirements

Before accepting external material, separately approve submission terms, rights and provenance checks, contributor identity and privacy handling, contract and licensing needs, conflict handling, response and withdrawal obligations, secure storage, access controls, retention and deletion, and procedures for protecting unreleased audio. No external intake is active.

## Governing Principle

Audience research informs creative and market decisions. Audience research does not replace artistic judgment, source fidelity, rights review, technical validation, or human editorial authority.
