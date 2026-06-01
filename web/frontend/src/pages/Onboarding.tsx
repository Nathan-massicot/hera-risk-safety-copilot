import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, type ApiError, type OnboardingProfile } from "../api/client";
import { useAuth } from "../auth/AuthContext";

const APP_TYPES = [
  "Symptom tracker",
  "Medication reminder",
  "Teleconsultation",
  "Mental health / chatbot",
  "Remote monitoring",
  "AI triage",
  "Wellness / fitness",
  "Pregnancy tracker",
  "Chronic-disease management",
  "Other",
];

const empty: OnboardingProfileInput = {
  app_name: "",
  app_type: "",
  app_purpose: "",
  target_users: "",
  data_collected: "",
  technology: "",
  has_ai: false,
  deployment_markets: "",
  extra_notes: "",
  consent: false,
};

type OnboardingProfileInput = {
  app_name: string;
  app_type: string;
  app_purpose: string;
  target_users: string;
  data_collected: string;
  technology: string;
  has_ai: boolean;
  deployment_markets: string;
  extra_notes: string;
  consent: boolean;
};

export default function Onboarding() {
  const { refresh, user } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState<OnboardingProfileInput>(empty);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    api
      .get<OnboardingProfile | null>("/api/onboarding")
      .then((p) => {
        if (p) {
          setForm({
            app_name: p.app_name,
            app_type: p.app_type,
            app_purpose: p.app_purpose,
            target_users: p.target_users,
            data_collected: p.data_collected,
            technology: p.technology,
            has_ai: p.has_ai,
            deployment_markets: p.deployment_markets,
            extra_notes: p.extra_notes ?? "",
            consent: user?.consent_given ?? false,
          });
        }
      })
      .finally(() => setLoaded(true));
  }, [user?.consent_given]);

  function update<K extends keyof OnboardingProfileInput>(
    key: K,
    value: OnboardingProfileInput[K]
  ) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await api.post<OnboardingProfile>("/api/onboarding", form);
      await refresh();
      navigate("/chat");
    } catch (err) {
      setError((err as ApiError).detail ?? "Failed to save profile");
    } finally {
      setSubmitting(false);
    }
  }

  if (!loaded) {
    return <div className="text-ink-500">Loading…</div>;
  }

  return (
    <div>
      <header className="mb-8">
        <div className="mb-2 inline-block rounded-full bg-fluo-100 px-3 py-1 text-xs font-bold uppercase tracking-wider text-fluo-700">
          Step 1 — Onboarding
        </div>
        <h1 className="text-3xl font-bold text-ink-900">Tell us about your app</h1>
        <p className="mt-2 max-w-2xl text-sm text-ink-600">
          The HERA Copilot uses this context to skip basic questions and dive
          straight into the most relevant ethical and regulatory dimensions.
          You can update this profile at any time.
        </p>
      </header>

      <form onSubmit={onSubmit} className="space-y-6">
        <section className="card space-y-4">
          <h2 className="text-base font-semibold text-ink-900">App basics</h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="label">App name</label>
              <input
                className="input"
                value={form.app_name}
                onChange={(e) => update("app_name", e.target.value)}
                required
              />
            </div>
            <div>
              <label className="label">App type</label>
              <select
                className="input"
                value={form.app_type}
                onChange={(e) => update("app_type", e.target.value)}
                required
              >
                <option value="">Select…</option>
                {APP_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="label">Purpose / problem solved</label>
            <textarea
              className="input min-h-[80px]"
              value={form.app_purpose}
              onChange={(e) => update("app_purpose", e.target.value)}
              required
              placeholder="e.g. Help type-2 diabetic patients log meals and glucose readings…"
            />
          </div>
        </section>

        <section className="card space-y-4">
          <h2 className="text-base font-semibold text-ink-900">Users & data</h2>
          <div>
            <label className="label">Target users</label>
            <textarea
              className="input min-h-[60px]"
              value={form.target_users}
              onChange={(e) => update("target_users", e.target.value)}
              required
              placeholder="Adults newly diagnosed with type-2 diabetes; clinicians for monitoring…"
            />
          </div>
          <div>
            <label className="label">Data collected</label>
            <textarea
              className="input min-h-[60px]"
              value={form.data_collected}
              onChange={(e) => update("data_collected", e.target.value)}
              required
              placeholder="Email, weight, glucose readings, photos of meals…"
            />
          </div>
        </section>

        <section className="card space-y-4">
          <h2 className="text-base font-semibold text-ink-900">Tech & deployment</h2>
          <div>
            <label className="label">Technology stack</label>
            <textarea
              className="input min-h-[60px]"
              value={form.technology}
              onChange={(e) => update("technology", e.target.value)}
              required
              placeholder="React Native frontend, Node backend, Postgres, AWS eu-central-1…"
            />
          </div>
          <label className="flex items-center gap-2 text-sm text-ink-700">
            <input
              type="checkbox"
              checked={form.has_ai}
              onChange={(e) => update("has_ai", e.target.checked)}
              className="h-4 w-4 accent-fluo-500"
            />
            This app uses AI / machine learning
          </label>
          <div>
            <label className="label">Deployment markets</label>
            <input
              className="input"
              value={form.deployment_markets}
              onChange={(e) => update("deployment_markets", e.target.value)}
              required
              placeholder="EU (Germany, France), Switzerland…"
            />
          </div>
          <div>
            <label className="label">Anything else we should know? (optional)</label>
            <textarea
              className="input min-h-[60px]"
              value={form.extra_notes}
              onChange={(e) => update("extra_notes", e.target.value)}
              placeholder="Existing certifications, regulatory questions you already have, etc."
            />
          </div>
        </section>

        <section className="card space-y-3 border-fluo-200 bg-fluo-50/40">
          <h2 className="text-base font-semibold text-ink-900">
            Research consent
          </h2>
          <p className="text-sm text-ink-700">
            HERA Copilot is part of an MSc research project at BFH. By ticking
            the box below you agree that your conversations may be stored
            locally for research purposes (no third-party sharing without your
            additional consent). You can request deletion at any time.
          </p>
          <label className="flex items-start gap-2 text-sm text-ink-800">
            <input
              type="checkbox"
              checked={form.consent}
              onChange={(e) => update("consent", e.target.checked)}
              className="mt-0.5 h-4 w-4 accent-fluo-500"
              required
            />
            I consent to the local storage of my conversations for the purpose
            of this research project.
          </label>
        </section>

        {error && (
          <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="flex items-center justify-end gap-3">
          <button
            type="submit"
            disabled={submitting || !form.consent}
            className="btn-primary"
          >
            {submitting ? "Saving…" : "Save and continue to chatbot"}
          </button>
        </div>
      </form>
    </div>
  );
}
