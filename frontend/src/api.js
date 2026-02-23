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
