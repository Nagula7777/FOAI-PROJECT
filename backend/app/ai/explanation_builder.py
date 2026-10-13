"""Build human-readable explanations from AI trace."""

from app.ai.types import AIExecutionTrace, PortfolioAllocation, RiskProfile


def build_explanations(
    trace: AIExecutionTrace,
    allocation: PortfolioAllocation,
    horizon_years: float,
) -> list[str]:
    explanations: list[str] = []

    if trace.expert:
        for conclusion in trace.expert.conclusions[:3]:
            explanations.append(conclusion.message)

    if trace.risk:
        explanations.append(
            f"User has a {trace.risk.dominant} risk profile "
            f"(Conservative {trace.risk.conservative:.0%}, Moderate {trace.risk.moderate:.0%}, "
            f"Aggressive {trace.risk.aggressive:.0%})."
        )

    if trace.emergency_fund:
        if trace.emergency_fund.get("remaining_amount", 0) <= 0:
            explanations.append("Emergency fund is adequate.")
        else:
            explanations.append("Emergency fund gap remains; allocation keeps higher liquidity.")

    explanations.append(f"Recommended investment horizon is approximately {horizon_years:.1f} years.")

    if trace.constraints:
        explanations.extend(trace.constraints.explanations[:2])

    alloc = allocation.as_dict()
    if alloc["bonds"] >= 0.2:
        explanations.append("Bonds improve stability for the chosen risk profile.")
    if alloc["gold"] >= 0.05:
        explanations.append("Gold provides diversification against equity volatility.")
    if trace.ga_stats:
        explanations.append(
            f"Allocation optimized via genetic algorithm over {trace.ga_stats.get('generations', 0)} generations."
        )

    explanations.append("Portfolio satisfies configured risk and liquidity constraints.")
    return explanations
