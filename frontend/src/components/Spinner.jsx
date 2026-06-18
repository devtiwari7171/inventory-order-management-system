export default function Spinner({ label = 'Loading…' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-slate-500">
      <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin" />
      <p className="mt-3 text-sm">{label}</p>
    </div>
  );
}
