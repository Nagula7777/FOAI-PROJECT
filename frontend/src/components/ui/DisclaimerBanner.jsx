import { FINANCIAL_DISCLAIMER } from '../../config/constants';

export default function DisclaimerBanner({ className = '' }) {
  return (
    <div
      className={`rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 ${className}`}
      role="note"
    >
      {FINANCIAL_DISCLAIMER}
    </div>
  );
}
