export function Metric({ label, value, tone = "default" }: { label: string; value: string; tone?: "default" | "mint" | "amber" }) {
  const color = tone === "mint" ? "text-mint" : tone === "amber" ? "text-amber" : "text-white";
  return (
    <div className="min-w-0">
      <div className="text-xs uppercase tracking-wide text-steel">{label}</div>
      <div className={`mt-1 truncate text-2xl font-semibold ${color}`}>{value}</div>
    </div>
  );
}
