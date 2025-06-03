"""
Lab 04 ▸ Exercise — Genetic Algorithm (max-3-bit)
=================================================
Takeaways:
    • GA loop = *Selection → Crossover → Mutation → Replacement*             # exam mantra
    • **Fitness** = decimal value of the 3-bit string → goal is 7 (111)      # page 4 PDF
    • **Roulette selection** biases toward fitter parents but keeps diversity
    • **Single-point crossover** + **bit-flip mutation** explore search space
"""

import random
from typing import List, Tuple, Set

# -------------------- hyper-parameters ------------------------------------- #
N_BITS              = 3              # chromosome length
POPULATION_SIZE     = 4              # small so trace fits on paper
P_MUTATION          = 0.2            # bit-flip probability
MAX_GENERATIONS     = 30             # stop-gap if optimum never found
TARGET_FITNESS      = 7              # 3-bit maximum

Individual = Tuple[int, ...]         # alias for readability


# -------------------- GA primitives ---------------------------------------- #
def fitness_function(ind: Individual) -> int:
    """Return decimal value of bit-string (admissible, monotonic)."""
    # enumerate(reversed(..)) → least-significant bit gets 2**0
    return sum(bit * (2 ** idx) for idx, bit in enumerate(reversed(ind)))


def random_selection(population: Set[Individual]) -> Tuple[Individual, Individual]:
    """Roulette-wheel selection – probability ∝ fitness+1 (avoid zeros)."""
    pop_list: List[Individual] = list(population)
    fitnesses = [fitness_function(ind) + 1 for ind in pop_list]  # +1 to handle all-zero pop
    total = sum(fitnesses)
    probs = [f / total for f in fitnesses]
    mother, father = random.choices(pop_list, weights=probs, k=2)
    return mother, father


def reproduce(mother: Individual, father: Individual) -> Individual:
    """Single-point crossover → child keeps prefix of mother + suffix of father."""
    cp = random.randint(1, N_BITS - 1)                   # avoid 0 & len
    return mother[:cp] + father[cp:]


def mutate(ind: Individual) -> Individual:
    """Bit-flip one random locus (with P_MUTATION outside)."""
    idx = random.randrange(N_BITS)
    mutated = list(ind)
    mutated[idx] = 1 - mutated[idx]                      # toggle 0↔1
    return tuple(mutated)


# -------------------- GA driver -------------------------------------------- #
def genetic_algorithm(initial_pop: Set[Individual]) -> Individual:
    population = set(initial_pop)
    for gen in range(MAX_GENERATIONS):
        best = max(population, key=fitness_function)
        print(f"Gen {gen:02d}  Best {best}  Fit={fitness_function(best)}")

        if fitness_function(best) >= TARGET_FITNESS:
            print("Optimum reached!\n")
            return best

        # --- produce next generation -------------------------------------- #
        new_population: Set[Individual] = set()
        while len(new_population) < POPULATION_SIZE:
            mom, dad = random_selection(population)
            child = reproduce(mom, dad)
            if random.random() < P_MUTATION:
                child = mutate(child)
            new_population.add(child)

        population = new_population                    # generational replacement

    print("Max generations hit — returning best found.\n")
    return max(population, key=fitness_function)


# -------------------- helper ------------------------------------------------ #
def random_individual() -> Individual:
    return tuple(random.randint(0, 1) for _ in range(N_BITS))


# -------------------- demo run --------------------------------------------- #
if __name__ == "__main__":
    seed_pop = {random_individual() for _ in range(POPULATION_SIZE)}
    print("Initial population:", seed_pop, "\n")
    best = genetic_algorithm(seed_pop)
    print("Best individual :", best)
    print("Decimal value   :", fitness_function(best))
