import Link from "next/link";

import { auth, signOut } from "@/auth";

export default async function HomePage() {
  const session = await auth();

  return (
    <main>
      <h1>PromptCraft Auth Service</h1>
      {session?.user ? (
        <>
          <p>Signed in as {session.user.email}</p>
          <form
            action={async () => {
              "use server";
              await signOut({ redirectTo: "/" });
            }}
          >
            <button type="submit">Sign out</button>
          </form>
          <p>
            <Link href="/protected">Open protected page</Link>
          </p>
        </>
      ) : (
        <>
          <p>No active session.</p>
          <p>
            <Link href="/login">Login</Link> | <Link href="/register">Register</Link>
          </p>
        </>
      )}
    </main>
  );
}
