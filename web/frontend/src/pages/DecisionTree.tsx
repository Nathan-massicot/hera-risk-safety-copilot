import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";

// --- Decision tree types (accumulator model) ------------------------------
type Answer = { value: string; label: string; adds: string[]; next: string };
type Question = {
  id: string;
  text: string;
  rationale?: string;
  type?: string;
  answers: Answer[];
};
type Exit = { id: string; title: string; type: string; summary: string };
type Regulation = {
  id: string;
  title: string;
  jurisdiction?: string;
  summary: string;
  key_articles?: string[];
  official_url?: string;
};
type Tree = {
  title: string;
  subtitle: string;
  start: string;
  questions: Question[];
  exits: Exit[];
  regulations: Regulation[];
};

function jurisdictionClass(j?: string) {
  const v = (j || "").toLowerCase();
  if (v.includes("eu")) return "bg-blue-100 text-blue-700";
  if (v.includes("ch") || v.includes("switz")) return "bg-rose-100 text-rose-700";
  return "bg-ink-100 text-ink-600";
}

export default function DecisionTree() {
  const [tree, setTree] = useState<Tree | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [path, setPath] = useState<Answer[]>([]);

  useEffect(() => {
    api
      .get<Tree>("/api/decision-tree")
      .then(setTree)
      .catch(() => setError("Could not load the decision tree."));
  }, []);

  const byId = useMemo(() => {
    const q: Record<string, Question> = {};
    const x: Record<string, Exit> = {};
    const r: Record<string, Regulation> = {};
    tree?.questions.forEach((it) => (q[it.id] = it));
    tree?.exits.forEach((it) => (x[it.id] = it));
    tree?.regulations.forEach((it) => (r[it.id] = it));
    return { q, x, r };
  }, [tree]);

  // Accumulated regulation ids (in first-seen order) + the ids added by the last step.
  const accumulatedIds = useMemo(() => {
    const seen = new Set<string>();
    const ordered: string[] = [];
    for (const a of path)
      for (const id of a.adds)
        if (!seen.has(id)) {
          seen.add(id);
          ordered.push(id);
        }
    return ordered;
  }, [path]);

  const lastAdded = new Set(path.length ? path[path.length - 1].adds : []);

  if (error)
    return <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>;
  if (!tree)
    return <div className="text-sm text-ink-500">Loading decision tree…</div>;

  const currentId = path.length ? path[path.length - 1].next : tree.start;
  const question = byId.q[currentId];
  const exit = byId.x[currentId];
  const regs = accumulatedIds.map((id) => byId.r[id]).filter(Boolean) as Regulation[];

  return (
    <div className="flex h-[calc(100vh-3rem)] flex-col">
      <header className="mb-4">
        <div className="mb-2 inline-block rounded-full bg-ink-200 px-3 py-1 text-xs font-bold uppercase tracking-wider text-ink-700">
          Reference — Decision tree
        </div>
        <h1 className="text-2xl font-bold text-ink-900">{tree.title}</h1>
        <p className="mt-1 text-sm text-ink-500">{tree.subtitle}</p>
      </header>

      <div className="grid flex-1 gap-6 overflow-hidden lg:grid-cols-5">
        {/* Main: current question or exit */}
        <div className="flex flex-col overflow-y-auto lg:col-span-3">
          {question ? (
            <QuestionCard
              question={question}
              step={path.length + 1}
              onAnswer={(a) => setPath((p) => [...p, a])}
            />
          ) : exit ? (
            <ExitCard exit={exit} regCount={regs.length} />
          ) : (
            <div className="card text-sm text-ink-500">
              Unknown node <code>{currentId}</code>.
            </div>
          )}

          <div className="mt-4 flex items-center gap-2">
            <button
              onClick={() => setPath((p) => p.slice(0, -1))}
              disabled={path.length === 0}
              className="btn-secondary"
            >
              ← Back
            </button>
            <button
              onClick={() => setPath([])}
              disabled={path.length === 0}
              className="btn-ghost"
            >
              Restart
            </button>
            <span className="ml-auto text-xs text-ink-400">
              {regs.length} regulation{regs.length === 1 ? "" : "s"} so far
            </span>
          </div>
        </div>

        {/* Side panel: stacked regulations */}
        <aside className="flex flex-col overflow-hidden rounded-xl border border-ink-200 bg-white lg:col-span-2">
          <div className="border-b border-ink-200 px-4 py-3">
            <h2 className="text-sm font-bold text-ink-900">
              Applicable regulations{" "}
              <span className="text-fluo-600">({regs.length})</span>
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            {regs.length === 0 ? (
              <p className="text-sm italic text-ink-400">
                Answer the questions — every applicable regulation will stack here, with
                its scope and key articles.
              </p>
            ) : (
              <ul className="space-y-3">
                {regs.map((r) => (
                  <RegCard key={r.id} reg={r} highlight={lastAdded.has(r.id)} />
                ))}
              </ul>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

function QuestionCard({
  question,
  step,
  onAnswer,
}: {
  question: Question;
  step: number;
  onAnswer: (a: Answer) => void;
}) {
  return (
    <div className="card">
      <div className="mb-1 text-xs font-bold uppercase tracking-wide text-fluo-600">
        Step {step}
      </div>
      <h2 className="text-lg font-bold text-ink-900">{question.text}</h2>

      <div className="mt-4 space-y-2">
        {question.answers.map((a) => (
          <button
            key={a.value}
            onClick={() => onAnswer(a)}
            className="group flex w-full items-center justify-between gap-3 rounded-lg border border-ink-200 px-4 py-3 text-left text-sm font-medium text-ink-800 transition-colors hover:border-fluo-400 hover:bg-fluo-50"
          >
            <span>{a.label}</span>
            <span className="flex items-center gap-2 text-xs text-ink-400">
              {a.adds.length > 0 && (
                <span className="rounded-full bg-ink-100 px-2 py-0.5 font-semibold group-hover:bg-fluo-100 group-hover:text-fluo-700">
                  +{a.adds.length}
                </span>
              )}
              <span className="text-ink-300 group-hover:text-fluo-500">→</span>
            </span>
          </button>
        ))}
      </div>

      {question.rationale && (
        <details className="mt-4 rounded-md bg-ink-50 px-3 py-2 text-xs text-ink-500">
          <summary className="cursor-pointer select-none font-semibold text-ink-600">
            Why we ask this
          </summary>
          <p className="mt-1 leading-relaxed">{question.rationale}</p>
        </details>
      )}
    </div>
  );
}

function ExitCard({ exit, regCount }: { exit: Exit; regCount: number }) {
  const isRecap = exit.type === "recap";
  return (
    <div className={`card border-t-4 ${isRecap ? "border-t-fluo-500" : "border-t-ink-300"}`}>
      <div className="mb-1 text-xs font-bold uppercase tracking-wide text-fluo-600">
        {isRecap ? "Result" : "End"}
      </div>
      <h2 className="text-lg font-bold text-ink-900">{exit.title}</h2>
      <p className="mt-2 text-sm leading-relaxed text-ink-600">{exit.summary}</p>
      {isRecap && (
        <p className="mt-3 text-sm font-medium text-ink-700">
          {regCount} regulation{regCount === 1 ? "" : "s"} apply to your app — see the panel
          on the right. Use <span className="font-semibold">Back</span> to revise an answer
          or <span className="font-semibold">Restart</span> to begin again.
        </p>
      )}
    </div>
  );
}

function RegCard({ reg, highlight }: { reg: Regulation; highlight: boolean }) {
  return (
    <li
      className={`rounded-lg border p-3 transition-colors ${
        highlight ? "border-fluo-300 bg-fluo-50" : "border-ink-200"
      }`}
    >
      <div className="mb-1 flex items-start justify-between gap-2">
        <span className="text-sm font-semibold text-ink-900">{reg.title}</span>
        {reg.jurisdiction && (
          <span
            className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${jurisdictionClass(
              reg.jurisdiction
            )}`}
          >
            {reg.jurisdiction}
          </span>
        )}
      </div>
      <p className="text-xs leading-relaxed text-ink-600">{reg.summary}</p>
      {reg.key_articles && reg.key_articles.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {reg.key_articles.map((art, i) => (
            <span
              key={i}
              className="rounded bg-ink-100 px-1.5 py-0.5 text-[10px] font-medium text-ink-600"
            >
              {art}
            </span>
          ))}
        </div>
      )}
      {reg.official_url && (
        <a
          href={reg.official_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-block text-xs font-medium text-fluo-600 hover:underline"
        >
          Official text ↗
        </a>
      )}
    </li>
  );
}
