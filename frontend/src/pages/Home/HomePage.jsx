import { Link } from "react-router-dom";
import styles from "./HomePage.module.css";

export default function HomePage() {
  return (
    <div className={styles.page}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <span className={styles.badge}>AI Prompt Practice Game</span>

            <h1 className={styles.title}>
              Master Prompt Engineering
              <span className={styles.gradientText}> One Image at a Time.</span>
            </h1>

            <p className={styles.subtitle}>
              PromptCraft helps you practice writing better AI image prompts by
              challenging you to recreate a target image, score your result, and
              improve over time.
            </p>

            <div className={styles.heroActions}>
              <Link to="/practice" className={styles.primaryButton}>
                Start Practicing
              </Link>
              <Link to="/progress" className={styles.secondaryButton}>
                View Progress
              </Link>
            </div>

            <div className={styles.statsRow}>
              <div className={styles.statCard}>
                <h3>Practice</h3>
                <p>Unlimited rounds to sharpen your prompting skills.</p>
              </div>
              <div className={styles.statCard}>
                <h3>Score</h3>
                <p>See how close your generated image is to the target.</p>
              </div>
              <div className={styles.statCard}>
                <h3>Improve</h3>
                <p>Track your progress and get better over time.</p>
              </div>
            </div>
          </div>

          <div className={styles.heroVisual}>
            <div className={styles.previewWindow}>
              <div className={styles.previewHeader}>
                <span className={styles.previewDot}></span>
                <span className={styles.previewDot}></span>
                <span className={styles.previewDot}></span>
              </div>

              <div className={styles.previewBody}>
                <div className={styles.imageCompare}>
                  <div className={styles.imageCard}>
                    <span className={styles.imageLabel}>Target Image</span>
                    <div className={styles.mockImage + " " + styles.targetMock}>
                      Ancient Temple
                    </div>
                  </div>

                  <div className={styles.imageCard}>
                    <span className={styles.imageLabel}>Generated Result</span>
                    <div className={styles.mockImage + " " + styles.resultMock}>
                      Your AI Output
                    </div>
                  </div>
                </div>

                <div className={styles.scorePanel}>
                  <div>
                    <p className={styles.scoreLabel}>Similarity Score</p>
                    <h2 className={styles.scoreValue}>82%</h2>
                  </div>
                  <div className={styles.scoreBar}>
                    <div className={styles.scoreFill}></div>
                  </div>
                  <p className={styles.scoreHint}>
                    Strong composition match. Try improving lighting and detail.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className={styles.section}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionTag}>How It Works</span>
          <h2>Simple, competitive, and addictive in the best way!</h2>
          <p>
            PromptCraft turns prompt engineering into a hands-on challenge
            instead of just guessing what works.
          </p>
        </div>

        <div className={styles.stepsGrid}>
          <div className={styles.stepCard}>
            <div className={styles.stepNumber}>01</div>
            <h3>Get a target image</h3>
            <p>
              Start a round and receive an image you need to recreate using only
              text.
            </p>
          </div>

          <div className={styles.stepCard}>
            <div className={styles.stepNumber}>02</div>
            <h3>Write your prompt</h3>
            <p>
              Think carefully about subject, style, lighting, colors, and scene
              details.
            </p>
          </div>

          <div className={styles.stepCard}>
            <div className={styles.stepNumber}>03</div>
            <h3>Submit and score</h3>
            <p>
              Generate your result, compare it to the target, and see how close
              you got.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className={styles.sectionAlt}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionTag}>Why PromptCraft</span>
          <h2>Built to feel like a real AI training product</h2>
          <p>
            This is not just random image generation. It is structured practice
            with measurable feedback.
          </p>
        </div>

        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <h3>AI-Powered Scoring</h3>
            <p>
              Each submission is evaluated to show how closely your result
              matches the target image.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>Progress Tracking</h3>
            <p>
              Watch your scores improve and see how your prompting skills grow
              over time.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>Unlimited Practice</h3>
            <p>
              Keep refining your wording, retry your prompts, and experiment
              without pressure.
            </p>
          </div>

          <div className={styles.featureCard}>
            <h3>Challenge Potential</h3>
            <p>
              Expand into daily or weekly challenges to add competition and
              replay value.
            </p>
          </div>
        </div>
      </section>

      {/* CLIP AI Section */}
