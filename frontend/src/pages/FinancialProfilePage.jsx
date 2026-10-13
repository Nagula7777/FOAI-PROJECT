import { useEffect, useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { profileApi } from '../services/financialService';

const emptyProfile = {
  personal: { age: 30, employment_status: 'employed', dependents: 0 },
  income: { monthly_income: 0, other_monthly_income: 0 },
  expenses: { rent: 0, food: 0, transportation: 0, education: 0, utilities: 0, healthcare: 0, other: 0 },
  income_stability: 'medium',
  investment_experience: 'beginner',
};

export default function FinancialProfilePage() {
  const [form, setForm] = useState(emptyProfile);
  const [debts, setDebts] = useState([]);
  const [assets, setAssets] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    profileApi.get().then((data) => data && setForm(data));
    profileApi.listDebts().then(setDebts);
    profileApi.listAssets().then(setAssets);
  }, []);

  const saveProfile = async (e) => {
    e.preventDefault();
    await profileApi.update(form);
    setMessage('Profile saved successfully.');
  };

  const addDebt = async () => {
    const debt = await profileApi.createDebt({
      loan_type: 'personal', outstanding_amount: 100000, emi: 5000, interest_rate: 14,
    });
    setDebts((prev) => [...prev, debt]);
  };

  const addAsset = async () => {
    const asset = await profileApi.createAsset({
      asset_class: 'cash', name: 'Savings Account', current_value: 50000, is_emergency_fund: true,
    });
    setAssets((prev) => [...prev, asset]);
  };

  const setNested = (section, key, value) => {
    setForm((prev) => ({ ...prev, [section]: { ...prev[section], [key]: Number(value) || value } }));
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Financial Profile</h1>
      <DisclaimerBanner />
      {message && <div className="rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{message}</div>}

      <form onSubmit={saveProfile} className="card grid gap-4 md:grid-cols-2">
        <h2 className="md:col-span-2 text-lg font-semibold">Personal & Income</h2>
        {['age', 'dependents'].map((field) => (
          <label key={field} className="text-sm">
            {field}
            <input className="input-field mt-1" type="number" value={form.personal[field]}
              onChange={(e) => setNested('personal', field, e.target.value)} />
          </label>
        ))}
        {['monthly_income', 'other_monthly_income'].map((field) => (
          <label key={field} className="text-sm">
            {field.replace('_', ' ')}
            <input className="input-field mt-1" type="number" value={form.income[field]}
              onChange={(e) => setNested('income', field, e.target.value)} />
          </label>
        ))}
        <h2 className="md:col-span-2 text-lg font-semibold">Expenses</h2>
        {Object.keys(form.expenses).map((field) => (
          <label key={field} className="text-sm">
            {field}
            <input className="input-field mt-1" type="number" value={form.expenses[field]}
              onChange={(e) => setNested('expenses', field, e.target.value)} />
          </label>
        ))}
        <div className="md:col-span-2">
          <button type="submit" className="btn-primary">Save Profile</button>
        </div>
      </form>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Debts</h2>
            <button type="button" className="btn-secondary" onClick={addDebt}>Add Sample Debt</button>
          </div>
          <ul className="space-y-2 text-sm">{debts.map((d) => <li key={d.id}>{d.loan_type}: ₹{d.outstanding_amount} @ {d.interest_rate}%</li>)}</ul>
        </div>
        <div className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Assets</h2>
            <button type="button" className="btn-secondary" onClick={addAsset}>Add Sample Asset</button>
          </div>
          <ul className="space-y-2 text-sm">{assets.map((a) => <li key={a.id}>{a.name}: ₹{a.current_value}</li>)}</ul>
        </div>
      </div>
    </div>
  );
}
