# Music Taxonomy and Creator-Intent Framework

## Purpose and Authority

This document is the repository's authoritative baseline for music taxonomy and creator-intent analysis. It consolidates terminology already present in the repository and distinguishes controlled values from examples, descriptive language, workflow states, and unresolved concepts.

The framework does not change demo, review, artist, voice, or catalog records. It does not infer a review conclusion from intake data. Where the repository has no approved value set, the gap is explicit: retain `UNKNOWN` rather than inventing a value.

The creative sequence remains source-first: source material informs the emotional objective; artist assignment and genre serve that objective. Creator intent records what the creator meant to request. Founder review independently assesses the resulting work and may agree or disagree with that intent.

### Term status

- **Current controlled vocabulary:** An enumerated set already governed by a repository standard or registry.
- **Evidence-grounded taxonomy term:** A normalized category drawn from existing repository language. Preserve the source wording and subtype where available.
- **Descriptor or example:** Useful descriptive language, but not a closed list of permitted values.
- **Unresolved:** No approved vocabulary or definition exists. Keep the corresponding record value `UNKNOWN` until governance approves one.

Use stable identifiers in future structured data. Keep display labels, aliases, parent relationships, definitions, provenance, and taxonomy version separate. A term's appearance in a prompt, example, or template does not by itself make it a controlled value.

## 1. Source Material Taxonomy

The following source families are grounded in the repertoire structure and foundational documents. They are a reusable classification baseline, not a claim that every possible source has been enumerated. A source may belong to more than one family; preserve the exact source reference and any more specific subtype.

| Source family | Documented material and provenance |
|---|---|
| Scripture and spiritual texts | Psalms, Scripture, daily readings, sacred poetry, spiritual narratives, and meditations. The Psalms Initiative specifically names Psalms, daily readings, sacred poetry, and related spiritual themes. |
| Historical texts and narratives | Historical documents, primary sources, stories, speeches, letters, and civic narratives. Repository collections include Revolutionary War material and historical documents. |
| Poetry and literary works | Poetry, literature, and literary material. Keep poetry distinct from the broader literary-work family where the source record supports that distinction. |
| Virtue, moral, and civic material | Virtue literature, character-focused material, civic themes, and civic virtues. |
| Saints' lives and hagiography | Saints' lives, hagiography, and related spiritual narratives. |
| Personal narratives | Personal stories and narratives, including creator-provided material where applicable. |
| Original lyrics and written content | Original lyrics and other written content that serve as a source for a work. Preserve the source separately from adapted lyrics. |
| Thematic concepts | A theme or concept used as the creative starting point when there is no discrete source text. |
| Other or not yet classified | Use `UNKNOWN` when evidence is unavailable. Do not use this as a catch-all label when a more specific source family is supported. |

Repository folders such as `psalms/`, `daily-readings/`, `revolutionary-war/`, `historical-documents/`, `virtues/`, `saints/`, and `poetry/` are documented source collections. They are useful subtypes, but folder names alone do not establish authorship, edition, rights, or a complete source taxonomy.

Keep these separate from source material type:

- **Source origin and ownership:** creator, submitter, publisher, acquisition, or other provenance.
- **Submission class:** how a demo arrived; see the intake vocabulary below.
- **Topic or theme:** what a source is about.
- **Adaptation:** how the source was changed into lyrics or another work.
- **Rights status:** a separate review, never inferred from age, source type, or ownership assertion.

For each source, record enough provenance to identify and revisit the exact material, including title, author or origin when known, edition or translation, dates, access details, adaptation notes, and rights or permission status.

## 2. Genre Taxonomy

The `Supported Genres` section of the genre portfolio enumerates the following **22 labels**. These are the current evidence-backed genre terms; the portfolio does not define a consistent family/subgenre hierarchy.

