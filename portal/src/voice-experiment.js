const answerChoices = {
  identify_treatment_clips: ["Yes", "No", "Unsure"],
  sounds_more_like_actual_voice: ["Yes", "No", "Unsure"],
  pronunciation_change: ["Yes", "No", "Unsure"],
  cadence_or_pacing_change: ["Yes", "No", "Unsure"],
  realism_change: ["More realistic", "Less realistic", "No meaningful difference"],
  vocal_timbre_change: ["Yes", "No", "Unsure"],
  reliably_distinguish_groups: ["Yes", "No", "Unsure"],
  treatment_strength: ["None", "Slight", "Moderate", "Strong", "Extremely Obvious"],
  reuse_voice_asset: ["Yes", "No", "Need More Testing"],
};

const commentFields = [
  "more_like_actual_voice_comments",
  "pronunciation_comments",
  "cadence_or_pacing_comments",
  "realism_comments",
  "timbre_comments",
  "reuse_voice_comments",
];

function nullableText(value) {
  const text = String(value ?? "").trim();
  return text || null;
}

export function validateVoiceEvaluationFormValues(formValues) {
  if (!formValues || typeof formValues !== "object" || Array.isArray(formValues)) {
    throw new Error("Evaluation form values must be an object.");
  }

  const allowedFields = new Set([
    "listener_name",
    ...Object.keys(answerChoices),
    ...commentFields,
    "one_sentence_conclusion",
  ]);
  const unexpectedField = Object.keys(formValues).find((field) => !allowedFields.has(field));
  if (unexpectedField) {
    throw new Error(`Unexpected evaluation field: ${unexpectedField}.`);
  }

  const listenerName = formValues.listener_name;
  if (
    typeof listenerName !== "string" ||
    listenerName.trim().length === 0
  ) {
    throw new Error("Listener name is required.");
  }

  const answers = {};
  for (const [field, choices] of Object.entries(answerChoices)) {
    const rawValue = formValues[field];
    if (rawValue !== undefined && rawValue !== null && typeof rawValue !== "string") {
      throw new Error(`Invalid answer for ${field}.`);
    }
    const value = nullableText(rawValue);
    if (value !== null && !choices.includes(value)) {
      throw new Error(`Invalid answer for ${field}.`);
    }
    answers[field] = value;
  }
  for (const field of commentFields) {
    const rawValue = formValues[field];
    if (rawValue !== undefined && rawValue !== null && typeof rawValue !== "string") {
      throw new Error(`Invalid comment for ${field}.`);
    }
    answers[field] = nullableText(rawValue);
  }
  if (
    formValues.one_sentence_conclusion !== undefined &&
    formValues.one_sentence_conclusion !== null &&
    typeof formValues.one_sentence_conclusion !== "string"
  ) {
    throw new Error("Invalid one_sentence_conclusion.");
  }
  answers.one_sentence_conclusion = nullableText(formValues.one_sentence_conclusion);

  return {
    listener_name: listenerName,
    answers,
  };
}

export function buildVoiceEvaluationExport(
  experiment,
  formValues,
  exportedAt = new Date().toISOString(),
  writeback = null,
) {
  if (!experiment || experiment.experiment_id !== "Voice-ID-001") {
    throw new Error("A Voice-ID-001 experiment record is required.");
  }
  const validated = validateVoiceEvaluationFormValues(formValues);

  const evaluation = experiment.human_evaluation;
  return {
    schema_version: 2,
    experiment_id: experiment.experiment_id,
    evaluation_date: evaluation.evaluation_date,
    listener: validated.listener_name,
    listening_status: evaluation.listening_status,
    observation_source: evaluation.observation_source,
    evidence_classification: evaluation.evidence_classification,
    observation: evaluation.observation,
    exported_at: exportedAt,
    context: {
      workspace: experiment.workspace,
      assets: experiment.assets.map((asset) => ({
        condition: asset.condition,
        song_id: asset.song_id,
        song_url: asset.song_url,
        duration_seconds: asset.duration_seconds,
        model: asset.model,
        voice_id_in_audio_wait: asset.voice_id_in_audio_wait,
      })),
      metadata_findings: experiment.metadata_findings,
    },
    structured_answers: validated.answers,
    ...(writeback ? { writeback } : {}),
  };
}
