# Temporary Founder Review Workbench

The existing `portal/` prototype is retained as a temporary local workflow-learning tool. The Voice-ID-001 form has an accepted alpha writeback proof-of-concept; all other workflows remain read-only. This is not the final Founder Review Portal and may be discarded after the workflow is understood. See the [accepted evaluation persistence principles](../docs/architecture/founder-review-workbench.md#evaluation-persistence-design-principles) before extending writeback to other workflows.

The repository remains authoritative. The workbench reads canonical `catalog/metadata/demos.yaml`, `catalog/metadata/demo-reviews.yaml`, and `catalog/metadata/voice-experiments.yaml` inputs. The voice experiment record is a separate evidence stream; it does not participate in demo intake or the founder-review eligibility gate. Do not treat an uncommitted repository snapshot or displayed status as an approval.

## Current Capabilities

- Dashboard counts for registered demos, pending reviews, completed reviews, and classification eligibility.
- Read-only intake summary with source links and required evidence.
- Searchable/filterable demo review queue.
- Source-first demo detail with the repository ID, working title, source context, creative material, creator intent, constraints, source labels, readiness blockers, governance, and advanced metadata.
- Review completion and eligibility derived from existing review fields.
- Dedicated Voice Experiment Review view for Voice-ID-001 with control/treatment clip links, evidence-separated findings, and a structured listening assessment form.
- Listener name is free-form with datalist suggestions from the existing observation and prior Voice-ID-001 submissions. Names are evaluation metadata, not authenticated identities.
- Voice-ID-001 submissions are validated and saved through a loopback-only Vite development middleware to the experiment YAML and its two Markdown records. Each save appends an audit entry and a uniquely named JSON snapshot; the earlier dated export is preserved.

The prototype has no authentication, user accounts, permissions, database, deployment workflow, or production hosting configuration. The writeback endpoint exists only in Vite's development server, is limited to Voice-ID-001, and is not included in production builds. Classification, seed qualification, demo disposition, founder review, focus groups, and discovery intake remain read-only or unimplemented.

The demo detail view and Voice Experiment Review read canonical YAML. Screenshot-observed source metadata that has not been captured in demo records is clearly identified as not captured; the UI does not hardcode or infer it. The Voice-ID-001 page loads its original observation from the experiment registry and the latest structured submission from repository state. The review-readiness panel explains the existing founder-review gate and lists its blockers without changing the gate.

## Local Development

Requirements: Node.js `^20.19.0` or `>=22.12.0` and npm.

```sh
cd portal
npm ci
npm test
npm run dev
```

Vite serves the workbench at loopback and hosts the Voice-ID-001 writeback API. Canonical YAML sources are parsed with `js-yaml`. The API writes only `catalog/metadata/voice-experiments.yaml`, `research/suno-platform/experiments/voice-id-validation-registry.md`, and `research/suno-platform/experiments/voice-influence-test-2026-11-24.md`; it also creates a unique JSON snapshot without overwriting existing exports. Submissions include the exact listener name and an audit of changed values. There is no authentication or identity verification; the listener-name field is evaluation metadata only.

The endpoint rejects non-loopback and cross-origin writes, unknown fields, stale revisions, and invalid answer values. It is a controlled Voice-ID-001 proof-of-concept, not a general repository write service. Do not deploy it, expose it on a network interface, or reuse it for founder reviews, focus groups, or discovery intake. Use the architecture documents under `docs/architecture/` for the workflow boundaries and audit model.
