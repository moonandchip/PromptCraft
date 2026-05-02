import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Create Account</h1>

        {/* Error Banner */}
        <ErrorBanner message={error} onClose={() => setError(null)} />

        <form onSubmit={handleSubmit} className={styles.form}>
          <input
            className={styles.input}
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <div className={styles.passwordWrapper}>
            <input
              className={styles.input}
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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

          <button className={styles.button} type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>
      </div>
    </div>
  );
}
