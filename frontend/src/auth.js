import { setGlobalLoading } from "./components/LoadingContext";

const AUTH_URL = import.meta.env.VITE_AUTH_URL;

/**
 * Register a new user with email and password.
 * Shows global loading while the request is in progress.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{ message: string }>} Registration response data
 * @throws {Error} Throws on registration failure
 */
export async function register(email, password) {
  setGlobalLoading(true);
  try {
    const res = await fetch(`${AUTH_URL}/api/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) throw new Error(data.error || "Registration failed");

    return data;
  } finally {
    setGlobalLoading(false);
  }
}

/**
 * Log in a user with email and password.
 * Shows global loading while the request is in progress.
 * Stores JWT in localStorage on success.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{ access_token: string }>} Login response
 * @throws {Error} Throws on login failure or missing token
 */
export async function login(email, password) {
  setGlobalLoading(true);
  try {
    const res = await fetch(`${AUTH_URL}/api/internal/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) throw new Error(data.error || "Login failed");
    if (!data.access_token) throw new Error("No access token returned");

    localStorage.setItem("token", data.access_token);

    return data;
  } finally {
    setGlobalLoading(false);
  }
}

/**
 * Get the JWT token from localStorage.
 * @returns {string|null} JWT token or null if missing
 */
export function getToken() {
  return localStorage.getItem("token");
}

const USER_CACHE_KEY = "promptcraft_user_cache";
const USER_CACHE_TTL_MS = 5 * 60 * 1000;

/**
 * Returns the cached user object if still fresh, otherwise null.
 * The cache is keyed off the current token; stale entries are dropped.
 */
export function getCachedUser() {
  try {
    const raw = localStorage.getItem(USER_CACHE_KEY);
    if (!raw) return null;
    const { user, token, expiresAt } = JSON.parse(raw);
    if (!user || token !== getToken() || Date.now() > expiresAt) {
      localStorage.removeItem(USER_CACHE_KEY);
      return null;
    }
    return user;
  } catch {
    localStorage.removeItem(USER_CACHE_KEY);
    return null;
  }
}

export function cacheUser(user) {
  if (!user) return;
  try {
    localStorage.setItem(
      USER_CACHE_KEY,
      JSON.stringify({
        user,
        token: getToken(),
        expiresAt: Date.now() + USER_CACHE_TTL_MS,
      }),
    );
  } catch {
    // Storage full or unavailable — caching is best-effort.
  }
}

export function clearCachedUser() {
  localStorage.removeItem(USER_CACHE_KEY);
}

/**
 * Fetch the currently logged-in user's info.
 * Shows global loading while the request is in progress.
 * @returns {Promise<{ user: object }>} User data
 * @throws {Error} Throws if no token or unauthorized
 */
export async function getMe() {
  const token = getToken();
  if (!token) throw new Error("No token");

  setGlobalLoading(true);
  try {
    const res = await fetch(`${AUTH_URL}/api/internal/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) throw new Error(data.error || "Unauthorized");

    if (data.user) cacheUser(data.user);
    return data;
  } finally {
    setGlobalLoading(false);
  }
}
