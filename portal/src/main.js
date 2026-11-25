import { load } from "js-yaml";
import demoYaml from "../../catalog/metadata/demos.yaml?raw";
import reviewYaml from "../../catalog/metadata/demo-reviews.yaml?raw";
import voiceExperimentYaml from "../../catalog/metadata/voice-experiments.yaml?raw";
import "./styles.css";
import { deriveReviewState } from "./review-state.js";
import { validateVoiceEvaluationFormValues } from "./voice-experiment.js";

const REPOSITORY_URL = "https://github.com/cjbower/Suno";
const elements = {
  error: document.querySelector("#load-error"),
  dashboardMetrics: document.querySelector("#dashboard-metrics"),
  dashboardTable: document.querySelector("#dashboard-table"),
  intakeList: document.querySelector("#intake-list"),
  queueTable: document.querySelector("#queue-table"),
  search: document.querySelector("#demo-search"),
  reviewFilter: document.querySelector("#review-filter"),
  detail: document.querySelector("#demo-detail"),
  backToQueue: document.querySelector("#back-to-queue"),
  voiceExperimentInformation: document.querySelector("#voice-experiment-information"),
  voiceExperimentReferenceLinks: document.querySelector("#voice-experiment-reference-links"),
  voiceMetadataFindings: document.querySelector("#voice-metadata-findings"),
  voiceControlClips: document.querySelector("#voice-control-clips"),
  voiceTreatmentClips: document.querySelector("#voice-treatment-clips"),
  voiceHumanEvidence: document.querySelector("#voice-human-evidence"),
  voiceObservation: document.querySelector("#voice-observation"),
  voiceInterpretation: document.querySelector("#voice-interpretation"),
  voiceOpenQuestions: document.querySelector("#voice-open-questions"),
  voiceListeningStatus: document.querySelector("#voice-listening-status"),
  voiceReviewForm: document.querySelector("#voice-review-form"),
  voiceListenerName: document.querySelector("#voice-listener-name"),
  voiceListenerSuggestions: document.querySelector("#voice-listener-suggestions"),
  voiceWritebackStatus: document.querySelector("#voice-writeback-status"),
  views: [...document.querySelectorAll(".view")],
  navigation: [...document.querySelectorAll(".nav-item[data-view]")],
};

function parseRecords(source, key, label) {
  const document = load(source);
  if (!document || !Array.isArray(document[key])) {
    throw new Error(`${label} must contain a ${key} array.`);
  }
  return document[key];
}

function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  if (text !== undefined) {
    element.textContent = text;
  }
  return element;
}

function createLink(label, href) {
  const link = createElement("a", "inline-link", label);
  link.href = href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  return link;
}

function isKnown(value) {
  return value !== undefined && value !== null && String(value).trim() !== "" && value !== "UNKNOWN";
}

function githubRecordLink(recordPath) {
  return `${REPOSITORY_URL}/blob/main/${recordPath}`;
}

function statusBadge(label, variant) {
  return createElement("span", `status-badge status-${variant}`, label);
}

function reviewFor(demo) {
  return deriveReviewState(demo, reviewRecords);
}

