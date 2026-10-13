import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { ProgressBar } from '../components/charts/FinanceCharts';
import { goalApi } from '../services/financialService';

export default function GoalDetailsPage() {
  const { id } = useParams();
  const [goal, setGoal] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    goalApi.get(id).then(setGoal);
    goalApi.analysis(id).then(setAnalysis);
  }, [id]);

  if (!goal) return <div className="text-sm text-slate-500">Loading...</div>;

  return (
    <div className="space-y-6">
      <Link to="/goals" className="text-sm text-brand-700">← Back to goals</Link>
      <h1 className="text-2xl font-bold">{goal.name}</h1>
      <DisclaimerBanner />

      <div className="card">
        <ProgressBar value={goal.current_amount} max={goal.target_amount} label="Progress" />
        <div className="mt-4 grid gap-3 sm:grid-cols-2 text-sm">
          <div>Target: ₹{goal.target_amount.toLocaleString()}</div>
          <div>Current: ₹{goal.current_amount.toLocaleString()}</div>
          <div>Monthly contribution: ₹{goal.monthly_contribution.toLocaleString()}</div>
          <div>Status: <strong>{goal.status.replace('_', ' ')}</strong></div>
        </div>
      </div>

      {analysis && (
        <div className="card space-y-3 text-sm">
          <h2 className="text-lg font-semibold">Goal Achievement Analysis</h2>
          <div className="grid gap-2 sm:grid-cols-2">
            <div>Remaining: ₹{analysis.remaining_amount.toLocaleString()}</div>
            <div>Months remaining: {analysis.months_remaining}</div>
            <div>Required monthly: ₹{analysis.required_monthly_contribution.toLocaleString()}</div>
            <div>Estimated FV: ₹{analysis.estimated_future_value.toLocaleString()}</div>
          </div>
          <p className="text-xs text-amber-700">{analysis.assumption_note}</p>
        </div>
      )}
    </div>
  );
}
