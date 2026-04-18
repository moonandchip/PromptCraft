import { useEffect, useState } from "react";
import { getStats } from "../../api";
import styles from "./ProgressPage.module.css";
import ErrorBanner from "../../components/ErrorBanner";

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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getStats();
        if (!data) throw new Error("Failed to load stats.");
        setStats(data);
      } catch (err) {
        setError(err.message || "Error loading stats.");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className={styles.message}>Loading stats...</div>;
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

      {/* Error Banner (does NOT block page) */}
      <ErrorBanner message={error} onClose={() => setError(null)} />

      {stats && (
        <>
          <div className={styles.stat}>
            <span>Rounds Played:</span>
            <span>{stats.total_rounds}</span>
          </div>
          <div className={styles.stat}>
            <span>Average Score:</span>
            <span>{formatScore(stats.average_score)}</span>
          </div>
          <div className={styles.stat}>
            <span>Total Attempts:</span>
            <span>{stats.total_attempts}</span>
          </div>
          <div className={styles.stat}>
            <span>Best Score:</span>
            <span>{formatScore(stats.best_score)}</span>
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
    </div>
  );
}
