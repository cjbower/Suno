# Founder Review Portal Wireframes

> **Status update:** These earlier portal sketches are retained as history. Phase 3.1A now treats the existing prototype as a temporary workflow workbench. See the [current workbench wireframes](founder-review-workbench-wireframes.md).

These are workflow wireframes, not visual specifications. They describe the earlier read-only portal scope; the current temporary-workbench screens and status are documented in the linked workbench wireframes.

## 1. Dashboard

```text
+-----------------------------------------------------------------------+
| Founder Review Portal                   Read-only | Repository source |
+------------------+----------------------------------------------------+
| Overview         | Founder review overview                            |
| Demo intake      |                                                    |
| Review queue     | [Registered demos] [Review pending] [Review complete]|
|                  | [Classification eligible]                          |
|                  |                                                    |
|                  | Needs attention                                    |
|                  | ID          Demo       Founder state   Disposition  |
|                  | DEMO-...    Carillon   Pending         Hold         |
|                  |                                                    |
|                  | Future workflows                                   |
|                  | Classification: unavailable                       |
|                  | Seed qualification: unavailable                   |
+------------------+----------------------------------------------------+
```

**Workflow:** Show counts derived from repository records and make the next pending review easy to open. Eligibility is a gate state, not an assigned value.

## 2. Demo Intake

```text
+-----------------------------------------------------------------------+
| Demo intake                                        Read-only source   |
+-----------------------------------------------------------------------+
| Demo ID: DEMO-2026-0001     Intake state: intake_incomplete          |
| Title: Carillon              Creator attribution: Christopher Bower   |
| Source: [Open Suno page]     Submitted: 2026-11-21                   |
|                                                                       |
| Intake evidence                                                       |
| Original audio: Not received     Checksum: UNKNOWN                   |
| Prompt and model: UNKNOWN        Rights review: UNKNOWN              |
| Provenance: [Open repository record]                                 |
|                                                                       |
| Missing evidence                                                     |
| - Original audio and checksum                                         |
| - Source material, rights context, prompt and model information       |
|                                                                       |
| [Open intake standard]                                                |
| Write intake: Not available in this read-only MVP                    |
+-----------------------------------------------------------------------+
```

**Workflow:** Make known and missing evidence explicit. The interface does not accept a submission or modify the canonical record.

## 3. Demo Review Queue

```text
+-----------------------------------------------------------------------+
| Review queue                                                         |
| Search [ID, title, creator...]   Review state [All v]                 |
|                                                                       |
| Demo         Review state   Founder review   Eligible   Disposition   |
| Carillon     Review Pending Pending          No         Hold          |
|                                                                       |
| Select a demo to view its review and evidence.                        |
+-----------------------------------------------------------------------+
```

**Workflow:** Search and filter records without changing them. Pending, complete, and eligible states are derived from linked review records.

## 4. Individual Demo Review

```text
+-----------------------------------------------------------------------+
| < Back to queue       DEMO-2026-0001                                  |
| Carillon | Intake incomplete | Review Pending                        |
+-----------------------------------------------------------------------+
| Source and provenance         | Founder review                        |
| Suno page: [Open]              | State: Pending                       |
| Provenance: [Open record]      | Reviewer: AI intake assistant        |
| Rights: UNKNOWN                | Audio reviewed: No                   |
|                                | Grades: N/R                           |
|                                | Evidence: N/R explanations            |
+--------------------------------+--------------------------------------+
| Current classification: UNKNOWN      Seed designation: UNKNOWN       |
| Classification Eligible: No          Disposition: Hold                |
|                                                                       |
| Founder review form: Not available in this read-only MVP              |
+-----------------------------------------------------------------------+
```

**Workflow:** Present intake facts separately from review conclusions. The MVP links to the canonical evidence and does not create a review.

## 5. Future Classification Workflow

```text
+-----------------------------------------------------------------------+
| Classification | DEMO-YYYY-NNNN                                       |
| Gate: Founder review complete and evidence present                    |
|                                                                       |
| Primary classification [Choose after evidence review]                 |
| Supporting evidence [Required]                                        |
| Rationale [Required]                                                  |
|                                                                       |
| Save as proposal: Disabled until write-back governance is approved    |
+-----------------------------------------------------------------------+
```

**Workflow:** Require a qualifying founder review first. Classification and rationale are proposed together; a UI selection alone must not change the authoritative value.

## 6. Future Seed Qualification Workflow

```text
+-----------------------------------------------------------------------+
| Seed qualification | DEMO-YYYY-NNNN                                   |
| Gate: Classification review complete and seed evidence present        |
|                                                                       |
| Seed designation [Choose after evidence review]                       |
| Reusable value and development potential [Evidence required]          |
| Rationale [Required]                                                  |
|                                                                       |
| Save as proposal: Disabled until write-back governance is approved    |
+-----------------------------------------------------------------------+
```

**Workflow:** Keep seed qualification separate from classification and require its own evidence and rationale. Disposition and development decisions remain separate approvals.
