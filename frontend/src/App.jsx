import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/layout/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';
import LandingPage from './pages/LandingPage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import OnboardingPage from './pages/OnboardingPage';
import FinancialProfilePage from './pages/FinancialProfilePage';
import RiskAssessmentPage from './pages/RiskAssessmentPage';
import DashboardPage from './pages/DashboardPage';
import FinancialHealthPage from './pages/FinancialHealthPage';
import GoalsPage from './pages/GoalsPage';
import GoalDetailsPage from './pages/GoalDetailsPage';
import AIRecommendationPage from './pages/AIRecommendationPage';
import PortfolioPage from './pages/PortfolioPage';
import InvestmentExplorerPage from './pages/InvestmentExplorerPage';
import WhatIfSimulatorPage from './pages/WhatIfSimulatorPage';
import RebalancingPage from './pages/RebalancingPage';
import MonthlyReportsPage from './pages/MonthlyReportsPage';
import ReportDetailsPage from './pages/ReportDetailsPage';
import SettingsPage from './pages/SettingsPage';
import AdminDashboardPage from './pages/admin/AdminDashboardPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />

          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/onboarding" element={<OnboardingPage />} />
              <Route path="/profile" element={<FinancialProfilePage />} />
              <Route path="/risk-assessment" element={<RiskAssessmentPage />} />
              <Route path="/financial-health" element={<FinancialHealthPage />} />
              <Route path="/goals" element={<GoalsPage />} />
              <Route path="/goals/:id" element={<GoalDetailsPage />} />
              <Route path="/recommendation" element={<AIRecommendationPage />} />
              <Route path="/portfolio" element={<PortfolioPage />} />
              <Route path="/investments" element={<InvestmentExplorerPage />} />
              <Route path="/simulator" element={<WhatIfSimulatorPage />} />
              <Route path="/rebalancing" element={<RebalancingPage />} />
              <Route path="/reports" element={<MonthlyReportsPage />} />
              <Route path="/reports/:id" element={<ReportDetailsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </Route>

          <Route element={<ProtectedRoute adminOnly />}>
            <Route element={<AppLayout />}>
              <Route path="/admin" element={<AdminDashboardPage />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
