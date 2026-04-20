import { getToken } from "./auth";
import { setGlobalLoading } from "./components/LoadingContext";

const VITE_API_URL = import.meta.env.VITE_API_URL;

/**
 * Wrapper around fetch() that automatically attaches JWT, handles errors,
 * optionally triggers global loading, and redirects to /login if the token is expired.
 * @param {string} url - Endpoint URL to fetch.
 * @param {object} [options={}] - Fetch options like method, headers, body.
 * @param {object} [config={}] - Extra config options.
 * @param {boolean} [config.useGlobalLoading=true] - Whether to show global loading spinner.
 * @returns {Promise<any>} - Resolves with JSON response.
 * @throws {Error} - Throws on HTTP error, network error, or 401 token expiration.
 */
export async function apiFetch(
  url,
  options = {},
  { useGlobalLoading = true } = {},
) {
  const token = getToken();
  const headers = {
    ...options.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  if (useGlobalLoading) setGlobalLoading(true);

  try {
    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      throw new Error("Session expired. Redirecting to login...");
    }

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Request failed (${response.status})`);
    }

    return await response.json();
  } catch (err) {
    if (!err.message) err.message = "Network error or server unreachable.";
    throw err;
  } finally {
    if (useGlobalLoading) setGlobalLoading(false);
  }
}

/**
 * Check backend health status.
 * @returns {Promise<any>} - Resolves with health information or null on failure.
 */
export async function getHealth() {
  try {
    return await apiFetch(`${VITE_API_URL}/health`);
  } catch (error) {
    console.error(`Error fetching /health: ${error}`);
    return null;
  }
}

/**
 * Fetch all available practice rounds.
 * @returns {Promise<Array<{id: string, title: string, difficulty: string, reference_image: string}>>}
 */
export async function getRounds() {
  return apiFetch(`${VITE_API_URL}/round/rounds`);
}

/**
 * Start a new practice round.
 * Uses local loading spinner; global loading is disabled.
 * @returns {Promise<{ round_id: string, target_image_url: string }>} - The new round info.
 */
export async function startRound() {
  const data = await apiFetch(
    `${VITE_API_URL}/round/start`,
    { method: "POST" },
    { useGlobalLoading: false },
  );
  return data.data;
}

/**
 * Submit a prompt for a given round and receive a generated image.
 * Uses local loading spinner; global loading is disabled.
 * @param {{ round_id: string, user_prompt: string }} payload - Round ID and user prompt.
 * @returns {Promise<{ generated_image_url: string, similarity_score: number }>} - Resulting image and similarity score.
 */
export async function submitPrompt(payload) {
  return apiFetch(
    `${VITE_API_URL}/round/submit`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    { useGlobalLoading: false },
  );
}

/**
 * Fetch user statistics.
 * @returns {Promise<{
 *   total_rounds: number,
 *   total_attempts: number,
 *   average_score: number,
 *   best_score: number,
 *   recent_attempts: Array<{
 *     round_id: string,
 *     attempt_number: number,
 *     prompt: string,
 *     generated_image_url: string,
 *     similarity_score: number,
 *     created_at: string
 *   }>
 * }>} - User stats including totals and recent attempts.
 */
export async function getStats() {
  const data = await apiFetch(`${VITE_API_URL}/stats/me`);
  return data.data;
}
