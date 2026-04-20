import { useEffect, useState } from "react";
import { startRound, submitPrompt } from "../../api";
import styles from "./PracticePage.module.css";
import ErrorBanner from "../../components/ErrorBanner";

const PRACTICE_STORAGE_KEY = "promptcraft_practice_round_state";

function loadSavedPracticeState() {
  try {
    const raw = localStorage.getItem(PRACTICE_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    console.error("Failed to parse saved practice state:", error);
    localStorage.removeItem(PRACTICE_STORAGE_KEY);
    return null;
  }
}

function clearSavedPracticeState() {
  localStorage.removeItem(PRACTICE_STORAGE_KEY);
}

export default function PracticePage() {
  const savedState = loadSavedPracticeState();
  const [referenceImage, setReferenceImage] = useState(savedState?.referenceImage ?? null);
  const [referenceRoundId, setReferenceRoundId] = useState(savedState?.referenceRoundId ?? null);
  const [generatedImage, setGeneratedImage] = useState(savedState?.generatedImage ?? null);
  const [prompt, setPrompt] = useState(savedState?.prompt ?? "");
  const [loadingGenerated, setLoadingGenerated] = useState(false);
  const [similarityScore, setSimilarityScore] = useState(savedState?.similarityScore ?? null);
  const [error, setError] = useState(null);
  const [referenceError, setReferenceError] = useState(null);
  const [attemptHistory, setAttemptHistory] = useState(savedState?.attemptHistory ?? []);
  const [showAttemptHistory, setShowAttemptHistory] = useState(savedState?.showAttemptHistory ?? false);
  const loadReference = async () => {
    clearSavedPracticeState();
    try {
      const data = await startRound();
      setReferenceImage(
        `/reference_images/${data.target_image_url.replace("/static/", "")}`,
      );
      setReferenceRoundId(data.round_id);
      setGeneratedImage(null);
      setSimilarityScore(null);
      setPrompt("");
      setError(null);
      setReferenceError(null);
      setAttemptHistory([]);
      setShowAttemptHistory(false);
    } catch (err) {
      console.error("Failed to load reference image:", err);
      clearSavedPracticeState();
      setReferenceError("Failed to load reference image.");
    }
  };

  useEffect(() => {
  if (!savedState?.referenceRoundId || !savedState?.referenceImage) {
    loadReference();
  }
}, []);

  useEffect(() => {
  if (!referenceRoundId || !referenceImage) return;

  const stateToSave = {
    referenceImage,
    referenceRoundId,
    generatedImage,
    prompt,
    similarityScore,
    attemptHistory,
    showAttemptHistory,
  };

  localStorage.setItem(PRACTICE_STORAGE_KEY, JSON.stringify(stateToSave));
}, [
  referenceImage,
  referenceRoundId,
  generatedImage,
  prompt,
  similarityScore,
  attemptHistory,
  showAttemptHistory,
]);

  const handlePromptChange = (e) => {
    setPrompt(e.target.value.slice(0, 2000));
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoadingGenerated(true);
    setGeneratedImage(null);
    setSimilarityScore(null);
    setError(null);

    try {
      const result = await submitPrompt({
        round_id: referenceRoundId,
        user_prompt: prompt.trim(),
      });

      setGeneratedImage(result.data.generated_image_url);
      setSimilarityScore(Number(result.data.similarity_score));
      setAttemptHistory((prev) => [
        ...prev,
        {
          prompt: prompt.trim(),
          generatedImageUrl: result.data.generated_image_url,
          similarityScore: Number(result.data.similarity_score),
          submittedAt: Date.now(),
        },
      ]);

    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to generate image.");
    } finally {
      setLoadingGenerated(false);
    }
  };

  const handleTryAgain = () => {
    setPrompt("");
    setGeneratedImage(null);
    setSimilarityScore(null);
    setError(null);
  };

  const handleNewRound = async () => {
    await loadReference(); // starts a completely new round
  };

  const hasResult = similarityScore !== null;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Practice Mode</h1>

      {/* Errors */}
      <ErrorBanner
        message={referenceError}
        onClose={() => setReferenceError(null)}
      />
      <ErrorBanner message={error} onClose={() => setError(null)} />

      {/* Images */}
      <div className={styles.imagesRow}>
        {/* Reference */}
        <div className={styles.imageBundle}>
          <div className={styles.label}>Reference Image</div>
          <div className={styles.imageWrapper}>
            {referenceImage ? (
              <img src={referenceImage} alt="Reference" />
            ) : referenceError ? (
              <span className={styles.placeholder}>
                <span className={styles.emoji}>❌</span>
                <span>{referenceError}</span>
              </span>
            ) : (
              <span className={styles.placeholder}>
                <div className={styles.spinner}></div>
                <span>Loading reference...</span>
              </span>
            )}
          </div>
        </div>

        {/* Generated */}
        <div className={styles.imageBundle}>
          <div className={styles.label}>Your Generated Image</div>
          <div className={styles.imageWrapper}>
            {loadingGenerated ? (
              <span className={styles.placeholder}>
                <div className={styles.spinner}></div>
                <span>Generating...</span>
              </span>
            ) : generatedImage ? (
              <img src={generatedImage} alt="Generated" />
            ) : (
              <span className={styles.placeholder}>
                <span className={styles.emoji}>✨</span>
                <span>Your image will appear here.</span>
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Prompt */}
      <div className={styles.promptSection}>
        <label className={styles.promptLabel}>Your Prompt</label>

        <textarea
          className={styles.promptInput}
          value={prompt}
          onChange={handlePromptChange}
          placeholder="Describe what you want the AI to generate..."
          disabled={loadingGenerated || hasResult}
        />

        <div className={styles.promptControls}>
          <button
            onClick={handleGenerate}
            className={styles.generateButton}
            disabled={!prompt.trim() || loadingGenerated || hasResult}
          >
            Generate Image
          </button>

          <span className={styles.charCounter}>{prompt.length} / 2000</span>
        </div>
      </div>

      {/* Result + Try Again + New Round */}
      {hasResult && (
        <>
          <div className={styles.scoreRow}>
            <span className={styles.scoreLabel}>Similarity Score:</span>
            <span className={styles.scorePill}>
              {similarityScore.toFixed(1)} / 100
            </span>
          </div>

          <div className={styles.resultButtons}>
            <button onClick={handleTryAgain} className={styles.tryAgainButton}>
              Try Again
            </button>
            <button onClick={handleNewRound} className={styles.newRoundButton}>
              New Round
            </button>
          </div>
        </>
      )}
       {attemptHistory.length > 0 && (
  <div className={styles.attemptHistorySection}>
    <button
      type="button"
      className={styles.attemptHistoryToggle}
      onClick={() => setShowAttemptHistory((prev) => !prev)}
    >
      {showAttemptHistory
        ? `Hide Previous Attempts (${attemptHistory.length})`
        : `Show Previous Attempts (${attemptHistory.length})`}
    </button>

    {showAttemptHistory && (
      <div className={styles.attemptHistoryList}>
        {attemptHistory.map((attempt, index) => (
          <div key={`${attempt.submittedAt}-${index}`} className={styles.attemptCard}>
            <div className={styles.attemptHeader}>
              <span className={styles.attemptTitle}>
                Attempt {index + 1}
              </span>
              <span className={styles.attemptScore}>
                {attempt.similarityScore.toFixed(1)} / 100
              </span>
            </div>

            <div className={styles.attemptPrompt}>
              <strong>Prompt:</strong> {attempt.prompt}
            </div>

            <div className={styles.attemptImageWrapper}>
              <img
                src={attempt.generatedImageUrl}
                alt={`Attempt ${index + 1}`}
                className={styles.attemptImage}
              />
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
)}
    </div>
  );
}
