import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { ApiError } from "../api/client";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const u = await login(email, password, remember);
      const redirect =
        (location.state as { from?: string } | null)?.from ??
        (u.onboarded ? "/chat" : "/onboarding");
      navigate(redirect, { replace: true });
    } catch (err) {
      setError((err as ApiError).detail ?? "Login failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthShell title="Sign in">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="label" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div>
          <label className="label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <label className="flex items-center gap-2 text-sm text-ink-600">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="h-4 w-4 accent-fluo-500"
          />
          Remember me for 30 days
        </label>

        {error && (
          <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="btn-primary w-full"
        >
          {submitting ? "Signing in…" : "Sign in"}
        </button>
      </form>

      <p className="mt-6 text-center text-xs text-ink-500">
        Have an invite?{" "}
        <Link to="/register" className="font-semibold text-fluo-600 hover:underline">
          Create an account
        </Link>
      </p>
    </AuthShell>
  );
}

export function AuthShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-100 px-4">
      <div className="w-full max-w-md">
        <div className="mb-6 flex items-center justify-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-ink-900 text-2xl font-extrabold text-fluo-500">
            H
          </div>
          <div>
            <div className="text-xl font-bold text-ink-900">HERA Copilot</div>
            <div className="text-xs uppercase tracking-wider text-ink-500">
              Risk &amp; safety
            </div>
          </div>
        </div>
        <div className="card">
          <h1 className="mb-6 text-lg font-semibold text-ink-900">{title}</h1>
          {children}
        </div>
      </div>
    </div>
  );
}
