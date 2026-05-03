import { NextRequest, NextResponse } from "next/server";

/**
 * Comma-separated list of explicit allowed origins. Reads
 * CORS_ALLOWED_ORIGINS at request time so we don't have to redeploy when
 * the list changes. Falls back to localhost dev if unset.
 */
function getAllowedOrigins(): string[] {
  const raw = (process.env.CORS_ALLOWED_ORIGINS ?? "").trim();
  if (!raw) return ["http://localhost:5173"];
  return raw.split(",").map((o) => o.trim()).filter(Boolean);
}

/**
 * Optional regex for matching subdomains (e.g. apex + www + previews).
 * Same env var the backend uses, so a single Terraform var covers both.
 */
function getAllowedOriginRegex(): RegExp | null {
  const raw = (process.env.CORS_ALLOWED_ORIGIN_REGEX ?? "").trim();
  if (!raw) return null;
  try {
    return new RegExp(raw);
  } catch {
    return null;
  }
}

function isOriginAllowed(origin: string | null): origin is string {
  if (!origin) return false;
  if (getAllowedOrigins().includes(origin)) return true;
  const regex = getAllowedOriginRegex();
  return regex !== null && regex.test(origin);
}

function applyCorsHeaders(response: NextResponse, origin: string | null): NextResponse {
  if (isOriginAllowed(origin)) {
    response.headers.set("Access-Control-Allow-Origin", origin);
  }
  // Always vary on Origin so caches/CDNs never serve a response with the
  // wrong allow-origin header to a different client.
  response.headers.set("Vary", "Origin");
  response.headers.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  response.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  response.headers.set("Access-Control-Allow-Credentials", "true");
  return response;
}

export function middleware(request: NextRequest) {
  const origin = request.headers.get("origin");

  if (request.method === "OPTIONS") {
    return applyCorsHeaders(new NextResponse(null, { status: 204 }), origin);
  }

  return applyCorsHeaders(NextResponse.next(), origin);
}

export const config = {
  matcher: ["/api/:path*"],
};
