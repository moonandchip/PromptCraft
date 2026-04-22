import { useEffect, useState } from "react";
import { startRound, submitPrompt } from "../../api";
import ErrorBanner from "../../components/ErrorBanner";
import styles from "./PracticePage.module.css";

const PRACTICE_STORAGE_KEY = "promptcraft_practice_round_state";
const DIFFICULTIES = ["any", "easy", "medium", "hard"];
const DIFFICULTY_STORAGE_KEY = "promptcraft_practice_difficulty";

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

function loadSavedDifficulty() {
  const value = localStorage.getItem(DIFFICULTY_STORAGE_KEY);
  return DIFFICULTIES.includes(value) ? value : "any";
}

export default function PracticePage() {
  const savedState = loadSavedPracticeState();

  const [referenceImage, setReferenceImage] = useState(savedState?.referenceImage ?? null);
  const [referenceRoundId, setReferenceRoundId] = useState(savedState?.referenceRoundId ?? null);
  const [roundTitle, setRoundTitle] = useState(savedState?.roundTitle ?? null);
  const [roundDifficulty, setRoundDifficulty] = useState(savedState?.roundDifficulty ?? null);
  const [targetPrompt, setTargetPrompt] = useState(savedState?.targetPrompt ?? null);
  const [generatedImage, setGeneratedImage] = useState(savedState?.generatedImage ?? null);
  const [prompt, setPrompt] = useState(savedState?.prompt ?? "");
  const [loadingGenerated, setLoadingGenerated] = useState(false);
  const [similarityScore, setSimilarityScore] = useState(savedState?.similarityScore ?? null);
  const [error, setError] = useState(null);
  const [referenceError, setReferenceError] = useState(null);
  const [attemptHistory, setAttemptHistory] = useState(savedState?.attemptHistory ?? []);
  const [showAttemptHistory, setShowAttemptHistory] = useState(savedState?.showAttemptHistory ?? false);
  const [feedback, setFeedback] = useState(savedState?.feedback ?? []);
  const [showFeedback, setShowFeedback] = useState(savedState?.showFeedback ?? true);
  const [difficulty, setDifficulty] = useState(loadSavedDifficulty);

  const loadReference = async (chosenDifficulty = difficulty) => {
    clearSavedPracticeState();

    try {
      const data = await startRound({
        difficulty: chosenDifficulty === "any" ? undefined : chosenDifficulty,
      });

      setReferenceImage(
        `/reference_images/${data.target_image_url.replace("/static/", "")}`,
      );
      setReferenceRoundId(data.round_id);
      setRoundTitle(data.title ?? null);
      setRoundDifficulty(data.difficulty ?? null);
      setTargetPrompt(data.target_prompt ?? null);
      setGeneratedImage(null);
      setSimilarityScore(null);
      setPrompt("");
      setError(null);
      setReferenceError(null);
      setAttemptHistory([]);
      setShowAttemptHistory(false);
      setFeedback([]);
      setShowFeedback(true);
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!referenceRoundId || !referenceImage) return;

    const stateToSave = {
      referenceImage,
      referenceRoundId,
      roundTitle,
      roundDifficulty,
      targetPrompt,
      generatedImage,
      prompt,
      similarityScore,
      attemptHistory,
      showAttemptHistory,
      feedback,
      showFeedback,
    };

    localStorage.setItem(PRACTICE_STORAGE_KEY, JSON.stringify(stateToSave));
  }, [
    referenceImage,
    referenceRoundId,
    roundTitle,
    roundDifficulty,
    targetPrompt,
    generatedImage,
    prompt,
    similarityScore,
    attemptHistory,
    showAttemptHistory,
    feedback,
    showFeedback,
  ]);

  const handlePromptChange = (e) => {
    setPrompt(e.target.value.slice(0, 2000));
  };

  const handleDifficultyChange = (e) => {
    const value = e.target.value;
    setDifficulty(value);
    localStorage.setItem(DIFFICULTY_STORAGE_KEY, value);
    loadReference(value);
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

      const score = Number(result.data.similarity_score);

      setGeneratedImage(result.data.generated_image_url);
      setSimilarityScore(score);
      setFeedback(result.data.feedback || []);
      setShowFeedback(true);

      setAttemptHistory((prev) => [
        ...prev,
        {
          prompt: prompt.trim(),
          generatedImageUrl: result.data.generated_image_url,
          similarityScore: score,
          feedback: result.data.feedback || [],
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
    setFeedback([]);
    setShowFeedback(true);
    setError(null);
  };

  const handleNewRound = async () => {
    await loadReference();
  };

  const hasResult = similarityScore !== null;
  const hasAnyAttempt = attemptHistory.length > 0;

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Practice Mode</h1>

      <div className={styles.controlsRow}>
        <label className={styles.controlLabel} htmlFor="practice-difficulty-select">
          Difficulty
        </label>
        <select
          id="practice-difficulty-select"
          className={styles.difficultySelect}
          value={difficulty}
          onChange={handleDifficultyChange}
          disabled={loadingGenerated}
        >
          <option value="any">Any</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        {roundTitle && (
          <div className={styles.roundBadge}>
            <span className={styles.badgeTitle}>{roundTitle}</span>
            {roundDifficulty && (
              <span className={`${styles.badgeDifficulty} ${styles[`difficulty-${roundDifficulty}`]}`}>
                {roundDifficulty}
              </span>
            )}
          </div>
        )}
      </div>

      <ErrorBanner
        message={referenceError}
        onClose={() => setReferenceError(null)}
      />
      <ErrorBanner message={error} onClose={() => setError(null)} />

      <div className={styles.imagesRow}>
        <div className={styles.imageBundle}>
          <div className={styles.label}>Reference Image</div>
          <div className={styles.imageWrapper}>
            {renderReferenceImage(referenceImage, referenceError, styles)}
          </div>
        </div>

        <div className={styles.imageBundle}>
          <div className={styles.label}>Your Generated Image</div>
          <div className={styles.imageWrapper}>
            {renderGeneratedImage(loadingGenerated, generatedImage, styles)}
          </div>
        </div>
      </div>

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

      {hasResult && (
        <>
          <div className={styles.scoreRow}>
            <span className={styles.scoreLabel}>Similarity Score:</span>
            <span className={styles.scorePill}>
              {similarityScore.toFixed(1)} / 100
            </span>
          </div>

          {feedback.length > 0 && (
            <div className={styles.feedbackSection}>
              <div className={styles.feedbackHeader}>
                <h3 className={styles.feedbackTitle}>Hints</h3>
                <button
                  type="button"
                  className={styles.feedbackToggle}
                  onClick={() => setShowFeedback((prev) => !prev)}
                >
                  {showFeedback ? "Hide Feedback" : "Show Hints"}
                </button>
              </div>

              {showFeedback && (
                <ul className={styles.feedbackList}>
                  {feedback.map((tip, i) => (
                    <li key={i} className={styles.feedbackItem}>
                      {tip}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

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

      {hasAnyAttempt && (
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
                <div key={attempt.submittedAt} className={styles.attemptCard}>
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

function renderReferenceImage(referenceImage, referenceError, styles) {
  if (referenceImage) {
    return <img src={referenceImage} alt="Reference" />;
  }
  if (referenceError) {
    return (
      <span className={styles.placeholder}>
        <span className={styles.emoji}>❌</span>
        <span>{referenceError}</span>
      </span>
    );
  }
  return (
    <span className={styles.placeholder}>
      <div className={styles.spinner}></div>
      <span>Loading reference...</span>
    </span>
  );
}

function renderGeneratedImage(loadingGenerated, generatedImage, styles) {
  if (loadingGenerated) {
    return (
      <span className={styles.placeholder}>
        <div className={styles.spinner}></div>
        <span>Generating...</span>
      </span>
    );
  }
  if (generatedImage) {
    return <img src={generatedImage} alt="Generated" />;
  }
  return (
    <span className={styles.placeholder}>
      <span className={styles.emoji}>✨</span>
      <span>Your image will appear here.</span>
    </span>
  );
}