import { redirect } from "next/navigation";

import { auth } from "@/auth";

export default async function ProtectedPage() {
  const session = await auth();

  if (!session?.user) {
    redirect("/login");
  }

  return (
    <main>
      <h1>Protected</h1>
      <p>User id: {session.user.id}</p>
      <p>Email: {session.user.email}</p>
    </main>
  );
}
