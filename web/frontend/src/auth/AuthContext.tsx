import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api, type User } from "../api/client";

type AuthState = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string, remember: boolean) => Promise<User>;
  logout: () => Promise<void>;
  register: (
    inviteToken: string,
    email: string,
    password: string
  ) => Promise<User>;
  refresh: () => Promise<void>;
};

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const me = await api.get<User>("/api/auth/me");
      setUser(me);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const login = useCallback(
    async (email: string, password: string, remember_me: boolean) => {
      const u = await api.post<User>("/api/auth/login", {
        email,
        password,
        remember_me,
      });
      setUser(u);
      return u;
    },
    []
  );

  const logout = useCallback(async () => {
    await api.post("/api/auth/logout");
    setUser(null);
  }, []);

  const register = useCallback(
    async (invite_token: string, email: string, password: string) => {
      const u = await api.post<User>("/api/auth/register", {
        invite_token,
        email,
        password,
      });
      return u;
    },
    []
  );

  const value = useMemo<AuthState>(
    () => ({ user, loading, login, logout, register, refresh }),
    [user, loading, login, logout, register, refresh]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
