import { useLocation } from 'react-router-dom';

const titles = {
  '/dashboard': 'Dashboard',
  '/products': 'Products',
  '/customers': 'Customers',
  '/orders': 'Orders',
};

export default function Navbar() {
  const { pathname } = useLocation();
  const title = titles[pathname] || 'Inventory OS';
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center px-6">
      <h1 className="text-lg font-semibold text-slate-800">{title}</h1>
      <div className="ml-auto text-sm text-slate-500 hidden sm:block">
        Manage your inventory with ease
      </div>
    </header>
  );
}
