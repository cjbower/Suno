# Decision Log

**Purpose:** Record and document all significant architectural, creative, and operational decisions made within Suno Studio.

**Scope:** Decisions about artist development, album creation, genre selection, release strategy, and repository governance.

---

## Decision Record Format

Each decision record contains:

- **Decision ID:** Unique identifier
- **Title:** Short title for the decision
- **Date:** When the decision was made or recorded
- **Category:** Creative | Operational | Governance | Personnel | Technology
- **Status:** Active | Superseded | On Hold | Reversed
- **Rationale:** Why this decision was made
- **Source:** Who made the decision or what document/discussion led to it
- **Confidence:** High | Medium | Low
- **Impact:** Affected areas or implications
- **Related Decisions:** Links to related decisions

---

## Decision Log

[PLACEHOLDER: Decisions will be recorded here with full details as projects proceed]

### Decision Template

**ID:** [PLACEHOLDER]

**Title:** [PLACEHOLDER]

**Date:** [PLACEHOLDER: YYYY-MM-DD]

**Category:** [Creative | Operational | Governance | Personnel | Technology]

**Status:** [Active | Superseded | On Hold | Reversed]

**Rationale:** [PLACEHOLDER: Why was this decision made?]

**Source:** [PLACEHOLDER: Who made it? What document or discussion led to it?]

**Confidence:** [High | Medium | Low]

**Impact:** [PLACEHOLDER: What areas are affected?]

**Related Decisions:** [Links to related decisions]

---

## Architectural Decisions from Manifesto V2

The following decisions were established in Manifesto V2 and serve as foundational guidance:

1. **Source Material Principle** – Source material determines emotional objective, which determines artist assignment, which determines genre selection. This order is non-negotiable.

2. **Identity Persistence** – Artist identities must remain stable and recognizable over time. Catalog continuity is more important than any individual song.

3. **Genre Freedom** – No genre is excluded or privileged. Genre is selected based on source material and emotional objective, not commercial viability or convention.

4. **Contemporary Production** – Target production quality should be comparable to mainstream commercial releases. Traditional church presentation is not required.

5. **Emotional Authenticity** – Emotional authenticity is more important than genre purity or technical perfection.

6. **Label Structure** – The studio operates as a label with multiple artist rosters, bands, and producer projects, not as a single-artist operation.

7. **Catalog-First Architecture** – Catalog continuity and long-term artist identity are prioritized over short-term commercial considerations.

### Phase 2B.5 – Durable Music-Production and Release Platform

**ID:** DEC-2B5-01

**Title:** Develop Suno Studio as a durable music-production and release platform

**Date:** Not recorded

**Category:** Operational | Governance | Technology

**Status:** Approved

**Decision:** Suno Studio is intentionally being developed as a durable music-production and release platform, not merely as a catalog of songs. The platform includes content intake, rights review, artist and voice strategy, generation workflow, quality review, similarity review, metadata, distribution, monetization, catalog management, governance, automation, and audience development.

**Rationale:** Songs are products of the system, while reusable workflows, governance, automation, distribution knowledge, audience, and catalog are also durable assets.

**Source:** [AI music platform thesis and strategic vision](../foundations/ai-music-platform-thesis-and-strategic-vision.md)

**Authority:** Christopher Bower

**Confidence:** High

**Impact:** Establishes the platform thesis as an approved strategic direction. It does not approve any unapproved operational recommendation, account, contract, release, or capability.

**Related Decisions:** Catalog-First Architecture; Phase 2B.4 Demo and Audience Research Boundaries.

### Phase 2B.6 - Real-Person Voice Consent

**ID:** DEC-2B6-02

**Title:** Require explicit, scoped authorization and separate rights review before real-person voice use

**Date:** 2026-11-25

**Category:** Governance | Creative

**Status:** Approved

**Decision:** Consented real-person voice use is an approved future quality-control direction for assessing consistency, reproducibility, and drift. Do not capture, analyze for replication, model, assign, generate with, edit into a work, or distribute an identifiable real person's voice without documented, informed, scope-specific authorization and separate rights review. Authorization for one person, model, artist, work, platform, or medium does not imply authorization for another. This is not an operational production workflow and does not establish a voice assignment or automated approval.

**Rationale:** Technical access or public availability does not establish a person's consent or clear rights. Voice identity, source recording rights, and the intended use must be reviewed separately.

**Source:** Approved governance direction supplied for the 2026-11-25 documentation phase; see [Real-Person Voice Consent and Rights Governance](real-voice-consent-and-rights-governance.md).

**Authority:** Christopher Bower

**Confidence:** High

**Impact:** Establishes a governance gate for future work only. It creates no voice assignment, contract, production use, or legal determination.

**Related Decisions:** Identity Persistence; DEC-2B4-01.

### Phase 3.0 – Classification Requires Founder Review

**ID:** DEC-3-01

**Title:** Require documented founder review before demo classification or seed designation

**Date:** 2026-11-21

**Category:** Operational | Governance

**Status:** Active

**Discovery:** The first demo intake assigned classification and seed values from public-page facts before a completed founder review.

**Decision:** For all current and future demos, intake records existence, provenance, identifiers, and source references only. `classification.primary` and `seed_designation.primary` must remain `UNKNOWN` until a completed, documented founder review provides written evidence supporting those conclusions. Intake never determines value; review determines value.

**Rationale:** Classification, seed value, development potential, and disposition rationale are evaluative conclusions rather than intake facts.

**Source:** Phase 3.0 Governance Refinement.

**Confidence:** High

**Impact:** AI intake screens, N/R-only reviews, titles, lyrics, and public-page metadata do not authorize classification or seed assignment. Unsupported primary values and rationales remain `UNKNOWN`; disposition and development authority remain separately governed.

**Related Decisions:** DEC-2B4-01.

### Phase 2B.4 – Demo and Audience Research Boundaries

**ID:** DEC-2B4-01

**Title:** Keep demo intake, development, audience research, and release authority separate

**Date:** Not recorded

**Category:** Operational | Governance

**Status:** Active

**Rationale:** Demos are persistent creative assets and require provenance, rights context, review, and explicit development authorization. Audience research informs creative and market decisions but does not replace artistic judgment, source fidelity, rights review, technical validation, or human editorial authority.

**Source:** Phase 2B.4 approved project direction and `docs/demo-and-audience-research-governance.md`.

**Confidence:** High

**Impact:** Demo Intake and A&R owns intake, evaluation, and the Approved Development Brief; Internal Studio Development owns authorized execution; Audience Research Operations owns participant process, instruments, session integrity, privacy, analysis, and reporting; A&R and human editorial review retain decision authority. Catalog and release promotion remain separate approvals. The initial internal founder-demo class is the only active intake class; external submissions and audience research remain inactive.

**Related Decisions:** Source Material Principle; Identity Persistence; Catalog-First Architecture.

---

## Cross-References

- Manifesto V2: `../foundations/AI_Music_Project_Manifesto_and_Notes_v2.md`
- Delta report: `manifesto-delta-report.md`
- Operations: `../operations/`
