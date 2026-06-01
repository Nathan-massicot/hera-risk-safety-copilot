import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
  requireOnboarded?: boolean;
};

export default function ProtectedRoute({ children, requireOnboarded }: Props) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center text-ink-500">
        Loading…
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (requireOnboarded && !user.onboarded) {
    return <Navigate to="/onboarding" replace />;
  }

  return <>{children}</>;
}
