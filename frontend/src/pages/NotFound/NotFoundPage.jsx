import { Link } from "react-router-dom";
import styles from "./NotFoundPage.module.css";

export default function NotFoundPage() {
  return (
    <main className={styles.page}>
      <div className={styles.backgroundDecor1}></div>
      <div className={styles.backgroundDecor2}></div>
      <div className={styles.backgroundDecor3}></div>

      <div className={styles.card}>
        <p className={styles.kicker}>Page not found</p>
        <h1 className={styles.code}>404</h1>
        <p className={styles.message}>
          The page you&apos;re looking for took a wrong turn at the prompt.
        </p>

        <div className={styles.actions}>
          <Link to="/" className={styles.primaryButton}>
            Back home
          </Link>
          <Link to="/practice" className={styles.secondaryButton}>
            Play practice
          </Link>
        </div>
      </div>
    </main>
  );
}
