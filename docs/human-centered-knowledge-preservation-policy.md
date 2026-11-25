# Human-Centered Knowledge Preservation Policy

## Purpose

Protect strategic, creative, historical, interpretive, research, policy, and other human-oriented knowledge from destructive automated cleanup.

## Governing Principle

Preserve first.

Annotate uncertainty.

Seek human approval before removal.

## Scope

This policy covers human-centered knowledge in strategy, vision, mission, creative guidance, historical context, research notes, naming inspiration, interpretive analysis, cultural observations, lessons learned, working hypotheses, editorial judgment, policy intent, governance rationale, architecture rationale, decision history, founder observations, long-term direction, audience concepts, business concepts, product concepts, and documentation that explains why the project exists and how it developed.

Approximate, interpretive, incomplete, subjective, historical, unverified, or provisionally sourced material may remain useful when its status and purpose are understandable to a human reader.

## Distinction From Code

Application code, tests, scripts, schemas, configuration, build output, generated artifacts, machine-readable registries, credentials, duplicate binaries, temporary products, invalid syntax, and deterministically obsolete implementation details may require precise technical correction or different handling.

This policy does not weaken technical quality, security, rights, legal, privacy, financial, or production-record standards. When a document combines operational facts and human-centered context, distinguish the two and apply the appropriate standard to each; do not erase the human-centered context merely because it is not machine-enforceable.

## Evidence Classes

Use clear labels and context to distinguish evidence and purpose:

1. **Authoritative operational record:** An approved source of truth for a defined operational fact or state.
2. **Verified external evidence:** Information checked against an identified external source, with provenance and verification date where relevant.
3. **Research finding:** A recorded result of a stated research activity, including its scope and limitations.
4. **Interpretation:** Human analysis or meaning drawn from evidence; not itself a verified fact.
5. **Creative guidance:** Direction intended to inform human creative judgment, not necessarily to constrain automation.
6. **Historical context:** Material preserved to explain prior conditions, decisions, or development.
7. **Working hypothesis:** A provisional explanation or proposition that may be tested or revised.
8. **Inspiration or brainstorming material:** Ideas and associations retained to support exploration and future judgment.
9. **Unknown or unverified information:** Information whose accuracy, source, or current applicability has not been established.

Classes 3-9 may remain useful to people without being suitable for automated enforcement. Preserve their labels, provenance, limitations, and intended use; do not present them as authoritative operational records.

## Mandatory Human Review

Luna must obtain explicit founder approval before substantively deleting, replacing, deprecating, archiving, or meaning-changingly consolidating human-centered knowledge. This requirement applies even when a change is recoverable through Git history.

The review request must include the information and approval choices specified in **Required Review Packet** below. Until explicit approval is received, preserve the material as-is. Do not infer approval from a broad task instruction or from a general preservation principle.

## Destructive-Change Thresholds

Human review is mandatory when a proposed operation:

- Deletes more than 25 substantive lines from one human-centered file.
- Deletes more than 100 substantive lines across a task.
- Removes a table, list, dataset, example set, narrative section, rationale, or historical record.
- Replaces detailed content with a summary.
- Changes strategic or policy meaning.
- Withdraws or deprecates human-oriented research.
- Moves content to a less discoverable location.
- Removes content because source retrieval failed or it cannot be revalidated.
- Removes subjective or interpretive content because it is not machine-verifiable.

These are minimum review triggers, not permission to delete smaller amounts without judgment. The approval requirement also applies to the substantive actions listed under **Mandatory Human Review**, regardless of line count.

## Required Review Packet

Before a destructive or meaning-altering action, present:

1. Exact files affected.
2. Exact sections affected.
3. A summary of information that would be removed or materially changed.
4. Why the change is believed necessary.
5. Evidence supporting the concern.
6. Preservation alternatives.
7. Expected line deletions and additions.
8. Whether historical knowledge would become available only through Git history.
9. Potential loss of context, nuance, provenance, or future usefulness.
10. A proposed non-destructive alternative.
11. An explicit approval choice.

The approval choices must include:

- Preserve as-is.
- Preserve and annotate.
- Move to a clearly indexed historical or exploratory section.
- Revise without deleting substantive content.
- Delete the identified content.
- Cancel the proposed change.

Silence or an absent response means preserve as-is.

## Allowed Non-Destructive Alternatives

Prefer alternatives that retain the original perspective and make uncertainty legible:

- Add a status banner.
- Add provenance.
- Add limitations.
- Add a verification date.
- Add a superseding note.
- Preserve historical text in place.
- Move a copy to an indexed archive with explicit pointers.
- Separate authoritative conclusions from exploratory notes.
- Mark content as unsuitable for automation.
- Add counter-evidence without deleting the original perspective.

## Approval Semantics

- Silence is not approval.
- A broad task is not approval for a destructive change.
- Tool inability to verify a claim is not evidence that the claim is false.
- Failed retrieval is not authorization for deletion.
- Code-level precision must not automatically govern creative documentation.
- Human-centered knowledge must not be rewritten into machine-oriented language without approval.
- When uncertain, Luna must preserve the material and ask.

## Emergency Exceptions

Immediate, narrowly scoped removal is allowed only for:

- Exposed secrets or credentials.
- Malware.
- Private personal data improperly committed.
- Material whose retention creates an immediate, documented legal or safety risk.
- Corrupted generated artifacts that are reproducible and are not source material.

Even in these cases, preserve an audit record, minimize scope, notify the founder, and do not silently remove surrounding context.

## Audit Requirements

Document:

- The request.
- The proposed deletion.
- The human decision.
- Files changed.
- Content preserved elsewhere.
- Commit SHA.
- Validation.
- Rollback method.

## Ownership

**Owner:** Christopher Bower

**Policy status:** Approved

**Effective:** Immediately upon commit
