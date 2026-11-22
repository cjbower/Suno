# Temporary Founder Review Workbench Wireframes

These are workflow-first sketches for the existing read-only prototype and future discovery conversations. They do not authorize new functionality. The current prototype implements the dashboard, demo queue, intake summary, and demo detail; the worksheets are read-only context or future design concepts.

## 1. Dashboard

```text
+--------------------------------------------------------------+
| Temporary Founder Review Workbench          Repository source |
+------------------+-------------------------------------------+
| Dashboard        | Portfolio snapshot                        |
| Demo queue       |                                           |
| Pending reviews  | Demos: 1  Review pending: 1               |
|                  | Review complete: 0  Classification: 0     |
|                  |                                           |
|                  | Next action                               |
|                  | DEMO-2026-0001  Carillon  Review pending   |
|                  | Hold  | Required evidence: 4               |
+------------------+-------------------------------------------+
```

**Questions to observe:** Which counts change the founder's next action? Is an evidence count useful, or is the evidence list needed immediately?

## 2. Demo Queue

```text
+--------------------------------------------------------------+
| Demo queue                                                   |
| Search [ID, title, creator...]   State [All v]               |
|                                                              |
| Demo         Intake       Founder review    Disposition      |
| Carillon     Incomplete   Pending           Hold             |
|                                                              |
| Select a row to inspect source, review, and next action.      |
+--------------------------------------------------------------+
```

**Questions to observe:** Does the founder search by title, ID, creator, source, status, or next action? Which sort and filter choices are actually used?

## 3. Pending Founder Reviews

```text
+--------------------------------------------------------------+
| Pending founder reviews                                      |
|                                                              |
| DEMO-2026-0001  Carillon                                    |
| Founder status: Pending     Audio reviewed: No              |
| Review record: REVIEW-2026-0001                              |
| Missing: original audio, source context, founder listening   |
| [Open demo detail]                                           |
+--------------------------------------------------------------+
```

**Questions to observe:** Is a separate pending queue useful, or is a filter on the demo queue sufficient? Which missing item blocks action?

## 4. Demo Detail View

```text
+--------------------------------------------------------------+
| < Queue       DEMO-2026-0001  Carillon                       |
| Review pending | Founder review pending | Not eligible       |
|                                                              |
| Source / provenance          Intake                          |
| Suno URL                     Status: intake_incomplete        |
| Provenance record            Rights: UNKNOWN                  |
| Audio: not received          Checksum: UNKNOWN                |
|                                                              |
| Current classification: UNKNOWN   Seed: UNKNOWN               |
| Disposition: Hold   Next action: receive source audio         |
| Required evidence: [list]    Risks: [list]                    |
+--------------------------------------------------------------+
```

**Questions to observe:** Which fields should be above the fold? Which links or unknowns are repeatedly revisited?

## 5. Review Worksheet

```text
+--------------------------------------------------------------+
| Founder review worksheet | DEMO-2026-0001                    |
| Audio: unavailable   Founder state: Pending                   |
|                                                              |
| Criterion                  Grade       Written evidence      |
| Emotional impact           N/R         No audition            |
| Song concept               N/R         Context incomplete     |
| Hook                       N/R         No audition            |
| Source fidelity            N/R         Source unknown         |
| Voice / production / ...   N/R         No audition            |
|                                                              |
| Reviewer, date, completion state, evidence links             |
| Save/write: not available in temporary workbench              |
+--------------------------------------------------------------+
```

**Current prototype:** Displays linked review summary; it does not provide an editable worksheet or create a review record.

## 6. Classification Worksheet

```text
+--------------------------------------------------------------+
| Classification worksheet                                     |
| Gate: qualifying founder review required                     |
| Current primary: UNKNOWN                                     |
|                                                              |
| Allowed value [Not defined yet]                              |
| Evidence reference [Required]                                |
| Rationale [Required]                                         |
|                                                              |
| Decision / save: not available                               |
+--------------------------------------------------------------+
```

**Discovery question:** What classification values and criteria are genuinely useful? Do not encode choices before the founder defines them.

## 7. Seed Qualification Worksheet

```text
+--------------------------------------------------------------+
| Seed qualification worksheet                                 |
| Gate: founder review complete                                |
| Current designation: UNKNOWN                                 |
|                                                              |
| Seed value criteria [Not defined yet]                        |
| Evidence reference [Required]                                |
| Reusable potential and rationale [Required]                  |
|                                                              |
| Decision / save: not available                               |
+--------------------------------------------------------------+
```

**Discovery question:** What distinguishes a seed from a promising demo, and what evidence supports that distinction?

## 8. Disposition Worksheet

```text
+--------------------------------------------------------------+
| Disposition worksheet                                        |
| Recommended disposition [Select from approved standard]      |
| Rationale [Required]                                         |
| Owner [Required for nonterminal action]                      |
| Next action [Bounded]   Required evidence [List]              |
| Review trigger [Event or date]   Risks [List]                 |
|                                                              |
| Development authorization: separate Approved Development Brief|
| Decision / save: not available                               |
+--------------------------------------------------------------+
```

**Discovery question:** Which disposition fields are repeatedly missing or difficult to maintain consistently with the hold plan?

## 9. Future Artist Fit Review

```text
+--------------------------------------------------------------+
| Artist fit review - future workflow                          |
| Gate: review and rights evidence available                  |
|                                                              |
| Candidate entity      Evidence for fit      Counter-evidence |
| Existing artist       Source / emotion      Identity conflict |
| Band / producer       Voice / production    Rights / gaps     |
|                                                              |
| Status: unassigned until explicit human approval             |
| Assignment and Development Brief: separate decisions         |
+--------------------------------------------------------------+
```

**Discovery question:** What evidence is needed to compare fit without turning suggestions into automatic assignment?
