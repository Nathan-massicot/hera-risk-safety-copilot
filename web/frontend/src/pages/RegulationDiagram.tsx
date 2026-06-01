export default function RegulationDiagram() {
  return (
    <div>
      <header className="mb-8">
        <div className="mb-2 inline-block rounded-full bg-ink-200 px-3 py-1 text-xs font-bold uppercase tracking-wider text-ink-700">
          Step 2 — Regulation diagram
        </div>
        <h1 className="text-3xl font-bold text-ink-900">
          HERA taxonomy at a glance
        </h1>
        <p className="mt-2 max-w-2xl text-sm text-ink-600">
          A visual map of the 7 pillars and 37 dimensions covered by the HERA
          taxonomy. The interactive version with click-through to source
          frameworks (EU AI Act, MDR, GDPR, WHO, ISO 82304-2…) is{" "}
          <span className="font-semibold text-fluo-600">coming soon</span>.
        </p>
      </header>

      <div className="card flex items-center justify-center bg-white p-4">
        <object
          data="/api/diagram/hera.svg"
          type="image/svg+xml"
          className="max-h-[70vh] w-full"
          aria-label="HERA taxonomy diagram"
        >
          <p className="text-sm text-ink-500">
            Diagram could not be loaded. Make sure{" "}
            <code className="rounded bg-ink-100 px-1">
              document/HERA_Taxonomy.svg
            </code>{" "}
            exists.
          </p>
        </object>
      </div>

      <div className="mt-6 rounded-md border border-dashed border-ink-300 bg-white px-4 py-3 text-xs text-ink-500">
        TODO — Replace this placeholder with an interactive D3 / SVG renderer
        that lets the developer click each dimension to see source citations,
        example risks, and mitigations.
      </div>
    </div>
  );
}
