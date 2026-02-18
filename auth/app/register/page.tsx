import Link from "next/link";
import { redirect } from "next/navigation";
import bcrypt from "bcryptjs";

import { prisma } from "@/lib/prisma";
import { signIn } from "@/auth";

export default function RegisterPage() {
  return (
    <main>
      <h1>Register</h1>
      <form
        action={async (formData) => {
          "use server";
          const name = String(formData.get("name") ?? "");
          const email = String(formData.get("email") ?? "");
          const password = String(formData.get("password") ?? "");

          if (!email || password.length < 8) {
            redirect("/register?error=invalid_input");
          }

          const existingUser = await prisma.user.findUnique({ where: { email } });
          if (existingUser) {
            redirect("/register?error=email_exists");
          }

          const hashedPassword = await bcrypt.hash(password, 12);
          await prisma.user.create({
            data: {
              name: name || null,
              email,
              password: hashedPassword,
            },
          });

          await signIn("credentials", {
            email,
            password,
            redirect: false,
          });

          redirect("/");
        }}
      >
        <input name="name" type="text" placeholder="Name (optional)" />
        <input name="email" type="email" placeholder="Email" required />
        <input name="password" type="password" placeholder="Password (min 8 chars)" required />
        <button type="submit">Create account</button>
      </form>
      <p>
        Have an account? <Link href="/login">Sign in</Link>
      </p>
    </main>
  );
}
