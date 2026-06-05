import { NavLink } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const links = [
  { to: "/diagram", label: "Regulation diagram" },
  { to: "/decision-tree", label: "Decision tree" },
  { to: "/chat", label: "HERA Chatbot" },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-ink-200 bg-ink-900 text-ink-100">
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-fluo-500 text-lg font-extrabold text-ink-900">
          H
        </div>
        <div>
          <div className="text-sm font-bold tracking-tight text-white">
            HERA Copilot
          </div>
          <div className="text-[11px] uppercase tracking-wide text-ink-400">
            Risk &amp; safety
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) =>
              [
                "group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-fluo-500 text-white"
                  : "text-ink-300 hover:bg-ink-800 hover:text-white",
              ].join(" ")
            }
          >
            {l.label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-ink-800 p-4">
        <div className="mb-2 truncate text-xs text-ink-400">{user?.email}</div>
        <button
          onClick={() => logout()}
          className="w-full rounded-md border border-ink-700 px-3 py-2 text-xs font-semibold text-ink-200 hover:bg-ink-800"
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
