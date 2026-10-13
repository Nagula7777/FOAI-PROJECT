import { useEffect, useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { aiApi } from '../services/financialService';

export default function FinancialHealthPage() {
  const [health, setHealth] = useState(null);

  useEffect(() => { aiApi.health().then(setHealth).catch(() => {}); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Financial Health</h1>
      <DisclaimerBanner />
      {health ? (
        <>
          <div className="card text-center">
            <p className="text-sm text-slate-500">Financial Health Score</p>
            <p className="mt-2 text-5xl font-bold text-brand-700">{health.total_score}/100</p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {Object.entries(health.components).map(([key, val]) => (
              <div key={key} className="card">
                <p className="text-sm capitalize text-slate-500">{key.replace('_', ' ')}</p>
                <p className="mt-1 text-2xl font-bold">{val.score}</p>
                <p className="text-xs text-slate-400">Value: {val.value}</p>
              </div>
            ))}
          </div>
          <div className="card">
            <h2 className="font-semibold">How this score was calculated</h2>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              {health.explanation.map((line) => <li key={line}>• {line}</li>)}
            </ul>
          </div>
        </>
      ) : (
        <div className="card text-sm text-slate-500">Complete your financial profile to see your health score.</div>
      )}
    </div>
  );
}
