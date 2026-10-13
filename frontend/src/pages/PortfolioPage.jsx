import { useEffect, useState } from 'react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';
import { AllocationChart } from '../components/charts/FinanceCharts';
import { portfolioApi } from '../services/financialService';

export default function PortfolioPage() {
  const [portfolio, setPortfolio] = useState(null);

  useEffect(() => { portfolioApi.get().then(setPortfolio); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Portfolio</h1>
      <DisclaimerBanner />
      {portfolio && (
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card">
            <h2 className="font-semibold">Current Allocation</h2>
            <AllocationChart allocation={portfolio.current_allocation} />
          </div>
          <div className="card">
            <h2 className="font-semibold">Target Allocation (AI)</h2>
            <AllocationChart allocation={portfolio.target_allocation} />
            {portfolio.needs_rebalancing && (
              <p className="mt-3 text-sm text-amber-700">Portfolio drift detected. See Rebalancing page.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
