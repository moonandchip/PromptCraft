import { useEffect, useState } from "react";
import { getStats } from "../../api";
import styles from "./ProgressPage.module.css";

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

  if (loading) return <div className={styles.message}>Loading stats...</div>;
  if (error) return <div className={styles.message}>{error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Progress</h1>
      <div className={styles.stat}>
        <span>Rounds Played:</span>
        <span>{stats.total_rounds}</span>
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
  );
}
