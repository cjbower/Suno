# Real-Person Voice Consent and Rights Governance

**Status:** Governance requirement for future work. No real-person voice assignment or production use is approved by this document.
**Scope:** Identifiable human voices used as source recordings, references, voice IDs, model inputs, generated performances, or other synthetic voice implementations.

## Core Rule

Do not capture, ingest, analyze for voice replication, train or configure a voice model, assign a real-person voice to an artist, generate with it, edit it into a work, or distribute it until documented, informed, and sufficiently specific authorization and separate rights review are complete.

Consent must be affirmative and tied to the person whose voice is involved. It cannot be inferred from public availability, prior collaboration, a platform setting, a voice being technically accessible, a similar name, a model provider's general terms, or an artist's fictional identity. Consent and permission for a recording, composition, lyrics, likeness, or other rights are separate questions.

## Future Quality-Control Direction

Consented real-person voice use is an approved future quality-control direction for assessing voice consistency, reproducibility, and unintended drift across implementations or model changes. Any evaluation must compare against an authorized reference and retain the model/version and relevant generation context. Human review remains authoritative; no similarity threshold, automatic approval, or production workflow is established here.

Quality control does not require cloning or generating a person's voice. Each capture, analysis, model, assignment, and generation activity remains subject to its own documented authorization and rights review. No real-person voice is assigned or used by this document.

## Separate Permissions

Before any future use, document the permissions that apply to each intended activity rather than treating one general approval as blanket consent:

- Collection and storage of a voice recording or reference.
- Voice analysis, model creation, fine-tuning, or other training.
- Inference or generation using an existing model or voice ID.
- Editing, transformation, translation, or creation of derivative performances.
- Assignment to a named artist or character.
- Internal evaluation, commercial use, advertising, public distribution, and cross-media use.
- Retention, model access, transfer to providers, and post-termination handling.

The consent record should identify the permitted materials, model or provider where known, purpose, channels, territories, duration, compensation terms if any, attribution or disclosure expectations, restrictions, and how the person can raise concerns or request a pause. The terms must be clear about whether generated output may be reused and whether consent can be withdrawn from future use.

Consent is not legal advice and does not establish ownership or clear third-party rights. Obtain appropriate legal and rights review before using agreements or relying on permissions.

## Human Review Gates

1. **Identity and provenance:** Confirm who provided the voice and who controls the source recording. Do not use an assumed identity or rely on voice similarity alone.
2. **Scope and authorization:** Confirm the person understands the specific capture, modeling, generation, edits, attribution, distribution, and reuse contemplated.
3. **Rights review:** Separately assess source recordings, music, lyrics, likeness, contractual restrictions, provider terms, and applicable law.
4. **Assignment approval:** Record an explicit, time-bounded relationship between the person, voice implementation/version, artist, and permitted work. Do not infer one from registry structure or an experiment.
5. **Release review:** Confirm that the final use remains inside the authorized scope and apply any approved disclosure or attribution.
6. **Change and withdrawal handling:** Pause new use when authorization is disputed, expired, or withdrawn; review existing outputs and obligations with the authorized human and legal reviewer.

No automated similarity, provenance, consent, or rights check can approve a use. A human reviewer must be able to inspect the evidence and record the decision.

## Prohibited Inferences and Higher-Risk Cases

- Do not imitate an identifiable person or imply that they performed, endorsed, or approved material without explicit authorization.
- Do not treat a public, community, or platform-provided voice as cleared merely because it can be selected.
- Do not extend authorization from one artist, work, model, platform, or medium to another without checking the documented scope.
- Do not use a minor's voice or a deceased person's voice absent specific legal, rights, and safeguarding review; pause and escalate rather than infer authority.
- Do not represent an AI-generated artist as a real person or fabricate a performance history.

## Records and Privacy

Maintain a minimal, access-controlled record of the authorization decision, scope, status, reviewer, dates, and evidence location. Store signed agreements, raw voice recordings, identity documents, and other sensitive materials only in an approved secure system, not in Git by default. A repository record may contain a non-sensitive evidence reference and status, but not a copy of confidential consent documents or raw voice data.

Follow the existing [Audience Research Privacy and Retention](../operations/audience-research/privacy-and-retention.md) principles for minimization, access, retention, withdrawal, and escalation where research is involved. Research participation does not constitute voice-use consent.

## Current Repository State

This standard changes no voice metadata, assignment, or experiment record. The placeholder entries in `catalog/metadata/voices.yaml` remain placeholders. Voice-ID-001 remains a partially validated experiment record; its metadata and human observations do not establish production readiness, a real-person assignment, or broad consent. See the [Voice Architecture Assessment](voice-architecture-assessment.md) and [Voice-ID-001 Registry](../research/suno-platform/experiments/voice-id-validation-registry.md).

## Related Governance

- [Voice Architecture](../creative/voice-architecture.md)
- [Voice Governance Principles](voice-governance-principles.md)
- [AI Music Platform Thesis](../foundations/ai-music-platform-thesis-and-strategic-vision.md)
- [Demo and Audience Research Governance](demo-and-audience-research-governance.md)
