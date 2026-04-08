import { useNavigate } from "react-router-dom";
import PlatformCard from "./PlatformCard";
import styles from "./HeroPlatform.module.css";

export default function HeroPlatform() {
  const navigate = useNavigate();

  return (
    <PlatformCard className={styles.heroCard}>
      <div className={styles.grassTop}></div>

      <div className={styles.content}>
        <p className={styles.kicker}>PromptCraft</p>

        <h1 className={styles.title}>
          Recreate the image. Master the prompt.
        </h1>

        <p className={styles.subtitle}>
          A creative AI game where your prompt determines the outcome.
        </p>

        <div className={styles.actions}>
          <button
            className={styles.primaryButton}
            onClick={() => navigate("/practice")}
          >
            Start Game
          </button>

          <button
            className={styles.secondaryButton}
            onClick={() => navigate("/how-to-play")}
          >
            How to Play
          </button>
        </div>
      </div>
    </PlatformCard>
  );
}