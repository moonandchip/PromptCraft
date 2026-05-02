import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { login, getMe } from "../../auth";
import { useAuth } from "../../components/AuthContext";
import { validateEmail, validatePassword } from "../../utils/authValidation";
import styles from "./LoginPage.module.css";
import ErrorBanner from "../../components/ErrorBanner";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sessionExpired, setSessionExpired] = useState(false);

  const { setUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.sessionExpired) {
      setSessionExpired(true);
      // Clear the flag so refreshing this page doesn't keep showing the notice.
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate]);

  async function handleSubmit(e) {
    e.preventDefault();

    const emailError = validateEmail(email);
    if (emailError) {
      setError(emailError);
      return;
    }
    const passwordError = validatePassword(password, "login");
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setError(null);
    setLoading(true);

    try {
      await login(email.trim(), password);
      const me = await getMe();
      setUser(me.user);
      navigate("/");
    } catch (err) {
      setError(err.message || "Login failed.");
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
        <p className={styles.kicker}>Welcome back</p>
        <h1 className={styles.title}>Sign in</h1>

        {sessionExpired && (
          <output className={styles.sessionExpired}>
            Your session expired. Please log in again.
          </output>
        )}

        <ErrorBanner message={error} onClose={() => setError(null)} />

        <form onSubmit={handleSubmit} className={styles.form}>
          <label className={styles.fieldLabel} htmlFor="login-email">Email</label>
          <input
            id="login-email"
            className={styles.input}
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />

          <label className={styles.fieldLabel} htmlFor="login-password">Password</label>
          <div className={styles.passwordWrapper}>
            <input
              id="login-password"
              className={styles.input}
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
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

          <button className={styles.primaryButton} type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className={styles.linkRow}>
          <Link to="/forgot-password" className={styles.link}>
            Forgot password?
          </Link>
        </p>

        <p className={styles.linkRow}>
          Don&apos;t have an account?{" "}
          <Link to="/register" className={styles.link}>
            Register
          </Link>
        </p>
      </div>
    </main>
  );
}
