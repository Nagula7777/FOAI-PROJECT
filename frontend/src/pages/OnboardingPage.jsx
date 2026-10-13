import { Link } from 'react-router-dom';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';

export default function OnboardingPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Welcome to FOAI Financial Planner</h1>
      <DisclaimerBanner />
      <div className="card">
        <p className="text-sm text-slate-600">Complete these steps to unlock AI recommendations:</p>
        <ol className="mt-4 space-y-3 text-sm">
          <li><Link className="text-brand-700" to="/profile">1. Enter your financial profile</Link></li>
          <li><Link className="text-brand-700" to="/goals">2. Create financial goals</Link></li>
          <li><Link className="text-brand-700" to="/risk-assessment">3. Complete risk assessment</Link></li>
          <li><Link className="text-brand-700" to="/recommendation">4. Run AI financial plan</Link></li>
        </ol>
      </div>
    </div>
  );
}
