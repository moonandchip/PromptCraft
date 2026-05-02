import { useState } from "react";
import { Link } from "react-router-dom";
import { requestPasswordReset } from "../../auth";
import { validateEmail } from "../../utils/authValidation";
import ErrorBanner from "../../components/ErrorBanner";
import styles from "./ForgotPasswordPage.module.css";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    const emailError = validateEmail(email);
    if (emailError) {
      setError(emailError);
      return;
    }
    setError(null);
    setLoading(true);
    try {
      await requestPasswordReset(email.trim().toLowerCase());
      setSubmitted(true);
    } catch (err) {
      setError(err.message || "Could not send reset email.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={styles.page}>
      <div className={styles.backgroundDecor1}></div>
      <div className={styles.backgroundDecor2}></div>
      <div className={styles.backgroundDecor3}></div>

      <div className={styles.card}>
        <p className={styles.kicker}>Forgot password</p>
        <h1 className={styles.title}>Reset access</h1>

        {submitted ? (
          <>
            <p className={styles.message}>
              If an account with that email exists, we&apos;ve sent a reset
              link. Check your inbox (and spam folder) — the link expires in
              60 minutes.
            </p>
            <Link to="/login" className={styles.primaryButtonLink}>
              Back to login
            </Link>
          </>
        ) : (
          <>
            <p className={styles.message}>
              Enter the email you used to register and we&apos;ll send a link
              to set a new password.
            </p>

            <ErrorBanner message={error} onClose={() => setError(null)} />

            <form onSubmit={handleSubmit} className={styles.form}>
              <label className={styles.fieldLabel} htmlFor="forgot-email">Email</label>
              <input
                id="forgot-email"
                className={styles.input}
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />

              <button className={styles.primaryButton} type="submit" disabled={loading}>
                {loading ? "Sending..." : "Send reset link"}
              </button>
            </form>

            <p className={styles.linkRow}>
              <Link to="/login" className={styles.link}>
                Back to login
              </Link>
            </p>
          </>
        )}
      </div>
    </main>
  );
}