| Genre label | Notes |
|---|---|
| Pop | Listed as a supported genre. |
| Rock | Listed as a supported genre; the description spans soft rock to hard rock. |
| Alternative | Described as an umbrella term. |
| Country | Listed as a supported genre and described as rooted in American folk traditions. |
| Americana | Described as a broad category encompassing American folk traditions, country, blues, gospel, and bluegrass. |
| Indie Rock | Listed as a supported genre; the description also references independent production and DIY identity. |
| Singer-Songwriter | Listed as a genre, although its description also denotes a creator/performer role and format. |
| Hip-Hop | Listed as a supported genre. |
| Rap | Listed separately from Hip-Hop; their boundary is not defined. |
| R&B | Listed as a supported genre and described as soul-influenced. |
| Electronic | Listed as a supported genre. |
| Dance | Listed as a supported genre. |
| House | Listed as a supported genre and described as a dance-music subgenre. |
| EDM | Listed as a supported genre and described as an umbrella that includes house, techno, and dubstep. |
| Alternative Pop | Listed as a supported genre. |
| Post-Punk | Listed as a supported genre. |
| Grunge | Listed as a supported genre and described as a rock subgenre. |
| Metal | Listed as a supported genre; the description spans heavy metal, progressive metal, and alternative metal. |
| Latin | Listed as an umbrella term; examples include salsa, cumbia, bachata, and reggaeton. |
| Regional Mexican | Listed as a musical tradition; examples include corridos, ranchero, and norteño. |
| Christian | Listed as a supported genre, although its description also denotes faith perspective or audience. |
| Gospel | Listed as a supported genre and described as a vocal and musical tradition. |

### Count discrepancy and correction

The genre portfolio and Manifesto V2 enumerate the same 22 labels. All four tracked revisions of the genre portfolio inspected during the discrepancy review also contain these same 22 headings; no removed, renamed, or merged twenty-third entry was found. The “23 genres” statements in the README, changelog, and Phase 2A validation report were count errors, not evidence of an additional genre.

On 2026-11-21, the current README was corrected to say “22 currently enumerated genres.” The historical changelog and Phase 2A validation report retain their original wording with an annotation explaining the count discrepancy. The foundations README's illustrative example no longer uses an unsupported count. This correction documents the existing list only; it does not change genre definitions or add a genre.

### Explicitly documented hierarchy and overlap

The portfolio and identity framework document the following relationships or examples. They are evidence of overlap, not a complete or consistently governed hierarchy:

- Rock ranges from soft rock to hard rock; Grunge is described as a rock subgenre.
- Americana encompasses American folk traditions, Country, blues, Gospel, and bluegrass.
- Alternative may incorporate post-punk, indie, or experimental elements.
- EDM includes House, techno, and dubstep; House is also separately listed and described as a dance subgenre.
- Metal ranges across heavy metal, progressive metal, and alternative metal.
- Latin includes salsa, cumbia, bachata, and reggaeton.
- Regional Mexican includes corridos, ranchero, and norteño.
- Christian music ranges from contemporary Christian music to Christian rock to Gospel.
- The identity framework uses `folk`, `Christian contemporary`, `Latin-influenced`, `folk ballad`, `uptempo pop`, and `electronic experimentation` as examples, not as additions to the 22-label supported list.

For future structured data, distinguish `genre_family`, `genre`, and `subgenre_or_idiom`, and record parent/child relationships only when approved. Do not silently merge Hip-Hop with Rap, House with EDM, Latin with Regional Mexican, or Christian with Gospel. Preserve multiple applicable labels when a work is hybrid.

## 3. Style Taxonomy

The repository does not establish one closed “style” vocabulary. It documents several distinct dimensions that should not be collapsed into genre:

| Style dimension | Existing evidence and boundary |
|---|---|
| Musical influence | Genre descriptions mention American folk, country, blues, Gospel, bluegrass, punk, indie, experimental elements, soul, heavy metal, Latin American and Latino traditions, Mexican regional traditions, and African American spiritual and church music. These are documented influences or traditions, not a complete influence list. |
| Arrangement and instrumentation | Examples include acoustic guitar, electric guitar, drums, bass, steel guitar, banjo, fiddle, Latin percussion, accordion, trumpet, synthesizers, and digital production. Treat these as arrangement/instrument descriptors, not genres. |
| Vocal performance | Standards prefer conversational and natural delivery, emotional authenticity, dynamic variation, clarity, and minimal processing. They discourage affectation, oversinging, unnecessary runs, and vocal gymnastics. |
| Production | The production guide prefers clean recordings, conversational vocals, minimal vocal processing, emotional connection, modern production, and dynamic contrast. It advises against excessive reverb or delay, theatrical Broadway or musical-theater delivery, overproduced vocals, and accidental robotic delivery. |
| Prompt-level sound descriptors | Suno experiments record terms such as close-mic, intimate, natural breathing, subtle imperfections, conversational phrasing, realistic dynamics, emotional nuance, clear diction, warm vocal tone, and professional studio recording. These are experimental prompt descriptors, not validated taxonomy values. |
| Arrangement constraints | `A cappella`, `solo voice only`, `no instruments`, and `no accompaniment` are prompt constraints or arrangement choices, not genres or voice archetypes. |

