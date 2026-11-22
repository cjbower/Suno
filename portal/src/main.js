import { load } from "js-yaml";
import demoYaml from "../../catalog/metadata/demos.yaml?raw";
import reviewYaml from "../../catalog/metadata/demo-reviews.yaml?raw";
import "./styles.css";
import { deriveReviewState } from "./review-state.js";

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

function detailField(label, value) {
  const wrapper = createElement("div", "detail-field");
  wrapper.append(
    createElement("dt", "", label),
    createElement("dd", "", isKnown(value) ? String(value) : "UNKNOWN"),
  );
  return wrapper;
}

function renderDemoDetail(demo) {
  const state = reviewFor(demo);
  const root = createElement("article", "detail-record");
  const heading = createElement("div", "detail-heading");
  const identity = createElement("div");
  const title = createElement("h2", "", demo.title || "Untitled demo");
  title.id = "detail-title";
  title.tabIndex = -1;
  identity.append(
    createElement("p", "eyebrow", demo.demo_id),
    title,
    createElement("p", "muted", demo.creator || "Creator UNKNOWN"),
  );
  const badges = createElement("div", "detail-badges");
  badges.append(
    statusBadge(state.reviewLabel, state.classificationEligible ? "complete" : "pending"),
    statusBadge(`Founder review ${state.founderReviewState.toLowerCase()}`, state.classificationEligible ? "complete" : "pending"),
    state.classificationEligible
      ? statusBadge("Classification Eligible", "eligible")
      : statusBadge("Not eligible yet", "neutral"),
  );
  heading.append(identity, badges);

  const facts = createElement("dl", "detail-grid");
  for (const [label, value] of [
    ["Review status", demo.review_status],
    ["Disposition", demo.current_disposition],
    ["Submission type", demo.submission_type],
    ["Submitted", demo.submitted_at],
    ["Creator attribution", demo.creator],
    ["Classification", demo.classification?.primary],
    ["Classification rationale", demo.classification_rationale],
    ["Seed designation", demo.seed_designation?.primary],
    ["Seed rationale", demo.seed_rationale],
    ["Rights review", demo.rights_review_status],
    ["Audio checksum", demo.audio_sha256],
  ]) {
    facts.append(detailField(label, value));
  }

  const reviewSection = createElement("section", "panel detail-section");
  reviewSection.append(
    createElement("p", "eyebrow", "Linked review"),
    createElement("h3", "", state.latestReview?.review_id || "No review record"),
  );
  if (state.latestReview) {
    const review = state.latestReview;
    const reviewFacts = createElement("dl", "detail-grid review-facts");
    for (const [label, value] of [
      ["Review type", review.review_type],
      ["Reviewer role", review.reviewer_role],
      ["Review date", review.review_date],
      ["Founder review state", review.founder_review_status],
      ["Audio reviewed", review.audio_reviewed === true ? "Yes" : "No"],
      ["Overall creative grade", review.overall_creative_grade],
      ["Recommended disposition", review.recommended_disposition],
    ]) {
      reviewFacts.append(detailField(label, value));
    }
    reviewSection.append(reviewFacts);
    if (isKnown(review.evaluation_instrument_version)) {
      reviewSection.append(createLink("Evaluation standard", githubRecordLink(review.evaluation_instrument_version)));
    }
  } else {
    reviewSection.append(createElement("p", "muted", "A founder review has not been recorded."));
  }

  const sourceLinks = createElement("div", "record-links");
  for (const [label, recordPath] of [
    ["Demo registry", "catalog/metadata/demos.yaml"],
    ["Review registry", "catalog/metadata/demo-reviews.yaml"],
    ["Provenance", demo.provenance_record],
    ["Evaluation", demo.evaluation_record],
    ["Disposition plan", demo.development_plan],
  ]) {
    if (isKnown(recordPath)) {
      sourceLinks.append(createLink(label, githubRecordLink(recordPath)));
    }
  }

  const factsPanel = createElement("section", "panel detail-section");
  factsPanel.append(createElement("p", "eyebrow", "Canonical demo record"));
  factsPanel.append(facts);

  root.append(heading);
  if (state.governanceConflict) {
    root.append(createElement(
      "p",
      "error-banner inline-error",
      "Governance check: a classification or seed value exists before a qualifying founder review.",
    ));
  }
  root.append(
    factsPanel,
    reviewSection,
  );
  const gateNote = createElement(
    "p",
    "gate-note",
    state.classificationEligible
      ? "The founder-review prerequisite is met. Classification and seed still require separate evidence and a documented decision."
      : "Classification and seed stay UNKNOWN until a qualifying, documented founder review is complete.",
  );
  root.append(gateNote, sourceLinks);
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
  console.error("Founder Review Portal could not load repository data.", error);
  elements.error.textContent = `Unable to load canonical repository data: ${error.message}`;
  elements.error.hidden = false;
}

let demos;
let reviewRecords;

try {
  demos = parseRecords(demoYaml, "demo_records", "Demo registry");
  reviewRecords = parseRecords(reviewYaml, "review_records", "Review registry");
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
  for (const button of elements.navigation) {
    button.addEventListener("click", () => showView(button.dataset.view));
  }
  for (const button of document.querySelectorAll("[data-view]:not(.nav-item)")) {
    button.addEventListener("click", () => showView(button.dataset.view));
  }
  elements.search.addEventListener("input", renderQueue);
  elements.reviewFilter.addEventListener("change", renderQueue);
  elements.backToQueue.addEventListener("click", () => showView("queue"));
} catch (error) {
  displayError(error);
}
