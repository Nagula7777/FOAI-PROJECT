import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Activity, AlertTriangle, PiggyBank, TrendingUp, Wallet } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { AllocationChart, StatCard } from '../components/charts/FinanceCharts';
import { ProgressBar } from '../components/charts/FinanceCharts';
import { aiApi, goalApi, profileApi } from '../services/financialService';

export default function DashboardPage() {
  const { user } = useAuth();
  const [health, setHealth] = useState(null);
  const [capacity, setCapacity] = useState(null);
  const [emergency, setEmergency] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [goals, setGoals] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    profileApi.get().then(setProfile).catch(() => {});
    aiApi.health().then(setHealth).catch(() => {});
    aiApi.capacity().then(setCapacity).catch(() => {});
    aiApi.emergencyFund().then(setEmergency).catch(() => {});
    aiApi.recommendation().then(setRecommendation).catch(() => {});
    goalApi.list().then(setGoals).catch(() => setGoals([]));
    aiApi.warnings().then(setWarnings).catch(() => setWarnings([]));
  }, []);

  const income = profile ? (profile.income?.monthly_income || 0) + (profile.income?.other_monthly_income || 0) : null;
  const expenses = profile ? Object.values(profile.expenses || {}).reduce((a, b) => a + b, 0) : null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-600">Welcome back, {user?.full_name}.</p>
      </div>
      <DisclaimerBanner />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Financial Health" value={health ? `${health.total_score}/100` : '—'} icon={Activity} hint="Rule-based score" />
        <StatCard label="Monthly Income" value={income != null ? `₹${income.toLocaleString()}` : '—'} icon={Wallet} />
        <StatCard label="Monthly Expenses" value={expenses != null ? `₹${expenses.toLocaleString()}` : '—'} icon={PiggyBank} />
        <StatCard label="Available Investment" value={capacity ? `₹${capacity.available_investment?.toLocaleString()}` : '—'} icon={TrendingUp} />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="card lg:col-span-2">
          <h2 className="font-semibold">Goals</h2>
          <div className="mt-4 space-y-4">
            {goals.slice(0, 3).map((g) => (
              <ProgressBar key={g.id} value={g.current_amount} max={g.target_amount} label={g.name} />
            ))}
            {!goals.length && <p className="text-sm text-slate-500"><Link to="/goals" className="text-brand-700">Add goals</Link> to track progress.</p>}
          </div>
        </div>
        <div className="card">
          <h2 className="font-semibold">Emergency Fund</h2>
          {emergency ? (
            <div className="mt-3 text-sm space-y-1">
              <p>Current: ₹{emergency.current_amount?.toLocaleString()}</p>
              <p>Required: ₹{emergency.required_amount?.toLocaleString()}</p>
              <p>Gap: ₹{emergency.remaining_amount?.toLocaleString()}</p>
            </div>
          ) : <p className="mt-3 text-sm text-slate-500">Complete profile first.</p>}
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold">AI Recommendation</h2>
            <Link to="/recommendation" className="text-sm text-brand-700">View details</Link>
          </div>
          {recommendation?.allocation ? (
            <div className="mt-4"><AllocationChart allocation={recommendation.allocation} /></div>
          ) : (
            <p className="mt-4 text-sm text-slate-500"><Link to="/recommendation" className="text-brand-700">Run AI Plan</Link> to get allocation.</p>
          )}
        </div>
        <div className="card">
          <h2 className="flex items-center gap-2 font-semibold"><AlertTriangle className="h-4 w-4 text-amber-600" /> Alerts</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {warnings.slice(0, 5).map((w) => (
              <li key={w.code} className="rounded-lg bg-amber-50 px-3 py-2 text-amber-900">{w.message}</li>
            ))}
            {!warnings.length && <li className="text-slate-500">No active warnings.</li>}
          </ul>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <Link to="/goals" className="btn-secondary">Add Goal</Link>
        <Link to="/profile" className="btn-secondary">Update Finances</Link>
        <Link to="/recommendation" className="btn-primary">Run AI Plan</Link>
        <Link to="/simulator" className="btn-secondary">What-If Analysis</Link>
        <Link to="/reports" className="btn-secondary">Monthly Reports</Link>
      </div>
    </div>
  );
}
