# Voice Architecture Assessment

## Current State

`catalog/metadata/voices.yaml` contains a schema reference and 12 registry entries. The reference describes artist identifiers and names, voice category, range, tone, production signature, emotional territories, technical notes, recording preferences, creation date, and notes.

Each current entry includes an artist ID and artist name, a voice category, placeholder values for descriptive fields, an empty emotional-territories list, and a creation date. The `notes` field appears in the schema reference but is absent from the current entries. The schema reference does not declare which fields are formally required.

The current top-level keys and artist fields directly associate each entry with an artist. This phase makes no new assignments and does not change the registry.

## Known Risks

- Artist-linked keys and fields can imply a one-voice-per-artist model and couple a voice record's identity to an artist identifier.
- Placeholder descriptions and empty territory lists do not provide usable voice profiles.
- There are no version, lifecycle, approval, drift-review, retirement, or replacement fields.
- The reference does not describe implementation provenance or configuration needed to reproduce a voice version.
- The registry does not define how historic catalog references remain stable when an implementation changes.

## Design Decisions

- Treat artist identity and voice identity as separate concepts with separate identifiers.
- Preserve voice versions and their historical references rather than overwriting them.
- Require documented, human-reviewed changes for activation, drift response, retirement, and replacement.
- Do not infer artist-to-voice relationships from names or key formats.
- Treat the current registry structure as an observation, not as approval of its entries or relationships.

## Unresolved Questions

- Can one artist use multiple voice identities, and can a voice identity be shared across artists?
- Which provider, model, model version, and generation settings must be recorded for reproducibility?
- What provenance, consent, and authorization information is required for voice sources?
- What review criteria and evidence are sufficient to approve a version, assess drift, or approve a replacement?
- How should version identifiers and effective dates be represented?

## Recommendations

- Define and approve the voice identifier, version, lifecycle, and artist-relationship model before populating profiles or making assignments.
- Establish change review and catalog-reference rules before adopting replacement voices.
- Keep the current placeholder registry unchanged until the future metadata design is approved.

## Future Metadata Needs

Future metadata may need to represent:

- A stable voice identifier independent of artist identifiers, plus version and lifecycle status.
- Versioned voice characteristics and implementation configuration sufficient for reproducibility.
- Provenance, authorization, review status, and change history.
- Effective dates and predecessor or successor relationships for versions and replacements.
- Explicit artist-to-voice relationships, including applicable periods and relationship status.
- Stable catalog references to the voice version used, without rewriting historical associations.
