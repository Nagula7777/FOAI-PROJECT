"""Genetic algorithm portfolio optimizer using DEAP."""

import random

from deap import algorithms, base, creator, tools

from app.ai.constraints import is_feasible
from app.ai.types import ConstraintBounds, FinancialContext, PortfolioAllocation, RiskProfile
from app.ai.utility import calculate_utility


def _repair(values: list[float], bounds: ConstraintBounds) -> list[float]:
    keys = ["equity", "bonds", "gold", "cash"]
    clipped = []
    for idx, key in enumerate(keys):
        clipped.append(max(bounds.min_alloc.get(key, 0), min(bounds.max_alloc.get(key, 1), values[idx])))
    total = sum(clipped) or 1.0
    return [v / total for v in clipped]


def optimize_portfolio(
    ctx: FinancialContext,
    risk: RiskProfile,
    bounds: ConstraintBounds,
    priorities: list[str],
    population_size: int = 60,
    generations: int = 40,
) -> tuple[PortfolioAllocation, dict]:
    if hasattr(creator, "FitnessMax"):
        del creator.FitnessMax
    if hasattr(creator, "Individual"):
        del creator.Individual

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    def random_individual():
        raw = [random.random() for _ in range(4)]
        total = sum(raw)
        return creator.Individual([v / total for v in raw])

    def evaluate(individual):
        repaired = _repair(list(individual), bounds)
        allocation = PortfolioAllocation.from_list(repaired)
        fitness = calculate_utility(allocation, ctx, risk, bounds, priorities)
        if not is_feasible(allocation, bounds, tolerance=0.03):
            fitness *= 0.5
        return (fitness,)

    def mate(ind1, ind2):
        for i in range(4):
            if random.random() < 0.5:
                ind1[i], ind2[i] = ind2[i], ind1[i]
        ind1[:] = _repair(list(ind1), bounds)
        ind2[:] = _repair(list(ind2), bounds)
        return ind1, ind2

    def mutate(individual):
        idx = random.randrange(4)
        individual[idx] = max(0, individual[idx] + random.uniform(-0.1, 0.1))
        individual[:] = _repair(list(individual), bounds)
        return (individual,)

    toolbox.register("individual", random_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", mate)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)
    algorithms.eaSimple(
        population,
        toolbox,
        cxpb=0.6,
        mutpb=0.25,
        ngen=generations,
        verbose=False,
    )

    best = tools.selBest(population, k=1)[0]
    repaired = _repair(list(best), bounds)
    allocation = PortfolioAllocation.from_list(repaired)
    stats = {
        "generations": generations,
        "population_size": population_size,
        "best_fitness": float(best.fitness.values[0]),
    }
    return allocation, stats
