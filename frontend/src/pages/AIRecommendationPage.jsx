import { useEffect, useState } from 'react';
import { Sparkles } from 'lucide-react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import ExplanationPanel from '../components/ai/ExplanationPanel';
import { AllocationChart } from '../components/charts/FinanceCharts';
import { aiApi } from '../services/financialService';

export default function AIRecommendationPage() {
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const loadExisting = () => {
    aiApi.recommendation().then((data) => setAnalysis({ recommendation: data })).catch(() => {});
  };

  useEffect(() => { loadExisting(); }, []);

  const runAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await aiApi.analyze();
      setAnalysis(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Complete profile, goals, and risk assessment first.');
    } finally {
      setLoading(false);
    }
  };

  const rec = analysis?.recommendation;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="flex items-center gap-2 text-2xl font-bold"><Sparkles className="h-6 w-6 text-brand-600" /> AI Recommendation</h1>
        <button type="button" className="btn-primary" onClick={runAnalysis} disabled={loading}>
          {loading ? 'Analyzing...' : 'Run AI Plan'}
        </button>
      </div>
      <DisclaimerBanner />
      {error && <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>}

      {rec && (
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card space-y-4">
            <h2 className="text-lg font-semibold">Recommended Allocation</h2>
            <AllocationChart allocation={rec.allocation} />
            <div className="grid grid-cols-2 gap-2 text-sm">
              {Object.entries(rec.allocation).map(([k, v]) => (
                <div key={k} className="rounded-lg bg-slate-50 p-3 capitalize">{k}: {(v * 100).toFixed(0)}%</div>
              ))}
            </div>
            <div className="border-t pt-4 text-sm">
              <p><strong>Monthly investment:</strong> ₹{rec.monthly_investment_amount?.toLocaleString()}</p>
              <p><strong>Horizon:</strong> {rec.recommended_horizon_years} years</p>
            </div>
          </div>

          <div className="space-y-4">
            <ExplanationPanel explanations={rec.explanations} />
            {rec.recommended_products?.length > 0 && (
              <div className="card">
                <h3 className="font-semibold">Suggested Products</h3>
                <ul className="mt-3 space-y-2 text-sm">
                  {rec.recommended_products.map((p) => (
                    <li key={p.product_id}>{p.name}: {(p.allocation_pct * 100).toFixed(0)}% · ₹{p.monthly_amount?.toLocaleString()}/mo</li>
                  ))}
                </ul>
              </div>
            )}
            {analysis?.capacity && (
              <div className="card text-sm">
                <h3 className="font-semibold">Investment Capacity</h3>
                <ul className="mt-2 space-y-1 text-slate-600">
                  {analysis.capacity.breakdown?.map((line) => <li key={line}>{line}</li>)}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {!rec && !loading && (
        <div className="card text-center text-sm text-slate-500">
          Click &quot;Run AI Plan&quot; to generate your personalized portfolio recommendation.
        </div>
      )}
    </div>
  );
}
