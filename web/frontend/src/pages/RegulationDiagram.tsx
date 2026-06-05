import { useEffect, useState } from "react";
import {
  api,
  type HeraDimension,
  type HeraPillar,
  type HeraTaxonomy,
} from "../api/client";

// Per-pillar accent classes (full literal strings so Tailwind's JIT keeps them).
const PILLAR_STYLE: Record<string, { bar: string; chip: string; dot: string }> = {
  P1: { bar: "border-t-rose-400", chip: "bg-rose-100 text-rose-700", dot: "bg-rose-400" },
  P2: { bar: "border-t-blue-400", chip: "bg-blue-100 text-blue-700", dot: "bg-blue-400" },
  P3: { bar: "border-t-violet-400", chip: "bg-violet-100 text-violet-700", dot: "bg-violet-400" },
  P4: { bar: "border-t-amber-400", chip: "bg-amber-100 text-amber-700", dot: "bg-amber-400" },
  P5: { bar: "border-t-cyan-400", chip: "bg-cyan-100 text-cyan-700", dot: "bg-cyan-400" },
  P6: { bar: "border-t-emerald-400", chip: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-400" },
  P7: { bar: "border-t-fluo-500", chip: "bg-fluo-100 text-fluo-700", dot: "bg-fluo-500" },
};

const fallbackStyle = { bar: "border-t-ink-300", chip: "bg-ink-100 text-ink-700", dot: "bg-ink-400" };
const styleFor = (pid: string) => PILLAR_STYLE[pid] ?? fallbackStyle;

type Selection = { pillar: HeraPillar; dim: HeraDimension } | null;

export default function RegulationDiagram() {
  const [taxonomy, setTaxonomy] = useState<HeraTaxonomy | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Selection>(null);

  useEffect(() => {
    api
      .get<HeraTaxonomy>("/api/taxonomy")
      .then(setTaxonomy)
      .catch(() => setError("Could not load the HERA taxonomy."));
  }, []);

  useEffect(() => {
    if (!selected) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selected]);

  const nDims = taxonomy
    ? taxonomy.pillars.reduce((n, p) => n + p.dimensions.length, 0)
    : 0;

  return (
    <div>
      <header className="mb-6">
        <div className="mb-2 inline-block rounded-full bg-ink-200 px-3 py-1 text-xs font-bold uppercase tracking-wider text-ink-700">
          HERA taxonomy
        </div>
        <h1 className="text-3xl font-bold text-ink-900">HERA taxonomy explorer</h1>
        <p className="mt-2 max-w-2xl text-sm text-ink-600">
          The {taxonomy ? taxonomy.pillars.length : 7} pillars and {nDims || 38}{" "}
          dimensions of the HERA framework.{" "}
          <span className="font-semibold text-fluo-600">Click any dimension</span> to see
          its reflection questions, example risks, mitigations, and the regulatory sources
          that apply.
        </p>
      </header>

      {error && (
        <div className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>
      )}

      {!taxonomy && !error ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="h-48 animate-pulse rounded-xl bg-ink-100" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {taxonomy?.pillars.map((pillar) => {
            const st = styleFor(pillar.id);
            return (
              <section
                key={pillar.id}
                className={`flex flex-col rounded-xl border border-ink-200 border-t-4 bg-white p-4 shadow-sm ${st.bar}`}
              >
                <div className="mb-3">
                  <div className="flex items-center gap-2">
                    <span className={`rounded px-1.5 py-0.5 text-xs font-bold ${st.chip}`}>
                      {pillar.id}
                    </span>
                    <h2 className="text-sm font-bold leading-tight text-ink-900">
                      {pillar.name}
                    </h2>
                  </div>
                  <p className="mt-1 text-xs italic text-ink-400">{pillar.focus}</p>
                </div>
                <ul className="space-y-1.5">
                  {pillar.dimensions.map((dim) => (
                    <li key={dim.id}>
                      <button
                        onClick={() => setSelected({ pillar, dim })}
                        className="group flex w-full items-center gap-2 rounded-md border border-ink-100 px-2 py-1.5 text-left text-xs transition-colors hover:border-fluo-300 hover:bg-fluo-50"
                      >
                        <span className="font-mono text-[10px] font-semibold text-ink-400 group-hover:text-fluo-600">
                          {dim.id}
                        </span>
                        <span className="flex-1 text-ink-700">{dim.name}</span>
                        {dim.sources.length > 0 && (
                          <span
                            title={`${dim.sources.length} regulatory source(s)`}
                            className="rounded-full bg-ink-100 px-1.5 text-[10px] font-semibold text-ink-500 group-hover:bg-fluo-100 group-hover:text-fluo-700"
                          >
                            {dim.sources.length}
                          </span>
                        )}
                      </button>
                    </li>
                  ))}
                </ul>
              </section>
            );
          })}
        </div>
      )}

      {selected && (
        <DetailPanel selection={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}

function DetailPanel({
  selection,
  onClose,
}: {
  selection: { pillar: HeraPillar; dim: HeraDimension };
  onClose: () => void;
}) {
  const { pillar, dim } = selection;
  const st = styleFor(pillar.id);
  return (
    <div className="fixed inset-0 z-40 flex justify-end">
      <div
        className="absolute inset-0 bg-ink-900/30 backdrop-blur-[1px]"
        onClick={onClose}
        aria-hidden
      />
      <aside className="relative z-10 flex h-full w-full max-w-md flex-col overflow-y-auto border-l border-ink-200 bg-white shadow-2xl">
        <div className="sticky top-0 z-10 border-b border-ink-200 bg-white px-6 py-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="mb-1 flex items-center gap-2">
                <span className={`rounded px-1.5 py-0.5 text-xs font-bold ${st.chip}`}>
                  {pillar.id} · {pillar.name}
                </span>
              </div>
              <h2 className="text-lg font-bold leading-tight text-ink-900">
                <span className="font-mono text-sm text-ink-400">{dim.id}</span>{" "}
                {dim.name}
              </h2>
            </div>
            <button
              onClick={onClose}
              className="rounded-md p-1 text-ink-400 hover:bg-ink-100 hover:text-ink-700"
              aria-label="Close"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="space-y-6 px-6 py-5">
          <p className="text-sm leading-relaxed text-ink-700">{dim.description}</p>

          <Section title="Reflection questions" dot={st.dot}>
            <ul className="space-y-2">
              {dim.reflection_questions.map((q, i) => (
                <li key={i} className="flex gap-2 text-sm text-ink-700">
                  <span className="text-ink-400">{i + 1}.</span>
                  <span>{q}</span>
                </li>
              ))}
            </ul>
          </Section>

          <Section title="Example risks" dot={st.dot}>
            <ul className="space-y-2">
              {dim.example_risks.map((r, i) => (
                <li
                  key={i}
                  className="flex gap-2 rounded-md bg-red-50 px-3 py-2 text-sm text-red-800"
                >
                  <span aria-hidden>⚠</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </Section>

          <Section title="Example mitigations" dot={st.dot}>
            <ul className="space-y-2">
              {dim.example_mitigations.map((m, i) => (
                <li
                  key={i}
                  className="flex gap-2 rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800"
                >
                  <span aria-hidden>✓</span>
                  <span>{m}</span>
                </li>
              ))}
            </ul>
          </Section>

          <Section title={`Regulatory sources (${dim.sources.length})`} dot={st.dot}>
            {dim.sources.length === 0 ? (
              <p className="text-sm italic text-ink-400">
                No regulatory source mapped to this dimension yet.
              </p>
            ) : (
              <ul className="space-y-3">
                {dim.sources.map((s, i) => (
                  <li key={i} className="rounded-md border border-ink-200 p-3">
                    <div className="mb-1 flex items-start gap-2">
                      <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${st.dot}`} />
                      <span className="text-sm font-semibold text-ink-800">{s.title}</span>
                    </div>
                    <p className="pl-3.5 text-sm text-ink-600">{s.why}</p>
                  </li>
                ))}
              </ul>
            )}
          </Section>
        </div>
      </aside>
    </div>
  );
}

function Section({
  title,
  dot,
  children,
}: {
  title: string;
  dot: string;
  children: React.ReactNode;
}) {
  return (
    <section>
      <h3 className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-ink-500">
        <span className={`h-2 w-2 rounded-full ${dot}`} />
        {title}
      </h3>
      {children}
    </section>
  );
}
