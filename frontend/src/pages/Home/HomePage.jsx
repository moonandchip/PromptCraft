import styles from "./HomePage.module.css";
import HeroPlatform from "../../components/Home/HeroPlatform";
import GamePreviewPlatform from "../../components/Home/GamePreviewPlatform";
import PlatformCard from "../../components/Home/PlatformCard";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getChallengeLeaderboard } from "../../api";

export default function HomePage() {
  const navigate = useNavigate();
  const [topEntries, setTopEntries] = useState([]);
  const [leaderboardLoaded, setLeaderboardLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await getChallengeLeaderboard(3);
        if (!cancelled) setTopEntries(data.entries ?? []);
      } catch {
        // Leaderboard failure shouldn't break the home page; just hide the section.
      } finally {
        if (!cancelled) setLeaderboardLoaded(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main className={styles.page}>
      <div className={styles.skyBackground}>
        <div className={styles.pixelDecor1}></div>
        <div className={styles.pixelDecor2}></div>
        <div className={styles.pixelDecor3}></div>
        <div className={styles.pixelDecor4}></div>

        <section className={styles.heroSection}>
          <HeroPlatform />
        </section>

        <section className={styles.previewSection}>
          <GamePreviewPlatform />
        </section>

        <section className={styles.modesSection}>
          <div className={styles.modesWrapper}>
            <PlatformCard className={styles.practiceCard}>
              <div className={styles.grassTop}></div>
              <h3 className={styles.cardTitle}>Practice Mode</h3>
              <p className={styles.cardText}>
                Play unlimited rounds and keep improving your prompts.
              </p>
              <button
                className={styles.cardButton}
                onClick={() => navigate("/practice")}
              >
                Play Practice
              </button>
            </PlatformCard>

            <PlatformCard className={styles.challengeCard}>
              <div className={styles.grassTop}></div>
              <h3 className={styles.cardTitle}>Daily Challenge</h3>
              <p className={styles.cardText}>
                Compete for the best score and climb the leaderboard.
              </p>
              <button
                className={styles.cardButton}
                onClick={() => navigate("/challenge")}
              >
                View Challenge
              </button>
            </PlatformCard>

            <PlatformCard className={styles.progressCard}>
              <div className={styles.grassTop}></div>
              <h3 className={styles.cardTitle}>Progress</h3>
              <p className={styles.cardText}>
                Track your rounds, high scores, and overall growth.
              </p>
              <button
                className={styles.cardButton}
                onClick={() => navigate("/progress")}
              >
                See Progress
              </button>
            </PlatformCard>
          </div>
        </section>

        {leaderboardLoaded && topEntries.length > 0 && (
          <section className={styles.leaderboardSection}>
            <PlatformCard className={styles.leaderboardCard}>
              <div className={styles.grassTop}></div>
              <h2 className={styles.leaderboardTitle}>Top Players Today</h2>

              <div className={styles.leaderboardList}>
                {topEntries.map((entry) => (
                  <div key={entry.user_id} className={styles.leaderboardRow}>
                    <span>#{entry.rank}</span>
                    <span>{entry.display_name}</span>
                    <span>{entry.best_score.toFixed(1)}</span>
                  </div>
                ))}
              </div>
            </PlatformCard>
          </section>
        )}
      </div>
    </main>
  );
}