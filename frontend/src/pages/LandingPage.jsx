import { Link } from 'react-router-dom';
import { ArrowRight, Brain, LineChart, ShieldCheck, Sparkles } from 'lucide-react';
import DisclaimerBanner from '../components/ui/DisclaimerBanner';

const features = [
  {
    icon: Brain,
    title: 'Classical AI Reasoning',
    description:
      'Expert rules, fuzzy logic, constraints, utility scoring, and genetic optimization — no black-box ML.',
  },
  {
    icon: LineChart,
    title: 'Personalized Planning',
    description:
      'Analyze income, expenses, debts, goals, and risk tolerance to build explainable recommendations.',
  },
  {
    icon: ShieldCheck,
    title: 'Transparent & Safe',
    description:
      'Every major recommendation includes a clear explanation. Estimates are labeled, never guaranteed.',
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-slate-200">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <div className="flex items-center gap-2 font-semibold text-slate-900">
            <Sparkles className="h-5 w-5 text-brand-600" />
            FOAI Financial Planner
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login" className="btn-secondary">
              Login
            </Link>
            <Link to="/register" className="btn-primary">
              Get Started
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
          <div className="max-w-3xl">
            <p className="mb-4 text-sm font-semibold uppercase tracking-wide text-brand-600">
              Foundation of AI — Academic Project
            </p>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
              AI-Based Personalized Financial Planning System
            </h1>
            <p className="mt-6 text-lg leading-8 text-slate-600">
              A decision-support platform that analyzes your financial profile, goals, and risk
              tolerance to recommend how much to save, invest, and allocate — with clear
              explanations at every step.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/register" className="btn-primary gap-2">
                Create Account
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/login" className="btn-secondary">
                Sign In
              </Link>
            </div>
          </div>
        </section>

        <section className="border-y border-slate-200 bg-slate-50 py-16">
          <div className="mx-auto grid max-w-6xl gap-6 px-4 sm:grid-cols-3 sm:px-6">
            {features.map(({ icon: Icon, title, description }) => (
              <div key={title} className="card">
                <div className="mb-4 inline-flex rounded-lg bg-brand-50 p-3 text-brand-700">
                  <Icon className="h-5 w-5" />
                </div>
                <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
                <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
          <DisclaimerBanner />
        </section>
      </main>
    </div>
  );
}
