import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import ExplanationPanel from '../components/ai/ExplanationPanel';
import { aiApi } from '../services/financialService';

const questions = [
  { key: 'loss_tolerance', label: 'How comfortable are you with temporary losses?' },
  { key: 'market_reaction', label: 'How would you react to a 20% market drop?' },
  { key: 'investment_knowledge', label: 'How would you rate your investment knowledge?' },
  { key: 'horizon_comfort', label: 'How comfortable are you with long investment horizons?' },
  { key: 'volatility_comfort', label: 'How comfortable are you with portfolio volatility?' },
];

export default function RiskAssessmentPage() {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState({ loss_tolerance: 3, market_reaction: 3, investment_knowledge: 3, horizon_comfort: 3, volatility_comfort: 3 });
  const [result, setResult] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    const data = await aiApi.submitRisk(answers);
    setResult(data);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Risk Assessment</h1>
      <DisclaimerBanner />
      <form onSubmit={submit} className="card space-y-4">
        {questions.map(({ key, label }) => (
          <label key={key} className="block text-sm">
            {label}
            <input type="range" min="1" max="5" value={answers[key]} className="mt-2 w-full"
              onChange={(e) => setAnswers((prev) => ({ ...prev, [key]: Number(e.target.value) }))} />
            <span className="text-slate-500">Score: {answers[key]}</span>
          </label>
        ))}
        <button type="submit" className="btn-primary">Submit Assessment</button>
      </form>
      {result && (
        <>
          <div className="card">
            <h2 className="text-lg font-semibold">Fuzzy Risk Profile</h2>
            <p className="mt-2 text-sm">Dominant profile: <strong>{result.dominant_profile}</strong></p>
            <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
              <div>Conservative: {(result.fuzzy_output.conservative * 100).toFixed(0)}%</div>
              <div>Moderate: {(result.fuzzy_output.moderate * 100).toFixed(0)}%</div>
              <div>Aggressive: {(result.fuzzy_output.aggressive * 100).toFixed(0)}%</div>
            </div>
            <button type="button" className="btn-secondary mt-4" onClick={() => navigate('/recommendation')}>
              Continue to AI Plan
            </button>
          </div>
          <ExplanationPanel explanations={result.explanation} />
        </>
      )}
    </div>
  );
}
