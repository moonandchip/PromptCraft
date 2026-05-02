import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { resetPassword } from "../../auth";
import { validatePassword } from "../../utils/authValidation";
import ErrorBanner from "../../components/ErrorBanner";
import styles from "./ResetPasswordPage.module.css";

export default function ResetPasswordPage() {
  const { token } = useParams();
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    const passwordError = validatePassword(password, "register");
    if (passwordError) {
      setError(passwordError);
      return;
    }
    if (password !== confirm) {
      setError("Passwords don't match.");
      return;
    }

    setError(null);
    setLoading(true);
    try {
      await resetPassword(token, password);
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.message || "Could not reset password.");
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
        <p className={styles.kicker}>Reset password</p>
        <h1 className={styles.title}>Set new password</h1>

        {success ? (
          <>
            <p className={styles.message}>
              Password updated. Redirecting you to the login page...
            </p>
            <Link to="/login" className={styles.primaryButtonLink}>
              Go to login
            </Link>
          </>
        ) : (
          <>
            <ErrorBanner message={error} onClose={() => setError(null)} />

            <form onSubmit={handleSubmit} className={styles.form}>
              <label className={styles.fieldLabel} htmlFor="reset-password">New password</label>
              <div className={styles.passwordWrapper}>
                <input
                  id="reset-password"
                  className={styles.input}
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="new-password"
                  required
                  minLength={8}
                />
                <button
                  type="button"
                  className={styles.passwordToggle}
                  onClick={() => setShowPassword((prev) => !prev)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
              <p className={styles.hint}>
                Use 8+ characters with at least one letter and one number.
              </p>

              <label className={styles.fieldLabel} htmlFor="reset-confirm">Confirm password</label>
              <input
                id="reset-confirm"
                className={styles.input}
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
                required
                minLength={8}
              />

              <button className={styles.primaryButton} type="submit" disabled={loading}>
                {loading ? "Updating..." : "Update password"}
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
