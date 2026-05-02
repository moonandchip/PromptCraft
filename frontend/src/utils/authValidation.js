// Lightweight client-side validation. Server-side rules are still authoritative.

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateEmail(email) {
  const trimmed = (email ?? "").trim();
  if (!trimmed) return "Email is required.";
  if (!EMAIL_REGEX.test(trimmed)) return "Enter a valid email address.";
  return null;
}

/**
 * Returns null when the password is acceptable, otherwise a short message.
 * `mode === "register"` enforces the full ruleset; `mode === "login"` only
 * checks that something was entered (servers vary, so don't pre-block logins).
 */
export function validatePassword(password, mode = "register") {
  const value = password ?? "";
  if (!value) return "Password is required.";
  if (mode === "login") return null;

  if (value.length < 8) return "Password must be at least 8 characters.";
  if (!/[A-Za-z]/.test(value)) return "Password must contain at least one letter.";
  if (!/[0-9]/.test(value)) return "Password must contain at least one number.";
  return null;
}
