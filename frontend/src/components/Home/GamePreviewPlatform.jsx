import PlatformCard from "./PlatformCard";
import styles from "./GamePreviewPlatform.module.css";

export default function GamePreviewPlatform() {
  return (
    <PlatformCard className={styles.previewCard}>
      <div className={styles.grassTop}></div>

      <div className={styles.headerRow}>
        <h2 className={styles.title}>How a Round Works</h2>
        <span className={styles.badge}>Preview</span>
      </div>

      <div className={styles.previewGrid}>
        <div className={styles.imagePanel}>
          <p className={styles.label}>Target Image</p>
          <div className={styles.imageMock}>
            <img
              src="/reference_images/promptcraft-icon.png"
              alt="Target preview"
              className={styles.previewImage}
            />
          </div>
        </div>

        <div className={styles.promptPanel}>
          <p className={styles.label}>Your Prompt</p>

          <div className={styles.inputMock}>
            A simple pixel art image of a framed landscape with green mountains, a blue sky, 
            and a small sun, with a speech bubble and sparkles, minimal composition, 
            clean retro 8-bit style, centered
            
          </div>

          <button className={styles.generateButton} type="button">
            Generate
          </button>

          <div className={styles.resultBox}>
            <p className={styles.resultText}>Match Score</p>
            <h3 className={styles.score}>82%</h3>
            <p className={styles.resultSubtext}>
              Try adjusting the setting, lighting, and background details.
            </p>
          </div>
        </div>
      </div>
    </PlatformCard>
  );
}