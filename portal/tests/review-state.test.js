import test from "node:test";
import assert from "node:assert/strict";
import { deriveReviewState } from "../src/review-state.js";

const demo = {
  demo_id: "DEMO-TEST-0001",
  classification: { primary: "UNKNOWN" },
  seed_designation: { primary: "UNKNOWN" },
};

const pendingIntakeReview = {
  demo_id: demo.demo_id,
  review_id: "REVIEW-TEST-0001",
  reviewer_role: "AI intake assistant; founder review pending",
  reviewer_id: "UNKNOWN",
  review_date: "2026-11-21",
  founder_review_status: "pending",
  audio_reviewed: false,
  overall_creative_grade: "N/R",
  category_evidence: { hook_strength: "N/R - no audio audition." },
};

function completedFounderReview(overrides = {}) {
  return {
    demo_id: demo.demo_id,
    review_id: "REVIEW-TEST-0002",
    reviewer_role: "Founder",
    reviewer_id: "founder-1",
    review_date: "2026-11-21",
    founder_review_status: "complete",
    audio_reviewed: true,
    overall_creative_grade: "B",
    category_evidence: { hook_strength: "Strong recurring melodic hook." },
    ...overrides,
  };
}

test("AI intake and N/R-only evidence remain pending and ineligible", () => {
  const state = deriveReviewState(demo, [pendingIntakeReview]);

  assert.equal(state.reviewLabel, "Review Pending");
  assert.equal(state.founderReviewState, "Pending");
  assert.equal(state.classificationEligible, false);
  assert.ok(state.eligibilityBlockers.includes("Founder review is not marked complete."));
  assert.ok(state.eligibilityBlockers.includes("Original audio has not been reviewed."));
  assert.ok(state.eligibilityBlockers.includes("No rateable evaluation grade is recorded."));
});

test("documented founder review opens classification eligibility without assigning values", () => {
  const state = deriveReviewState(demo, [completedFounderReview()]);

  assert.equal(state.reviewLabel, "Review Complete");
  assert.equal(state.founderReviewState, "Complete");
  assert.equal(state.classificationEligible, true);
  assert.deepEqual(state.eligibilityBlockers, []);
  assert.equal(demo.classification.primary, "UNKNOWN");
  assert.equal(demo.seed_designation.primary, "UNKNOWN");
});

test("records without a linked review explain the eligibility blocker", () => {
  const state = deriveReviewState(demo, []);

  assert.deepEqual(state.eligibilityBlockers, [
    "No linked review record is available.",
  ]);
});

test("incomplete founder evidence does not open the gate", () => {
  const state = deriveReviewState(demo, [
    completedFounderReview({ audio_reviewed: false }),
  ]);

  assert.equal(state.reviewLabel, "Review Pending");
  assert.equal(state.classificationEligible, false);
});

test("records without a linked review remain pending and report no founder review", () => {
  const state = deriveReviewState(demo, []);

  assert.equal(state.reviewLabel, "Review Pending");
  assert.equal(state.founderReviewState, "Not recorded");
  assert.equal(state.classificationEligible, false);
});
