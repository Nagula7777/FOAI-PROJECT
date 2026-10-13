import { useEffect, useState } from 'react';
import { Shield } from 'lucide-react';
import apiClient from '../../services/apiClient';
import { useAuth } from '../../context/AuthContext';
import DisclaimerBanner from '../../components/ui/DisclaimerBanner';

export default function AdminDashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    apiClient.get('/api/admin/dashboard').then((r) => setStats(r.data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Shield className="h-6 w-6 text-brand-600" />
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      </div>
      <p className="text-sm text-slate-600">Welcome, {user?.full_name}.</p>
      <DisclaimerBanner />
      {stats && (
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="card"><p className="text-sm text-slate-500">Users</p><p className="text-2xl font-bold">{stats.users}</p></div>
          <div className="card"><p className="text-sm text-slate-500">Recommendations</p><p className="text-2xl font-bold">{stats.recommendations}</p></div>
          <div className="card"><p className="text-sm text-slate-500">Reports</p><p className="text-2xl font-bold">{stats.reports}</p></div>
        </div>
      )}
      <div className="card text-sm text-slate-600">
        Admin CRUD for rules, products, and constraints can be extended via API at /docs.
      </div>
    </div>
  );
}
