# Roadmap

**Purpose:** Define long-term strategic direction and planning for Suno Studio.

**Scope:** 1-3 year vision, major initiatives, and strategic milestones.

---

## Approved Strategic Direction

Suno Studio is developing a durable, human-led, source-centered music-production and release platform. Music is central, and the platform may support intentionally selected companion media when it serves the source and editorial purpose. Sources, rights, contributor permissions, artist identity, and derivative relationships must remain traceable. See [DEC-2B5-01](../docs/decision-log.md), [DEC-2B6-01](../docs/decision-log.md), and the [Adaptive Media Strategy](../research/ai-artists/adaptive-media-strategy-and-governance.md).

The approved distribution progression is production and release operations, then branded distribution using wholesale infrastructure, then selective direct DSP relationships and direct distributor or aggregator capability. The branded-service planning target is 3-9 months; the direct capability target is 12-18 months preferred and less than 24 months outer. See [DEC-2B6-03](../docs/decision-log.md).

These are founder planning targets, not external guarantees or evidence of readiness. No provider is selected, no distribution service is operational, and no direct DSP agreement or approval is claimed.

## Roadmap Classification

### Approved Direction - Not Activated

- Preserve the source-first creative sequence and catalog continuity.
- Develop reusable workflows that retain provenance, rights review, human editorial authority, and format-specific lineage.
- Consider companion media only when supported by a specific source and editorial brief.
- Require documented scope-specific authorization and separate rights review before any real-person voice use.
- Pursue branded music distribution on wholesale or third-party delivery infrastructure, followed by direct distributor or aggregator capability, subject to readiness gates.

### Research or Design Candidates - Unscheduled

These remain unscheduled candidates and are not necessary conditions for the approved distribution workstream unless a gate requires them:

- Define source-to-derivative catalog relationships and minimum provenance fields.
- Evaluate an approval workflow for format-specific rights, accessibility, and contributor consent.
- Assess potential companion formats against editorial purpose, cost, rights, and audience evidence.
- Evaluate rapid-response/time-sensitive media and weekly sports/tailgate playlists as proposed use cases, not launched products.
- Evaluate personalized and values-aware media only as a proposed capability with privacy, consent, bias, copyright, accessibility, and safety review.
- Refresh official naming datasets and collision research using reproducible, current sources.
- Define voice authorization evidence and secure handling without storing sensitive documents in Git.

### High Priority: Branded Distribution (3-9-Month Planning Target)

**Approved direction:** Develop a customer-facing branded distribution service operated by Suno Studio and delivered to DSPs through an evaluated wholesale, white-label, or third-party provider where direct relationships do not yet exist.

The studio intends to own and operate the artist/client experience and the internal functions that pass readiness review. A delivery partner may provide DSP delivery infrastructure. Provider-supplied and internally operated functions must be identified accurately. Disclose the underlying provider where legally, contractually, or operationally required; do not imply direct DSP agreements before they exist.

The target window is for planning and gated readiness work, not a promise of commercial availability. Distinguish:

- **Internal readiness target:** Complete requirements, architecture, and readiness work toward a controlled pilot within the 3-9-month planning window.
- **Pilot-launch target:** A very small private pilot may be considered in that window only if its entry gates pass and it receives explicit go/no-go approval.
- **Commercial availability:** No date is set; it requires successful pilot evidence and completed legal, financial, provider, security, support, and operational gates.
- **Direct DSP approval:** External and not guaranteed by this roadmap.
- **Full production capability:** Not declared by the existence of a portal or successful individual delivery; requires sustained operational evidence and approved readiness review.

#### Workstreams

1. **Business and legal:** Identify the required operating entity, banking and tax obligations, and qualified review for terms, privacy, artist/client agreements, distribution authorization, contributor/split terms, takedown/dispute, AI-content, voice/likeness, refunds/termination, and retention. Do not present drafts as authoritative legal instruments without qualified review.
2. **Wholesale-provider due diligence:** Compare white-label availability, DSP coverage and AI-content rules, limits, fees/revenue share, terms and exit rights, catalog/identifier portability, review/correction/takedown, fraud controls, royalty and tax data, payment timing, API/file exchange, branding and data ownership, support/escalation, service levels, security, continuity, and provider-failure handling. Do not select solely on price.
3. **Intake and catalog architecture:** Design client, artist, and release intake; rights evidence; contributor data; metadata and asset validation; identifier governance, including ISRC/UPC handling and portability; approval; delivery receipt; catalog, correction, and takedown states; and royalty/statement linkage. Keep assessment separate from remediation.
4. **Accounting and royalty operations:** Design report ingestion and normalization, artist/track matching, split calculations, fee/deduction/adjustment handling, statements, payout approval, reconciliation, tax evidence, disputes, and immutable audit history. Define reserves only where legally appropriate and after qualified review. Do not handle client funds until financial controls are reviewed and tested.
5. **Security and reliability:** Define least privilege and role separation, credential management, MFA, audit logs, backup/recovery, idempotent delivery and duplicate prevention, reconciliation, monitoring/alerts, incident response, rollback, provider-outage handling, and a small pilot blast radius.
6. **Support operations:** Define intake, release-review, correction, takedown, escalation, incident communications, artist support, data requests, account closure, and catalog migration expectations.

