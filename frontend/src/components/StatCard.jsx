export default function StatCard({ label, value, icon, accent = 'brand' }) {
  const colors = {
    brand: 'bg-brand-50 text-brand-700',
    green: 'bg-emerald-50 text-emerald-700',
    amber: 'bg-amber-50 text-amber-700',
    red: 'bg-red-50 text-red-700',
    slate: 'bg-slate-100 text-slate-700',
  };
  return (
    <div className="card p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-2 text-3xl font-bold text-slate-800">{value}</p>
        </div>
        <span className={`w-10 h-10 rounded-lg flex items-center justify-center text-xl ${colors[accent]}`}>
          {icon}
        </span>
      </div>
    </div>
  );
}
