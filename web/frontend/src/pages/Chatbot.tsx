import { useEffect, useRef, useState } from "react";
import {
  api,
  type ApiError,
  type ChatStatus,
  type Conversation,
  type Message,
} from "../api/client";

export default function Chatbot() {
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [status, setStatus] = useState<ChatStatus | null>(null);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.get<Conversation>("/api/chat/conversation").then(setConversation);
    api.get<ChatStatus>("/api/chat/status").then(setStatus);
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [conversation?.messages.length, sending]);

  async function send() {
    const content = draft.trim();
    if (!content || sending) return;
    setSending(true);
    setError(null);

    // Optimistic user bubble
    const optimistic: Message = {
      id: -Date.now(),
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };
    setConversation((c) =>
      c ? { ...c, messages: [...c.messages, optimistic] } : c
    );
    setDraft("");

    try {
      const res = await api.post<{
        user_message: Message;
        assistant_message: Message;
        conversation_id: number;
      }>("/api/chat/message", { content });
      setConversation((c) => {
        if (!c) return c;
        const withoutOptimistic = c.messages.filter((m) => m.id !== optimistic.id);
        return {
          ...c,
          id: res.conversation_id,
          messages: [...withoutOptimistic, res.user_message, res.assistant_message],
        };
      });
    } catch (err) {
      setError((err as ApiError).detail ?? "Send failed");
      setConversation((c) =>
        c ? { ...c, messages: c.messages.filter((m) => m.id !== optimistic.id) } : c
      );
      setDraft(content);
    } finally {
      setSending(false);
    }
  }

  async function reset() {
    if (!confirm("Start a new conversation? The current one will be archived.")) return;
    const fresh = await api.post<Conversation>("/api/chat/reset");
    setConversation(fresh);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  const messages = conversation?.messages ?? [];

  return (
    <div className="flex h-[calc(100vh-5rem)] flex-col">
      <header className="mb-4 flex items-start justify-between gap-4">
        <div>
          <div className="mb-2 inline-block rounded-full bg-fluo-100 px-3 py-1 text-xs font-bold uppercase tracking-wider text-fluo-700">
            Step 3 — Chatbot
          </div>
          <h1 className="text-3xl font-bold text-ink-900">
            HERA Risk &amp; Safety Copilot
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={status} />
          <button onClick={reset} className="btn-secondary">
            New conversation
          </button>
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
            {sending && <TypingIndicator />}
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
          disabled={sending}
        />
        <button onClick={send} disabled={sending || !draft.trim()} className="btn-primary">
          {sending ? "Thinking…" : "Send"}
        </button>
      </div>
    </div>
  );
}

function Bubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  return (
    <li className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={[
          "max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-fluo-500 text-white"
            : "border border-ink-200 bg-ink-50 text-ink-800",
        ].join(" ")}
      >
        {message.content}
      </div>
    </li>
  );
}

function TypingIndicator() {
  return (
    <li className="flex justify-start">
      <div className="flex items-center gap-1.5 rounded-2xl border border-ink-200 bg-ink-50 px-4 py-3">
        <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
        <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
        <span className="dot h-2 w-2 rounded-full bg-fluo-500" />
      </div>
    </li>
  );
}

function EmptyState() {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center justify-center py-16 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-fluo-100 text-2xl font-extrabold text-fluo-600">
        H
      </div>
      <h3 className="text-lg font-semibold text-ink-900">
        Start a HERA risk reflection
      </h3>
      <p className="mt-1 text-sm text-ink-500">
        Greet the copilot or jump straight in — it already has the context you
        provided during onboarding.
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
