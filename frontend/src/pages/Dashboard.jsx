import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import StatCard from '../components/StatCard.jsx';
import Spinner from '../components/Spinner.jsx';
import { dashboardService } from '../services/dashboardService';
import { formatCurrency, formatDate } from '../utils/formatters';
import { LOW_STOCK_THRESHOLD } from '../utils/constants';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    dashboardService
      .stats()
      .then((data) => {
        if (alive) setStats(data);
      })
      .catch((e) => alive && setError(e.message))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, []);

  if (loading) return <Spinner label="Loading dashboard…" />;

  if (error) {
    return (
      <div className="card p-6 border-red-200 bg-red-50">
        <p className="text-red-700 font-medium">Couldn't load dashboard</p>
        <p className="text-sm text-red-600 mt-1">{error}</p>
        <p className="text-xs text-slate-500 mt-3">
          Make sure the backend is running at http://localhost:8000
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Dashboard</h2>
        <p className="text-sm text-slate-500 mt-1">
          Overview of your inventory and order activity.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Products" value={stats.total_products} icon="📦" accent="brand" />
        <StatCard label="Total Customers" value={stats.total_customers} icon="👥" accent="green" />
        <StatCard label="Total Orders" value={stats.total_orders} icon="🧾" accent="amber" />
        <StatCard
          label="Low Stock Items"
          value={stats.low_stock_products.length}
          icon="⚠️"
          accent={stats.low_stock_products.length > 0 ? 'red' : 'slate'}
        />
      </div>

      <div className="card">
        <div className="flex items-center justify-between p-5 border-b border-slate-200">
          <div>
            <h3 className="font-semibold text-slate-800">Low Stock Products</h3>
            <p className="text-xs text-slate-500 mt-1">
              Items at or below {LOW_STOCK_THRESHOLD} units.
            </p>
          </div>
          <Link to="/products" className="btn-secondary text-xs">
            Manage products →
          </Link>
        </div>
        {stats.low_stock_products.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">
            🎉 No low-stock items right now.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600 text-left">
                <tr>
                  <th className="px-5 py-3 font-medium">SKU</th>
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Price</th>
                  <th className="px-5 py-3 font-medium">Stock</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {stats.low_stock_products.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50">
                    <td className="px-5 py-3 font-mono text-xs">{p.sku}</td>
                    <td className="px-5 py-3 font-medium text-slate-800">{p.name}</td>
                    <td className="px-5 py-3">{formatCurrency(p.price)}</td>
                    <td className="px-5 py-3 font-semibold">{p.stock_quantity}</td>
                    <td className="px-5 py-3">
                      <span
                        className={`badge ${
                          p.stock_quantity === 0
                            ? 'bg-red-100 text-red-700'
                            : 'bg-amber-100 text-amber-700'
                        }`}
                      >
                        {p.stock_quantity === 0 ? 'Out of stock' : 'Low'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="text-xs text-slate-400 text-center pt-4">
        Last updated: {formatDate(new Date().toISOString())}
      </div>
    </div>
  );
}