Artist-specific production DNA may refine general preferences for an artist, but current roster documents are mostly placeholders. The motif library is also a template with no populated controlled motif vocabulary. Do not infer artist style or musical influence from an artist name or placeholder.

## 4. Creator Intent Taxonomy

No separate creator-intent value list or `creator_intent` object currently exists in the demo registry. The framework establishes five intent dimensions for future analysis:

1. **Source material:** what text, narrative, theme, or other material the creator intended to use.
2. **Intended genre:** the creator's stated genre or genres, mapped to the genre taxonomy when possible.
3. **Intended style:** the creator's stated influences, arrangement, performance, and production descriptors.
4. **Intended voice:** the requested voice identity or sound, kept distinct from assigned artist and technical voice profile.
5. **Intended project purpose:** what the creator wants the work or project to accomplish.

These are facets of intent, not review judgments. Keep the creator's wording and the normalized taxonomy mapping side by side. An unrecognized phrase remains available as raw text and is not forced into the nearest category.

### Prompt analysis procedure

For future intake:

1. Preserve the original prompt, exclusion prompt, creator notes, and lyrics without rewriting them. Record whether each item was supplied or unavailable.
2. Extract explicit statements first. Attribute each statement to its source, such as prompt, creator note, lyric, or intake metadata.
3. Map explicit terms to the relevant taxonomy domain. Preserve the exact phrase, normalized term, evidence location, and taxonomy version.
4. Treat an interpretation based on lyrics or context as an inference, not a creator statement. Record its rationale and uncertainty separately; do not overwrite explicit intent.
5. If evidence is absent, conflicting, or ambiguous, retain `UNKNOWN` for the unresolved facet and request clarification when appropriate.
6. Record generator and model/version when available. Suno prompt behavior and outputs may vary by model/version; prompt terms are not guarantees about the resulting audio.

An intent analysis describes the creator's requested direction. It does not establish that the generated audio meets the request, that the work is valuable, or that it should be classified or developed.

## 5. Project Purpose Taxonomy

There is no controlled project-purpose list. The repository documents these purpose concepts, which can inform a future multi-valued vocabulary but are not yet approved as closed enum values:

- Artistic expression and emotional authenticity.
- Faithful cultural translation into contemporary forms and meaningful listening.
- Education and context for historical or scriptural source material.
- Spiritual reflection and storytelling.
- Stewardship of source material, creative work, decisions, and institutional knowledge.
- Catalog development and continuity.

Distinguish a project's **purpose** from its **medium**, **source**, **theme**, and **commercial or release status**. Documented media include music, podcasts, publishing, and related media. “Psalms Initiative” and “Historical Initiative” are named program contexts, not purpose values or genres. Purpose may be multi-valued and should retain creator wording and provenance.

## 6. Review Classification Taxonomy

### Demo-value classification

The demo registry has `classification.primary` and secondary classification fields, but does not define permitted classification values. The evaluation standard requires a completed, documented founder review with written evidence before a primary classification is assigned. Until a vocabulary is approved and evidence supports an individual conclusion, the classification remains `UNKNOWN`.

The historical strings `song_candidate` and `song_seed` are not approved classification or seed values. A `song_candidate` or `collaboration_candidate` field in the registry can be an entity reference; it does not define a demo-value classification.

### Review evaluation grades

The evaluation standard does define this controlled grading vocabulary:

| Grade | Meaning |
|---|---|
| `A` | Exceptional: strong emotional response and clear development or release potential. |
| `B` | Strong: meaningfully above average and worth developing with identifiable improvements. |
| `C` | Average or mixed: viable or interesting, but not compelling enough to prioritize without more evidence. |
| `D` | Weak: substantial problems; preserve only if specific elements retain value. |
| `F` | Does not work in its current form; archive unless a salvageable element is identified. |
| `N/R` | Not rateable because context was insufficient, a technical problem occurred, or the criterion could not be evaluated fairly. |

