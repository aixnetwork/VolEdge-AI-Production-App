import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { SignalBar } from "@/components/SignalBar";
import { getSectorData } from "@/lib/api";

export default async function SectorRadar() {
  const sectors = await getSectorData();

  return (
    <AppShell title="Sector Volatility Radar">
      <section className="grid gap-4 md:grid-cols-2">
        {sectors.map((sector) => (
          <article key={sector.symbol} className="rounded border border-line bg-panel/80 p-5">
            <div className="flex items-start justify-between">
              <div>
                <div className="text-sm uppercase tracking-wide text-steel">{sector.sector}</div>
                <div className="text-4xl font-black">{sector.symbol}</div>
              </div>
              <div className="text-right">
                <div className="text-xs uppercase text-steel">Volatility</div>
                <div className="text-6xl font-black text-mint">{sector.score}</div>
              </div>
            </div>
            <div className="mt-4">
              <SignalBar value={sector.score} />
            </div>
            <div className="mt-5 grid grid-cols-2 gap-4">
              <Metric label="Signal" value={sector.signal} tone={sector.signal === "Watch" ? "amber" : "mint"} />
              <Metric label="Relative Strength" value={sector.strength} />
            </div>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
