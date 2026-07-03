import { AppShell } from "@/components/AppShell";
import { SignalBar } from "@/components/SignalBar";
import { getRiskData } from "@/lib/api";

export default async function PortfolioRisk() {
  const riskExposures = await getRiskData();

  return (
    <AppShell title="Portfolio Risk">
      <section className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <div className="grid gap-3">
          {riskExposures.map((risk) => (
            <div key={risk.label} className="rounded border border-line bg-panel/80 p-5">
              <div className="mb-3 flex items-center justify-between">
                <div>
                  <div className="text-lg font-bold">{risk.label}</div>
                  <div className="text-sm text-steel">{risk.tone}</div>
                </div>
                <div className="text-4xl font-black text-mint">{risk.value}</div>
              </div>
              <SignalBar value={Number(risk.value.replace("%", ""))} />
            </div>
          ))}
        </div>
        <div className="rounded border border-line bg-panel/90 p-5">
          <h2 className="text-lg font-bold">Risk Guardrails</h2>
          <div className="mt-4 grid gap-3 text-sm text-slate-200">
            <div className="rounded border border-line bg-ink/45 p-3">No automatic orders</div>
            <div className="rounded border border-line bg-ink/45 p-3">Manual approval required</div>
            <div className="rounded border border-line bg-ink/45 p-3">Stop loss required on every alert</div>
          </div>
        </div>
      </section>
    </AppShell>
  );
}