<section className={styles.sectionAlt}>
  <div className={styles.clipSection}>
    <div className={styles.clipText}>
      <span className={styles.sectionTag}>AI Scoring Engine</span>

      <h2>Powered by CLIP</h2>

      <p>
        PromptCraft uses CLIP, an AI model developed by OpenAI, to measure how
        closely your generated image matches the target image.
      </p>

      <p>
        Instead of guessing or using simple rules, CLIP understands both images
        and text, allowing it to evaluate similarity in a meaningful way.
      </p>

      <ul className={styles.clipList}>
        <li>Analyzes visual content using deep learning</li>
        <li>Compares image meaning, not just pixels</li>
        <li>Provides real similarity scores using AI</li>
      </ul>
    </div>

    <div className={styles.clipVisual}>
      <div className={styles.clipFlowCard}>
        <div className={styles.clipInputs}>
          <div className={styles.clipMiniBox}>
            <span className={styles.clipMiniLabel}>Target</span>
            <div className={`${styles.clipMiniImage} ${styles.clipTargetMini}`}></div>
          </div>

          <div className={styles.clipMiniBox}>
            <span className={styles.clipMiniLabel}>Generated</span>
            <div className={`${styles.clipMiniImage} ${styles.clipGeneratedMini}`}></div>
          </div>
        </div>

        <div className={styles.clipCenter}>
          <div className={styles.clipCenterBadge}>CLIP Analysis</div>
          <p className={styles.clipCenterText}>
            Embeds and compares visual meaning
          </p>
        </div>

        <div className={styles.clipOutput}>
          <span className={styles.clipOutputLabel}>Match Score</span>
          <div className={styles.clipScoreRing}>
            <div className={styles.clipScoreInner}>82%</div>
          </div>
          <p className={styles.clipOutputText}>
            Semantic similarity between both images
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

      {/* Demo / Showcase Section */}
      <section className={styles.section}>
        <div className={styles.showcase}>
          <div className={styles.showcaseText}>
            <span className={styles.sectionTag}>Gameplay Preview</span>
            <h2>Train like a player. Improve like a creator.</h2>
            <p>
              PromptCraft is designed to help users go beyond vague prompts and
              start thinking intentionally about visual detail, composition, and
              style.
            </p>

            <ul className={styles.showcaseList}>
              <li>Practice with image-based rounds</li>
              <li>See scoring feedback instantly</li>
              <li>Build intuition for better prompts</li>
              <li>Turn AI prompting into a repeatable skill</li>
            </ul>

            <Link to="/practice" className={styles.primaryButton}>
              Try a Round
            </Link>
          </div>

          <div className={styles.showcasePanel}>
            <div className={styles.miniPanel}>
              <p className={styles.miniLabel}>Example Prompt</p>
              <div className={styles.promptBox}>
                “Ancient stone temple in a jungle, golden sunlight, cinematic,
                realistic, detailed architecture, overgrown vines”
              </div>
            </div>

            <div className={styles.miniPanel}>
              <p className={styles.miniLabel}>Why this works</p>
              <div className={styles.feedbackBox}>
                Specific environment, lighting, mood, and visual style improve
                image alignment.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className={styles.ctaSection}>
        <div className={styles.ctaBox}>
          <span className={styles.sectionTag}>Ready to Start?</span>
          <h2>Start building better prompts today.</h2>
          <p>
            Jump into a round, test your creativity, and see how close you can
            get.
          </p>

          <div className={styles.heroActions}>
            <Link to="/practice" className={styles.primaryButton}>
              Start Practicing
            </Link>
            <Link to="/register" className={styles.secondaryButton}>
              Create Account
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}