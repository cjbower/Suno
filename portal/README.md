# Temporary Founder Review Workbench

The existing `portal/` prototype is retained and reclassified as a temporary Phase 3.1A workflow-learning tool. It is experimental, read-only, local-development software; it is not the final Founder Review Portal and may be discarded after the workflow is understood.

The repository remains authoritative. The workbench reads the canonical `catalog/metadata/demos.yaml` and `catalog/metadata/demo-reviews.yaml` inputs. Do not add a separate metadata registry, edit generated output, or treat a displayed status as an approval.

## Current Capabilities

- Dashboard counts for registered demos, pending reviews, completed reviews, and classification eligibility.
- Read-only intake summary with source links and required evidence.
- Searchable/filterable demo review queue.
- Source-first demo detail with the repository ID, working title, source context, creative material, creator intent, constraints, source labels, readiness blockers, governance, and advanced metadata.
- Review completion and eligibility derived from existing review fields.

The prototype has no data-entry form, write-back, audio upload, authentication, backend, database, deployment workflow, or production hosting configuration. Classification, seed qualification, disposition changes, and artist assignment are not performed by the workbench.

The detail view reads only fields present in the canonical YAML. Screenshot-observed source metadata that has not been captured in those records is clearly identified as not captured; the UI does not hardcode or infer it. The review-readiness panel explains the existing founder-review gate and lists its blockers without changing the gate.

## Local Development

Requirements: Node.js `^20.19.0` or `>=22.12.0` and npm.

```sh
cd portal
npm ci
npm test
npm run dev
```

Vite serves the workbench locally. The YAML source is imported from the repository and parsed with `js-yaml`; there is no runtime API or database. Use the architecture and wireframe documents under `docs/architecture/` to record workflow findings.

Do not deploy the workbench, create Pages configuration or Actions, or implement write-back in this phase. The existing build script remains part of the prototype source but should not be used to create deployment output for this workflow-discovery exercise.
