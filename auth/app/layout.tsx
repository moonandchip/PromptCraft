import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PromptCraft Auth",
  description: "Authentication service for PromptCraft",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
