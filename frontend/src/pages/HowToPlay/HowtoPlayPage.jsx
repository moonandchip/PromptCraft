import { useNavigate } from "react-router-dom";
import styles from "./HowToPlayPage.module.css";

export default function HowToPlayPage() {
  const navigate = useNavigate();

  return (
    <main className={styles.page}>
      <div className={styles.backgroundDecor1}></div>
      <div className={styles.backgroundDecor2}></div>
      <div className={styles.backgroundDecor3}></div>

      <div className={styles.container}>
        <header className={styles.hero}>
          <p className={styles.kicker}>How to Play</p>
          <h1 className={styles.title}>Learn the game, then beat the image.</h1>
          <p className={styles.subtitle}>
            PromptCraft is all about writing strong prompts to recreate a target
            image as closely as possible.
          </p>

          <div className={styles.actions}>
            <button
              className={styles.primaryButton}
              onClick={() => navigate("/practice")}
            >
              Start Playing
            </button>
            <button
              className={styles.secondaryButton}
              onClick={() => navigate("/")}
            >
              Back Home
            </button>
          </div>
        </header>

        <section className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>What is PromptCraft?</h2>
          <p className={styles.sectionText}>
            PromptCraft is a game where you try to recreate a given image by
            writing the best possible text prompt. The closer your generated
            image matches the target, the better your score.
          </p>
        </section>

        <section className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>How a Round Works</h2>

          <div className={styles.stepsGrid}>
            <div className={styles.stepCard}>
              <span className={styles.stepNumber}>1</span>
              <h3 className={styles.stepTitle}>Look at the target image</h3>
              <p className={styles.stepText}>
                Study the subject, colors, lighting, background, and overall
                style.
              </p>
            </div>

            <div className={styles.stepCard}>
              <span className={styles.stepNumber}>2</span>
              <h3 className={styles.stepTitle}>Write your prompt</h3>
              <p className={styles.stepText}>
                Describe the image as clearly and specifically as you can.
              </p>
            </div>

            <div className={styles.stepCard}>
              <span className={styles.stepNumber}>3</span>
              <h3 className={styles.stepTitle}>Generate your result</h3>
              <p className={styles.stepText}>
                Submit your prompt and see what image the system creates.
              </p>
            </div>

            <div className={styles.stepCard}>
              <span className={styles.stepNumber}>4</span>
              <h3 className={styles.stepTitle}>Check your score</h3>
              <p className={styles.stepText}>
                Your result is compared to the target image and scored based on
                similarity.
              </p>
            </div>

            <div className={styles.stepCard}>
              <span className={styles.stepNumber}>5</span>
              <h3 className={styles.stepTitle}>Improve and try again</h3>
              <p className={styles.stepText}>
                Adjust your wording, add better details, and keep experimenting.
              </p>
            </div>
          </div>
        </section>

        <section className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>Game Modes</h2>

          <div className={styles.modeList}>
            <div className={styles.modeItem}>
              <h3 className={styles.modeTitle}>Practice Mode</h3>
              <p className={styles.modeText}>
                Play unlimited rounds and use repeated attempts to sharpen your
                prompt writing.
              </p>
            </div>

            <div className={styles.modeItem}>
              <h3 className={styles.modeTitle}>Weekly Challenge</h3>
              <p className={styles.modeText}>
                Compete against other players and try to reach the top of the
                leaderboard.
              </p>
            </div>

            <div className={styles.modeItem}>
              <h3 className={styles.modeTitle}>Progress</h3>
              <p className={styles.modeText}>
                Track your rounds played, scores, and improvement over time.
              </p>
            </div>
          </div>
        </section>

        <section className={styles.sectionCard}>
            <h2 className={styles.sectionTitle}>How Scoring Works</h2>
            <p className={styles.sectionText}>
                PromptCraft uses CLIP scoring to compare your generated image to the target
                image. CLIP is an AI model that measures how visually similar the two images
                are. The closer your result matches the target in content and overall look,
                the higher your score will be.
             </p>
        </section>

        <section className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>Tips for Better Prompts</h2>

          <div className={styles.tipsList}>
            <div className={styles.tipItem}>
              Mention the main subject clearly.
            </div>
            <div className={styles.tipItem}>
              Include lighting, colors, and mood.
            </div>
            <div className={styles.tipItem}>
              Describe the setting and background.
            </div>
            <div className={styles.tipItem}>
              Be specific instead of vague.
            </div>
            <div className={styles.tipItem}>
              Revise your wording after each attempt.
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}