import { createContext, useContext, useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { cacheUser, clearCachedUser, getCachedUser, getMe, getToken } from "../auth";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => getCachedUser());
  const navigate = useNavigate();
  const location = useLocation();

  const loadUser = async ({ force = false } = {}) => {
    const token = getToken();
    if (!token) {
      setUser(null);
      clearCachedUser();
      return;
    }

    if (!force) {
      const cached = getCachedUser();
      if (cached) {
        setUser(cached);
        return;
      }
    }

    try {
      const data = await getMe();
      setUser(data.user);
      cacheUser(data.user);
    } catch {
      setUser(null);
      clearCachedUser();
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  useEffect(() => {
    const handleExpired = () => {
      setUser(null);
      clearCachedUser();
      // Don't bounce if we're already on a public page.
      const publicPaths = ["/login", "/register", "/", "/how-to-play"];
      if (!publicPaths.includes(location.pathname)) {
        navigate("/login", { replace: true, state: { sessionExpired: true } });
      }
    };
    window.addEventListener("auth:expired", handleExpired);
    return () => window.removeEventListener("auth:expired", handleExpired);
  }, [navigate, location.pathname]);

  const logout = () => {
    localStorage.removeItem("token");
    clearCachedUser();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, logout, loadUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
