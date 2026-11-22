const RATEABLE_GRADES = new Set(["A", "B", "C", "D", "F"]);
const GRADE_FIELDS = [
  "emotional_impact_grade",
  "song_concept_grade",
  "hook_grade",
  "source_fidelity_grade",
  "voice_performance_grade",
  "production_identity_grade",
  "arrangement_grade",
  "technical_quality_grade",
  "roster_fit_grade",
  "development_potential_grade",
  "overall_creative_grade",
];

function isKnown(value) {
  return typeof value === "string" && value.trim() !== "" && value.trim() !== "UNKNOWN";
}

function hasWrittenCategoryEvidence(review) {
  return Object.values(review.category_evidence ?? {}).some((value) => {
    if (!isKnown(value)) {
      return false;
    }

    return !/^(?:N\/R\b|not assessed\b)/i.test(value.trim());
  });
}

function isQualifyingFounderReview(review) {
  const reviewerRole = String(review.reviewer_role ?? "");
  const reviewDate = String(review.review_date ?? "");
  const hasRateableGrade = GRADE_FIELDS.some((field) =>
    RATEABLE_GRADES.has(String(review[field] ?? "").toUpperCase()),
  );

  return (
    String(review.founder_review_status ?? "").toLowerCase() === "complete" &&
    /\bfounder\b/i.test(reviewerRole) &&
    isKnown(review.reviewer_id) &&
    isKnown(reviewDate) &&
    !Number.isNaN(Date.parse(reviewDate)) &&
    review.audio_reviewed === true &&
    hasRateableGrade &&
    hasWrittenCategoryEvidence(review)
  );
}

export function deriveReviewState(demo, allReviews) {
  const linkedReviews = allReviews
    .filter((review) => review.demo_id === demo.demo_id)
    .slice()
    .sort((left, right) =>
      String(right.review_date ?? "").localeCompare(String(left.review_date ?? "")),
    );
  const qualifyingReview = linkedReviews.find(isQualifyingFounderReview);
  const reviewComplete = Boolean(qualifyingReview);
  const classification = demo.classification?.primary ?? "UNKNOWN";
  const seedDesignation = demo.seed_designation?.primary ?? "UNKNOWN";

  return {
    linkedReviews,
    latestReview: linkedReviews[0] ?? null,
    founderReviewState: reviewComplete
      ? "Complete"
      : linkedReviews.length > 0
        ? "Pending"
        : "Not recorded",
    reviewLabel: reviewComplete ? "Review Complete" : "Review Pending",
    classificationEligible: reviewComplete,
    governanceConflict:
      !reviewComplete &&
      (classification !== "UNKNOWN" || seedDesignation !== "UNKNOWN"),
  };
}
