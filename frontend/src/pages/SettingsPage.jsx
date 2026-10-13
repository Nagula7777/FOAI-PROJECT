import { useAuth } from '../context/AuthContext';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>
      <DisclaimerBanner />
      <div className="card space-y-3 text-sm">
        <div><span className="text-slate-500">Name:</span> {user?.full_name}</div>
        <div><span className="text-slate-500">Email:</span> {user?.email}</div>
        <div><span className="text-slate-500">Role:</span> {user?.role}</div>
        <div><span className="text-slate-500">Onboarding:</span> {user?.onboarding_completed ? 'Complete' : 'Incomplete'}</div>
      </div>
    </div>
  );
}
