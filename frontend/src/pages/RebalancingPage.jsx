import { useEffect, useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import ExplanationPanel from '../components/ai/ExplanationPanel';
import { portfolioApi } from '../services/financialService';

export default function RebalancingPage() {
  const [data, setData] = useState(null);

  useEffect(() => { portfolioApi.rebalancing().then(setData); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Portfolio Rebalancing</h1>
      <DisclaimerBanner />
      {data && (
        <>
          <div className="card overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="py-2">Asset</th><th>Current</th><th>Target</th><th>Drift</th></tr></thead>
              <tbody>
                {Object.keys(data.target_allocation).map((key) => (
                  <tr key={key} className="border-b">
                    <td className="py-2 capitalize">{key}</td>
                    <td>{(data.current_allocation[key] * 100).toFixed(1)}%</td>
                    <td>{(data.target_allocation[key] * 100).toFixed(1)}%</td>
                    <td className={Math.abs(data.drift[key]) > 0.05 ? 'text-amber-700 font-medium' : ''}>{(data.drift[key] * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {data.suggestions?.length > 0 && (
            <div className="card">
              <h2 className="font-semibold">Suggestions</h2>
              <ul className="mt-2 space-y-1 text-sm">{data.suggestions.map((s) => <li key={s}>• {s}</li>)}</ul>
            </div>
          )}
          <ExplanationPanel title="Why rebalancing?" explanations={data.explanation} />
        </>
      )}
    </div>
  );
}
