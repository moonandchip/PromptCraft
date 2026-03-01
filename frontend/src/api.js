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
 * @returns {Promise<{ generated_image_url: string, similarity_score: number }>}
 */
export async function submitPrompt({ round_id, user_prompt }) {
  const response = await fetch(`${VITE_API_URL}/round/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ round_id, user_prompt }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Generation failed (${response.status})`);
  }
  return response.json();
}
