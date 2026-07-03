import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { SignalBar } from "@/components/SignalBar";
import { getOpportunity } from "@/lib/api";

export default async function EtfDetail({ params }: { params: { symbol: string } }) {
  const symbol = params.symbol.toUpperCase();
  const opportunity = await getOpportunity(symbol);

  if (!opportunity) {
    notFound();
  }

  return (
    <AppShell title={`${opportunity.symbol} Intelligence`}>
      <section className="grid gap-4 lg:grid-cols-[1fr_380px]">
        <div className="rounded border border-line bg-panel/90 p-5">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-sm uppercase tracking-wide text-steel">{opportunity.category}</div>
              <div className="text-6xl font-black">{opportunity.symbol}</div>
              <div className="mt-2 text-lg text-slate-200">{opportunity.pattern}</div>
            </div>
            <div className="text-right">
              <div className="text-sm uppercase tracking-wide text-steel">VolEdge Score</div>
              <div className="text-8xl font-black leading-none text-mint">{opportunity.score}</div>
              <div className="mt-3 grid grid-cols-2 gap-4 text-left">
                <Metric label="Confidence" value={String(opportunity.confidenceScore ?? opportunity.accuracy)} tone="mint" />
                <Metric label="Risk" value={String(opportunity.riskScore ?? 50)} tone="amber" />
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-4">
            <Metric label="Latest Price" value={opportunity.currentPrice} />
            <Metric label="Price Change" value={opportunity.priceChangePercent} tone={opportunity.priceTone === "amber" ? "amber" : opportunity.priceTone === "mint" ? "mint" : undefined} />
            <Metric label="Historical Accuracy" value={`${opportunity.accuracy}%`} tone="amber" />
            <Metric label="Matches" value={String(opportunity.matches)} />
            <Metric label="Expected Value" value={opportunity.expectedValue ?? opportunity.expectedReturn} tone="mint" />
            <Metric label="Profit Factor" value={opportunity.profitFactor ?? "1.00"} />
            <Metric label="Avg Loss" value={opportunity.averageLoss ?? "N/A"} tone="amber" />
            <Metric label="Best Window" value={opportunity.window} />
          </div>

          <div className="mt-6 rounded border border-line bg-ink/45 p-4">
            <div className="text-sm uppercase tracking-wide text-steel">AI Explanation</div>
            <p className="mt-2 text-base leading-7 text-slate-200">{opportunity.explanation}</p>
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded border border-line bg-ink/45 p-4">
              <div className="text-xs uppercase text-steel">Market Regime</div>
              <div className="mt-1 text-xl font-bold">{opportunity.marketRegime ?? "Pending"}</div>
              <div className="mt-2 text-sm text-steel">{opportunity.regimeEvidence}</div>
            </div>
            <div className="rounded border border-line bg-ink/45 p-4">
              <div className="text-xs uppercase text-steel">Timeframe Alignment</div>
              <div className="mt-1 text-xl font-bold text-mint">{opportunity.timeframeAlignment ?? 0}/100</div>
            </div>
            <div className="rounded border border-line bg-ink/45 p-4">
              <div className="text-xs uppercase text-steel">Adaptive Weight Focus</div>
              <div className="mt-1 text-sm font-semibold text-slate-200">{opportunity.adaptiveWeightSummary ?? "Pending"}</div>
            </div>
          </div>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <h2 className="text-lg font-bold">Trade Plan</h2>
          <div className="mt-4 grid gap-4">
            <Metric label="Swing Transition" value={opportunity.transitionAction ?? "Hold"} tone={opportunity.transitionStatus === "Arming" ? "mint" : undefined} />
            <Metric label="Transition Score" value={String(opportunity.transitionScore ?? 0)} tone="mint" />
            <Metric label="Latest Price" value={opportunity.currentPrice} />
            <Metric label="Suggested Entry" value={opportunity.entry} />
            <Metric label="Suggested Stop Loss" value={opportunity.stop} />
            <Metric label="Suggested Target" value={opportunity.target} tone="mint" />
            <Metric label="Risk/Reward" value={opportunity.riskReward} tone="amber" />
          </div>
          <button className="mt-5 h-12 w-full rounded bg-mint font-bold text-ink">Manual Approval</button>
        </div>
      </section>

      <section className="mt-5 rounded border border-line bg-panel/80 p-5">
        <h2 className="mb-4 text-lg font-bold">Signal Stack</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            ["Confidence Score", opportunity.confidenceScore ?? opportunity.accuracy],
            ["Institutional Confirmation", opportunity.institutionalScore ?? 0],
            ["Risk Control", 100 - (opportunity.riskScore ?? 50)]
          ].map(([label, value]) => (
            <div key={label} className="rounded border border-line bg-ink/45 p-4">
              <div className="mb-2 flex justify-between text-sm">
                <span className="text-steel">{label}</span>
                <span className="font-bold text-white">{value}</span>
              </div>
              <SignalBar value={Number(value)} />
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
