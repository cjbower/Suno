# Suno Prompt Behavior Research

**Status:** Research synthesis; not a prompt standard or guarantee
**Authority:** The linked experiment records are the evidence sources. This document consolidates their findings and limitations for discovery.
**Scope:** Prompt fields, lyrical and style context, exclusions, instrumentation, model/version variation, and repeatable testing.

## Purpose and Authority

This document synthesizes prompt-related knowledge from the [Suno Research Reference](./suno-research-reference.md) and the [Suno Music Generation Investigation, 2026-11-22](./experiments/suno-classification-investigation-2026-11-22.md). The master reference contains the earlier direct voice-prompt experiment and source register; the dated investigation preserves the later exploratory observations and proposed experiments.

This is not an authoritative Suno specification. Suno is a closed, changing system. User-visible prompt fields and model outputs may vary by model/version, and no prompt wording in these reports is guaranteed to produce a specific result. Do not treat interpretations of internal processing as verified implementation facts.

## Evidence Summary

| Topic | What the repository records | Evidence status and limit |
|---|---|---|
| Paired generations | The master reference reports that paired outputs often sounded related while differing in register, timbre, melody, and sometimes instrumentation. | Direct listening observations as reported in the earlier experiment. They do not prove shared seeds, voice embeddings, or one output being transformed from the other. |
| Style-field meaning | The 2026-11-22 investigation reports that lyrical/semantic text accidentally placed in the Style field affected generation. | Preliminary observation from the investigation; exact prompt, screenshot, model/version, and generated audio are not included in that report. |
| Lyrics, style, and instrumentation | The investigation reports that these inputs appeared to influence subject, genre, or vocal-family outcomes. | Exploratory observations and interpretations, not a validated classifier model or causal result. |
| Exclusions and prompt placement | The investigation reports that negative instructions sometimes appeared weaker than positive cues and that placement may affect outcomes. | Preliminary hypotheses; no controlled run log is included to establish effect size or repeatability. |
| Model/version effects | The master reference and research method emphasize recording the model/version because behavior can change across releases. | Operationally important research control; do not generalize a result from one model/version to another. |

The investigation's working theory describes a possible sequence from lyrics/style/instrumentation through semantic categorization to genre, voice, arrangement, and generation. This is a conceptual hypothesis only. It must not be presented as a verified description of Suno's internal architecture.

## Durable Lessons

1. Treat prompt fields as distinct inputs and record which exact content was entered in each field. Do not assume that a field named “Style” contains only genre tags or that lyrics alone determine the result.
2. Keep positive creative direction and negative constraints separate in the experimental record. A failed exclusion is useful evidence; do not silently omit it from a summary.
3. Record the model/version, date, all visible controls, source lyrics/text, exact prompt text, and output identifiers. Without these, later readers cannot reliably compare or reproduce an observation.
4. Compare multiple generations and preserve rejected or ambiguous outputs. A single preferred result is not sufficient evidence that a prompt change caused an effect.
5. Separate what was heard from why it may have happened. Listening observations can be recorded directly; claims about internal semantic classification, singer selection, or prompt weighting remain hypotheses unless independently established.
6. Preserve prompts and source text as experimental inputs. Do not rewrite an old prompt when refining it; create a new version or experiment.

These are research safeguards, not newly approved production requirements. The [Music Taxonomy and Intent Framework](../../foundations/music-taxonomy-and-intent-framework.md) governs repository taxonomy and creator-intent classification; prompt experiments do not establish taxonomy values or founder review conclusions.

## Recommended Experiment Record

For future tests, use a small record containing:

- Experiment ID and date/time.
- Question and the single variable being tested.
- Exact lyrics/source text and exact contents of each prompt field.
- Suno model/version and visible generation controls.
- Pair/output IDs and links to preserved original audio where available.
- Observed subject, genre impression, vocal qualities, instrumentation, prompt adherence, and artifacts.
- Selection/rejection result with evidence notes.
- Separate interpretation, confidence, and unresolved questions.

Use the [experimental method in the master reference](./suno-research-reference.md#7-experimental-method-for-future-prompt-research) as the current method source; this summary does not duplicate its full observation field list.

## Open Experiments

The 2026-11-22 investigation proposes comparing fixed lyrics against changes to the style field, genre direction, instrumentation, and exclusion wording. These experiments remain proposed, not completed by this document. To make results useful:

- Keep all non-target inputs and controls fixed.
- Repeat each condition across multiple output pairs.
- Record every output, including failures.
- Compare normalized listening conditions when judging perceived voice or production.
- Avoid claiming internal mechanism from output similarity alone.

## Provenance and Maintenance

- [Master Suno research reference](./suno-research-reference.md): company/model context, the earlier direct prompting experiment, source register, and general research method.
- [Classification investigation (2026-11-22)](./experiments/suno-classification-investigation-2026-11-22.md): original operator report retained as an exploratory record, now explicitly labeled with its evidence limitations.

When adding results, preserve dated experiment records and update this synthesis only when the evidence basis is clear. Retain contradicted or superseded observations with their provenance; do not silently promote hypotheses to facts.
