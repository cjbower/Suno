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

### Phase 2B.6 - Source-Centered Adaptive Media

**ID:** DEC-2B6-01

**Title:** Develop a source-centered creative platform that can support intentionally selected companion media

**Date:** 2026-11-25

**Category:** Creative | Operational | Governance

**Status:** Approved

**Decision:** Music remains a central expression of Suno Studio's work, while approved source material may also be considered for distinct companion formats when they serve the source and editorial purpose. Adaptations must preserve source provenance, use format-specific rights and consent review, remain traceable as distinct works, and receive separate human production and release approval.

**Rationale:** A durable, source-led platform should make purposeful cross-media work possible without assuming that every source belongs in every medium or that approval for one format extends to another.

**Source:** Approved strategic direction supplied for the 2026-11-25 documentation phase; see [Adaptive Media Strategy and Governance](../research/ai-artists/adaptive-media-strategy-and-governance.md).

**Authority:** Christopher Bower

**Confidence:** High

**Impact:** Establishes a planning direction only. It does not activate a new format, product, service, account, audience-data collection, production workflow, distribution channel, or release.

**Related Decisions:** DEC-2B5-01; DEC-2B4-01; Source Material Principle; Catalog-First Architecture.

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

### Phase 2B.6 - Branded and Direct Distribution

**ID:** DEC-2B6-03

**Title:** Pursue branded distribution on wholesale infrastructure, followed by direct distributor capability

**Date:** 2026-11-25

**Category:** Operational | Governance | Technology

**Status:** Approved strategic direction

**Decision:** Pursue a branded music-distribution service using wholesale or third-party delivery infrastructure as the short-term company capability, with a founder planning target of 3-9 months. After establishing and operating the branded service, pursue direct digital-distributor or aggregator capability, with a preferred target of 12-18 months and an outer target of less than 24 months.

**Rationale:** Existing production, intake, metadata, quality-review, catalog, release, and automation work can become an operational foundation for distribution. Wholesale delivery provides a planned intermediate phase while the company develops the delivery reliability, catalog operations, accounting, compliance, support, and DSP relationships required for direct distribution.

**Source:** Approved founder direction supplied for the 2026-11-25 documentation phase; see the [Roadmap](../operations/roadmap.md) and [AI Music Platform Thesis](../foundations/ai-music-platform-thesis-and-strategic-vision.md).

**Authority:** Christopher Bower

**Confidence:** High for the strategic direction and planning targets; external provider and DSP acceptance remain uncertain.

**Impact:** Approves planning toward these capabilities, not operational readiness or launch. No provider, account, legal or financial readiness, direct DSP agreement, client funds handling, or release delivery is established or claimed. Targets are not promises, contracts, or guarantees of platform acceptance.

**Conditions:** Pass the legal, financial, provider, security, operational, and human go/no-go gates before any pilot or commercial launch. Do not claim direct DSP relationships before agreements exist.

**Related Decisions:** DEC-2B5-01; DEC-2B6-01; DEC-2B4-01.

### Phase 2B.6 - Dynamic Event-Driven Media

**ID:** DEC-2B6-04

**Title:** Dynamic event-driven, preference-matched media is an approved platform end state

**Date:** 2026-11-25

**Category:** Creative | Operational | Governance | Technology

**Status:** Approved strategic direction

**Decision:** Permanent catalog music and dynamic event-driven media are complementary. The approved end-state direction includes a continuously refreshed, source-to-lyrics process; preference-matched music and sports-information channels; direct audience leverage; portability across catalog, audience, production, distribution, and analytics; early practical implementation; and replaceable generation providers. Providers advance foundational models; the company retains responsibility for publication quality, source integrity, identity, rights, audience alignment, and operational reliability. See the [Adaptive Media Strategy and Governance](../research/ai-artists/adaptive-media-strategy-and-governance.md) for the detailed boundaries and examples.

**Rationale:** A durable creative platform can serve both long-lived catalog listening and timely, audience-aligned storytelling. Early practical integration may create learning and strategic options, while portability and clear provider boundaries reduce avoidable dependence on a single generation or distribution path. The five-to-ten-year platform thesis is founder direction, not a verified market outcome.

**Source:** Approved founder strategic direction supplied for the 2026-11-25 documentation phase.

**Authority:** Christopher Bower

**Confidence:** High that this is approved founder direction; future platform behavior, market timing, provider performance, and first-mover outcomes remain uncertain.

**Impact:** Records a strategic end state and planning direction only. It does not activate a product, channel, audience-data collection, preference or subscriber record, generation workflow, media output, provider relationship, distribution relationship, platform affiliation, or release.

**Conditions:** The permanent catalog remains; rights and consent remain mandatory; publication quality remains human-governed; external platform timing remains outside company control; no team, league, platform, or other affiliation is implied; no provider is irreplaceable; and early adoption does not guarantee success. No stage is complete until separately scoped and approved.

**Related Decisions:** DEC-2B5-01; DEC-2B6-01; DEC-2B6-03; DEC-2B4-01.

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

### Phase 3.0 – Human-Centered Knowledge Preservation

**ID:** DEC-3-02

**Title:** Require preservation-first governance and founder approval for destructive changes to human-centered knowledge

**Date:** 2026-11-25

**Category:** Governance | Operational

**Status:** Approved

**Decision:** Strategic, creative, historical, interpretive, research, policy, and other human-oriented repository content must not be substantively removed, replaced, deprecated, or consolidated in a meaning-changing way without explicit founder approval. Uncertainty should be labeled and contextualized rather than treated as permission to erase useful knowledge.

**Rationale:** Lost knowledge is difficult to identify or reconstruct after removal. The repository supports human learning, creativity, strategic continuity, and future judgment in addition to machine execution. Code-level precision and validation standards must not be applied indiscriminately to human-centered documentation.

**Source:** Founder-approved direction recorded in the [Human-Centered Knowledge Preservation Policy](human-centered-knowledge-preservation-policy.md).

**Authority:** Christopher Bower

**Confidence:** High

**Impact:** Establishes preservation-first handling and an explicit human-review gate for destructive changes to covered documentation; it does not lower technical standards for executable or machine-enforced material.

**Conditions:** Technical, security, legal, privacy, financial, and machine-enforced records continue to require appropriate precision. This rule does not protect secrets, malware, improperly stored private data, or immediately dangerous material. Destructive changes require a review packet and explicit approval. Preservation does not convert an interpretation into verified fact.

**Related Decisions:** DEC-3-01; DEC-2B4-01.

---

## Cross-References

- Manifesto V2: `../foundations/AI_Music_Project_Manifesto_and_Notes_v2.md`
- Delta report: `manifesto-delta-report.md`
- Operations: `../operations/`
