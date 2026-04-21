import { useEffect, useState } from "react";
import { getRoundAttempts, getRoundHistory, getStats } from "../../api";
import ErrorBanner from "../../components/ErrorBanner";
import styles from "./ProgressPage.module.css";

function resolveReferenceUrl(targetImageUrl) {
  if (!targetImageUrl) return null;
  return `/reference_images/${targetImageUrl.replace("/static/", "")}`;
}

function renderAttemptsPanel(isLoading, attempts, styles) {
  if (isLoading) {
    return <div className={styles.attemptsLoading}>Loading attempts...</div>;
  }
  if (attempts.length === 0) {
    return <div className={styles.attemptsLoading}>No attempts found.</div>;
  }
  return (
    <ol className={styles.attemptsList}>
      {attempts.map((attempt) => (
        <li key={attempt.attempt_number} className={styles.attemptCard}>
          <div className={styles.attemptHeader}>
            <span>Attempt {attempt.attempt_number}</span>
            <span className={styles.attemptScore}>
              {attempt.similarity_score.toFixed(1)} / 100
            </span>
          </div>
          <div className={styles.attemptPrompt}>
            <strong>Prompt:</strong> {attempt.prompt}
          </div>
          {attempt.generated_image_url && (
            <img
              src={attempt.generated_image_url}
              alt={`Attempt ${attempt.attempt_number}`}
              className={styles.attemptImage}
            />
          )}
        </li>
      ))}
    </ol>
  );
}

export default function ProgressPage() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRoundId, setExpandedRoundId] = useState(null);
  const [attemptsByRound, setAttemptsByRound] = useState({});
  const [loadingRoundId, setLoadingRoundId] = useState(null);
  const [attemptError, setAttemptError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [statsData, historyData] = await Promise.all([
          getStats(),
          getRoundHistory(),
        ]);
        if (cancelled) return;
        setStats(statsData);
        setHistory(historyData ?? []);
      } catch (err) {
        if (!cancelled) setError(err.message || "Error loading progress.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const toggleRound = async (roundId) => {
    if (expandedRoundId === roundId) {
      setExpandedRoundId(null);
      return;
    }
    setExpandedRoundId(roundId);
    if (attemptsByRound[roundId]) return;

    setLoadingRoundId(roundId);
    setAttemptError(null);
    try {
      const attempts = await getRoundAttempts(roundId);
      setAttemptsByRound((prev) => ({ ...prev, [roundId]: attempts ?? [] }));
    } catch (err) {
      setAttemptError(err.message || "Failed to load attempts for this round.");
    } finally {
      setLoadingRoundId(null);
    }
  };

  if (loading) {
    return <div className={styles.message}>Loading progress...</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Progress</h1>

      <ErrorBanner message={error} onClose={() => setError(null)} />

      {stats && (
        <div className={styles.statsBlock}>
          <div className={styles.stat}>
            <span>Rounds Played:</span>
            <span>{stats.total_rounds}</span>
          </div>
          <div className={styles.stat}>
            <span>Total Attempts:</span>
            <span>{stats.total_attempts}</span>
          </div>
          <div className={styles.stat}>
            <span>Average Score:</span>
            <span>{stats.average_score}</span>
          </div>
          <div className={styles.stat}>
            <span>Best Score:</span>
            <span>{stats.best_score}</span>
          </div>
        </div>
      )}

      <h2 className={styles.subtitle}>Round History</h2>
      <ErrorBanner message={attemptError} onClose={() => setAttemptError(null)} />

      {history.length === 0 ? (
        <div className={styles.emptyState}>
          You haven&apos;t played any rounds yet. Head to Practice to start.
        </div>
      ) : (
        <ul className={styles.historyList}>
          {history.map((round) => {
            const isExpanded = expandedRoundId === round.round_id;
            const attempts = attemptsByRound[round.round_id] ?? [];
            const isLoadingAttempts = loadingRoundId === round.round_id;
            return (
              <li key={round.round_id} className={styles.historyItem}>
                <button
                  type="button"
                  className={styles.historyHeader}
                  onClick={() => toggleRound(round.round_id)}
                  aria-expanded={isExpanded}
                >
                  <img
                    src={resolveReferenceUrl(round.target_image_url)}
                    alt={round.title}
                    className={styles.thumb}
                  />
                  <div className={styles.historyMeta}>
                    <span className={styles.roundTitle}>{round.title}</span>
                    <span className={`${styles.difficultyTag} ${styles[`difficulty-${round.difficulty}`]}`}>
                      {round.difficulty}
                    </span>
                  </div>
                  <div className={styles.historyStats}>
                    <span className={styles.historyBest}>
                      Best: {round.best_score.toFixed(1)}
                    </span>
                    <span className={styles.historyCount}>
                      {round.attempt_count === 1
                        ? "1 attempt"
                        : `${round.attempt_count} attempts`}
                    </span>
                  </div>
                  <span className={styles.chevron}>{isExpanded ? "▾" : "▸"}</span>
                </button>

                {isExpanded && (
                  <div className={styles.attemptsPanel}>
                    {renderAttemptsPanel(isLoadingAttempts, attempts, styles)}
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
