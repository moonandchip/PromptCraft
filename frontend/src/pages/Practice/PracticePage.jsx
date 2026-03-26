import { useEffect, useState } from "react";
import { startRound, submitPrompt } from "../../api";
import { getToken } from "../../auth";
import styles from "./PracticePage.module.css";

const TEST_ROUND_ID = "ancient-temple";

export default function PracticePage() {
  const [referenceImage, setReferenceImage] = useState(null);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [loadingGenerated, setLoadingGenerated] = useState(false);
  const [similarityScore, setSimilarityScore] = useState(null);
  const [error, setError] = useState(null);
  const [referenceError, setReferenceError] = useState(null);

  useEffect(() => {
    async function loadReference() {
      try {
        const data = await startRound();
        setReferenceImage(data.target_image_url);
      } catch (err) {
        console.error("Failed to load reference image:", err);
        setReferenceError("Failed to load reference image.");
      }
    }
    loadReference();
  }, []);

  const handlePromptChange = (e) => setPrompt(e.target.value.slice(0, 2000));

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoadingGenerated(true);
    setGeneratedImage(null);
    setSimilarityScore(null);
    setError(null);

    try {
      const result = await submitPrompt(
        { round_id: TEST_ROUND_ID, user_prompt: prompt.trim() },
        getToken(),
      );
      setGeneratedImage(result.data.generated_image_url);
      setSimilarityScore(Number(result.data.similarity_score));
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to generate image.");
    } finally {
      setLoadingGenerated(false);
    }
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Practice Mode</h1>

      {/* Images Row */}
      <div className={styles.imagesRow}>
        {/* Reference Image Bundle */}
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
                <span className={styles.emoji}>🖼️</span>
                <span>Loading reference...</span>
              </span>
            )}
          </div>
        </div>

        {/* Generated Image Bundle */}
        <div className={styles.imageBundle}>
          <div className={styles.label}>Your Generated Image</div>
          <div className={styles.imageWrapper}>
            {loadingGenerated ? (
              <span className={styles.placeholder}>
                <span className={styles.emoji}>⏳</span>
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

      {/* Prompt Section */}
      <div className={styles.promptSection}>
        <label className={styles.promptLabel}>Your Prompt</label>
        <textarea
          className={styles.promptInput}
          value={prompt}
          onChange={handlePromptChange}
          placeholder="Describe what you want the AI to generate..."
          disabled={loadingGenerated}
        />
        <div className={styles.promptControls}>
          <button
            onClick={handleGenerate}
            className={styles.generateButton}
            disabled={!prompt.trim() || loadingGenerated}
          >
            Generate Image
          </button>
          <span className={styles.charCounter}>{prompt.length} / 2000</span>
        </div>
      </div>

      {error && <div className={styles.errorBanner}>{error}</div>}

      {similarityScore !== null && (
        <div className={styles.scoreRow}>
          <span className={styles.scoreLabel}>Similarity Score:</span>
          <span className={styles.scorePill}>
            {similarityScore.toFixed(1)} / 100
          </span>
        </div>
      )}
    </div>
  );
}