Grades require written evidence. Overall grades are editorial judgments, not arithmetic averages. `N/R` is not a negative creative judgment. These review grades are not demo classifications, seed designations, dispositions, or lifecycle states.

The evaluation schema names dimensions such as emotional impact, song concept, hook, source fidelity, voice performance, production identity, arrangement, technical quality, roster fit, development potential, and overall creative grade. These are review criteria, not classification terms.

The review schema also records narrative semantic profiles for the pairs forgettable/memorable, generic/distinctive, artificial/human, weak/powerful, confusing/clear, dated/contemporary, and emotionally flat/emotionally affecting. These comments are not scores or controlled demo classifications.

## 7. Seed Designation Taxonomy

The demo registry defines primary and secondary strategic seed-designation fields, but no permitted seed values. A primary seed designation requires a completed founder review and written supporting evidence. Until an approved vocabulary and sufficient evidence exist, retain `UNKNOWN`.

Do not conflate:

- **Seed designation:** an evaluative conclusion about strategic seed value; its values remain undefined.
- **Disposition `approve_as_seed`:** an A&R recommendation to preserve a demo as an approved development reference; it is not production authorization.
- **Lifecycle state `approved_seed`:** a workflow state in the demo registry, not a seed taxonomy term.
- **Development authorization:** requires a separate Approved Development Brief.

Do not migrate the historical `song_seed` label as an approved value or infer seed status from a disposition, review grade, or intake field.

## 8. Disposition Taxonomy

The A&R disposition standard defines these 13 values. A disposition is a recommendation or bounded next-step path, not a creative classification, seed value, lifecycle state, or automatic authorization.

| Disposition | Governed meaning |
|---|---|
| `approve_as_seed` | Preserve as an approved development reference; not production authorization. |
| `develop_concept` | Authorize concept work only through an approved Development Brief. |
| `develop_voice` | Evaluate a voice approach through an approved brief; does not create or assign a voice. |
| `develop_song` | Develop the composition through an approved brief. |
| `develop_production` | Develop production through an approved brief. |
| `assign_to_existing_artist` | Recommend assignment; requires explicit human approval and documented fit. |
| `evaluate_as_new_artist` | Recommend identity evaluation only; does not create an artist. |
| `evaluate_as_new_band` | Recommend identity evaluation only; does not create a band. |
| `route_to_producer_project` | Recommend review by an existing producer project; does not alter project ownership. |
| `collaboration_candidate` | Preserve a possible collaboration path; no contact or commitment is implied. |
| `handoff_candidate` | Preserve a possible external or internal handoff path; no transfer is implied. |
| `hold` | Preserve pending a named trigger or additional evidence. |
| `archive` | Preserve without current action; not deletion. |

Every nonterminal disposition must name the owner, next action, required evidence, review trigger, and open risks. If any required item is unknown, record `UNKNOWN` and keep the matter unresolved. Disposition is an A&R recommendation until authorized human review; only an Approved Development Brief permits Internal Studio Development.

## 9. Artist Archetype Taxonomy

No controlled artist-archetype vocabulary or populated archetype assignments were found. The solo artist template describes an internal archetype as a “character archetype or emotional signature” for consistent assignment; `artists.yaml` contains an `archetype` field, but its entries are placeholders.

Do not infer archetypes from artist names, genres, audience descriptions, or vocal categories. Before introducing controlled archetypes, define whether the concept describes narrative/persona, emotional territory, creative role, or some combination; keep those facets distinguishable and evidence-based.

The repository does document project/roster structures that are not archetypes: solo artists, bands/ensembles, and producer-led projects. The producer-project template explicitly organizes a project around production identity rather than artist identity.

## 10. Voice Archetype Taxonomy

No controlled voice-archetype vocabulary or populated archetype assignments were found. `voices.yaml` documents a `voice_category` field with schema examples `male`, `female`, and `ensemble`; current registry entries use `male` or `female`, while range and tone fields are placeholders. The artist-development template gives `baritone` and `soprano` as range examples, not assigned voice archetypes.

Keep these concepts separate:

