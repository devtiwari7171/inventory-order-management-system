import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="card p-12 text-center max-w-md mx-auto">
      <div className="text-6xl">🧭</div>
      <h2 className="mt-4 text-2xl font-bold text-slate-800">Page not found</h2>
      <p className="mt-2 text-slate-500">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/dashboard" className="btn-primary mt-6 inline-flex">
        Back to dashboard
      </Link>
    </div>
  );
}
