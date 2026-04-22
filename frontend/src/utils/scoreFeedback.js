/**
 * Maps a CLIP similarity score (0-100) to a short, actionable hint.
 * Used by Practice and Challenge result panels.
 * @param {number} score
 * @returns {string}
 */
export function scoreFeedback(score) {
  const value = Number(score);
  if (Number.isNaN(value)) return "Score unavailable.";
  if (value >= 85) return "Near-perfect match — almost identical to the reference.";
  if (value >= 70) return "Strong match. Try refining colors, lighting, or composition for the last few points.";
  if (value >= 55) return "Decent match. Add more concrete subject and style details to the prompt.";
  if (value >= 40) return "Some elements landed. Name the subject, setting, and mood explicitly.";
  return "Off target. Describe what's literally in the image — subject, environment, art style.";
}
