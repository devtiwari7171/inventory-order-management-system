import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/products', label: 'Products', icon: '📦' },
  { to: '/customers', label: 'Customers', icon: '👥' },
  { to: '/orders', label: 'Orders', icon: '🧾' },
];

export default function Sidebar() {
  return (
    <aside className="hidden md:flex md:w-64 bg-white border-r border-slate-200 flex-col">
      <div className="p-6 flex items-center gap-2 border-b border-slate-200">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold">
          IO
        </div>
        <span className="font-semibold text-slate-800">Inventory OS</span>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-brand-50 text-brand-700'
                  : 'text-slate-600 hover:bg-slate-100'
              }`
            }
          >
            <span className="text-lg">{l.icon}</span>
            {l.label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-200 text-xs text-slate-500">
        v1.0.0 · FastAPI + React
      </div>
    </aside>
  );
}
