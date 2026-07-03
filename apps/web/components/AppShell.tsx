import Link from "next/link";
import { referenceTaglines } from "@/lib/mock-data";
import { SidebarNav } from "@/components/SidebarNav";

export function AppShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <main className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 hidden w-56 border-r border-line bg-ink/90 px-4 py-5 backdrop-blur lg:block">
        <Link href="/" className="mb-7 flex h-12 items-center gap-3 rounded bg-mint px-3 text-ink">
          <span className="grid h-7 w-7 place-items-center rounded bg-ink text-sm font-black text-mint">V</span>
          <span className="text-sm font-black">VolEdge AI</span>
        </Link>
        <SidebarNav />
      </aside>

      <section className="mx-auto max-w-7xl px-4 py-5 lg:pl-64">
        <header className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-sm font-semibold text-mint">VolEdge AI</div>
            <h1 className="text-2xl font-bold tracking-normal sm:text-3xl">{title}</h1>
            <div className="mt-1 text-sm text-steel">{referenceTaglines.alternate}</div>
          </div>
          <div className="rounded border border-line bg-panel px-4 py-2 text-sm font-semibold text-white">Alert-only mode</div>
        </header>
        {children}
      </section>
    </main>
  );
}
