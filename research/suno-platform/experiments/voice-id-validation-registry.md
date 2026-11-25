# EXP-Voice-ID-Validation Registry

**Purpose:** Durable registry for controlled investigations of Suno voice-ID behavior.<br>
**Workspace:** `EXP-Voice-ID-Validation`<br>
**Workspace ID:** `9f39af6d-d8b4-43d9-b35d-d9fdf90b1a8e`<br>
**Current outcome:** Partially validated<br>
**Structured source:** [Voice experiment metadata](../../../catalog/metadata/voice-experiments.yaml)<br>
**Current work:** A controlled, local repository-writeback proof-of-concept is enabled for Voice-ID-001 only. No audio was generated, no existing songs were modified, and no evaluation was submitted while implementing this workflow.

## Experiment Index

| Experiment ID | Name | Status | Record |
|---|---|---|---|
| Voice-ID-001 | Music voice influence control/treatment test | Partially validated; metadata, human observations, and a structured submission recorded | [Voice influence test](voice-influence-test-2026-11-24.md) |
| Voice-ID-002 | v6-mini replication | Backlog | Planned |
| Voice-ID-003 | Speech comparison | Backlog | Planned |
| Voice-ID-004 | Nebraska anthem comparison | Backlog | Planned |
| Voice-ID-005 | Cover generation comparison | Backlog | Planned |

## Voice-ID-001: Music Voice Influence

### Goal

Determine whether supplying `voice_id` materially changes generated music.

### Hypothesis

- The voice asset influences generated singing.
- The influence is detectable by human listeners.

The hypothesis is not considered supported or rejected until listening evidence is recorded.

### Experimental Design

| Element | Specification |
|---|---|
| Control | Generate without `voice_id`. |
| Treatment | Generate with the previously observed voice ID; the account-specific value is redacted. |
| Constants | Same lyrics, style, 15-second target duration, title, and generation workflow. |
| Recorded variables | Whether `voice_id` was present; returned model; output duration; generation/wait and library metadata; workspace assignment. |
| Title | `Prairie Light - Nebraska Voice Test` |
| Style | `Short acoustic Nebraska folk, sparse acoustic guitar, solo lead vocal, natural restrained delivery, no backing choir.` |
| Duration settings | Target 15 seconds; duration guidance and strict duration enabled. |
| Model handling | Model was omitted from both requests and returned metadata identified `v6`; the model was therefore recorded, not explicitly controlled. |
| Workflow | Two `audio-create` requests with matching inputs except for `voice_id`; each returned two clips. |

The lyrics were identical between conditions and are retained with the original generation records rather than copied here. The output durations varied despite the shared target.

### Generated Assets

