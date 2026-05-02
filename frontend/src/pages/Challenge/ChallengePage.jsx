import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  getChallengeLeaderboard,
  getCurrentChallenge,
  submitChallengePrompt,
} from "../../api";
import { useAuth } from "../../components/AuthContext";
import ErrorBanner from "../../components/ErrorBanner";
import { scoreFeedback } from "../../utils/scoreFeedback";
import styles from "./ChallengePage.module.css";

function resolveReferenceUrl(targetImageUrl) {
  if (!targetImageUrl) return null;
  return `/reference_images/${targetImageUrl.replace("/static/", "")}`;
}

function formatTimeRemaining(periodEnd) {
  if (!periodEnd) return "";
  const end = new Date(periodEnd).getTime();
  const diff = end - Date.now();
  if (diff <= 0) return "Resetting...";
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
}

export default function ChallengePage() {
  const { user } = useAuth();
  const [challenge, setChallenge] = useState(null);
  const [leaderboard, setLeaderboard] = useState({ entries: [] });
  const [prompt, setPrompt] = useState("");
  const [loadingChallenge, setLoadingChallenge] = useState(true);
  const [loadingLeaderboard, setLoadingLeaderboard] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [latestScore, setLatestScore] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [showFeedback, setShowFeedback] = useState(true);
  const [error, setError] = useState(null);
  const [loadError, setLoadError] = useState(null);
  const [, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoadingChallenge(true);
    setLoadingLeaderboard(true);
    setLoadError(null);

    getCurrentChallenge()
      .then((current) => {
        if (!cancelled) setChallenge(current);
      })
      .catch((err) => {
        if (!cancelled) setLoadError(err.message || "Failed to load challenge.");
      })
      .finally(() => {
        if (!cancelled) setLoadingChallenge(false);
      });

    getChallengeLeaderboard(10)
      .then((board) => {
        if (!cancelled) setLeaderboard(board);
      })
      .catch(() => {
        // Leaderboard failure shouldn't block the page; keep the existing state.
      })
      .finally(() => {
        if (!cancelled) setLoadingLeaderboard(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => setTick((t) => t + 1), 60_000);
    return () => clearInterval(interval);
  }, []);

  const referenceImage = useMemo(
    () => resolveReferenceUrl(challenge?.target_image_url),
    [challenge?.target_image_url],
  );

  const attemptsRemaining = challenge
    ? Math.max(challenge.max_attempts - challenge.attempts_used, 0)
    : 0;
  const limitReached = challenge ? attemptsRemaining === 0 : false;

  const handleSubmit = async () => {
    if (prompt.trim().length < 10 || submitting || limitReached) return;
    setSubmitting(true);
    setError(null);
    setGeneratedImage(null);
    setLatestScore(null);
    setFeedback([]);
    setShowFeedback(true);

    // Optimistically bump the attempts counter so the user sees feedback
    // immediately, even though the actual submit takes ~10s. Reverted on error.
    const optimisticChallenge = challenge;
    setChallenge((prev) =>
      prev
        ? { ...prev, attempts_used: Math.min(prev.attempts_used + 1, prev.max_attempts) }
        : prev,
    );

    try {
      const result = await submitChallengePrompt(prompt.trim());
      setGeneratedImage(result.generated_image_url);
      setLatestScore(Number(result.similarity_score));
      setFeedback(result.feedback || []);
      setChallenge((prev) =>
        prev
          ? {
              ...prev,
              attempts_used: result.attempts_used,
              best_score: Math.max(prev.best_score, Number(result.best_score)),
              current_streak: result.current_streak ?? prev.current_streak,
              longest_streak: result.longest_streak ?? prev.longest_streak,
            }
          : prev,
      );
      // Refetch on the last attempt so target_prompt comes through from the backend.
      if (result.attempts_remaining === 0) {
        try {
          const refreshed = await getCurrentChallenge();
          setChallenge(refreshed);
        } catch {
          // Non-fatal: the user still sees the result; just no target_prompt reveal.
        }
      }
      setLoadingLeaderboard(true);
      try {
        const board = await getChallengeLeaderboard(10);
        setLeaderboard(board);
      } finally {
        setLoadingLeaderboard(false);
      }
    } catch (err) {
      // Roll back the optimistic counter bump.
      setChallenge(optimisticChallenge);
      setError(err.message || "Failed to submit challenge prompt.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingChallenge) {
    return (
      <main className={styles.page}>
        <div className={styles.backgroundDecor1}></div>
        <div className={styles.backgroundDecor2}></div>
        <div className={styles.backgroundDecor3}></div>
        <div className={styles.container}>
          <h1 className={styles.title}>Daily Challenge</h1>
          <div className={styles.loadingBox}>
            <div className={styles.spinner}></div>
            <span>Loading today&apos;s challenge...</span>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className={styles.page}>
      <div className={styles.backgroundDecor1}></div>
      <div className={styles.backgroundDecor2}></div>
      <div className={styles.backgroundDecor3}></div>
      <div className={styles.container}>
        <h1 className={styles.title}>Daily Challenge</h1>

        <ErrorBanner message={loadError} onClose={() => setLoadError(null)} />
        <ErrorBanner message={error} onClose={() => setError(null)} />

      {challenge && (
        <div className={styles.headerCard}>
          <div className={styles.headerRow}>
            <div className={styles.headerCell}>
              <span className={styles.headerLabel}>Today&apos;s Round</span>
              <span className={styles.headerValue}>{challenge.title}</span>
            </div>
            <div className={styles.headerCell}>
              <span className={styles.headerLabel}>Difficulty</span>
              <span className={`${styles.headerValue} ${styles[`difficulty-${challenge.difficulty}`]}`}>
                {challenge.difficulty}
              </span>
            </div>
            <div className={styles.headerCell}>
              <span className={styles.headerLabel}>Attempts Used</span>
              <span className={styles.headerValue}>
                {challenge.attempts_used} / {challenge.max_attempts}
              </span>
            </div>
            <div className={styles.headerCell}>
              <span className={styles.headerLabel}>Streak</span>
              <span className={styles.headerValue}>
                🔥 {challenge.current_streak ?? 0}
                {challenge.longest_streak > (challenge.current_streak ?? 0) && (
                  <span className={styles.streakBest}>
                    {" "}(best {challenge.longest_streak})
                  </span>
                )}
              </span>
            </div>
            <div className={styles.headerCell}>
              <span className={styles.headerLabel}>Resets In</span>
              <span className={styles.headerValue}>
                {formatTimeRemaining(challenge.period_end)}
              </span>
            </div>
          </div>
          <div className={styles.attemptRules}>
            You get <strong>{challenge.max_attempts}</strong> attempts per day.
            Best score wins.{" "}
            <Link to="/challenge/archive" className={styles.archiveLink}>
              View archive →
            </Link>
          </div>
        </div>
      )}

      <div className={styles.imagesRow}>
        <div className={styles.imageBundle}>
          <div className={styles.label}>Reference Image</div>
          <div className={styles.imageWrapper}>
            {referenceImage ? (
              <img src={referenceImage} alt="Reference" />
            ) : (
              <span className={styles.placeholder}>
                <span className={styles.emoji}>❌</span>
                <span>Reference unavailable.</span>
              </span>
            )}
          </div>
        </div>

        <div className={styles.imageBundle}>
          <div className={styles.label}>Your Generated Image</div>
          <div className={styles.imageWrapper}>
            {submitting ? (
              <span className={styles.placeholder}>
                <div className={styles.spinner}></div>
                <span>Generating your image...</span>
                <span className={styles.placeholderHint}>
                  This can take up to a minute.
                </span>
              </span>
            ) : generatedImage ? (
              <img src={generatedImage} alt="Generated" />
            ) : (
              <span className={styles.placeholder}>
                <span className={styles.emoji}>✨</span>
                <span>Submit a prompt to play.</span>
              </span>
            )}
          </div>
        </div>
      </div>

      <div className={styles.promptSection}>
        <label className={styles.promptLabel}>Your Prompt</label>
        <textarea
          className={styles.promptInput}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value.slice(0, 2000))}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder={
            limitReached
              ? "You've used all your attempts for today. Come back tomorrow!"
              : "Describe what you want the AI to generate... (Ctrl+Enter to submit)"
          }
          disabled={submitting || limitReached}
        />
        <div className={styles.promptControls}>
          <button
            onClick={handleSubmit}
            className={styles.generateButton}
            disabled={prompt.trim().length < 10 || submitting || limitReached}
          >
            {limitReached ? "Limit Reached" : "Submit Attempt"}
          </button>
          <span className={styles.charCounter}>
            {prompt.length < 10 && prompt.length > 0
              ? `${prompt.length} / 2000 (min 10)`
              : `${prompt.length} / 2000`}
          </span>
        </div>
      </div>

      {latestScore !== null && (
        <div className={styles.scoreCard}>
          <div className={styles.scoreRow}>
            <span className={styles.scoreLabel}>Score:</span>
            <span className={styles.scorePill}>
              {latestScore.toFixed(1)} / 100
            </span>
          </div>
          <p className={styles.feedback}>{scoreFeedback(latestScore)}</p>
        </div>
      )}

      {feedback.length > 0 && (
        <div className={styles.tipsSection}>
          <div className={styles.tipsHeader}>
            <h3 className={styles.tipsTitle}>Hints</h3>
            <button
              type="button"
              className={styles.tipsToggle}
              onClick={() => setShowFeedback((prev) => !prev)}
            >
              {showFeedback ? "Hide" : "Show"}
            </button>
          </div>
          {showFeedback && (
            <ul className={styles.tipsList}>
              {feedback.map((tip) => (
                <li key={tip} className={styles.tipItem}>{tip}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {limitReached && challenge?.target_prompt && (
        <div className={styles.revealCard}>
          <h3 className={styles.revealTitle}>The prompt behind today&apos;s image</h3>
          <p className={styles.revealPrompt}>{challenge.target_prompt}</p>
          <p className={styles.revealHint}>
            Compare it with your prompts to see what landed and what missed.
            Come back tomorrow for a new round.
          </p>
        </div>
      )}

      <div className={styles.leaderboardSection}>
        <h2 className={styles.leaderboardTitle}>Leaderboard</h2>
        {loadingLeaderboard ? (
          <div className={styles.emptyLeaderboard}>
            <div className={styles.spinner}></div>
            <span>Loading leaderboard...</span>
          </div>
        ) : leaderboard.entries.length === 0 ? (
          <div className={styles.emptyLeaderboard}>
            No scores yet today, be the first!
          </div>
        ) : (
          <ol className={styles.leaderboardList}>
            {leaderboard.entries.map((entry) => {
              const isMe = user?.id === entry.user_id;
              return (
                <li
                  key={entry.user_id}
                  className={`${styles.leaderboardRow} ${isMe ? styles.leaderboardMe : ""}`}
                >
                  <span className={styles.rank}>#{entry.rank}</span>
                  <span className={styles.player}>
                    {entry.display_name}
                    {isMe && <span className={styles.youTag}> (you)</span>}
                  </span>
                  <span className={styles.attemptsCell}>
                    {entry.attempts_used} attempts
                  </span>
                  <span className={styles.score}>
                    {entry.best_score.toFixed(1)}
                  </span>
                </li>
              );
            })}
          </ol>
        )}
      </div>
      </div>
    </main>
  );
}
