import type { ReactNode } from "react";
import Sidebar from "./Sidebar";

type Props = { children: ReactNode };

export default function Layout({ children }: Props) {
  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto bg-ink-50">
        <div className="mx-auto max-w-5xl px-8 py-10">{children}</div>
      </main>
    </div>
  );
}