| Condition | Song ID | Link | Duration | `audio-wait` metadata |
|---|---|---|---:|---|
| Control | `5b2f7776-9c9f-4293-8c67-8e8f04d82b87` | [Open in Suno](https://suno.com/song/5b2f7776-9c9f-4293-8c67-8e8f04d82b87) | 15.52 sec | `voice_id` absent |
| Control | `51572459-0f68-49b2-8b02-9fd169ae6ad0` | [Open in Suno](https://suno.com/song/51572459-0f68-49b2-8b02-9fd169ae6ad0) | 14.32 sec | `voice_id` absent |
| Treatment | `1d7e002f-4255-4b81-9c5b-3fe8f98294a8` | [Open in Suno](https://suno.com/song/1d7e002f-4255-4b81-9c5b-3fe8f98294a8) | 14.80 sec | `voice_id` present; value redacted |
| Treatment | `fd5bca7b-83c2-4f07-a4a3-aac66502c2df` | [Open in Suno](https://suno.com/song/fd5bca7b-83c2-4f07-a4a3-aac66502c2df) | 14.80 sec | `voice_id` present; value redacted |

All four clips are assigned to `EXP-Voice-ID-Validation`, as recorded in the structured experiment metadata.

### Verified Metadata Evidence

- **Verified:** `audio-wait` metadata contains `voice_id` for both treatment clips.
- **Verified:** `audio-wait` metadata does not contain `voice_id` for either control clip.
- **Verified:** `library-list` omits `voice_id` for all four clips.
- **Verified:** All four generation results identify model `v6`; the generation requests omitted the model parameter.
- **Verified:** All four clips are assigned to the dedicated experiment workspace.
- **Unknown:** Whether metadata presence corresponds to an audible change in the generated singing.

These findings confirm request/response metadata association only. They are not evidence that the audio changed or that listeners can identify the treatment condition.

### Verified Human Evidence

**Listening status:** Recorded<br>
**Evaluation date:** 2026-11-24<br>
**Listener / observation source:** Christopher Bower<br>
**Evidence classification:** Human Listening Evidence<br>
**Recorded observation:** “The output is obvious.”

The original statement remains separate from the later structured submission. Christopher Bower also reported, “The voices are completely different” and “It mostly sounds like me.” All four recordings were reported to pronounce “plains” as “plain”; the issue appeared in both control and treatment groups. The recorded interpretation is that the pronunciation issue appears independent of `voice_id`. No further conclusion is inferred.

The [export snapshot](voice-id-001-evaluation-2026-11-24.json) was saved at 2026-11-25T00:24:17.657Z. It records the then-current `listening_status` as `Completed`; the canonical status is now `Recorded`. The snapshot is preserved unchanged as evidence of the export, not treated as the current source of truth.

### Initial Structured-Answer State

The table below records the original pre-submission state. The later structured submission is retained in the repository-backed history section.

| Question | Recorded answer | Comments |
|---|---|---|
| Could you identify the treatment clips without being told? | Not recorded | Not recorded |
| Did the treatment clips sound more like your actual voice? | Not recorded | Not recorded |
| Did pronunciation change? | Not recorded | Not recorded |
| Did cadence or pacing change? | Not recorded | Not recorded |
| Did realism change? | Not recorded | Not recorded |
| Did vocal timbre change? | Not recorded | Not recorded |
| Could you reliably distinguish the two groups? | Not recorded | No comments field was requested for this question. |
| Treatment Strength | Not recorded | Not applicable |
| Would you use the voice asset again? | Not recorded | Not recorded |
| One Sentence Conclusion | The output is obvious. | Exact reported observation; no added inference. |

### Interpretation

The original statement, later structured answers, and additional observations are preserved separately. The interpretation about pronunciation is limited to the explicit cross-condition observation; no other audible attribute or causal conclusion is inferred.

### Open Questions

- Would the reported distinction replicate in a blind or otherwise controlled comparison?

### Outcome Classification

**Current status: Partially validated.**

- **Metadata evidence:** Verified.
- **Listening evidence:** Human observations and a structured submission are recorded.
- **Hypothesis conclusion:** Partially validated. The status is retained without inferring beyond the recorded observations and answers.

### Lessons Learned

- Voice metadata is visible in generation/wait metadata for treatment outputs.
- Voice metadata is not visible in `library-list` records for these clips.
- The dedicated `EXP-Voice-ID-Validation` workspace is created and all four clips are assigned to it.
- The prior test returned model `v6` because the model parameter was omitted. Future voice testing defaults to `v6-mini` unless a specific hypothesis justifies another model; record the selected model explicitly.
- Matching a target duration does not make returned clip durations identical; record actual durations as well as requested settings.

### Future Experiments

These are backlog items only. No generation is authorized or performed by listing them.

| Experiment ID | Proposed comparison | Planning note |
|---|---|---|
| Voice-ID-002 | Replicate the music control/treatment test using `v6-mini`. | Keep lyrics, style, title, duration settings, and workflow matched; explicitly set and record the model. |
| Voice-ID-003 | Compare speech generation with and without `voice_id`. | Determine whether the speech workflow exposes a measurable, listener-assessable voice effect. |
| Voice-ID-004 | Compare voice-ID influence on a Nebraska anthem-style test. | Keep conditions matched and use `v6-mini` unless the hypothesis warrants otherwise. |
| Voice-ID-005 | Compare cover generation with and without `voice_id`. | Define a controlled source-song and evaluation method before any generation. |

### Voice-ID-001 Repository Writeback Proof-of-Concept

- The local Voice Experiment Review form validates the listener name and structured answers, then writes only this experiment's submission history to `catalog/metadata/voice-experiments.yaml`, this registry, and the [detailed experiment record](voice-influence-test-2026-11-24.md).
- Each submission records a timestamp, listener name as evaluation metadata (`user`), modified fields, previous values, new values, and the full answer snapshot.
- Listener names are free-form and are suggested from this experiment's existing listener names. They are not authenticated identities. No account, permission, founder-review, focus-group, A/B-test, or discovery-intake writeback is included.
- A uniquely named schema-version-2 JSON snapshot is created after repository files are updated. The existing dated schema-version-1 export is preserved.
- The endpoint is restricted to fixed Voice-ID-001 paths and a same-origin loopback Vite development server. It is not part of a production build; repository files still require a Git commit for version-control persistence.

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

## Related References

- [Voice-ID-001 detailed record](voice-influence-test-2026-11-24.md)
- [Structured Voice-ID experiment metadata](../../../catalog/metadata/voice-experiments.yaml)
