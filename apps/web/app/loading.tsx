import { AppShell } from "@/components/AppShell";

const skeletonRows = Array.from({ length: 6 }, (_, index) => index);

export default function Loading() {
  return (
    <AppShell title="Loading">
      <section className="rounded border border-line bg-panel/90 p-5">
        <div className="mb-5 flex items-center justify-between gap-4">
          <div>
            <div className="h-4 w-32 animate-pulse rounded bg-line" />
            <div className="mt-3 h-8 w-56 animate-pulse rounded bg-line" />
          </div>
          <div className="h-12 w-12 animate-spin rounded-full border-2 border-line border-t-mint" />
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {skeletonRows.map((row) => (
            <div key={row} className="rounded border border-line bg-ink/35 p-4">
              <div className="h-4 w-20 animate-pulse rounded bg-line" />
              <div className="mt-3 h-7 w-28 animate-pulse rounded bg-line" />
              <div className="mt-5 h-16 animate-pulse rounded bg-line/70" />
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
