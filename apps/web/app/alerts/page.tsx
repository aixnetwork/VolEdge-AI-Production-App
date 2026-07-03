import { AppShell } from "@/components/AppShell";
import { getAlertsData } from "@/lib/api";

export default async function Alerts() {
  const alerts = await getAlertsData();

  return (
    <AppShell title="Alerts">
      <section className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <div className="grid gap-3">
          {alerts.map((alert) => (
            <div key={alert.symbol + alert.condition} className="rounded border border-line bg-panel/80 p-5">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <div className="text-3xl font-black">{alert.symbol}</div>
                  <div className="text-sm text-steel">{alert.condition}</div>
                </div>
                <div className="rounded bg-mint px-3 py-1 text-sm font-bold text-ink">{alert.status}</div>
              </div>
            </div>
          ))}
        </div>
        <form className="rounded border border-line bg-panel/90 p-5">
          <h2 className="text-lg font-bold">Create Alert</h2>
          <input className="mt-4 h-11 w-full rounded border border-line bg-ink px-3 text-white" placeholder="Symbol" defaultValue="UVIX" />
          <input className="mt-3 h-11 w-full rounded border border-line bg-ink px-3 text-white" placeholder="Condition" defaultValue="VolEdge Score above" />
          <input className="mt-3 h-11 w-full rounded border border-line bg-ink px-3 text-white" placeholder="Threshold" defaultValue="85" />
          <button className="mt-4 h-11 w-full rounded bg-mint font-bold text-ink">Save Alert</button>
        </form>
      </section>
    </AppShell>
  );
}
