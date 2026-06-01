// Thin fetch wrapper that always sends cookies and surfaces JSON errors.

export type ApiError = { status: number; detail: string };

async function request<T>(
  method: string,
  path: string,
  body?: unknown
): Promise<T> {
  const res = await fetch(path, {
    method,
    credentials: "include",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return undefined as T;

  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const detail =
      (data && (data.detail as string)) || `Request failed (${res.status})`;
    throw { status: res.status, detail } as ApiError;
  }
  return data as T;
}

export const api = {
  get: <T>(path: string) => request<T>("GET", path),
  post: <T>(path: string, body?: unknown) => request<T>("POST", path, body),
};

export type User = {
  id: number;
  email: string;
  onboarded: boolean;
  consent_given: boolean;
  created_at: string;
};

export type OnboardingProfile = {
  app_name: string;
  app_type: string;
  app_purpose: string;
  target_users: string;
  data_collected: string;
  technology: string;
  has_ai: boolean;
  deployment_markets: string;
  extra_notes: string | null;
  updated_at: string;
};

export type Message = {
  id: number;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
};

export type Conversation = {
  id: number;
  created_at: string;
  messages: Message[];
};

export type ChatStatus = {
  ollama_ok: boolean;
  ollama_status: string;
  model: string;
};
