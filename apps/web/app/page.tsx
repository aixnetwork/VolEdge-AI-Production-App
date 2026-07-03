import { Activity, CheckCircle2, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { OpportunityCard } from "@/components/OpportunityCard";
import { SignalBar } from "@/components/SignalBar";
import { getRadarData, getSectorData } from "@/lib/api";
import { productArchitecture, referenceTaglines } from "@/lib/mock-data";

export default async function Home() {
  const [{ top, opportunities, usingFallback }, sectors] = await Promise.all([getRadarData(), getSectorData()]);
  const topTriggers = opportunities.slice(0, 5);
  const swingTransition =
    [...opportunities]
      .filter((item) => item.transitionAction && item.transitionAction !== "Hold" && item.transitionStatus !== "Triggered" && item.transitionStatus !== "Invalidated")
      .sort((a, b) => {
        const statusBoost = (b.transitionStatus === "Arming" ? 100 : 0) - (a.transitionStatus === "Arming" ? 100 : 0);
        return statusBoost || (b.transitionScore ?? 0) - (a.transitionScore ?? 0);
      })[0] ?? top;

  return (
    <AppShell title="Opportunity Radar">
      {usingFallback ? (
        <div className="mb-4 rounded border border-amber/40 bg-amber/10 px-4 py-3 text-sm text-amber">
          Demo data is active. Set NEXT_PUBLIC_API_BASE_URL to connect live API intelligence.
        </div>
      ) : null}
      <section className="mb-5 rounded border border-mint/35 bg-panel/95 p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="text-sm uppercase tracking-wide text-steel">Next Swing Transition</div>
            <div className="mt-1 flex flex-wrap items-end gap-3">
              <span className="text-5xl font-black">{swingTransition.symbol}</span>
              <span className="pb-1 text-2xl font-black text-mint">{swingTransition.transitionAction ?? swingTransition.action}</span>
              <span className="mb-1 rounded border border-line px-2 py-1 text-xs font-bold uppercase text-steel">{swingTransition.transitionStatus ?? "Waiting"}</span>
            </div>
            <p className="mt-3 max-w-3xl text-base leading-7 text-slate-200">{swingTransition.transitionReason ?? swingTransition.explanation}</p>
          </div>
          <div className="grid min-w-[260px] grid-cols-2 gap-4">
            <Metric label="Transition Score" value={String(swingTransition.transitionScore ?? swingTransition.score)} tone="mint" />
            <Metric label="Historical Accuracy" value={`${swingTransition.accuracy}%`} tone="amber" />
            <Metric label="Trigger Gap" value={swingTransition.triggerGap ?? "0.0%"} />
            <Metric label="Trigger Price" value={swingTransition.transitionTrigger ?? swingTransition.entry} />
          </div>
        </div>
      </section>
      <section className="mb-5 rounded border border-line bg-panel/90 p-5">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold">Top 5 Buy/Sell Triggers</h2>
            <div className="mt-1 text-sm text-steel">Extreme volatility ranked by score, trigger side, and directional setup.</div>
          </div>
          <TrendingUp className="text-mint" size={20} />
        </div>
        <div className="grid gap-3 lg:grid-cols-5">
          {topTriggers.map((item) => {
            const actionTone = item.action === "Sell" ? "text-amber" : item.action === "Buy" ? "text-mint" : "text-white";
            const actionBorder = item.action === "Sell" ? "border-amber/50" : item.action === "Buy" ? "border-mint/50" : "border-line";
            return (
              <article key={item.symbol} className={`rounded border ${actionBorder} bg-ink/45 p-4`}>
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-wide text-steel">Rank {item.rank}</div>
                    <div className="mt-1 text-3xl font-black">{item.symbol}</div>
                  </div>
                  <div className={`text-right text-2xl font-black ${actionTone}`}>{item.action}</div>
                </div>
                <div className="mt-3 text-xs uppercase tracking-wide text-steel">{item.triggerSide}</div>
                <div className="mt-1 text-2xl font-bold text-white">{item.entry}</div>
                <div className="mt-3 rounded border border-line bg-panel/60 p-3">
                  <div className="text-xs uppercase tracking-wide text-steel">Latest Price</div>
                  <div className="mt-1 flex items-end justify-between gap-2">
                    <span className="text-2xl font-black text-white">{item.currentPrice}</span>
                    <span className={`text-right text-sm font-bold ${item.priceTone === "amber" ? "text-amber" : item.priceTone === "mint" ? "text-mint" : "text-white"}`}>
                      {item.priceChangePercent}
                    </span>
                  </div>
                </div>
                <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <div className="text-xs uppercase text-steel">VolEdge</div>
                    <div className="font-bold text-mint">{item.score}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase text-steel">Risk</div>
                    <div className="font-bold text-amber">{item.riskScore ?? 50}</div>
                  </div>
                </div>
                <div className="mt-3 truncate text-sm text-steel">{item.marketRegime ?? item.pattern}</div>
              </article>
            );
          })}
        </div>
      </section>
      <section className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
        <div className="rounded border border-line bg-panel/90 p-5 shadow-2xl shadow-black/20">
          <div className="mb-4 flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-sm uppercase tracking-wide text-steel">Top Opportunity</div>
              <div className="mt-1 text-sm font-semibold text-mint">{referenceTaglines.primary}</div>
              <div className="mt-1 flex items-end gap-3">
                <span className="text-5xl font-black sm:text-7xl">{top.symbol}</span>
                <span className="pb-2 text-sm font-semibold text-mint">{top.category}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm uppercase tracking-wide text-steel">VolEdge Score</div>
              <div className="text-7xl font-black leading-none text-mint sm:text-8xl">{top.score}</div>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-4">
            <Metric label="Historical Accuracy" value={`${top.accuracy}%`} tone="amber" />
            <Metric label="Confidence Score" value={String(top.confidenceScore ?? top.accuracy)} tone="mint" />
            <Metric label="Risk Score" value={String(top.riskScore ?? 50)} tone="amber" />
            <Metric label="Historical Matches" value={String(top.matches)} />
          </div>

          <div className="mt-5 grid gap-4 border-t border-line pt-5 md:grid-cols-[1fr_0.85fr]">
            <p className="text-base leading-7 text-slate-200">{top.explanation}</p>
            <div className="grid grid-cols-2 gap-3">
              <Metric label="Latest Price" value={top.currentPrice} />
              <Metric label="Price Change" value={top.priceChangePercent} tone={top.priceTone === "amber" ? "amber" : top.priceTone === "mint" ? "mint" : undefined} />
              <Metric label="Expected Value" value={top.expectedValue ?? top.expectedReturn} tone="mint" />
              <Metric label="Best Window" value={top.window} />
              <Metric label="Trigger" value={top.entry} />
              <Metric label="Invalidation" value={top.stop} />
              <Metric label="Target" value={top.target} tone="mint" />
              <Metric label="Risk/Reward" value={top.riskReward} tone="amber" />
            </div>
          </div>

          <div className="mt-5 grid gap-3 border-t border-line pt-5 md:grid-cols-3">
            <div>
              <div className="text-xs uppercase tracking-wide text-steel">Market Regime</div>
              <div className="mt-1 text-xl font-bold text-white">{top.marketRegime ?? "Pending regime"}</div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wide text-steel">Timeframe Alignment</div>
              <div className="mt-1 text-xl font-bold text-mint">{top.timeframeAlignment ?? 0}/100</div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wide text-steel">Adaptive Weights</div>
              <div className="mt-1 text-sm font-semibold text-slate-200">{top.adaptiveWeightSummary ?? "Pending"}</div>
            </div>
          </div>

          <button className="mt-5 inline-flex h-12 w-full items-center justify-center gap-2 rounded bg-mint px-5 font-bold text-ink sm:w-auto">
            <CheckCircle2 size={19} /> Manual Approval
          </button>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold">Sector Volatility Radar</h2>
            <Activity className="text-mint" size={20} />
          </div>
          <div className="grid gap-3">
            {sectors.map((sector) => (
              <div key={sector.symbol} className="rounded border border-line bg-ink/45 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="font-semibold">{sector.sector}</div>
                    <div className="text-sm text-steel">{sector.symbol} / {sector.signal}</div>
                  </div>
                  <div className="text-3xl font-black text-mint">{sector.score}</div>
                </div>
                <div className="mt-3">
                  <SignalBar value={sector.score} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-5 grid gap-4 xl:grid-cols-[1fr_360px]">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-bold">Top Ranked ETF Opportunities</h2>
            <TrendingUp className="text-mint" size={20} />
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {opportunities.map((item) => (
              <OpportunityCard key={item.symbol} item={item} />
            ))}
          </div>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <h2 className="text-lg font-bold">Portfolio Risk</h2>
          <div className="mt-4 grid gap-4">
            <Metric label="Exposure Bias" value="Volatility Long" tone="amber" />
            <Metric label="Correlation Watch" value="SOXL / QQQ" />
            <Metric label="Platform Mode" value="Decision Support" tone="mint" />
          </div>
          <div className="mt-5 rounded border border-line bg-ink/50 p-4 text-sm leading-6 text-slate-200">
            No automatic trading is enabled. Every recommendation requires manual approval and includes entry, stop, target, risk/reward, historical accuracy, and explanation.
          </div>
        </div>
      </section>

      <section className="mt-5 rounded border border-line bg-panel/80 p-5">
        <h2 className="text-lg font-bold">Intelligence Architecture</h2>
        <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {productArchitecture.map((item) => (
            <div key={item} className="rounded border border-line bg-ink/45 px-4 py-3 text-sm font-semibold text-slate-200">
              {item}
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
