# Demo Triage Workflow

## Flow

1. **Receive** into the internal intake queue only when the submission class is active.
2. **Validate** required provenance, access, audio checksum, source context, and known rights conditions.
3. **Preserve intake facts** and mark classification and seed designation `UNKNOWN`.
4. **Conduct founder review** and record the reviewer, date, completed status, and written evidence.
5. **Classify and qualify** only when completed founder-review evidence supports the classification and seed designation; otherwise retain `UNKNOWN`.
6. **Determine disposition** and record its evidence, owner, next action, risks, and review trigger.
7. **Route** eligible opportunities as recommendations. Only an approved Development Brief can authorize internal development.

Intake never determines value. The required sequence is: demo exists → intake → UNKNOWN → founder review → classification → seed qualification → disposition → development decision.

## Lifecycle States

```text
submitted
intake_incomplete
intake_validated
triage
under_review
focus_group
development_candidate
in_development
on_hold
approved_seed
promoted_to_work
collaboration_candidate
handoff_candidate
licensing_candidate
declined
withdrawn
archived
```

`declined` means not accepted for current development. `withdrawn` means the authorized submitter removed it from consideration. `archived` means preserved without current action. `approved_seed` means approved as a development reference. `promoted_to_work` means a separate work or composition record was created; the original demo remains preserved.

## Triage Controls

- An intake pass is not creative approval, rights approval, an assignment, or a release decision.
- Classification and seed designation are not intake decisions; do not populate their primary values before a completed founder review.
- An AI intake screen, N/R-only review, title, lyrics, or public-page metadata does not satisfy the founder-review gate.
- A missing or technically inaccessible asset is not an F grade.
- Do not infer artist, band, producer-project, voice, or audience fit from the submitter or title.
- Preserve promising elements even when the complete demo is declined or archived.
- Every nonterminal disposition identifies an owner, next action, required evidence, review trigger, and open risks.

## Audience Research

Only A&R may request an audience study through Audience Research Operations. Research does not replace triage or authorize production, assignment, or release.
