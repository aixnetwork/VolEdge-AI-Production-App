import { AppShell } from "@/components/AppShell";
import { OpportunityCard } from "@/components/OpportunityCard";
import { getRadarData } from "@/lib/api";

export default async function Watchlist() {
  const { opportunities } = await getRadarData();

  return (
    <AppShell title="Watchlist">
      <section className="grid gap-3 md:grid-cols-2">
        {opportunities.map((item) => (
          <OpportunityCard key={item.symbol} item={item} />
        ))}
      </section>
    </AppShell>
  );
}
