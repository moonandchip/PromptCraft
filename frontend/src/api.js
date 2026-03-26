import { getToken } from "./auth";

const VITE_API_URL = import.meta.env.VITE_API_URL;

export async function getHealth() {
  try {
    const response = await fetch(`${VITE_API_URL}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching /health: ${error}`);
    return null;
  }
}

/**
 * Fetch all available practice rounds from the backend.
 * @returns {Promise<Array<{id: string, title: string, difficulty: string, reference_image: string}>>}
 */
export async function getRounds() {
  const response = await fetch(`${VITE_API_URL}/round/rounds`);
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to load rounds (${response.status})`);
  }
  return response.json();
}

/**
 * Submit a prompt for a given round and receive a generated image URL.
 * @param {{ round_id: string, user_prompt: string }} payload
 * @param {string} token  JWT access token
 * @returns {Promise<{ generated_image_url: string, similarity_score: number }>}
 */
export async function submitPrompt({ round_id, user_prompt }, token) {
  const response = await fetch(`${VITE_API_URL}/round/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ round_id, user_prompt }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Generation failed (${response.status})`);
  }
  return response.json();
}

/**
 * Start a new practice round via /round/start
 * @returns {Promise<{
 *   round_id: string,
 *   target_image_url: string
 * }>}
 */
export async function startRound() {
  const token = getToken();
  const response = await fetch(`${VITE_API_URL}/round/start`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to start round (${response.status})`);
  }

  const data = await response.json();
  return data.data;
}

/**
 * Fetch user stats from /stats/me
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
 * }>}
 */
export async function getStats() {
  const token = getToken();
  try {
    const response = await fetch(`${VITE_API_URL}/stats/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(
        err.detail || `Failed to load stats (${response.status})`,
      );
    }
    return await response.json().then((res) => res.data);
  } catch (error) {
    console.error(`Error fetching /stats/me: ${error}`);
    return null;
  }
}
