import { AppShell } from "@/components/AppShell";

export default function SettingsPage() {
  return (
    <AppShell title="Settings">
      <section className="grid gap-4 md:grid-cols-2">
        {[
          ["Market Data", "Provider-ready adapter: Polygon, Twelve Data, or Finnhub"],
          ["Authentication", "Supabase Auth"],
          ["Alerts", "Email, push, and in-app routing ready"],
          ["Trading Safety", "Version 1 remains alert-only"]
        ].map(([title, detail]) => (
          <div key={title} className="rounded border border-line bg-panel/80 p-5">
            <h2 className="text-lg font-bold">{title}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-200">{detail}</p>
          </div>
        ))}
      </section>
    </AppShell>
  );
}