function demoSearchText(demo) {
  const state = reviewFor(demo);
  return [
    demo.demo_id,
    demo.title,
    demo.creator,
    demo.current_disposition,
    state.reviewLabel,
    state.founderReviewState,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function renderMetric(label, value, note, variant) {
  const card = createElement("article", `metric-card metric-${variant}`);
  card.append(
    createElement("p", "metric-label", label),
    createElement("p", "metric-value", String(value)),
    createElement("p", "metric-note", note),
  );
  return card;
}

function renderMetrics() {
  const states = demos.map((demo) => reviewFor(demo));
  const pending = states.filter((state) => !state.classificationEligible).length;
  const complete = states.length - pending;
  const eligible = states.filter((state) => state.classificationEligible).length;

  elements.dashboardMetrics.replaceChildren(
    renderMetric("Registered demos", demos.length, "Canonical demo records", "neutral"),
    renderMetric("Review Pending", pending, "Founder review gate not met", "pending"),
    renderMetric("Review Complete", complete, "Qualifying founder reviews", "complete"),
    renderMetric("Classification Eligible", eligible, "Eligible to consider; not assigned", "eligible"),
  );
}

function renderDefinitionList(target, entries) {
  const children = [];
  for (const [label, value] of entries) {
    children.push(createElement("dt", "", label), createElement("dd", "", String(value)));
  }
  target.replaceChildren(...children);
}

function renderVoiceClip(target, asset) {
  const card = createElement("article", "voice-asset");
  const heading = createElement("h4", "", asset.song_id);
  const facts = createElement(
    "p",
    "muted",
    `${Number(asset.duration_seconds).toFixed(2)} sec · Model ${asset.model} · audio-wait voice_id ${asset.voice_id_in_audio_wait ? "present" : "absent"}`,
  );
  card.append(heading, facts, createLink("Open clip in Suno", asset.song_url));
  return card;
}

function renderVoiceExperiment(experiment) {
  const controlAssets = experiment.assets.filter((asset) => asset.condition === "control");
  const treatmentAssets = experiment.assets.filter((asset) => asset.condition === "treatment");
  if (
    experiment.experiment_id !== "Voice-ID-001" ||
    controlAssets.length !== 2 ||
    treatmentAssets.length !== 2
  ) {
    throw new Error("Voice experiment metadata must contain Voice-ID-001 with two control and two treatment clips.");
  }

  renderDefinitionList(elements.voiceExperimentInformation, [
    ["Experiment ID", experiment.experiment_id],
    ["Current outcome", experiment.outcome_status],
    ["Objective", experiment.objective],
    ["Workspace", `${experiment.workspace.name} (${experiment.workspace.id})`],
  ]);
  elements.voiceExperimentReferenceLinks.replaceChildren(
    createLink(
      "Experiment registry",
      githubRecordLink("research/suno-platform/experiments/voice-id-validation-registry.md"),
    ),
    createLink(
      "Structured experiment metadata",
      githubRecordLink("catalog/metadata/voice-experiments.yaml"),
    ),
    createLink(
      "Workspace assignment record",
      githubRecordLink("operations/suno-workspace-assignment-queue-2026-11-24.md"),
    ),
  );
  elements.voiceMetadataFindings.replaceChildren(
    ...experiment.metadata_findings.map((item) =>
      createElement("li", "", `${item.evidence}: ${item.finding}`),
    ),
  );
  elements.voiceControlClips.replaceChildren(
    ...controlAssets.map((asset) => renderVoiceClip(elements.voiceControlClips, asset)),
  );
  elements.voiceTreatmentClips.replaceChildren(
    ...treatmentAssets.map((asset) => renderVoiceClip(elements.voiceTreatmentClips, asset)),
  );

  const evaluation = experiment.human_evaluation;
  const listeningStatus = String(evaluation.listening_status).toLowerCase();
  const statusVariant =
    listeningStatus === "completed"
      ? "complete"
      : listeningStatus === "pending"
        ? "pending"
        : "recorded";
  elements.voiceListeningStatus.className = `status-badge status-${statusVariant}`;
  elements.voiceListeningStatus.textContent = `Listening status: ${evaluation.listening_status}`;
  renderDefinitionList(elements.voiceHumanEvidence, [
    ["Listening status", evaluation.listening_status],
    ["Evaluation date", evaluation.evaluation_date],
    ["Listener", evaluation.listener],
    ["Observation source", evaluation.observation_source],
    ["Evidence classification", evaluation.evidence_classification],
  ]);
  elements.voiceObservation.textContent = `“${evaluation.observation}”`;
  elements.voiceInterpretation.textContent = evaluation.interpretation;
  elements.voiceOpenQuestions.replaceChildren(
    ...evaluation.open_questions.map((question) => createElement("li", "", question)),
  );

  const latestSubmission = evaluation.submissions?.at(-1);
  const answers = latestSubmission?.structured_answers ?? evaluation.answers;
  elements.voiceListenerName.value =
    latestSubmission?.listener_name ?? latestSubmission?.user ?? evaluation.listener;
  for (const [name, value] of Object.entries(answers)) {
    const field = elements.voiceReviewForm.elements.namedItem(name);
    if (!field) {
      throw new Error(`Voice evaluation form is missing the ${name} field.`);
    }
    field.value = value ?? "";
  }
}

function renderListenerSuggestions(names) {
  elements.voiceListenerSuggestions.replaceChildren(
    ...names.map((name) => {
      const option = document.createElement("option");
      option.value = name;
      return option;
    }),
  );
}

let writebackRevision;
let writebackReady = false;

async function loadVoiceWritebackState() {
  const submitButton = elements.voiceReviewForm.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  try {
    const response = await fetch("/api/voice-id-001/state", {
      headers: { Accept: "application/json" },
    });
    const state = await response.json();
    if (!response.ok) {
      throw new Error(state.error ?? "Repository writeback is unavailable.");
    }
    if (
      state.experiment_id !== "Voice-ID-001" ||
      typeof state.revision !== "string" ||
      !Array.isArray(state.listener_suggestions) ||
      !Array.isArray(state.submissions)
    ) {
      throw new Error("Repository writeback returned an invalid state.");
    }
    writebackRevision = state.revision;
    writebackReady = true;
    renderListenerSuggestions(state.listener_suggestions);
    voiceExperiment.human_evaluation.submissions = state.submissions;
    if (state.latest_submission) {
      renderVoiceExperiment(voiceExperiment);
    }
    submitButton.disabled = false;
    elements.voiceWritebackStatus.textContent = "Local repository connection ready.";
  } catch (error) {
    writebackReady = false;
    elements.voiceWritebackStatus.textContent =
      `Repository writeback unavailable: ${error.message}`;
  }
}

async function saveVoiceEvaluation(event) {
  event.preventDefault();
  if (!writebackReady || !writebackRevision) {
    elements.voiceWritebackStatus.textContent =
      "Repository writeback is unavailable; no changes were saved.";
    return;
  }

  const submitButton = elements.voiceReviewForm.querySelector('button[type="submit"]');
  const formValues = Object.fromEntries(new FormData(elements.voiceReviewForm).entries());
  try {
    validateVoiceEvaluationFormValues(formValues);
  } catch (error) {
    elements.voiceWritebackStatus.textContent = `Validation failed: ${error.message}`;
    return;
  }

  submitButton.disabled = true;
  elements.voiceWritebackStatus.textContent = "Validating and saving Voice-ID-001...";
  try {
    const response = await fetch("/api/voice-id-001", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        experiment_id: "Voice-ID-001",
        revision: writebackRevision,
        form_values: formValues,
      }),
    });
    const result = await response.json();
    if (!response.ok) {
      if (response.status === 409) {
        writebackReady = false;
        writebackRevision = undefined;
      }
      throw new Error(result.error ?? "Repository writeback failed.");
    }

    writebackRevision = result.revision;
    voiceExperiment.human_evaluation.submissions = result.submissions;
    renderListenerSuggestions(result.listener_suggestions);
    renderVoiceExperiment(voiceExperiment);
    elements.voiceWritebackStatus.textContent =
      `Saved to the repository. JSON snapshot: ${result.snapshot_name}`;
  } catch (error) {
    elements.voiceWritebackStatus.textContent = `Save failed: ${error.message}`;
  } finally {
    submitButton.disabled = !writebackReady;
  }
}

