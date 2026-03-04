import { useState, useEffect } from "react";
import { getRounds, submitPrompt } from "../../api";
import styles from "./PracticePage.module.css";

// Static image map – Vite resolves these at build time
import ancientTemple from "../../../reference_images/ancient-temple.jpg";
import futuristicCity from "../../../reference_images/futuristic-city.jpg";
import goldenSunset from "../../../reference_images/golden-sunset.jpeg";
import snowyForest from "../../../reference_images/snowy-forest.jpg";
import underwaterWorld from "../../../reference_images/underwater-world.jpeg";

const REFERENCE_IMAGE_MAP = {
  "ancient-temple.jpg": ancientTemple,
  "futuristic-city.jpg": futuristicCity,
  "golden-sunset.jpeg": goldenSunset,
  "snowy-forest.jpg": snowyForest,
  "underwater-world.jpeg": underwaterWorld,
};

// Fallback rounds if the backend isn't available yet
const FALLBACK_ROUNDS = [
  { id: "ancient-temple", title: "Ancient Temple", difficulty: "easy", reference_image: "ancient-temple.jpg" },
  { id: "futuristic-city", title: "Futuristic City", difficulty: "medium", reference_image: "futuristic-city.jpg" },
  { id: "golden-sunset", title: "Golden Sunset", difficulty: "easy", reference_image: "golden-sunset.jpeg" },
  { id: "snowy-forest", title: "Snowy Forest", difficulty: "easy", reference_image: "snowy-forest.jpg" },
  { id: "underwater-world", title: "Underwater World", difficulty: "hard", reference_image: "underwater-world.jpeg" },
];

const DIFFICULTY_ORDER = { easy: 0, medium: 1, hard: 2 };
const sortByDifficulty = (arr) =>
  [...arr].sort(
    (a, b) =>
      (DIFFICULTY_ORDER[a.difficulty] ?? 99) - (DIFFICULTY_ORDER[b.difficulty] ?? 99)
  );

const SORTED_FALLBACK_ROUNDS = sortByDifficulty(FALLBACK_ROUNDS);

const MAX_PROMPT_LENGTH = 2000;

export default function PracticePage() {
  const [rounds, setRounds] = useState(SORTED_FALLBACK_ROUNDS);
  const [selectedRound, setSelectedRound] = useState(SORTED_FALLBACK_ROUNDS[0]);
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImageUrl, setGeneratedImageUrl] = useState(null);
  const [similarityScore, setSimilarityScore] = useState(null);
  const [error, setError] = useState(null);

  // Fetch rounds from backend; fall back to local list if unavailable
  useEffect(() => {
    getRounds()
      .then((data) => {
        if (data && data.length > 0) {
          const sorted = sortByDifficulty(data);
          setRounds(sorted);
          setSelectedRound(sorted[0]);
        }
      })
      .catch(() => {
        // Use fallback rounds (already set)
      });
  }, []);

  function handleSelectRound(round) {
    setSelectedRound(round);
    setGeneratedImageUrl(null);
    setSimilarityScore(null);
    setError(null);
    setPrompt("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;

    setIsLoading(true);
    setGeneratedImageUrl(null);
    setSimilarityScore(null);
    setError(null);

    try {
      const result = await submitPrompt({
        round_id: selectedRound.id,
        user_prompt: prompt.trim(),
      });
      setGeneratedImageUrl(result.generated_image_url);
      setSimilarityScore(result.similarity_score);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  const referenceImageSrc = REFERENCE_IMAGE_MAP[selectedRound?.reference_image];
  const canSubmit = prompt.trim().length > 0 && !isLoading;

  return (
    <div className={styles.page}>
      {/* Header */}
      <div className={styles.header}>
        <h1>Practice Mode</h1>
        <p>Select a challenge, write a prompt, and see how close your AI generation matches the reference.</p>
      </div>

      {/* Round selector */}
      <div className={styles.roundSelector}>
        {rounds.map((round) => (
          <button
            key={round.id}
            className={`${styles.roundCard} ${selectedRound?.id === round.id ? styles.roundCardActive : ""}`}
            onClick={() => handleSelectRound(round)}
          >
            <span className={styles.roundCardTitle}>{round.title}</span>
            <span className={`${styles.difficultyBadge} ${styles[round.difficulty]}`}>
              {round.difficulty}
            </span>
          </button>
        ))}
      </div>

      {/* Image comparison */}
      <div className={styles.comparisonGrid}>
        {/* Reference image */}
        <div className={styles.imagePanel}>
          <span className={styles.imageLabel}>Reference Image</span>
          <div className={styles.imageBox}>
            {referenceImageSrc ? (
              <img src={referenceImageSrc} alt={selectedRound?.title} />
            ) : (
              <div className={styles.imagePlaceholder}>
                <span className={styles.imagePlaceholderIcon}>🖼️</span>
                <span>No reference image</span>
              </div>
            )}
          </div>
        </div>

        {/* Generated image */}
        <div className={styles.imagePanel}>
          <span className={styles.imageLabel}>Your Generated Image</span>
          <div className={styles.imageBox}>
            {isLoading ? (
              <div className={styles.imagePlaceholder}>
                <div className={styles.spinner} />
                <span>Generating image…</span>
              </div>
            ) : generatedImageUrl ? (
              <img src={generatedImageUrl} alt="AI generated result" />
            ) : (
              <div className={styles.imagePlaceholder}>
                <span className={styles.imagePlaceholderIcon}>✨</span>
                <span>Your image will appear here</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Prompt input */}
      <form className={styles.promptSection} onSubmit={handleSubmit}>
        <label className={styles.promptLabel} htmlFor="prompt-input">
          Your Prompt
        </label>
        <textarea
          id="prompt-input"
          className={styles.promptTextarea}
          placeholder={`Describe the scene you see in "${selectedRound?.title}"…`}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value.slice(0, MAX_PROMPT_LENGTH))}
          disabled={isLoading}
          rows={4}
        />

        <div className={styles.actionRow}>
          <button
            type="submit"
            className={styles.generateBtn}
            disabled={!canSubmit}
          >
            {isLoading ? "Generating…" : "Generate Image"}
          </button>
          <span className={styles.charCount}>
            {prompt.length} / {MAX_PROMPT_LENGTH}
          </span>
        </div>
      </form>

      {/* Error */}
      {error && <div className={styles.errorBanner}>{error}</div>}

      {/* Similarity score */}
      {similarityScore !== null && (
        <div className={styles.scoreRow}>
          <span className={styles.scoreLabel}>Similarity Score:</span>
          <span className={`${styles.scorePill} ${styles.scorePillActive}`}>
            {similarityScore === 0
              ? "Scoring…"
              : `${similarityScore.toFixed(1)} / 100`}
          </span>
        </div>
      )}
    </div>
  );
}
