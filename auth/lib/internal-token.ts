import crypto from "crypto";

type Claims = {
  sub: string;
  email: string;
  iat: number;
  exp: number;
};

function getSecret(): string {
  return process.env.AUTH_SECRET || "dev-auth-secret-change-me";
}

function encode(value: unknown): string {
  return Buffer.from(JSON.stringify(value)).toString("base64url");
}

function decode<T>(value: string): T {
  return JSON.parse(Buffer.from(value, "base64url").toString("utf8")) as T;
}

export function createInternalAccessToken(
  payload: { sub: string; email: string },
  expiresInSeconds = 3600,
): string {
  const header = { alg: "HS256", typ: "JWT" };
  const now = Math.floor(Date.now() / 1000);
  const claims: Claims = {
    ...payload,
    iat: now,
    exp: now + expiresInSeconds,
  };

  const encodedHeader = encode(header);
  const encodedPayload = encode(claims);
  const signingInput = `${encodedHeader}.${encodedPayload}`;

  const signature = crypto
    .createHmac("sha256", getSecret())
    .update(signingInput)
    .digest("base64url");

  return `${signingInput}.${signature}`;
}

export function verifyInternalAccessToken(token: string): Claims {
  const [encodedHeader, encodedPayload, signature] = token.split(".");
  if (!encodedHeader || !encodedPayload || !signature) {
    throw new Error("invalid token format");
  }

  const expected = crypto
    .createHmac("sha256", getSecret())
    .update(`${encodedHeader}.${encodedPayload}`)
    .digest("base64url");

  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
    throw new Error("invalid token signature");
  }

  const payload = decode<Claims>(encodedPayload);
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp < now) {
    throw new Error("token expired");
  }
  if (!payload.sub) {
    throw new Error("invalid token subject");
  }

  return payload;
}
