import { useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { AllocationChart } from '../components/charts/FinanceCharts';
import { portfolioApi } from '../services/financialService';

export default function WhatIfSimulatorPage() {
  const [form, setForm] = useState({ name: 'Salary Increase', monthly_income: '', monthly_investment_override: '', risk_override: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async (e) => {
    e.preventDefault();
    setLoading(true);
    const payload = { name: form.name };
    if (form.monthly_income) payload.monthly_income = Number(form.monthly_income);
    if (form.monthly_investment_override) payload.monthly_investment_override = Number(form.monthly_investment_override);
    if (form.risk_override) payload.risk_override = form.risk_override;
    const data = await portfolioApi.whatIf(payload);
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">What-If Simulator</h1>
      <DisclaimerBanner />

      <form onSubmit={run} className="card grid gap-4 md:grid-cols-2">
        <input className="input-field" placeholder="Scenario name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input className="input-field" type="number" placeholder="New monthly income" value={form.monthly_income} onChange={(e) => setForm({ ...form, monthly_income: e.target.value })} />
        <input className="input-field" type="number" placeholder="Investment override" value={form.monthly_investment_override} onChange={(e) => setForm({ ...form, monthly_investment_override: e.target.value })} />
        <select className="input-field" value={form.risk_override} onChange={(e) => setForm({ ...form, risk_override: e.target.value })}>
          <option value="">Keep current risk</option>
          <option value="conservative">Conservative</option>
          <option value="moderate">Moderate</option>
          <option value="aggressive">Aggressive</option>
        </select>
        <div className="md:col-span-2"><button type="submit" className="btn-primary" disabled={loading}>{loading ? 'Running...' : 'Run Scenario'}</button></div>
      </form>

      {result && (
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card">
            <h2 className="font-semibold">Current Plan</h2>
            <p className="text-sm">Capacity: ₹{result.baseline?.capacity?.available_investment?.toLocaleString()}</p>
            <p className="text-sm">Health: {result.baseline?.health?.total_score}/100</p>
            <AllocationChart allocation={result.baseline?.recommendation?.allocation} />
          </div>
          <div className="card">
            <h2 className="font-semibold">Scenario Plan</h2>
            <p className="text-sm">Capacity: ₹{result.scenario?.capacity?.available_investment?.toLocaleString()}</p>
            <p className="text-sm">Health: {result.scenario?.health?.total_score}/100</p>
            <AllocationChart allocation={result.scenario?.recommendation?.allocation} />
          </div>
          <div className="card lg:col-span-2 text-sm">
            <h3 className="font-semibold">Comparison</h3>
            <p>Capacity change: ₹{result.comparison?.capacity_delta?.toLocaleString()}</p>
            <p>Health change: {result.comparison?.health_delta} points</p>
          </div>
        </div>
      )}
    </div>
  );
}
