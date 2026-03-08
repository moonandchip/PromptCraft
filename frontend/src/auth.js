const AUTH_URL = import.meta.env.VITE_AUTH_URL;

export async function register(email, password) {
  const res = await fetch(`${AUTH_URL}/api/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || "Registration failed");
  }

  return data;
}

export async function login(email, password) {
  const res = await fetch(`${AUTH_URL}/api/internal/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || "Login failed");
  }

  if (!data.access_token) {
    throw new Error("No access token returned");
  }

  localStorage.setItem("token", data.access_token);

  return data;
}

export function getToken() {
  return localStorage.getItem("token");
}

export async function getMe() {
  const token = getToken();

  if (!token) {
    throw new Error("No token");
  }

  const res = await fetch(`${AUTH_URL}/api/internal/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || "Unauthorized");
  }

  return data;
}
