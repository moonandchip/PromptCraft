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

const CHART_WIDTH = 640;
const CHART_HEIGHT = 240;
const CHART_PADDING = 28;

function formatScore(score) {
  return Number(score ?? 0).toFixed(1);
}

function shouldShowXAxisLabel(index, total) {
  if (total <= 6) {
    return true;
  }

  if (index === 0 || index === total - 1) {
    return true;
  }

  const interval = Math.ceil(total / 5);
  return index % interval === 0;
}

function buildChart(points) {
  if (!points.length) {
    return {
      linePath: "",
      areaPath: "",
      chartPoints: [],
      yAxisTicks: [],
    };
  }

  const innerWidth = CHART_WIDTH - CHART_PADDING * 2;
  const innerHeight = CHART_HEIGHT - CHART_PADDING * 2;
  const maxScore = 100;
  const minScore = 0;

  const chartPoints = points.map((point, index) => {
    const x =
      points.length === 1
        ? CHART_WIDTH / 2
        : CHART_PADDING + (index / (points.length - 1)) * innerWidth;
    const normalizedScore = (point.score - minScore) / (maxScore - minScore || 1);
    const y = CHART_HEIGHT - CHART_PADDING - normalizedScore * innerHeight;

    return {
      ...point,
      x,
      y,
    };
  });

  const linePath = chartPoints
    .map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`)
    .join(" ");

  const areaPath = [
    `M ${chartPoints[0].x} ${CHART_HEIGHT - CHART_PADDING}`,
    ...chartPoints.map((point) => `L ${point.x} ${point.y}`),
    `L ${chartPoints[chartPoints.length - 1].x} ${CHART_HEIGHT - CHART_PADDING}`,
    "Z",
  ].join(" ");

  const yAxisTicks = [0, 25, 50, 75, 100].map((value) => ({
    value,
    y:
      CHART_HEIGHT -
      CHART_PADDING -
      ((value - minScore) / (maxScore - minScore || 1)) * innerHeight,
  }));

  return {
    linePath,
    areaPath,
    chartPoints,
    yAxisTicks,
  };
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

  const scoreTrend = (stats?.recent_attempts ?? [])
    .slice()
    .reverse()
    .map((attempt, index) => ({
      id: `${attempt.created_at ?? "attempt"}-${attempt.attempt_number}-${index}`,
      label: `Attempt ${index + 1}`,
      score: Number(attempt.similarity_score ?? 0),
      createdAt: attempt.created_at,
    }));

  const { linePath, areaPath, chartPoints, yAxisTicks } = buildChart(scoreTrend);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Progress</h1>

      <ErrorBanner message={error} onClose={() => setError(null)} />

            {stats && (
        <>
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
              <span>{formatScore(stats.average_score)}</span>
            </div>
            <div className={styles.stat}>
              <span>Best Score:</span>
              <span>{formatScore(stats.best_score)}</span>
            </div>
          </div>

          <section className={styles.chartSection} aria-labelledby="score-chart-title">
            <div className={styles.chartHeader}>
              <div>
                <h2 id="score-chart-title" className={styles.chartTitle}>
                  Score Trend
                </h2>
              </div>
            </div>

            {scoreTrend.length > 0 ? (
              <>
                <div className={styles.chartWrapper}>
                  <svg
                    viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`}
                    className={styles.chart}
                    role="img"
                    aria-label="Line chart showing score improvement over time"
                  >
                    {yAxisTicks.map((tick) => (
                      <g key={tick.value}>
                        <line
                          x1={CHART_PADDING}
                          x2={CHART_WIDTH - CHART_PADDING}
                          y1={tick.y}
                          y2={tick.y}
                          className={styles.gridLine}
                        />
                        <text
                          x={CHART_PADDING - 10}
                          y={tick.y + 4}
                          className={styles.axisLabel}
                        >
                          {tick.value}
                        </text>
                      </g>
                    ))}

                    <path d={areaPath} className={styles.areaPath} />
                    <path d={linePath} className={styles.linePath} />

                    {chartPoints.map((point) => (
                      <g key={point.id}>
                        <circle
                          cx={point.x}
                          cy={point.y}
                          r="5"
                          className={styles.dataPoint}
                        />
                        <title>{`${point.label}: ${formatScore(point.score)} / 100`}</title>
                      </g>
                    ))}
                  </svg>
                </div>

                <div className={styles.xAxisLabels} aria-hidden="true">
                  {scoreTrend.map((point, index) => (
                    <span key={point.id} className={styles.xAxisLabel}>
                      {shouldShowXAxisLabel(index, scoreTrend.length) ? index + 1 : ""}
                    </span>
                  ))}
                </div>

                <div className={styles.chartFooter}>
                  <span>Earlier attempts</span>
                  <span>Later attempts</span>
                </div>
              </>
            ) : (
              <div className={styles.emptyChart}>
                Complete a round to start tracking your scores over time.
              </div>
            )}
          </section>
        </>
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
