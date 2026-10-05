export const DEMO_ANALYSIS = {
  isDemo: true,
  score: 82,
  strength: "STRONG",
  risk_level: "LOW",
  score_note:
    "Security score is an analytical estimate based on multiple password characteristics and attack-resistance indicators.",
  entropy: 74.2,
  entropy_analysis: {
    theoretical_bits: 74.2,
    shannon_bits: 52.1,
    character_pool: 62,
    search_space_log10: 22.3,
    estimated_offline_crack_time: "about 26.5 years",
    assumption_guesses_per_second: 1000000000,
    caveat:
      "Theoretical entropy assumes uniformly random characters from the detected pool. Human-chosen passwords are typically much weaker.",
  },
  composition: { length: 14, uppercase: 2, lowercase: 8, digits: 3, special: 1, unique: 12 },
  radar: {
    length: 75,
    complexity: 78,
    entropy: 82,
    uniqueness: 80,
    dictionary_resistance: 88,
    pattern_resistance: 76,
    predictability: 79,
    attack_resistance: 84,
  },
  attack_resistance: {
    dictionary: 95,
    rule_based: 82,
    pattern: 76,
    brute_force: 88,
    overall: 86,
    levels: { dictionary: "HIGH", rule_based: "HIGH", pattern: "MEDIUM", brute_force: "HIGH" },
    details: {
      dictionary_match: false,
      predictable_patterns: "LOW",
      predictable_transformations: 1,
      estimated_search_space_bits: 74.2,
    },
    disclaimer:
      "Resistance scores are educational estimates. They do not attack any real system.",
  },
  patterns: [],
  pattern_detected: false,
  dictionary: {
    dictionary_match: false,
    similarity_score: 0.08,
    risk: "LOW",
    common_word_detected: false,
  },
  recommendations: [
    { severity: "ok", title: "Good password length", detail: "Length is in a healthier range for search-space resistance." },
    { severity: "ok", title: "Good character diversity", detail: "Multiple character classes were detected." },
    { severity: "medium", title: "Avoid predictable patterns", detail: "Review keyboard walks and year suffixes even in otherwise complex secrets." },
  ],
  improvement_path: [
    { label: "Current score", score: 82, change: null },
    { label: "Increase uniqueness", score: 86, change: 4 },
    { label: "Maintain unique per-account secrets", score: 88, change: 2 },
  ],
  ml_prediction: "STRONG",
  ml_confidence: 0.947,
  ml: {
    label: "STRONG",
    confidence: 0.947,
    available: true,
    model_name: "random_forest",
    probabilities: {
      VERY_WEAK: 0.012,
      WEAK: 0.023,
      MODERATE: 0.045,
      STRONG: 0.17,
      VERY_STRONG: 0.75,
    },
    feature_importance: [
      { feature: "length", importance: 0.28 },
      { feature: "entropy", importance: 0.22 },
      { feature: "dictionary_similarity", importance: 0.18 },
      { feature: "predictability_score", importance: 0.15 },
      { feature: "character_diversity", importance: 0.1 },
      { feature: "repeated_character_score", importance: 0.07 },
    ],
  },
};

export const STRENGTH_COLORS = {
  VERY_WEAK: "#ef4444",
  WEAK: "#f97316",
  MODERATE: "#f59e0b",
  STRONG: "#14b8a6",
  VERY_STRONG: "#22c55e",
};

export function localStrengthHint(password) {
  if (!password) return { score: 0, label: "Enter a password", color: "#64748b" };
  let score = Math.min(40, password.length * 4);
  const classes = [/[a-z]/, /[A-Z]/, /\d/, /[^A-Za-z0-9]/].filter((r) => r.test(password)).length;
  score += classes * 10;
  if (/(.)\1{2,}/.test(password)) score -= 10;
  if (/123456|qwerty|password|abcdef/i.test(password)) score -= 20;
  score = Math.max(0, Math.min(100, score));
  let label = "VERY WEAK";
  if (score > 20) label = "WEAK";
  if (score > 40) label = "MODERATE";
  if (score > 60) label = "STRONG";
  if (score > 80) label = "VERY STRONG";
  return { score, label, color: STRENGTH_COLORS[label.replace(" ", "_")] || STRENGTH_COLORS.MODERATE };
}

export function featureLabel(name) {
  return name
    .replaceAll("_", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
