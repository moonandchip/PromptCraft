import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className={styles.navbar}>
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

      <div className={styles.rightContainer}>
        {user ? (
          <>
            <span className={styles.userEmail}>{user.email}</span>
            <button className={styles.logoutButton} onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className={styles.navLink}>
              Login
            </Link>
            <Link to="/register" className={styles.navLink}>
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
