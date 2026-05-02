import { useEffect, useState } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  // Close the mobile menu whenever the route changes.
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  // Close on Escape for keyboard users.
  useEffect(() => {
    if (!menuOpen) return undefined;
    const onKey = (e) => {
      if (e.key === "Escape") setMenuOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [menuOpen]);

  const handleLogout = () => {
    setMenuOpen(false);
    logout();
    navigate("/login");
  };

  const navLinkClass = ({ isActive }) =>
    isActive ? `${styles.navLink} ${styles.navLinkActive}` : styles.navLink;

  return (
    <header className={styles.headerWrap}>
      <span className={`${styles.cloud} ${styles.cloudLeft}`} aria-hidden="true"></span>
      <span className={`${styles.cloud} ${styles.cloudRight}`} aria-hidden="true"></span>

      <nav className={styles.navbar}>
        <div className={styles.leftContainer}>
          <div className={styles.logo}>
            <Link to="/">
              <span className={styles.logoPrimary}>Prompt</span>
              <span className={styles.logoAccent}>Craft</span>
            </Link>
          </div>
          <div className={styles.mainLinks}>
            <NavLink to="/how-to-play" className={navLinkClass}>
              How to Play
            </NavLink>
            <NavLink to="/practice" className={navLinkClass}>
              Practice
            </NavLink>
            {user && (
              <>
                <NavLink to="/challenge" className={navLinkClass}>
                  Challenge
                </NavLink>
                <NavLink to="/progress" className={navLinkClass}>
                  Progress
                </NavLink>
              </>
            )}
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
              <NavLink to="/login" className={navLinkClass}>
                Login
              </NavLink>
              <NavLink to="/register" className={navLinkClass}>
                Register
              </NavLink>
            </>
          )}
        </div>

        <button
          type="button"
          className={styles.menuToggle}
          onClick={() => setMenuOpen((prev) => !prev)}
          aria-expanded={menuOpen}
          aria-controls="mobile-nav-panel"
          aria-label={menuOpen ? "Close menu" : "Open menu"}
        >
          <span className={`${styles.menuIcon} ${menuOpen ? styles.menuIconOpen : ""}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </nav>

      {menuOpen && (
        <div
          id="mobile-nav-panel"
          className={styles.mobilePanel}
          onClick={() => setMenuOpen(false)}
        >
          <div className={styles.mobileCard} onClick={(e) => e.stopPropagation()}>
            <NavLink to="/how-to-play" className={navLinkClass}>
              How to Play
            </NavLink>
            <NavLink to="/practice" className={navLinkClass}>
              Practice
            </NavLink>
            {user && (
              <>
                <NavLink to="/challenge" className={navLinkClass}>
                  Challenge
                </NavLink>
                <NavLink to="/progress" className={navLinkClass}>
                  Progress
                </NavLink>
              </>
            )}

            <div className={styles.mobileDivider}></div>

            {user ? (
              <>
                <span className={styles.mobileUserEmail}>{user.email}</span>
                <button className={styles.logoutButton} onClick={handleLogout}>
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" className={navLinkClass}>
                  Login
                </NavLink>
                <NavLink to="/register" className={navLinkClass}>
                  Register
                </NavLink>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
