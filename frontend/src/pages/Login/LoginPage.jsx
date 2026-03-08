import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, getMe } from "../../auth";
import { useAuth } from "../../components/AuthContext";
import styles from "./LoginPage.module.css";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { setUser } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    setError(null);
    setLoading(true);

    try {
      await login(email, password); // Store token in localStorage
      const me = await getMe(); // Fetch user from auth service
      setUser(me.user); // Update global auth state, so navbar re-renders
      navigate("/"); // Redirect to homepage
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Login</h1>

        <form onSubmit={handleSubmit} className={styles.form}>
          <input
            className={styles.input}
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            className={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button className={styles.button} type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {error && <p className={styles.error}>{error}</p>}

        <a href="/register" className={styles.link}>
          Don't have an account? Register
        </a>
      </div>
    </div>
  );
}
