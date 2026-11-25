# Voice Influence Experiment: Nebraska Test Clips

**Experiment ID:** Voice-ID-001<br>
**Captured:** 2026-11-24<br>
**Status:** Metadata verified; human observations and a structured listening submission recorded<br>
**Evidence source:** Approved Suno MCP `audio-create`, `audio-wait`, and `library-list` operations<br>
**Workspace:** `EXP-Voice-ID-Validation`

The durable experiment-series status and human-evaluation placeholder are maintained in the [EXP-Voice-ID-Validation registry](voice-id-validation-registry.md).

## Objective and Scope

This experiment paired a control condition without `voice_id` with a treatment condition using the previously observed voice asset. The question was whether supplying that voice ID changes music generation. Four clips were generated in two approved `audio-create` calls. No additional generation was performed during the subsequent workspace cleanup.

## Matched Inputs

Both calls used the same lyrics, style, title, and duration settings:

- **Title:** `Prairie Light - Nebraska Voice Test`
- **Style:** `Short acoustic Nebraska folk, sparse acoustic guitar, solo lead vocal, natural restrained delivery, no backing choir.`
- **Target duration:** 15 seconds
- **Duration guidance:** enabled
- **Strict duration:** enabled
- **Model parameter:** omitted from both requests; returned metadata identifies the model as `v6`
- **Control:** no `voice_id`
- **Treatment:** `voice_id` supplied; the account-specific value is redacted

The generated lyrics were identical between conditions and are not reproduced here. Each call returned two clip IDs. All four outputs were complete and private.

## Outputs

