import nodemailer, { type Transporter } from "nodemailer";

/**
 * Lazily-initialised SMTP transporter. Built once per process so we don't pay
 * the connection-pool setup cost per email. Returns null when SMTP isn't
 * configured — callers should fall back to logging in that case.
 */
let cached: Transporter | null | undefined;

function getTransporter(): Transporter | null {
  if (cached !== undefined) return cached;

  const user = (process.env.GMAIL_USER ?? "").trim();
  const pass = (process.env.GMAIL_APP_PASSWORD ?? "").trim();

  if (!user || !pass) {
    cached = null;
    return null;
  }

  cached = nodemailer.createTransport({
    service: "gmail",
    auth: { user, pass },
  });
  return cached;
}

interface SendEmailArgs {
  to: string;
  subject: string;
  html: string;
  text: string;
}

/**
 * Sends a transactional email via Gmail SMTP. Returns `true` if the message
 * was handed off to the SMTP server, `false` if SMTP wasn't configured.
 *
 * Requires a Google account with 2FA enabled and an "App Password" generated
 * at https://myaccount.google.com/apppasswords (regular Gmail passwords are
 * rejected by SMTP). Set:
 *   GMAIL_USER=you@gmail.com
 *   GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
 *
 * Optional:
 *   EMAIL_FROM=PromptCraft <noreply@promptcrafts.net>   # falls back to GMAIL_USER
 */
export async function sendEmail({ to, subject, html, text }: SendEmailArgs): Promise<boolean> {
  const transporter = getTransporter();
  if (!transporter) return false;

  const from =
    (process.env.EMAIL_FROM ?? "").trim() ||
    `PromptCraft <${process.env.GMAIL_USER}>`;

  await transporter.sendMail({ from, to, subject, html, text });
  return true;
}