function renderQueueTable(target, records) {
  const table = createElement("table", "demo-table");
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  for (const label of ["Demo", "Review", "Founder review", "Classification", "Disposition"]) {
    headerRow.append(createElement("th", "", label));
  }
  thead.append(headerRow);

  const tbody = document.createElement("tbody");
  if (records.length === 0) {
    const row = document.createElement("tr");
    const cell = createElement("td", "empty-cell", "No demos match this view.");
    cell.colSpan = 5;
    row.append(cell);
    tbody.append(row);
  }

  for (const demo of records) {
    const state = reviewFor(demo);
    const row = document.createElement("tr");
    const demoCell = document.createElement("td");
    const openButton = createElement("button", "demo-open-button");
    openButton.type = "button";
    openButton.dataset.demoId = demo.demo_id;
    openButton.append(
      createElement("span", "demo-title", demo.title || "Untitled demo"),
      createElement("span", "demo-id", demo.demo_id),
    );
    demoCell.append(openButton);

    const reviewCell = document.createElement("td");
    reviewCell.append(statusBadge(state.reviewLabel, state.classificationEligible ? "complete" : "pending"));

    const founderCell = createElement("td");
    founderCell.append(statusBadge(
      `Founder review ${state.founderReviewState.toLowerCase()}`,
      state.classificationEligible ? "complete" : "pending",
    ));

    const eligibilityCell = createElement("td");
    eligibilityCell.append(state.classificationEligible
      ? statusBadge("Classification Eligible", "eligible")
      : createElement("span", "muted-cell", "Not eligible"));

    const dispositionCell = createElement("td", "disposition-cell", isKnown(demo.current_disposition)
      ? demo.current_disposition
      : "UNKNOWN");

    row.append(demoCell, reviewCell, founderCell, eligibilityCell, dispositionCell);
    tbody.append(row);
  }

  table.append(thead, tbody);
  target.replaceChildren(table);
  for (const button of target.querySelectorAll("[data-demo-id]")) {
    button.addEventListener("click", () => showDemo(button.dataset.demoId));
  }
}

