import { useEffect, useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { portfolioApi } from '../services/financialService';

export default function InvestmentExplorerPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    const loadProducts = async () => {
      try {
        const data = await portfolioApi.products();
        if (!cancelled) {
          setProducts(data || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError('Unable to load investment products. Please make sure the backend is running.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadProducts();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Investment Explorer</h1>
      <DisclaimerBanner />

      {loading && <div className="card text-sm text-slate-600">Loading investment products...</div>}

      {!loading && error && (
        <div className="rounded border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          {error}
        </div>
      )}

      {!loading && !error && products.length === 0 && (
        <div className="card text-sm text-slate-600">
          No investment products are available yet. Please seed or add them from the admin panel.
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((p) => (
          <div key={p.id || p._id} className="card">
            <h3 className="font-semibold">{p.name}</h3>
            <p className="mt-1 text-sm capitalize text-slate-500">{p.asset_class} · {p.risk_category} risk</p>
            <p className="mt-2 text-sm">Est. return assumption: {(p.expected_return_assumption * 100).toFixed(1)}%</p>
            <p className="text-xs text-amber-700">Not guaranteed</p>
          </div>
        ))}
      </div>
    </div>
  );
}
