# AI-Based Personalized Financial Planning System

## 1. Project Overview
This project is a full-stack financial planning and recommendation system that helps users manage their personal finances using rule-based and classical AI techniques instead of machine learning. The platform allows users to register, complete their financial profile, set goals, assess financial risk, receive AI-driven recommendations, simulate scenarios, and monitor portfolio performance.

The system is designed for educational and decision-support use. It combines:
- expert system rules
- fuzzy logic risk analysis
- financial health score calculation
- emergency fund planning
- investment capacity evaluation
- portfolio optimization through genetic algorithms
- explainable recommendation outputs

The system is built with:
- Frontend: React + Vite + Tailwind CSS
- Backend: Python + FastAPI
- Database: MongoDB
- AI logic: NumPy, SciPy, scikit-fuzzy, DEAP

---

## 2. Website Workflow (End-to-End)

### Step 1: Landing and Authentication
When the user opens the website, they reach the landing page. From there they can:
- register a new account
- log in to an existing account
- access the default admin login for system administration

Authentication is handled through JWT (JSON Web Tokens) using FastAPI routes under `/api/auth`.

Typical flow:
1. User enters name, email, password.
2. Backend validates fields.
3. User is created in MongoDB.
4. JWT token is issued.
5. User is redirected to onboarding or dashboard.

### Step 2: Onboarding and Financial Profile
After login, the user completes onboarding.
This includes entering:
- age
- employment status
- dependents
- monthly income
- expenses
- debts
- assets
- savings or emergency fund status

This profile becomes the base financial context for all future decision-making. The backend stores profile data in MongoDB collections such as:
- users
- financial_profiles
- debts
- assets

### Step 3: Risk Assessment
The system evaluates the user’s risk profile using a questionnaire-based risk assessment.
This step helps determine:
- conservative, moderate, or aggressive risk preference
- risk tolerance
- investment comfort level

The risk data is later used by the AI pipeline and fuzzy logic modules.

### Step 4: Goal Creation and Goal Analysis
Users can create one or more financial goals such as:
- emergency fund
- buying a home
- education planning
- vacation / lifestyle goals
- retirement planning

Each goal contains:
- goal name
- target amount
- target date
- priority
- linked financial assumptions

The system assesses whether the goal is achievable based on current income, expenses, savings, and investment capacity.

### Step 5: Financial Health Evaluation
The backend computes a financial health score using rule-based evaluation.
This score considers:
- income vs expenses
- debt burden
- emergency fund adequacy
- asset strength
- budget stability
- risk sensitivity

The score is displayed on the dashboard and helps the user understand their financial position.

### Step 6: AI Recommendation Engine
After the user profile, goals, and risk assessment are ready, the system triggers the AI analysis pipeline.

The recommendation process uses a multi-stage flow:
1. Expert system evaluates user priorities and conditions.
2. Financial health score is computed.
3. Emergency fund requirement is estimated.
4. Investment capacity is calculated.
5. Fuzzy risk analysis determines the dominant risk profile.
6. Constraint bounds are derived.
7. Genetic algorithm optimizes the portfolio.
8. Utility ranking selects the best portfolio solution.
9. Explainable recommendations and warnings are generated.

The final output includes:
- recommended monthly investment amount
- recommended investment horizon
- asset allocation percentages
- recommended products
- explanations for each recommendation
- disclaimer statements

### Step 7: Portfolio and Investment Explorer
The system offers a portfolio view where users can see:
- current allocation
- target allocation
- drift from target
- risk exposure
- recommended holdings

The Investment Explorer page provides a list of investment products such as:
- Nifty 50 Index Fund
- Flexi-cap Fund
- Government Bonds
- Corporate Bonds
- Gold ETF
- Liquid Fund

Each product also includes:
- asset class
- risk category
- expected return assumption
- liquidity level
- minimum time horizon

### Step 8: What-if Simulator
The platform allows users to simulate financial scenarios such as:
- income increase
- change in expenses
- emergency fund changes
- change in target amount
- increased savings rate
- different investment assumptions

This helps the user understand how financial decisions affect future goals and portfolio planning.

