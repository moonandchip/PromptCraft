import Link from "next/link";
import { redirect } from "next/navigation";

import { signIn } from "@/auth";

export default function LoginPage() {
  return (
    <main>
      <h1>Login</h1>
      <form
        action={async (formData) => {
          "use server";
          const email = String(formData.get("email") ?? "");
          const password = String(formData.get("password") ?? "");

          const result = await signIn("credentials", {
            email,
            password,
            redirect: false,
          });

          if (result?.error) {
            redirect("/login?error=invalid_credentials");
          }

          redirect("/");
        }}
      >
        <input name="email" type="email" placeholder="Email" required />
        <input name="password" type="password" placeholder="Password" required />
        <button type="submit">Sign in</button>
      </form>
      <p>
        New user? <Link href="/register">Create account</Link>
      </p>
    </main>
  );
}