| Condition | Song ID | Suno link | Observed duration | Voice metadata |
|---|---|---|---:|---|
| Control | `5b2f7776-9c9f-4293-8c67-8e8f04d82b87` | [Open in Suno](https://suno.com/song/5b2f7776-9c9f-4293-8c67-8e8f04d82b87) | 15.52 sec | `voice_id` absent from `audio-wait` metadata |
| Control | `51572459-0f68-49b2-8b02-9fd169ae6ad0` | [Open in Suno](https://suno.com/song/51572459-0f68-49b2-8b02-9fd169ae6ad0) | 14.32 sec | `voice_id` absent from `audio-wait` metadata |
| Treatment | `1d7e002f-4255-4b81-9c5b-3fe8f98294a8` | [Open in Suno](https://suno.com/song/1d7e002f-4255-4b81-9c5b-3fe8f98294a8) | 14.80 sec | `voice_id` present; value redacted |
| Treatment | `fd5bca7b-83c2-4f07-a4a3-aac66502c2df` | [Open in Suno](https://suno.com/song/fd5bca7b-83c2-4f07-a4a3-aac66502c2df) | 14.80 sec | `voice_id` present; value redacted |

The target was 15 seconds; observed output durations were not identical. The connector's `library-list` metadata omitted `voice_id` for these clips, while the generation/wait metadata distinguished the control and treatment conditions.

## Verified Metadata Evidence

- **Verified:** Both `audio-create` requests completed successfully and returned two clips each. The four clips now appear in `EXP-Voice-ID-Validation`.
- **Observed:** The control request omitted `voice_id`; treatment included it. `audio-wait` metadata omitted `voice_id` for both controls and exposed it for both treatment clips. The returned model was `v6`.
- **Unknown:** Whether supplying the voice caused an audible change, and which clips or vocal properties Christopher meant by “The output is obvious.” The original technical capture did not include listening; the later human observation is preserved separately below.
- **Untested:** Whether the Suno UI presents condition-specific labels. The connector returned the same title for all four and no condition-label field.

The metadata verifies that the treatment parameter was accepted and surfaced on the resulting clips. It does **not** establish an audible influence or prove that listeners can distinguish the conditions.

## Human Listening Evidence

**Evaluation date:** 2026-11-24<br>
**Listener:** Christopher Bower<br>
**Listening status:** Recorded<br>
**Observation source:** Christopher Bower<br>
**Evidence classification:** Human Listening Evidence

**Recorded observation:** “The output is obvious.”

The original statement is preserved separately from the later structured submission. Christopher Bower also reported, “The voices are completely different” and “It mostly sounds like me.” All four recordings were reported to pronounce “plains” as “plain”; the issue appeared in both control and treatment groups. The recorded interpretation is that the pronunciation issue appears independent of `voice_id`. No further conclusion is inferred.

These observations are preserved in the [structured YAML source](../../../catalog/metadata/voice-experiments.yaml). A later structured submission and its [evaluation snapshot](voice-id-001-evaluation-writeback-2026-11-25T01-43-31-823Z-a6678067.json) are recorded separately below.

The [export snapshot](voice-id-001-evaluation-2026-11-24.json) is preserved unchanged. It captured `listening_status: Completed` at export time; the canonical current status is `Recorded`.

**Experiment conclusion:** The supplied human observations and structured answers are recorded without extending them into additional conclusions. The experiment status remains partially validated.

## Voice-ID-001 Repository Writeback Proof-of-Concept

The local review form can append structured submissions for Voice-ID-001 only. Each record preserves its exact listener name as evaluation metadata, timestamp, full answers, modified fields, and previous/new values. The name is not authenticated. Successful submissions update the experiment YAML and both human-readable experiment records, then create a uniquely named schema-version-2 JSON snapshot; the pre-existing dated schema-version-1 export is never overwritten.

The writeback endpoint is development-only, restricted to loopback and fixed Voice-ID-001 paths. It does not enable writes to founder reviews, A/B or focus-group evaluations, or discovery intake. No submission was made during implementation; a later submission is preserved in the managed history below.

<!-- voice-id-001-writeback:start -->
### Repository-Backed Evaluation Submissions

Listener names are evaluation metadata supplied by the form; they are not authenticated identities.

#### Submission 1

```json
{
  "submission_id": "a6678067-f126-498f-9be4-eac7d8f26659",
  "timestamp": "2026-11-25T01:43:31.823Z",
  "snapshot_name": "voice-id-001-evaluation-writeback-2026-11-25T01-43-31-823Z-a6678067.json",
  "user": "Christopher Bower",
  "listener_name": "Christopher Bower",
  "modified_fields": [
    "answers.identify_treatment_clips",
    "answers.sounds_more_like_actual_voice",
    "answers.pronunciation_change",
    "answers.cadence_or_pacing_change",
    "answers.realism_change",
    "answers.vocal_timbre_change",
    "answers.reliably_distinguish_groups",
    "answers.treatment_strength",
    "answers.reuse_voice_asset",
    "answers.pronunciation_comments"
  ],
  "previous_values": {
    "answers.identify_treatment_clips": null,
    "answers.sounds_more_like_actual_voice": null,
    "answers.pronunciation_change": null,
    "answers.cadence_or_pacing_change": null,
    "answers.realism_change": null,
    "answers.vocal_timbre_change": null,
    "answers.reliably_distinguish_groups": null,
    "answers.treatment_strength": null,
    "answers.reuse_voice_asset": null,
    "answers.pronunciation_comments": null
  },
  "new_values": {
    "answers.identify_treatment_clips": "Yes",
    "answers.sounds_more_like_actual_voice": "Yes",
    "answers.pronunciation_change": "No",
    "answers.cadence_or_pacing_change": "No",
    "answers.realism_change": "No meaningful difference",
    "answers.vocal_timbre_change": "Yes",
    "answers.reliably_distinguish_groups": "Yes",
    "answers.treatment_strength": "Strong",
    "answers.reuse_voice_asset": "Yes",
    "answers.pronunciation_comments": "Interesting, the displayed lyrics show \"plains\" (plural) and the voices, all of them, pronounce it is \"plain\""
  },
  "structured_answers": {
    "identify_treatment_clips": "Yes",
    "sounds_more_like_actual_voice": "Yes",
    "pronunciation_change": "No",
    "cadence_or_pacing_change": "No",
    "realism_change": "No meaningful difference",
    "vocal_timbre_change": "Yes",
    "reliably_distinguish_groups": "Yes",
    "treatment_strength": "Strong",
    "reuse_voice_asset": "Yes",
    "more_like_actual_voice_comments": null,
    "pronunciation_comments": "Interesting, the displayed lyrics show \"plains\" (plural) and the voices, all of them, pronounce it is \"plain\"",
    "cadence_or_pacing_comments": null,
    "realism_comments": null,
    "timbre_comments": null,
    "reuse_voice_comments": null,
    "one_sentence_conclusion": "The output is obvious."
  }
}
```

<!-- voice-id-001-writeback:end -->

## Credit and Model Notes

The user approved two generation calls (four clips). Audio downloads were not completed because Suno's download flow indicated a credit cost; the user chose to preserve links and metadata only. The model was `v6`, not `v6-mini`, because the model parameter was omitted and this experiment preceded the later instruction to use `v6-mini` for future voice-ID investigations unless a specific hypothesis justifies a higher-cost model. Do not generate replacements solely to change the model without separate approval.

## Repository and Catalog References

- [Voice experiment metadata](../../../catalog/metadata/voice-experiments.yaml)
- [EXP-Voice-ID-Validation registry](voice-id-validation-registry.md)
