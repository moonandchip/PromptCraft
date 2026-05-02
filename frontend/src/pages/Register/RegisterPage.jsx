import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getMe, login, register } from "../../auth";
import { useAuth } from "../../components/AuthContext";
import { validateEmail, validatePassword } from "../../utils/authValidation";
import styles from "./RegisterPage.module.css";
import ErrorBanner from "../../components/ErrorBanner";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { setUser } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    const emailError = validateEmail(email);
    if (emailError) {
      setError(emailError);
      return;
    }
    const passwordError = validatePassword(password, "register");
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const trimmedEmail = email.trim();
      await register(trimmedEmail, password);
      // Auto-login after successful registration so the user lands signed in.
      await login(trimmedEmail, password);
      const me = await getMe();
      setUser(me.user);
      navigate("/");
    } catch (err) {
      setError(err.message || "Registration failed.");
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
        <p className={styles.kicker}>Join the game</p>
        <h1 className={styles.title}>Create account</h1>

        <ErrorBanner message={error} onClose={() => setError(null)} />

        <form onSubmit={handleSubmit} className={styles.form}>
          <label className={styles.fieldLabel} htmlFor="register-email">Email</label>
          <input
            id="register-email"
            className={styles.input}
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />

          <label className={styles.fieldLabel} htmlFor="register-password">Password</label>
          <div className={styles.passwordWrapper}>
            <input
              id="register-password"
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

          <button className={styles.primaryButton} type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>

        <p className={styles.linkRow}>
          Already have an account?{" "}
          <Link to="/login" className={styles.link}>
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