- **Voice identity:** a governed vocal implementation with its own identifier and lifecycle; it is distinct from artist identity.
- **Voice category:** the current registry's coarse `male` / `female` values and schema example `ensemble`; these are not archetypes.
- **Range:** a technical description, not identity or artistic role.
- **Tone, performance, and production signature:** descriptive characteristics; current records are mostly placeholders.
- **Artist vocal identity:** an artist-level creative characteristic that may use a voice implementation but is not the voice record itself.

Do not infer a voice archetype from gender category, range, assigned artist, or prompt output. An approved taxonomy requires explicit definitions, evidence, and governance.

## Classification Perspectives (Governance)

Classification is multi-perspective. Preserve the evidence, label, interpretation, and perception in the perspective that produced it; do not require one genre determination to replace or reconcile all others. A repository-controlled term supports organization and retrieval, but does not erase the source label or make one perspective universally authoritative.

| Perspective | Evidence sources | Purpose and governance |
|---|---|---|
| **Creator Intent** | Prompt, creator notes, intake metadata, and direct creator clarification | Preserve what the creator intended. The original Creator Intent record must never be overwritten. A correction or clarification is a new, attributed statement; it does not replace the earlier record. |
| **Prompt Analysis** | Prompt text, lyrics, and intake metadata | Analytically infer likely genre, style, source material, and project purpose. Mark inference and uncertainty; this analysis is not creator-authored intent, founder review, or a decision. |
| **Founder Review** | Listening review and documented evaluation | Record what the founder observes and interprets about the work. Preserve supporting listening/evaluation evidence and distinguish observation from interpretation. |
| **Audience Perception** | Surveys, focus groups, and listener feedback | Record how listeners categorize or perceive the work. Retain the feedback source and available audience/method context; audience perception does not replace creator intent or founder review. |

These perspectives may agree, partially overlap, or conflict. Keep them separately attributable and time-stamped. Do not average them, silently promote one into another, or rewrite one perspective to resolve disagreement. This governance addition does not relax the founder-review gate in Section 6: any demo-value classification remains `UNKNOWN` until the existing review requirements are met.

### Controlled Vocabulary and Creator-Supplied Labels

- **Controlled Vocabulary** is the repository's governed terminology for organization, search, validation, and reporting. It may group or map labels, but is not a judgment that a work has one objectively correct genre.
- **Creator-Supplied Labels** preserve the creator's historical intent and terminology, including emerging or unfamiliar terms. Store the exact label with its source and context even when no controlled term exists.
- A mapping is supplemental and traceable. Retain the original label alongside any mapped term. Record the mapping rationale, relationship, taxonomy version, and whether the mapping is proposed or approved. A missing or disputed mapping does not invalidate the original label.
- One creator label may map to multiple controlled facets, and several labels may remain unmapped. Do not force a one-to-one mapping or discard a label because the taxonomy changes.

Example mapping:

```text
Creator Label (preserved): Post-Punk
Taxonomy Mapping (illustrative):
  Genre Family: Rock
  Style Family: Punk
```

`Post-Punk` is already listed as a supported genre in the portfolio. The Rock/Punk mapping illustrates broader organization; it does not rename or remove the creator label, add a new supported genre, or establish an otherwise undocumented hierarchy without a governed mapping decision.

### Emerging Genres and Creator-Defined Styles

Preserve emerging, hybrid, and creator-defined labels as supplied, including `Post-Punk`, `Country Punk`, `Darkwave`, and future terms not yet defined by the repository. `Post-Punk` is an existing portfolio label; the other examples illustrate terms that must not be presumed to be current controlled values.

When a broader mapping is useful:

1. Keep the raw label and identify whether it came from the creator, prompt analysis, founder review, or audience feedback.
2. Map only to supported terms that fit the evidence. A hybrid may relate to more than one genre family or style facet.
3. Record the relationship and its rationale (for example, family, influence, hybrid, or related style), plus mapping status and taxonomy version.
4. Leave the label unmapped or mark its mapping as proposed when the relationship is uncertain. Do not substitute `UNKNOWN` for the supplied label.
5. Add a new controlled term only through an explicit taxonomy governance decision with a definition, provenance, scope, parent/related terms, and effective version. Retain historical labels and mappings when the taxonomy evolves.

No new genre or classification values are established by these examples. They define how future labels are preserved and evaluated for possible mapping.

## Vocabulary Boundaries and Crosswalk

Several repository vocabularies may look similar but serve different purposes:

