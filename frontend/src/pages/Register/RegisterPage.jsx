import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../auth";
import styles from "./RegisterPage.module.css";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    setError(null);
    setSuccess(false);
    setLoading(true);

    try {
      await register(email, password);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Redirect to /login after successful registration
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        navigate("/login");
      }, 1000); // Wait 1 second so user sees success message
      return () => clearTimeout(timer);
    }
  }, [success, navigate]);

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Create Account</h1>

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
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        {success && (
          <p className={styles.success}>
            Registration successful! Redirecting...
          </p>
        )}
        {error && <p className={styles.error}>{error}</p>}
      </div>
    </div>
  );
}
