import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getChallengeArchive } from "../../api";
import ErrorBanner from "../../components/ErrorBanner";
import styles from "./ArchivePage.module.css";

function formatDate(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

export default function ArchivePage() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await getChallengeArchive(30);
        if (!cancelled) setEntries(data.entries);
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load archive.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className={styles.page}>
      <div className={styles.backgroundDecor1}></div>
      <div className={styles.backgroundDecor2}></div>
      <div className={styles.backgroundDecor3}></div>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Challenge Archive</h1>
          <Link to="/challenge" className={styles.backLink}>
            ← Back to today&apos;s challenge
          </Link>
        </div>

        <ErrorBanner message={error} onClose={() => setError(null)} />

      {loading ? (
        <div className={styles.loadingBox}>
          <div className={styles.spinner}></div>
          <span>Loading your archive...</span>
        </div>
      ) : entries.length === 0 ? (
        <div className={styles.empty}>
          <p>No challenges in your archive yet.</p>
          <Link to="/challenge" className={styles.cta}>
            Play today&apos;s challenge →
          </Link>
        </div>
      ) : (
        <ul className={styles.list}>
          {entries.map((entry) => {
            const played = entry.attempts_used > 0;
            const referenceUrl = `/reference_images/${entry.target_image_url.replace("/static/", "")}`;
            return (
              <li key={entry.challenge_id} className={styles.row}>
                <div className={styles.thumbWrapper}>
                  <img src={referenceUrl} alt={entry.title} className={styles.thumb} />
                </div>
                <div className={styles.meta}>
                  <span className={styles.date}>{formatDate(entry.period_start)}</span>
                  <span className={styles.entryTitle}>{entry.title}</span>
                  <span className={`${styles.difficultyTag} ${styles[`difficulty-${entry.difficulty}`]}`}>
                    {entry.difficulty}
                  </span>
                </div>
                <div className={styles.stats}>
                  {played ? (
                    <>
                      <span className={styles.score}>
                        {entry.best_score.toFixed(1)} / 100
                      </span>
                      <span className={styles.attempts}>
                        {entry.attempts_used} / {entry.max_attempts} attempts
                      </span>
                    </>
                  ) : (
                    <span className={styles.notPlayed}>Not played</span>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
      </div>
    </main>
  );
}
