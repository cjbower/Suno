import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { load } from "js-yaml";
import {
  buildVoiceEvaluationExport,
  validateVoiceEvaluationFormValues,
} from "../src/voice-experiment.js";

const voiceExperimentsSource = await readFile(
  new URL("../../catalog/metadata/voice-experiments.yaml", import.meta.url),
  "utf8",
);
const voiceExperiments = load(voiceExperimentsSource).experiment_records;
const experiment = voiceExperiments.find((record) => record.experiment_id === "Voice-ID-001");

test("evaluation export preserves only supplied answers and the exact observation", () => {
  const result = buildVoiceEvaluationExport(experiment, {
    listener_name: "Christopher Bower",
    one_sentence_conclusion: "The output is obvious.",
  }, "2026-11-24T00:00:00.000Z");

  assert.equal(result.schema_version, 2);
  assert.equal(result.listener, "Christopher Bower");
  assert.equal(result.listening_status, "Recorded");
  assert.equal(result.observation, "The output is obvious.");
  assert.equal(result.structured_answers.one_sentence_conclusion, "The output is obvious.");
  assert.equal(result.structured_answers.identify_treatment_clips, null);
  assert.equal(result.structured_answers.treatment_strength, null);
  assert.equal(result.exported_at, "2026-11-24T00:00:00.000Z");
  assert.equal(result.context.assets.length, 4);
  assert.ok(Array.isArray(result.context.assets));
  assert.ok(
    result.context.assets.every(
      (asset) => asset.song_url === `https://suno.com/song/${asset.song_id}`,
    ),
  );
  assert.equal(result.context.workspace.name, "EXP-Voice-ID-Validation");
});

test("evaluation export rejects values outside the displayed answer choices", () => {
  assert.throws(
    () =>
      buildVoiceEvaluationExport(experiment, {
        listener_name: "Christopher Bower",
        treatment_strength: "Very Strong",
      }),
    /Invalid answer for treatment_strength/,
  );
});

test("listener name is free-form, validated, and preserved exactly", () => {
  const formValues = validateVoiceEvaluationFormValues({
    listener_name: "  Kai O'Neil  ",
  });
  assert.equal(formValues.listener_name, "  Kai O'Neil  ");
  assert.throws(
    () => validateVoiceEvaluationFormValues({ listener_name: "   " }),
    /Listener name is required/,
  );
  assert.throws(
    () =>
      validateVoiceEvaluationFormValues({
        listener_name: "Christopher Bower",
        arbitrary_field: "not allowed",
      }),
    /Unexpected evaluation field/,
  );
});

test("Voice-ID-001 structured metadata separates the statement from unanswered questions", () => {
  assert.equal(experiment.human_evaluation.listening_status, "Recorded");
  assert.equal(experiment.human_evaluation.observation, "The output is obvious.");
  assert.equal(experiment.human_evaluation.answers.one_sentence_conclusion, "The output is obvious.");
  assert.deepEqual(experiment.assets.map((asset) => asset.condition), [
    "control",
    "control",
    "treatment",
    "treatment",
  ]);
  assert.equal(experiment.human_evaluation.answers.identify_treatment_clips, null);
  assert.equal(experiment.human_evaluation.answers.treatment_strength, null);
});
