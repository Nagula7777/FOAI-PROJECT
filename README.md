# AI-Based Personalized Financial Planning System

Academic full-stack project using **classical AI techniques** — expert systems, fuzzy logic, constraint satisfaction, utility-based decision making, and genetic algorithms. **No machine learning.**

## Features

- User registration/login with JWT
- Financial profile (income, expenses, debts, assets)
- Multiple financial goals with achievement analysis
- Fuzzy logic risk profiling
- Rule-based financial health score (0–100)
- Emergency fund planner & investment capacity calculator
- Full AI recommendation pipeline with explainable output
- Genetic algorithm portfolio optimization (DEAP)
- What-if simulator, rebalancing, warnings
- Monthly reports with PDF download
- Admin dashboard

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, Vite, Tailwind CSS, Recharts |
| Backend | Python, FastAPI, Pydantic |
| Database | MongoDB |
| AI | NumPy, SciPy, scikit-fuzzy, DEAP |

## Quick Start

### MongoDB

```bash
docker compose up -d
```

Or use a local MongoDB instance on `mongodb://localhost:27017`.

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Default Admin

- Email: `admin@foai.local`
- Password: `Admin@123456`

## User Workflow

1. Register → Enter financial profile
2. Create goals → Complete risk assessment
3. Run AI Plan → View recommendation & explanations
4. Track dashboard, run what-if scenarios, download monthly reports

## AI Pipeline Order

1. Expert system → 2. Health score → 3. Emergency fund → 4. Investment capacity → 5. Fuzzy risk → 6. Constraints → 7. Genetic algorithm → 8. Utility ranking → 9. Explanation

## Tests

```bash
cd backend
.venv\Scripts\pytest
```

## Disclaimer

This system provides educational/decision-support recommendations based on user-provided information and configured assumptions. It does not constitute guaranteed financial advice.