function renderIntakeSummary(demo) {
  const state = reviewFor(demo);
  const card = createElement("article", "intake-card");
  const header = createElement("div", "intake-card-header");
  const titleBlock = createElement("div");
  titleBlock.append(
    createElement("p", "eyebrow", demo.demo_id),
    createElement("h3", "", demo.title || "Untitled demo"),
    createElement("p", "muted", demo.creator || "Creator UNKNOWN"),
  );
  header.append(titleBlock, statusBadge(
    isKnown(demo.review_status) ? demo.review_status.replaceAll("_", " ") : "UNKNOWN",
    "neutral",
  ));

  const evidence = createElement("dl", "intake-facts");
  for (const [label, value] of [
    ["Submitted", demo.submitted_at],
    ["Submission type", demo.submission_type],
    ["Source", demo.submission_source],
    ["Audio received", demo.audio_downloaded === true ? "Yes" : "No"],
    ["Checksum", demo.audio_sha256],
    ["Rights review", demo.rights_review_status],
    ["Founder review", state.founderReviewState],
  ]) {
    evidence.append(
      createElement("dt", "", label),
      createElement("dd", "", isKnown(value) ? String(value) : "UNKNOWN"),
    );
  }

  const sourceLinks = createElement("div", "record-links");
  if (isKnown(demo.suno_url)) {
    sourceLinks.append(createLink("Open Suno source", demo.suno_url));
  }
  if (isKnown(demo.provenance_record)) {
    sourceLinks.append(createLink("Provenance record", githubRecordLink(demo.provenance_record)));
  }
  sourceLinks.append(createLink("Intake standard", `${REPOSITORY_URL}/blob/main/operations/demo-intake/intake-standard.md`));

  const missingEvidence = createElement("div", "missing-evidence");
  missingEvidence.append(createElement("h4", "", "Required evidence"));
  const evidenceList = document.createElement("ul");
  const requiredEvidence = Array.isArray(demo.required_evidence) ? demo.required_evidence : [];
  for (const item of requiredEvidence) {
    evidenceList.append(createElement("li", "", String(item)));
  }
  if (requiredEvidence.length === 0) {
    evidenceList.append(createElement("li", "muted", "No outstanding requirements recorded."));
  }
  missingEvidence.append(evidenceList);

  card.append(header, evidence, missingEvidence, sourceLinks);
  return card;
}

function renderIntake() {
  elements.intakeList.replaceChildren(...demos.map(renderIntakeSummary));
}

function renderDashboardTable() {
  const pendingDemos = demos.filter((demo) => !reviewFor(demo).classificationEligible);
  renderQueueTable(elements.dashboardTable, pendingDemos.slice(0, 5));
}

function renderQueue() {
  const search = elements.search.value.trim().toLowerCase();
  const filter = elements.reviewFilter.value;
  const filtered = demos.filter((demo) => {
    const state = reviewFor(demo);
    const matchesSearch = search === "" || demoSearchText(demo).includes(search);
    const matchesFilter =
      filter === "all" ||
      (filter === "pending" && !state.classificationEligible) ||
      (filter === "complete" && state.classificationEligible);
    return matchesSearch && matchesFilter;
  });
  renderQueueTable(elements.queueTable, filtered);
}

function valueAt(record, path) {
  return path.split(".").reduce((value, key) => value?.[key], record);
}

function firstKnownValue(record, paths) {
  for (const path of paths) {
    const value = valueAt(record, path);
    if (Array.isArray(value) ? value.some(isKnown) : isKnown(value)) {
      return value;
    }
  }
  return "UNKNOWN";
}

function formatValue(value) {
  if (Array.isArray(value)) {
    return value.filter(isKnown).map(String).join(", ") || "UNKNOWN";
  }
  if (value && typeof value === "object") {
    return JSON.stringify(value);
  }
  return isKnown(value) ? String(value) : "UNKNOWN";
}

function detailField(label, value, note) {
  const wrapper = createElement("div", "detail-field");
  wrapper.append(
    createElement("dt", "", label),
    createElement("dd", "", formatValue(value)),
  );
  if (note) {
    wrapper.append(createElement("p", "detail-field-note", note));
  }
  return wrapper;
}

function detailGrid(fields, className = "detail-grid") {
  const grid = createElement("dl", className);
  for (const [label, value, note] of fields) {
    grid.append(detailField(label, value, note));
  }
  return grid;
}