| Vocabulary | Examples | What it describes |
|---|---|---|
| Demo submission type | `internal_founder_demo`, `roster_artist_demo`, `band_demo`, `producer_project_demo`, `collaboration_demo`, `external_submission`, `acquired_concept`, `inbound_pitch`, `organic_discovery` | How a demo is categorized at intake. Only `internal_founder_demo` is currently active; the others are future-compatible schema values, not permission to accept submissions. |
| Demo lifecycle state | `submitted`, `intake_incomplete`, `intake_validated`, `triage`, `under_review`, `focus_group`, `development_candidate`, `in_development`, `on_hold`, `approved_seed`, `promoted_to_work`, `collaboration_candidate`, `handoff_candidate`, `licensing_candidate`, `declined`, `withdrawn`, `archived` | Workflow progress or outcome, not creative value. |
| Review grade | `A`, `B`, `C`, `D`, `F`, `N/R` | Evidence-backed evaluation of a criterion or overall creative result. |
| Disposition | The 13 values in Section 8 | A&R recommendation and bounded next path. |
| Release type | `album`, `ep`, `single`, `compilation` | Album-registry format, not a project purpose or genre. |
| Media format | Music, podcast, publishing, related media | Form of the work, not its source material or purpose. |
| Project/roster structure | Solo artist, band/ensemble, producer-led project | Organizational/creative project structure, not artist archetype or demo classification. |

The operational workflow term “Emotional Classification” is a process stage, not the controlled value set for `classification.primary`.

## Intent Comparison Model

```text
Creator prompt, notes, lyrics, and intake metadata
                         |
                         v
              Creator Intent Analysis
                         |
                         v
           Taxonomy Mapping with Provenance
                         |
                         v
                Founder Listening Review
                         |
                         v
          Outcome Assessment and Disposition
```

| Stage | Question answered | Boundary |
|---|---|---|
| Prompt and creator evidence | What material and direction did the creator provide? | Preserve original evidence; do not evaluate quality. |
| Creator intent analysis | What source, genre, style, voice, and purpose are explicitly intended or cautiously inferred? | Attribute each observation and preserve uncertainty. |
| Taxonomy mapping | Which approved terms correspond to the stated intent? | Keep unmapped language verbatim; mapping does not endorse it. |
| Founder review | What does the founder hear and conclude from the work and its evidence? | Human review is separate from intake and AI screening. |
| Outcome assessment | What classification, seed designation, rationale, disposition, or next decision is supported? | Set only after the required review gate; disposition does not itself authorize production. |

Intent and outcome may differ. Do not rewrite creator intent to match the review, or use inferred intent as evidence that the audio achieved it.

## Recommended Future Intake Metadata

The current demo schema preserves `original_prompt`, `exclude_prompt`, prompt status, lyrics status, source material, approximate genre, generator, and model version. It has no structured creator-intent object. The following is a design recommendation only; it is not a registry schema change or write-back implementation.

For each of the five intent facets, future data should be able to preserve:

- Original creator phrase and its evidence source.
- Normalized taxonomy term, if an approved mapping exists.
- Explicit, inferred, conflicting, or unknown status.
- Evidence location and concise mapping rationale.
- Confidence or uncertainty, if a governed scale is later approved.
- Taxonomy version and analysis provenance.

Keep the creator's source material reference distinct from the source-material category. Keep intended genre/style/voice/purpose distinct from observed audio, founder review, classification, seed designation, disposition, artist assignment, and development authorization. Do not populate new values in existing records as part of this documentation.

## Gap Analysis and Consolidation Recommendations

