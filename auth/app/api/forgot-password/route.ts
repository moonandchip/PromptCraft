import { randomBytes } from "crypto";
import { NextResponse } from "next/server";
import { z } from "zod";

import { sendEmail } from "@/lib/email";
import { prisma } from "@/lib/prisma";

const forgotSchema = z.object({
  email: z.email(),
});

const TOKEN_TTL_MINUTES = 60;

function buildResetEmail(resetUrl: string) {
  const subject = "Reset your PromptCraft password";
  const text = [
    "We received a request to reset your PromptCraft password.",
    "",
    "Click the link below to choose a new password (expires in 60 minutes):",
    resetUrl,
    "",
    "If you didn't request this, you can safely ignore this email.",
  ].join("\n");
  const html = `
    <div style="font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; max-width: 480px; margin: 0 auto; padding: 24px; color: #1f2937;">
      <h1 style="font-size: 22px; margin: 0 0 16px;">Reset your PromptCraft password</h1>
      <p style="line-height: 1.55;">We received a request to reset the password for your PromptCraft account.</p>
      <p style="margin: 24px 0;">
        <a href="${resetUrl}" style="display: inline-block; background: #2563eb; color: #ffffff; text-decoration: none; padding: 12px 20px; border-radius: 6px; font-weight: 600;">
          Reset password
        </a>
      </p>
      <p style="line-height: 1.55; font-size: 14px; color: #4b5563;">
        Or paste this URL into your browser:<br />
        <span style="word-break: break-all;">${resetUrl}</span>
      </p>
      <p style="line-height: 1.55; font-size: 14px; color: #4b5563;">
        This link expires in 60 minutes. If you didn't request a reset, you can safely ignore this email.
      </p>
    </div>
  `;
  return { subject, text, html };
}

/**
 * Issues a password reset token. Always responds with 200 to avoid email
 * enumeration — the client gets the same response whether the email exists
 * or not. Sends the reset link via Gmail SMTP when GMAIL_USER and
 * GMAIL_APP_PASSWORD are set; otherwise logs it to stdout as a dev fallback.
 */
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const parsed = forgotSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: "Invalid input" }, { status: 400 });
    }

    const email = parsed.data.email.trim().toLowerCase();
    const user = await prisma.user.findUnique({ where: { email } });

    if (user) {
      // Invalidate any prior outstanding tokens for this user so an attacker
      // who later steals an old email can't reuse a stale link.
      await prisma.passwordResetToken.updateMany({
        where: { userId: user.id, usedAt: null, expiresAt: { gt: new Date() } },
        data: { usedAt: new Date() },
      });

      const token = randomBytes(32).toString("base64url");
      const expiresAt = new Date(Date.now() + TOKEN_TTL_MINUTES * 60 * 1000);

      await prisma.passwordResetToken.create({
        data: { token, userId: user.id, expiresAt },
      });

      const appOrigin = process.env.APP_ORIGIN ?? "http://localhost:5173";
      const resetUrl = `${appOrigin.replace(/\/+$/, "")}/reset-password/${token}`;

      try {
        const { subject, text, html } = buildResetEmail(resetUrl);
        const sent = await sendEmail({ to: email, subject, text, html });
        if (!sent) {
          console.log(`[forgot-password] (no SMTP configured) reset link for ${email}: ${resetUrl}`);
        }
      } catch (sendErr) {
        // Email delivery failures must not be visible to the client (would
        // leak that the email is registered). Log + still respond 200.
        console.error(`[forgot-password] failed to email ${email}`, sendErr);
        console.log(`[forgot-password] (delivery failed) reset link for ${email}: ${resetUrl}`);
      }
    }

    // Identical response shape regardless of whether the user exists.
    return NextResponse.json({ status: "ok" }, { status: 200 });
  } catch (err) {
    console.error("[forgot-password] error", err);
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