#### Branded-Distribution Milestones

1. **Strategy and requirements:** Service boundary, provider requirements, legal/financial gaps, build-versus-buy analysis, and pilot scope documented and approved.
2. **Provider due diligence:** Candidates assessed for AI-content policy, coverage, portability, commercial terms, security, support, and exit risks; provider choice remains a separate decision.
3. **Internal alpha:** Internal catalog only; no external client promises. Test intake, metadata validation, delivery receipt, corrections/takedowns, royalty ingestion, and reconciliation.
4. **Controlled private pilot:** Very small number of consented participants under explicit pilot terms, manual approval gates, human-reviewed releases, verified financial reporting, and exercised support.
5. **Branded-service readiness:** Qualified legal review, financial and security controls, active provider and client agreements, catalog migration method, tested incident/rollback procedures, and approved go/no-go review.

Do not declare the service operational because a portal exists. Each milestone requires recorded evidence; calendar progress does not substitute for a gate.

### Strategic: Direct Digital Distributor or Aggregator (12-18-Month Preferred; Less-Than-24-Month Outer Target)

After proving branded-distribution operations, pursue production-grade direct distribution capability. The target is a preferred 12-18 months and an outer planning limit of less than 24 months; neither date guarantees direct DSP acceptance.

The target capability includes DSP partnership management; production DDEX delivery; release/resource metadata; commercial terms and territory data; delivery acknowledgments; corrections, takedowns, and replacements; identifier governance; rights representation; fraud controls; royalty ingestion, statements, and payouts; tax operations; support; security; continuity; and audit/compliance evidence.

Before pursuing or claiming readiness, document evidence for an established legal entity, controlled catalog, proven branded operations, low metadata/delivery error rates, rights/takedown controls, production DDEX, identifier governance, accounting and client reporting, timely payouts, tax/financial controls, security review, monitoring, incident response, continuity, support capacity, catalog migration, provider exit strategy, and direct-partner relationship capability. Assess technical, operational, financial, legal, and platform-acceptance readiness separately.

### Not Approved or Activated

- New media products, interactive or personalized experiences, synthetic presenters, or automated adaptation.
- Pricing, sponsorship, revenue forecasts, client funds handling, or external client commitments.
- Provider selection, new distribution accounts, direct DSP agreements, or claims of direct delivery approval.
- Podcast hosts, advertising, recruitment, audience studies, or audience-data collection.
- Real-person voice assignments, voice-model training, generation, or distribution.
- Release cadence, specific albums, release dates, international campaigns, or commitments to publish.

All windows above are founder-directed planning targets, not commitments. Other candidates remain unscheduled. External dependencies include provider availability and terms, changing AI-content policies, DSP review and acceptance, legal and tax requirements, payment/banking arrangements, and service-provider reliability. Each operational milestone requires explicit scope, evidence, human approval, rights and privacy review, and a separate go/no-go decision.

## Album Pipeline

No album or release pipeline is approved by this roadmap. Existing catalog-first principles allow future curation of related works after separate creative and release approvals.

## Artist Development

No roster expansion, artist assignment, biography, audience profile, or voice assignment is authorized here. Existing identities and placeholders remain unchanged.

## Podcasting and Extended Media

Podcasting and other media remain strategic possibilities, not activated channels. Any future proposal must follow the [Adaptive Media Strategy](../research/ai-artists/adaptive-media-strategy-and-governance.md) and obtain separate editorial, rights, privacy, accessibility, and release approvals.

## Catalog Building

Preserve stable identities, source provenance, version history, and relationships between approved works. No catalog targets or release volume commitments are set.

---

## Cross-References

- Release calendar: `release-calendar.md`
- Workflow notes: `workflow-notes.md`
- Decision log: `../docs/decision-log.md`
