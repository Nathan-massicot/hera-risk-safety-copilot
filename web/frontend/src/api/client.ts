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

// --- Streaming chat (Server-Sent Events) ----------------------------------

export type Citation = {
  cite: string;
  title: string;
  jurisdiction: string | null;
  score: number;
  snippet: string;
};

export type StreamMode = "chat" | "report";

export type StreamMeta = {
  conversation_id: number;
  user_message: Message;
  citations: Citation[];
};

export type StreamHandlers = {
  onMeta?: (meta: StreamMeta) => void;
  onToken?: (chunk: string) => void;
  onDone?: (info: { assistant_message_id: number | null }) => void;
  onError?: (detail: string) => void;
};

function dispatchEvent(raw: string, h: StreamHandlers) {
  let event: string | null = null;
  const dataLines: string[] = [];
  for (const line of raw.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).replace(/^ /, ""));
  }
  if (dataLines.length === 0) return;
  let data: unknown;
  try {
    data = JSON.parse(dataLines.join("\n"));
  } catch {
    return;
  }
  const d = data as Record<string, unknown>;
  if (event === "meta") h.onMeta?.(d as unknown as StreamMeta);
  else if (event === "done") h.onDone?.(d as { assistant_message_id: number | null });
  else if (event === "error") h.onError?.((d.detail as string) ?? "Stream error");
  else h.onToken?.((d.t as string) ?? "");
}

/** POST /api/chat/stream and drive the handlers as SSE events arrive. */
export async function streamChat(
  body: { content?: string; mode?: StreamMode },
  handlers: StreamHandlers,
  signal?: AbortSignal
): Promise<void> {
  let res: Response;
  try {
    res = await fetch("/api/chat/stream", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal,
    });
  } catch (e) {
    handlers.onError?.((e as Error).message ?? "Network error");
    return;
  }

  if (!res.ok || !res.body) {
    let detail = `Request failed (${res.status})`;
    try {
      const j = await res.json();
      detail = (j.detail as string) ?? detail;
    } catch {
      /* ignore */
    }
    handlers.onError?.(detail);
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx: number;
    while ((idx = buf.indexOf("\n\n")) !== -1) {
      const chunk = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      if (chunk.trim()) dispatchEvent(chunk, handlers);
    }
  }
}

// --- HERA taxonomy (interactive diagram) ----------------------------------

export type HeraSource = { cite: string; title: string; why: string };

export type HeraDimension = {
  id: string;
  name: string;
  description: string;
  reflection_questions: string[];
  example_risks: string[];
  example_mitigations: string[];
  sources: HeraSource[];
};

export type HeraPillar = {
  id: string;
  name: string;
  focus: string;
  description: string;
  dimensions: HeraDimension[];
};

export type HeraTaxonomy = {
  name: string;
  full_name: string;
  version: string;
  description: string;
  sources: string[];
  pillars: HeraPillar[];
};
