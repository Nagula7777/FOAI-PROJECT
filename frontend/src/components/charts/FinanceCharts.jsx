import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = ['#1a82f5', '#059669', '#d97706', '#64748b'];

export function AllocationChart({ allocation = {} }) {
  const data = Object.entries(allocation).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value: Math.round(value * 100),
  }));

  if (!data.length) {
    return <div className="text-sm text-slate-500">No allocation data</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
          {data.map((_, index) => (
            <Cell key={data[index].name} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => `${value}%`} />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function ProgressBar({ value, max = 100, label }) {
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
  return (
    <div>
      {label && <div className="mb-1 flex justify-between text-sm"><span>{label}</span><span>{pct.toFixed(0)}%</span></div>}
      <div className="h-2 rounded-full bg-slate-200">
        <div className="h-2 rounded-full bg-brand-600" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export function StatCard({ label, value, hint, icon: Icon }) {
  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-2 text-2xl font-bold text-slate-900">{value}</p>
          {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
        </div>
        {Icon && (
          <div className="rounded-lg bg-brand-50 p-2 text-brand-700">
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </div>
  );
}
