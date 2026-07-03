export function SignalBar({ value }: { value: number }) {
  return (
    <div className="h-2 rounded bg-line">
      <div className="h-2 rounded bg-mint" style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}
