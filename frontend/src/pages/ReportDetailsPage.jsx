import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { reportApi } from '../services/financialService';

export default function ReportDetailsPage() {
  const { id } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => { reportApi.get(id).then(setReport); }, [id]);

  if (!report) return <div className="text-sm text-slate-500">Loading...</div>;

  return (
    <div className="space-y-6">
      <Link to="/reports" className="text-sm text-brand-700">← Back to reports</Link>
      <h1 className="text-2xl font-bold">Report — {report.report_month}</h1>
      <DisclaimerBanner />

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="card">
          <h2 className="font-semibold">Financial Summary</h2>
          <ul className="mt-2 space-y-1 text-sm">
            {Object.entries(report.financial_summary || {}).map(([k, v]) => (
              <li key={k}>{k.replace('_', ' ')}: ₹{Number(v).toLocaleString()}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2 className="font-semibold">Health Score</h2>
          <p className="mt-2 text-3xl font-bold">{report.health_score?.current}/100</p>
          <p className="text-sm text-slate-500">Change: {report.health_score?.change >= 0 ? '+' : ''}{report.health_score?.change}</p>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold">Goal Progress</h2>
        <ul className="mt-2 space-y-2 text-sm">
          {(report.goal_progress || []).map((g) => (
            <li key={g.name}>{g.name}: {g.progress_pct}% · {g.status}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2 className="font-semibold">Next Month Plan</h2>
        <ul className="mt-2 space-y-1 text-sm">
          {Object.entries(report.next_month_plan || {}).map(([k, v]) => (
            <li key={k}>{k.replace('_', ' ')}: ₹{Number(v).toLocaleString()}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
