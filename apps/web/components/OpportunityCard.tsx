import Link from "next/link";
import { Metric } from "@/components/Metric";
import type { Opportunity } from "@/lib/mock-data";

export function OpportunityCard({ item }: { item: Opportunity }) {
  const actionColor = item.action === "Sell" ? "text-amber" : item.action === "Buy" ? "text-mint" : "text-white";
  return (
    <article className="rounded border border-line bg-panel/80 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm text-steel">Rank {item.rank}</div>
          <h3 className="text-3xl font-black">{item.symbol}</h3>
          <div className="text-sm text-steel">{item.pattern}</div>
          <div className={`mt-2 text-sm font-bold uppercase ${actionColor}`}>{item.action} / {item.triggerSide}</div>
        </div>
        <div className="text-right">
          <div className="text-xs uppercase text-steel">Score</div>
          <div className="text-5xl font-black text-mint">{item.score}</div>
        </div>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-2">
        <Metric label="Accuracy" value={`${item.accuracy}%`} tone="amber" />
        <Metric label="Confidence" value={item.confidence} tone="mint" />
        <Metric label="Risk/Reward" value={item.riskReward} />
      </div>
      <Link href={`/etf/${item.symbol}`} className="mt-4 inline-flex h-10 items-center rounded bg-mint px-4 text-sm font-bold text-ink">
        Open Detail
      </Link>
    </article>
  );
}