function detailPanel(number, title, description) {
  const panel = createElement("section", "panel detail-section");
  panel.setAttribute("aria-labelledby", `detail-section-${number}-title`);
  const heading = createElement("div", "detail-panel-heading");
  heading.append(
    createElement("p", "eyebrow", `Section ${number}`),
    createElement("h3", "", title),
  );
  heading.lastElementChild.id = `detail-section-${number}-title`;
  panel.append(heading);
  if (description) {
    panel.append(createElement("p", "detail-panel-description", description));
  }
  return panel;
}

function renderTextAsset(label, value, note, linkHref) {
  const disclosure = createElement("details", "creative-asset");
  disclosure.open = true;
  disclosure.append(createElement("summary", "", label));
  const content = createElement("div", "creative-asset-content");
  content.append(createElement(
    "div",
    isKnown(value) ? "creative-text" : "muted creative-text",
    formatValue(value),
  ));
  if (note) {
    content.append(createElement("p", "detail-field-note", note));
  }
  if (isHttpUrl(linkHref)) {
    content.append(createLink(`Open ${label.toLowerCase()} source`, linkHref));
  }
  disclosure.append(content);
  return disclosure;
}

function isHttpUrl(value) {
  if (!isKnown(value)) {
    return false;
  }
  try {
    const url = new URL(String(value));
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function renderSourceLabels(demo) {
  const labels = firstKnownValue(demo, [
    "source_snapshot.source_labels",
    "source_labels",
  ]);
  if (!Array.isArray(labels)) {
    return detailField("Source labels", labels);
  }

  const wrapper = createElement("div", "source-label-field");
  wrapper.append(createElement("p", "field-label", "Source labels"));
  if (labels.length === 0) {
    wrapper.append(createElement("p", "muted", "UNKNOWN"));
    return wrapper;
  }
  const chips = createElement("div", "source-label-list");
  for (const label of labels) {
    chips.append(createElement("span", "source-label-chip", String(label)));
  }
  wrapper.append(chips);
  return wrapper;
}

function renderArtwork(demo) {
  const artwork = firstKnownValue(demo, [
    "source_snapshot.artwork_reference",
    "artwork_reference",
  ]);
  const wrapper = createElement("div", "artwork-field");
  wrapper.append(createElement("p", "field-label", "Artwork"));
  if (!isKnown(artwork)) {
    wrapper.append(createElement("p", "muted", "UNKNOWN"));
    return wrapper;
  }

  if (isHttpUrl(artwork)) {
    const image = createElement("img", "artwork-preview");
    image.src = artwork;
    image.alt = `Artwork for ${demo.title || demo.demo_id}`;
    image.loading = "lazy";
    image.referrerPolicy = "no-referrer";
    wrapper.append(image, createLink("Open artwork source", artwork));
  } else {
    wrapper.append(createElement("p", "creative-text", String(artwork)));
  }
  return wrapper;
}

function renderReviewCard(review, index) {
  const card = createElement("article", "linked-review-card");
  card.append(
    createElement("p", "eyebrow", `Linked review ${index + 1}`),
    createElement("h4", "", review.review_id || "Review ID UNKNOWN"),
    detailGrid([
      ["Review type", review.review_type],
      ["Reviewer role", review.reviewer_role],
      ["Review date", review.review_date],
      ["Founder review status", review.founder_review_status],
      ["Audio reviewed", review.audio_reviewed === true ? "Yes" : review.audio_reviewed === false ? "No" : "UNKNOWN"],
      ["Overall creative grade", review.overall_creative_grade],
      ["Recommended disposition", review.recommended_disposition],
    ], "detail-grid review-facts"),
  );
  if (isKnown(review.evaluation_instrument_version)) {
    card.append(createLink(
      "Evaluation standard",
      githubRecordLink(review.evaluation_instrument_version),
    ));
  }
  return card;
}

function renderDemoDetail(demo) {
  const state = reviewFor(demo);
  const sourceUrl = firstKnownValue(demo, [
    "source_snapshot.source_url",
    "source_url",
    "suno_url",
  ]);
  const sourceLabelsNote =
    "Source labels were observed in the Suno screenshots but are not captured in the canonical demo record.";
  const heading = createElement("header", "detail-heading");
  const identity = createElement("div", "detail-identity");
  const demoId = createElement("h2", "detail-demo-id", formatValue(demo.demo_id));
  demoId.id = "detail-title";
  demoId.tabIndex = -1;
  identity.append(
    createElement("p", "eyebrow", "Demo ID"),
    demoId,
    createElement("p", "working-title", `Working Title: ${formatValue(demo.title)}`),
    createElement(
      "p",
      "muted",
      `Source creator display: ${formatValue(firstKnownValue(demo, [
        "source_snapshot.source_creator_display",
        "source_creator_display",
        "creator",
      ]))}`,
    ),
  );
  const badges = createElement("div", "detail-badges");
  badges.append(statusBadge(
    `Review Status: ${state.reviewLabel}`,
    state.classificationEligible ? "complete" : "pending",
  ));
  heading.append(identity, badges);

  const sourcePanel = detailPanel(1, "Source Context");
  sourcePanel.append(detailGrid([
    ["Source platform", firstKnownValue(demo, [
      "source_snapshot.source_platform",
      "source_platform",
      "generator",
    ])],
    ["Source URL", sourceUrl],
    ["Source song ID", firstKnownValue(demo, [
      "source_snapshot.source_song_id",
      "source_song_id",
      "suno_song_id",
    ])],
    ["Source display name", firstKnownValue(demo, [
      "source_snapshot.source_display_name",
      "source_display_name",
    ])],
    ["Source creator display", firstKnownValue(demo, [
      "source_snapshot.source_creator_display",
      "source_creator_display",
      "creator",
    ]), "Source attribution only; it does not establish project ownership, assigned artist, or performer."],
    ["Source account", firstKnownValue(demo, [
      "source_snapshot.source_account",
      "source_account",
    ])],
    ["Source playlist", firstKnownValue(demo, [
      "source_snapshot.source_playlist",
      "source_playlist",
    ]), "Observed in the source screenshots; not captured in the canonical demo record."],
    ["Source generation model", firstKnownValue(demo, [
      "source_snapshot.source_generation_model",
      "source_generation_model",
      "model_version",
    ]), "Observed in the source screenshots; not captured in the canonical demo record."],
    ["Source creation timestamp", firstKnownValue(demo, [
      "source_snapshot.source_created_timestamp",
      "source_created_timestamp",
      "creation_date",
    ]), "Observed in the source screenshots; not captured in the canonical demo record."],
    ["Observed timestamp", firstKnownValue(demo, [
      "source_snapshot.observed_at",
      "source_observed_at",
    ])],
  ]));
  if (isHttpUrl(sourceUrl)) {
    const links = createElement("div", "record-links");
    links.append(createLink("Open source", sourceUrl));
    sourcePanel.append(links);
  }
  sourcePanel.append(createElement(
    "p",
    "source-observation-note",
    "Screenshot-observed metadata is shown only when present in repository data. Playlist, model, labels, style description, and source creation timestamp are not captured in the canonical demo record, so this read-only view does not invent or duplicate their values.",
  ));

  const creativePanel = detailPanel(
    2,
    "Creative Context",
    "Source creative material is shown as observed. Missing values are not inferred.",
  );
  creativePanel.append(renderArtwork(demo));
  creativePanel.append(renderTextAsset(
    "Style Description",
    firstKnownValue(demo, [
      "source_snapshot.style_description",
      "style_description",
    ]),
    "Observed as a separate source item; not captured in the canonical demo record.",
  ));
  creativePanel.append(renderTextAsset(
    "Lyrics",
    firstKnownValue(demo, [
      "source_snapshot.lyrics",
      "lyrics",
      "lyrics_text",
    ]),
    demo.lyrics_status || "Lyrics text is not stored locally.",
    isKnown(demo.lyrics_location) ? demo.lyrics_location : sourceUrl,
  ));
  creativePanel.append(renderTextAsset(
    "Creator Notes",
    firstKnownValue(demo, [
      "source_snapshot.creator_notes",
      "creator_notes",
    ]),
    "No creator notes are captured in the canonical demo record.",
  ));
  creativePanel.append(renderTextAsset(
    "Prompt",
    firstKnownValue(demo, [
      "source_snapshot.prompt",
      "original_prompt",
    ]),
    "Prompt text is not captured in the canonical demo record.",
  ));

  const intentPanel = detailPanel(
    3,
    "Creator Intent",
    "Creator-stated targets are distinct from source labels and founder review.",
  );
  intentPanel.append(detailGrid([
    ["Source material", firstKnownValue(demo, [
      "creator_intent.source_material_type",
      "source_material_type",
      "source_material",
    ])],
    ["Genre target", firstKnownValue(demo, [
      "creator_intent.genre_target",
      "genre_target",
    ])],
    ["Style target", firstKnownValue(demo, [
      "creator_intent.style_target",
      "style_target",
    ])],
    ["Voice target", firstKnownValue(demo, [
      "creator_intent.voice_target",
      "voice_target",
    ])],
    ["Project purpose", firstKnownValue(demo, [
      "creator_intent.project_purpose",
      "project_purpose",
    ])],
    ["Tempo target", firstKnownValue(demo, [
      "creator_intent.tempo_target",
      "tempo_target",
    ])],
  ]));

  const constraintsPanel = detailPanel(
    4,
    "Creative Constraints",
    "Intent describes what should be created; constraints describe what should not be created.",
  );
  constraintsPanel.append(renderTextAsset(
    "Excluded Styles",
    firstKnownValue(demo, [
      "creative_constraints.exclude_styles",
      "exclude_styles",
      "exclude_prompt",
    ]),
    "No excluded styles or constraints are captured in the canonical demo record.",
  ));
  constraintsPanel.append(renderTextAsset(
    "Other Generation Constraints",
    firstKnownValue(demo, [
      "creative_constraints.other",
      "generation_constraints",
    ]),
    "No other generation constraints are captured in the canonical demo record.",
  ));

  const labelsPanel = detailPanel(
    5,
    "Source Labels",
    "Source wording is preserved as-is and is not taxonomy-mapped in this workbench.",
  );
  labelsPanel.append(renderSourceLabels(demo));
  labelsPanel.append(createElement("p", "detail-field-note", sourceLabelsNote));

  const readinessPanel = detailPanel(
    6,
    "Review Readiness",
    "Evidence state and gate reasons are derived from the canonical demo and linked review records.",
  );
  readinessPanel.append(detailGrid([
    ["Audio available", demo.audio_downloaded === true
      ? "Yes"
      : demo.audio_downloaded === false
        ? "No - original audio has not been received"
        : "UNKNOWN"],
    ["Rights review", demo.rights_review_status],
    ["Founder review status", state.founderReviewState],
    ["Intake status", demo.review_status],
    ["Classification eligibility", state.classificationEligible
      ? "Eligible to consider; value is not assigned"
      : "Not eligible yet"],
  ]));

  const blockers = createElement("div", "readiness-list");
  blockers.append(createElement("h4", "", "Why this cannot advance"));
  const blockerList = document.createElement("ul");
  for (const blocker of state.eligibilityBlockers) {
    blockerList.append(createElement("li", "", blocker));
  }
  if (blockerList.childElementCount === 0) {
    blockerList.append(createElement("li", "", "No founder-review gate blockers."));
  }
  blockers.append(blockerList);

  const requiredEvidence = createElement("div", "readiness-list");
  requiredEvidence.append(createElement("h4", "", "Required Evidence"));
  const evidenceList = document.createElement("ul");
  const evidenceItems = Array.isArray(demo.required_evidence) ? demo.required_evidence : [];
  for (const item of evidenceItems) {
    evidenceList.append(createElement("li", "", String(item)));
  }
  if (evidenceItems.length === 0) {
    evidenceList.append(createElement("li", "muted", "UNKNOWN"));
  }
  requiredEvidence.append(evidenceList);
  readinessPanel.append(
    blockers,
    requiredEvidence,
    createElement(
      "p",
      "gate-note",
      "Classification eligibility is only a prerequisite. It does not assign classification or seed, and rights and development decisions remain separate.",
    ),
  );

  const governancePanel = detailPanel(
    7,
    "Governance",
    "Governance outcomes remain below source, creative material, and readiness.",
  );
  governancePanel.append(detailGrid([
    ["Classification", demo.classification?.primary],
    ["Classification rationale", demo.classification_rationale],
    ["Seed designation", demo.seed_designation?.primary],
    ["Seed rationale", demo.seed_rationale],
    ["Disposition", demo.current_disposition],
  ]));
  if (state.governanceConflict) {
    governancePanel.append(createElement(
      "p",
      "error-banner inline-error",
      "Governance check: a classification or seed value exists before a qualifying founder review.",
    ));
  }
  governancePanel.append(createElement("h4", "linked-reviews-title", "Linked Reviews"));
  if (state.linkedReviews.length > 0) {
    for (const [index, review] of state.linkedReviews.entries()) {
      governancePanel.append(renderReviewCard(review, index));
    }
  } else {
    governancePanel.append(createElement("p", "muted", "No linked review record is available."));
  }
  const repositoryLinks = createElement("div", "record-links");
  for (const [label, recordPath] of [
    ["Demo registry", "catalog/metadata/demos.yaml"],
    ["Review registry", "catalog/metadata/demo-reviews.yaml"],
    ["Provenance", demo.provenance_record],
    ["Evaluation", demo.evaluation_record],
    ["Disposition plan", demo.development_plan],
  ]) {
    if (isKnown(recordPath)) {
      repositoryLinks.append(createLink(label, githubRecordLink(recordPath)));
    }
  }
  governancePanel.append(repositoryLinks);

  const advanced = createElement("details", "panel advanced-metadata");
  advanced.append(createElement("summary", "", "Section 8 - Advanced Metadata"));
  advanced.append(detailGrid([
    ["Submitted", demo.submitted_at],
    ["Submission type", demo.submission_type],
    ["Preserved audio location", demo.audio_downloaded === true ? demo.audio_location : "UNKNOWN"],
    ["Checksum", demo.audio_sha256],
    ["Archive metadata", demo.archive_metadata],
    ["Preservation metadata", demo.preservation_metadata],
    ["Integrity metadata", demo.integrity_metadata],
    ["Technical metadata", demo.technical_metadata],
  ]));

  const root = createElement("article", "detail-record");
  root.append(heading);
  if (state.governanceConflict) {
    root.append(createElement(
      "p",
      "error-banner inline-error",
      "Governance check: a classification or seed value exists before a qualifying founder review.",
    ));
  }
  root.append(
    sourcePanel,
    creativePanel,
    intentPanel,
    constraintsPanel,
    labelsPanel,
    readinessPanel,
    governancePanel,
    advanced,
  );
  return root;
}

function showView(name) {
  for (const view of elements.views) {
    view.hidden = view.id !== `${name}-view`;
  }
  for (const button of elements.navigation) {
    const active = button.dataset.view === name;
    button.classList.toggle("is-active", active);
    if (active) {
      button.setAttribute("aria-current", "page");
    } else {
      button.removeAttribute("aria-current");
    }
  }
}

function showDemo(demoId) {
  const demo = demos.find((record) => record.demo_id === demoId);
  if (!demo) {
    throw new Error(`Demo record not found: ${demoId}`);
  }
  elements.detail.replaceChildren(renderDemoDetail(demo));
  showView("detail");
  document.querySelector("#detail-title").focus?.();
}

function displayError(error) {
  console.error("Founder Review Portal could not load repository review data.", error);
  elements.error.textContent = `Unable to load repository review data: ${error.message}`;
  elements.error.hidden = false;
}

let demos;
let reviewRecords;
let voiceExperiment;

try {
  demos = parseRecords(demoYaml, "demo_records", "Demo registry");
  reviewRecords = parseRecords(reviewYaml, "review_records", "Review registry");
  const voiceExperiments = parseRecords(
    voiceExperimentYaml,
    "experiment_records",
    "Voice experiment registry",
  );
  voiceExperiment = voiceExperiments.find((record) => record.experiment_id === "Voice-ID-001");
  if (!voiceExperiment || voiceExperiments.length !== 1) {
    throw new Error("Voice experiment registry must contain exactly one Voice-ID-001 record.");
  }
  const demoIds = new Set(demos.map((demo) => demo.demo_id));
  if (demoIds.size !== demos.length || demos.some((demo) => !isKnown(demo.demo_id))) {
    throw new Error("Demo registry contains a missing or duplicate demo identifier.");
  }
  const orphanedReviews = reviewRecords.filter((review) => !demoIds.has(review.demo_id));
  if (orphanedReviews.length > 0) {
    throw new Error(`Review registry contains ${orphanedReviews.length} review record(s) without a matching demo.`);
  }

  renderMetrics();
  renderDashboardTable();
  renderIntake();
  renderQueue();
  renderVoiceExperiment(voiceExperiment);
  for (const button of elements.navigation) {
    button.addEventListener("click", () => showView(button.dataset.view));
  }
  for (const button of document.querySelectorAll("[data-view]:not(.nav-item)")) {
    button.addEventListener("click", () => showView(button.dataset.view));
  }
  elements.search.addEventListener("input", renderQueue);
  elements.reviewFilter.addEventListener("change", renderQueue);
  elements.backToQueue.addEventListener("click", () => showView("queue"));
  elements.voiceReviewForm.addEventListener("submit", saveVoiceEvaluation);
  void loadVoiceWritebackState();
} catch (error) {
  displayError(error);
}
