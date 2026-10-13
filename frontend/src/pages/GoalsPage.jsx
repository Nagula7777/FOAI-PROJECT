import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { ProgressBar } from '../components/charts/FinanceCharts';
import { goalApi } from '../services/financialService';

const statusColors = {
  on_track: 'bg-green-100 text-green-800',
  at_risk: 'bg-amber-100 text-amber-800',
  unlikely: 'bg-red-100 text-red-800',
};

export default function GoalsPage() {
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState({
    name: '', category: 'house', target_amount: 1000000, current_amount: 0,
    target_date: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10),
    priority: 1, monthly_contribution: 10000,
  });

  useEffect(() => { goalApi.list().then(setGoals).catch(() => setGoals([])); }, []);

  const createGoal = async (e) => {
    e.preventDefault();
    const goal = await goalApi.create({ ...form, target_date: new Date(form.target_date).toISOString() });
    setGoals((prev) => [...prev, goal]);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Financial Goals</h1>
        <Link to="/profile" className="btn-secondary">Update Finances</Link>
      </div>
      <DisclaimerBanner />

      <form onSubmit={createGoal} className="card grid gap-4 md:grid-cols-2">
        <h2 className="md:col-span-2 flex items-center gap-2 text-lg font-semibold"><Plus className="h-4 w-4" /> Add Goal</h2>
        <input className="input-field" placeholder="Goal name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <select className="input-field" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
          {['emergency_fund', 'education', 'vehicle', 'house', 'marriage', 'retirement', 'travel', 'other'].map((c) => (
            <option key={c} value={c}>{c.replace('_', ' ')}</option>
          ))}
        </select>
        <input className="input-field" type="number" placeholder="Target amount" value={form.target_amount} onChange={(e) => setForm({ ...form, target_amount: Number(e.target.value) })} />
        <input className="input-field" type="number" placeholder="Current amount" value={form.current_amount} onChange={(e) => setForm({ ...form, current_amount: Number(e.target.value) })} />
        <input className="input-field" type="date" value={form.target_date} onChange={(e) => setForm({ ...form, target_date: e.target.value })} />
        <input className="input-field" type="number" placeholder="Monthly contribution" value={form.monthly_contribution} onChange={(e) => setForm({ ...form, monthly_contribution: Number(e.target.value) })} />
        <div className="md:col-span-2"><button type="submit" className="btn-primary">Create Goal</button></div>
      </form>

      <div className="grid gap-4">
        {goals.map((goal) => (
          <Link key={goal.id} to={`/goals/${goal.id}`} className="card block hover:border-brand-300">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold">{goal.name}</h3>
                <p className="text-sm text-slate-500">{goal.category.replace('_', ' ')} · Priority {goal.priority}</p>
              </div>
              <span className={`rounded-full px-2 py-1 text-xs font-medium ${statusColors[goal.status] || statusColors.at_risk}`}>{goal.status.replace('_', ' ')}</span>
            </div>
            <div className="mt-4">
              <ProgressBar value={goal.current_amount} max={goal.target_amount} label={`₹${goal.current_amount.toLocaleString()} / ₹${goal.target_amount.toLocaleString()}`} />
            </div>
          </Link>
        ))}
        {!goals.length && <p className="text-sm text-slate-500">No goals yet. Create your first goal above.</p>}
      </div>
    </div>
  );
}
