import { useEffect, useMemo, useRef, useState } from "react";
import {
  api,
  streamChat,
  type ChatStatus,
  type Citation,
  type Conversation,
  type Message,
  type StreamMode,
} from "../api/client";

type ChatMessage = Message & {
  citations?: Citation[];
  streaming?: boolean;
};

export default function Chatbot() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<ChatStatus | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api
      .get<Conversation>("/api/chat/conversation")
      .then((c) => setMessages(c.messages))
      .catch(() => undefined);
    api
      .get<ChatStatus>("/api/chat/status")
      .then(setStatus)
      .catch(() => undefined);
  }, []);

  // Auto-scroll as messages grow or tokens stream in.
  const streamLen = useMemo(
    () => messages.reduce((n, m) => n + m.content.length, 0),
    [messages]
  );
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages.length, streamLen]);

  async function run(mode: StreamMode, content?: string) {
    if (busy) return;
    if (mode === "chat" && !content?.trim()) return;
    setBusy(true);
    setError(null);

    const stamp = Date.now();
    const tempUserId = -stamp;
    const tempAsstId = -(stamp + 1);
    const userContent =
      mode === "report"
        ? "Generate a structured HERA risk report"
        : (content ?? "").trim();

    setMessages((ms) => [
      ...ms,
      {
        id: tempUserId,
        role: "user",
        content: userContent,
        created_at: new Date(stamp).toISOString(),
      },
      {
        id: tempAsstId,
        role: "assistant",
        content: "",
        created_at: new Date(stamp + 1).toISOString(),
        streaming: true,
      },
    ]);
    if (mode === "chat") setDraft("");

    const patch = (id: number, fn: (m: ChatMessage) => ChatMessage) =>
      setMessages((ms) => ms.map((m) => (m.id === id ? fn(m) : m)));

    await streamChat(
      { content, mode },
      {
        onMeta: (meta) => {
          patch(tempUserId, (m) => ({ ...m, ...meta.user_message }));
          patch(tempAsstId, (m) => ({ ...m, citations: meta.citations }));
        },
        onToken: (chunk) => {
          patch(tempAsstId, (m) => ({ ...m, content: m.content + chunk }));
        },
        onDone: (info) => {
          patch(tempAsstId, (m) => ({
            ...m,
            streaming: false,
            id: info.assistant_message_id ?? m.id,
          }));
        },
        onError: (detail) => {
          setError(detail);
          setMessages((ms) => ms.filter((m) => m.id !== tempAsstId));
          if (mode === "chat") setDraft(userContent);
        },
      }
    );
    setBusy(false);
  }

  async function reset() {
    if (busy) return;
    if (!confirm("Start a new conversation? The current one will be archived.")) return;
    await api.post<Conversation>("/api/chat/reset");
    setMessages([]);
    setError(null);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      run("chat", draft);
    }
  }

  return (
    <div className="flex h-[calc(100vh-3rem)] flex-col">
      <header className="mb-4 flex items-start justify-between gap-4">
        <div>
          <div className="mb-2 inline-block rounded-full bg-fluo-100 px-3 py-1 text-xs font-bold uppercase tracking-wider text-fluo-700">
            HERA Chatbot
          </div>
          <h1 className="text-3xl font-bold text-ink-900">
            HERA Risk &amp; Safety Copilot
          </h1>
          <p className="mt-1 text-sm text-ink-500">
            RAG-grounded · cites the regulation it relies on · ask anything or let it
            probe your app.
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <StatusBadge status={status} />
          <div className="flex items-center gap-2">
            <button
              onClick={() => run("report")}
              disabled={busy || messages.length === 0}
              className="btn-secondary"
              title="Synthesize a structured HERA risk report from this conversation"
            >
              📋 Risk report
            </button>
            <button onClick={reset} disabled={busy} className="btn-ghost">
              New conversation
            </button>
          </div>
        </div>
      </header>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto rounded-xl border border-ink-200 bg-white p-6"
      >
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <ul className="space-y-5">
            {messages.map((m) => (
              <Bubble key={m.id} message={m} />
            ))}
          </ul>
        )}
      </div>

      {error && (
        <div className="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mt-3 flex items-end gap-2 rounded-xl border border-ink-200 bg-white p-3">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={onKeyDown}
          rows={2}
          className="flex-1 resize-none border-0 bg-transparent px-2 py-2 text-sm text-ink-900 focus:outline-none"
          placeholder="Describe your app or answer the copilot's question…  (Enter to send · Shift+Enter for newline)"
          disabled={busy}
        />
        <button
          onClick={() => run("chat", draft)}
          disabled={busy || !draft.trim()}
          className="btn-primary"
        >
          {busy ? "Streaming…" : "Send"}
        </button>
      </div>
    </div>
  );
}

function Bubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const showTyping = message.streaming && message.content === "";
  return (
    <li className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex max-w-[82%] flex-col gap-2 ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={[
            "rounded-2xl px-4 py-3 text-sm leading-relaxed",
            isUser
              ? "bg-fluo-500 text-white"
              : "border border-ink-200 bg-ink-50 text-ink-800",
          ].join(" ")}
        >
          {showTyping ? (
            <TypingDots />
          ) : (
            <div className="whitespace-pre-wrap">
              <Rich text={message.content} />
              {message.streaming && <Caret />}
            </div>
          )}
        </div>
        {!isUser && message.citations && message.citations.length > 0 && (
          <Sources citations={message.citations} />
        )}
      </div>
    </li>
  );
}

function Sources({ citations }: { citations: Citation[] }) {
  return (
    <details className="w-full rounded-lg border border-ink-200 bg-white px-3 py-2 text-xs">
      <summary className="cursor-pointer select-none font-semibold text-ink-600">
        Sources retrieved ({citations.length})
      </summary>
      <ul className="mt-2 space-y-2">
        {citations.map((c, i) => (
          <li key={i} className="border-l-2 border-fluo-300 pl-2">
            <div className="flex items-center gap-2">
              <span className="font-medium text-ink-700">{c.title}</span>
              <span className="text-ink-400">· {c.score.toFixed(2)}</span>
            </div>
            <p className="mt-0.5 text-ink-500">{c.snippet}…</p>
          </li>
        ))}
      </ul>
    </details>
  );
}

/** Minimal markdown: render **bold** segments; newlines preserved by pre-wrap parent. */
function Rich({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**") ? (
          <strong key={i} className="font-semibold">
            {p.slice(2, -2)}
          </strong>
        ) : (
          <span key={i}>{p}</span>
        )
      )}
    </>
  );
}

function Caret() {
  return <span className="ml-0.5 inline-block h-4 w-1.5 animate-pulse bg-fluo-500 align-middle" />;
}

function TypingDots() {
  return (
    <div className="flex items-center gap-1.5">
      <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
      <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
      <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
    </div>
  );
}

function EmptyState() {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center justify-center py-16 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-fluo-100 text-2xl font-extrabold text-fluo-600">
        H
      </div>
      <h3 className="text-lg font-semibold text-ink-900">Start a HERA risk reflection</h3>
      <p className="mt-1 text-sm text-ink-500">
        Greet the copilot or jump straight in — it already has the context you provided
        during onboarding, and grounds its answers in the regulatory corpus. When you're
        done, hit <span className="font-semibold text-fluo-600">Risk report</span> for a
        structured deliverable.
      </p>
    </div>
  );
}

function StatusBadge({ status }: { status: ChatStatus | null }) {
  if (!status) {
    return (
      <span className="rounded-full bg-ink-200 px-3 py-1 text-xs font-medium text-ink-600">
        Checking model…
      </span>
    );
  }
  const ok = status.ollama_ok;
  return (
    <span
      title={status.ollama_status}
      className={[
        "rounded-full px-3 py-1 text-xs font-semibold",
        ok ? "bg-emerald-100 text-emerald-700" : "bg-red-100 text-red-700",
      ].join(" ")}
    >
      {ok ? `${status.model} online` : "Ollama offline"}
    </span>
  );
}
