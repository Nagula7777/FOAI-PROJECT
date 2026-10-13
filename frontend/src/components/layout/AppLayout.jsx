import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  Activity, BarChart3, FlaskConical, Goal, LayoutDashboard, LineChart,
  LogOut, Shield, Sparkles, Wallet, FileText, Settings, RefreshCw,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const navLinkClass = ({ isActive }) =>
  `flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition ${
    isActive ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
  }`;

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/profile', label: 'Finances', icon: Wallet },
  { to: '/goals', label: 'Goals', icon: Goal },
  { to: '/risk-assessment', label: 'Risk Assessment', icon: Activity },
  { to: '/financial-health', label: 'Health Score', icon: BarChart3 },
  { to: '/recommendation', label: 'AI Plan', icon: Sparkles },
  { to: '/portfolio', label: 'Portfolio', icon: LineChart },
  { to: '/investments', label: 'Investments', icon: Wallet },
  { to: '/simulator', label: 'What-If', icon: FlaskConical },
  { to: '/rebalancing', label: 'Rebalancing', icon: RefreshCw },
  { to: '/reports', label: 'Reports', icon: FileText },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function AppLayout() {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <Link to="/dashboard" className="flex items-center gap-2 font-semibold text-slate-900">
            <Sparkles className="h-5 w-5 text-brand-600" />
            FOAI Financial Planner
          </Link>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-600 sm:inline">{user?.full_name}</span>
            <button type="button" onClick={handleLogout} className="btn-secondary gap-2 px-3 py-2">
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <aside className="hidden w-56 shrink-0 md:block">
          <nav className="card max-h-[calc(100vh-8rem)] space-y-1 overflow-y-auto p-3">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink key={to} to={to} className={navLinkClass}>
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
            {isAdmin && (
              <NavLink to="/admin" className={navLinkClass}>
                <Shield className="h-4 w-4" />
                Admin
              </NavLink>
            )}
          </nav>
        </aside>

        <main className="min-w-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