### Step 9: Rebalancing and Warnings
The system detects:
- financial warning conditions
- debt burden stress
- emergency fund shortfall
- goal mismatch
- over-concentration risk

It also suggests rebalancing actions to align the actual portfolio with recommended target allocation.

### Step 10: Monthly Reports
The system generates monthly reports summarizing:
- financial standing
- goal status
- risk profile
- AI recommendation outcome
- allocation analysis
- PDF export for reporting

Reports are stored in MongoDB and can be viewed or downloaded as PDF files.

### Step 11: Admin Dashboard
The admin can:
- view system summary metrics
- inspect overall usage
- manage product inventory
- monitor system activity
- manage user and recommendation data

The admin panel acts as the system control layer.

---

## 3. System Architecture

### Frontend Layer
The frontend is built in React and uses route-based navigation.
The main pages include:
- Landing
- Register/Login
- Onboarding
- Profile
- Risk Assessment
- Dashboard
- Goal Pages
- Recommendation Page
- Portfolio
- Investment Explorer
- Simulator
- Rebalancing
- Reports
- Admin Dashboard

### Backend Layer
FastAPI handles the REST API and business logic. It exposes endpoints such as:
- /api/auth/register
- /api/auth/login
- /api/auth/me
- /api/profile
- /api/goals
- /api/risk-assessment
- /api/financial-health
- /api/ai/analyze
- /api/ai/recommendation
- /api/portfolio
- /api/simulation/what-if
- /api/reports/monthly

### Database Layer
MongoDB stores:
- user accounts
- financial profiles
- goals
- risk assessments
- recommendations
- portfolio allocations
- reports
- product catalog

### AI Layer
The AI layer includes:
- expert system rules
- fuzzy membership logic
- health score computation
- emergency fund analysis
- investment capacity modeling
- genetic optimization for portfolio allocations

---

## 4. Data Flow Summary
User actions in the frontend trigger API calls. The backend loads the relevant user context, pulls current data from MongoDB, runs the AI logic, and returns the result as JSON. The frontend updates the dashboard, recommendations, charts, and portfolio views.

A simplified flow is:

Browser -> React Pages -> API Client -> FastAPI Routes -> Services -> MongoDB + AI logic -> JSON Response -> UI Update

---

## 5. Key Algorithms Used

### Expert System
Uses rule-based decision logic to evaluate user situations and infer priorities.
Examples:
- emergency fund shortage
- high-interest debt
- low savings
- aggressive investment need

### Fuzzy Risk Analysis
Uses fuzzy logic to interpret risk levels not as fixed numbers, but as degrees of belonging to categories such as conservative, moderate, and aggressive.

### Financial Health Score
Creates a score between 0 and 100 based on financial stability dimensions.

### Investment Capacity Calculation
Determines how much the user can invest monthly after considering emergency security and core obligations.

### Genetic Algorithm Optimization
Optimizes portfolio allocation across asset classes such as equity, bonds, gold, and cash by maximizing fit to the user’s goals and risk profile.

### Utility-Based Recommendation Ranking
Ranks different candidate portfolios based on suitability, expected return, risk balance, and practical constraints.

---

## 6. Security and User Experience Features
- JWT authentication
- protected routes for logged-in users
- admin-only routing
- disclaimers for financial recommendation scope
- clear visual dashboards and charts
- PDF report generation
- explainable AI output for decision support

---

## 7. Real-World Usefulness
This project is useful because it:
- simplifies financial planning for non-experts
- visualizes personal financial health
- supports goal-driven decisions
- demonstrates classical AI decision systems
- explains “why” behind recommendations
- encourages realistic and safer financial planning

---

## 8. Conclusion
The website works as a complete financial planning assistant for users who want to understand their current financial health, define goals, choose a risk profile, and receive practical recommendations. Its importance lies in combining classical AI with accessible web technology to help users make better financial decisions through structured reasoning and explainable suggestions.

This project is not only a financial website but also an educational demonstration of how expert systems, fuzzy logic, optimization algorithms, and decision-support systems can be implemented in a real application.
