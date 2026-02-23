import { Link } from "react-router-dom";
import styles from "./Navbar.module.css";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      {/* Left (Logo + main links) */}
      <div className={styles.leftContainer}>
        <div className={styles.logo}>
          <Link to="/">PromptCraft</Link>
        </div>
        <div className={styles.mainLinks}>
          <Link to="/practice" className={styles.navLink}>
            Practice
          </Link>
          <Link to="/challenge" className={styles.navLink}>
            Challenge
          </Link>
          <Link to="/progress" className={styles.navLink}>
            Progress
          </Link>
        </div>
      </div>

      {/* Right (Auth links) */}
      <div className={styles.rightContainer}>
        <Link to="/login" className={styles.navLink}>
          Login
        </Link>
        <Link to="/register" className={styles.navLink}>
          Register
        </Link>
      </div>
    </nav>
  );
}
