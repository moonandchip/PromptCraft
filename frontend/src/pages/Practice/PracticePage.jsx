import { useEffect, useState } from "react";
import { startRound, submitPrompt } from "../../api";
import styles from "./PracticePage.module.css";
import ErrorBanner from "../../components/ErrorBanner";

export default function PracticePage() {
  const [referenceImage, setReferenceImage] = useState(null);
  const [referenceRoundId, setReferenceRoundId] = useState(null);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [loadingGenerated, setLoadingGenerated] = useState(false);
  const [similarityScore, setSimilarityScore] = useState(null);
  const [error, setError] = useState(null);
  const [referenceError, setReferenceError] = useState(null);

  const loadReference = async () => {
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
    } catch (err) {
      console.error("Failed to load reference image:", err);
      setReferenceError("Failed to load reference image.");
    }
  };

  useEffect(() => {
    loadReference();
  }, []);

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
    </div>
  );
}