1. **Preserve the resolved genre count.** The portfolio currently enumerates 22 entries. Treat the annotated Phase 2A claim of 23 as a historical count error; do not infer a missing term or add a guessed label.
2. **Govern genre hierarchy.** Define family, genre, subgenre/idiom, aliases, and parent relationships. Clarify overlaps including Hip-Hop/Rap, Electronic/Dance/EDM/House, Latin/Regional Mexican, and Christian/Gospel.
3. **Separate descriptive facets.** Maintain genre, musical influence, arrangement/instrumentation, vocal performance, production, and purpose as distinct fields. Do not use “style” as an undifferentiated bucket.
4. **Define review classification values.** The registry has fields but no allowed vocabulary. Do not borrow genre labels, grades, dispositions, workflow states, or historical provisional values.
5. **Define seed designation values and criteria.** Keep designation distinct from `approve_as_seed` and `approved_seed`; the review gate already requires documented founder evidence.
6. **Decide which purpose concepts are controlled.** Existing purpose statements are meaningful but not an enum. Preserve purpose as attributed creator intent until a founder decision establishes permitted values.
7. **Define artist archetypes.** Existing archetype fields and templates are placeholders; no controlled values or assignments exist.
8. **Define voice archetypes.** Existing categories and range examples are insufficient to constitute an archetype system. Separate voice identity, category, range, tone, performance, and production.
9. **Keep source kind distinct from provenance and theme.** Repertoire folders supply useful source families but are not a complete source model.
10. **Preserve provenance and unknowns.** Add terms only with a definition, source evidence, owner, and decision record. Retain raw values during any future normalization; never silently translate an unknown or legacy value.

## Migration Impacts

- No existing demo, review, classification, seed designation, or artist/voice metadata is changed by this framework.
- Existing `UNKNOWN` values remain unchanged. The documented founder-review gate continues to control demo classification and seed designation.
- Do not automatically map historical `song_candidate` or `song_seed` strings into new values.
- Future schema work should add taxonomy identifiers and provenance while preserving existing raw prompt, source, and review evidence.
- Existing `approximate_genre` is an intake observation and should not be silently treated as creator intent or founder-reviewed classification.
- Existing artist/voice placeholders should remain placeholders until supported by reviewed evidence.
- Any enum, schema, or records migration requires a separate approved task, validation, and decision record.

## Evidence and Provenance Register

| Repository source | Evidence used |
|---|---|
| [creative/genre-portfolio.md](../creative/genre-portfolio.md) | The 22 supported genre headings, genre descriptions, examples, overlap, and source-material fit. |
| [foundations/creative-constitution.md](creative-constitution.md) | Source-first workflow, emotional objective, artist assignment, genre purpose, human editorial authority, metadata authority, and stewardship. |
| [foundations/AI_Music_Project_Manifesto_and_Notes_v2.md](AI_Music_Project_Manifesto_and_Notes_v2.md) | Source strategy, Psalms and Historical Initiatives, podcast purposes, catalog development, and media formats. |
| [catalog/repertoire/README.md](../catalog/repertoire/README.md) | Existing source collections: Psalms, daily readings, Revolutionary War, historical documents, virtues, saints, and poetry. |
| [catalog/metadata/demos.yaml](../catalog/metadata/demos.yaml) | Submission types, lifecycle states, intake fields, classification and seed fields, and unknown-value guidance. |
| [operations/demo-intake/intake-standard.md](../operations/demo-intake/intake-standard.md) | Intake boundary and founder-review gate for classification and seed designation. |
| [operations/demo-intake/evaluation-standard.md](../operations/demo-intake/evaluation-standard.md) | Review grades, evidence requirements, and founder-review eligibility gate. |
| [catalog/metadata/demo-reviews.yaml](../catalog/metadata/demo-reviews.yaml) | Review criteria, grade schema, and distinction between intake screen and founder review. |
| [operations/demo-intake/disposition-standard.md](../operations/demo-intake/disposition-standard.md) | The 13 governed dispositions and their authority boundaries. |
| [catalog/metadata/artists.yaml](../catalog/metadata/artists.yaml) and [creative/artist-development-template.md](../creative/artist-development-template.md) | Placeholder archetype field and intended internal-archetype concept. |
| [catalog/metadata/voices.yaml](../catalog/metadata/voices.yaml) and [creative/voice-architecture.md](../creative/voice-architecture.md) | Voice registry categories, placeholder profile fields, and separation of voice and artist identity. |
| [creative/production-style-guide.md](../creative/production-style-guide.md) and [creative/vocal-style-guide.md](../creative/vocal-style-guide.md) | Production and vocal preferences, constraints, and non-taxonomic descriptors. |
| [research/suno-platform/suno-research-reference.md](../research/suno-platform/suno-research-reference.md) | Experimental prompt descriptors and caution about model/version variability. |
| [docs/phase-2a-validation-report.md](../docs/phase-2a-validation-report.md) | Historical claim of 23 genres, annotated to record that the current portfolio enumerates 22 and no twenty-third label was found. |
