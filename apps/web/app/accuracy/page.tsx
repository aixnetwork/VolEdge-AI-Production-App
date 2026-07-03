import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { accuracyBreakdown, opportunities } from "@/lib/mock-data";

const top = opportunities[0];

export default function AccuracyDetail() {
  return (
    <AppShell title="Historical Accuracy Detail">
      <section className="grid gap-4 lg:grid-cols-[360px_1fr]">
        <div className="rounded border border-line bg-panel/90 p-5">
          <div className="text-sm uppercase tracking-wide text-steel">{top.symbol}</div>
          <div className="mt-1 text-7xl font-black text-amber">{top.accuracy}%</div>
          <div className="mt-2 text-slate-200">Calculated from historical OHLCV matching setups.</div>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {accuracyBreakdown.map((item) => (
            <div key={item.label} className="rounded border border-line bg-panel/80 p-5">
              <Metric label={item.label} value={item.value} tone={item.value.includes("+") ? "mint" : "default"} />
              <div className="mt-3 text-sm text-steel">{item.detail}</div>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
