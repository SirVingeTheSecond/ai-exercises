"""
Lab 04 ▸ Exercise 2 — Genetic Algorithm for N‑Queens (uses queens_fitness.py)
============================================================================
Takeaways:
    • Chromosome = permutation of 0…N‑1 ⇒ **one queen per column & row** (implicit constraint).
    • Fitness = queens_fitness.**fitness_fn_positive** (non‑attacking pairs); `--neg` flag switches to conflict‑count.
    • Operators: **Order‑1 crossover** + **swap mutation** keep permutation validity.
    • Tournament selection + elitism + plot of the board.
    • Stores population as **list** (sequence) so `random.sample` works.
"""

import argparse, random, sys
from typing import List, Tuple
from queens_fitness import fitness_fn_positive, fitness_fn_negative  # official fitness helpers

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # fallback if matplotlib unavailable

# ── CLI ----------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Genetic Algorithm for N‑Queens (permutation encoding)")
parser.add_argument("N", nargs="?", type=int, default=8, help="Board size N (default 8)")
parser.add_argument("--plot", action="store_true", help="Show matplotlib board of best solution")
parser.add_argument("--neg", action="store_true", help="Use fitness_fn_negative instead of positive")
args = parser.parse_args()

N: int = args.N
POP_SIZE = 200
MAX_GENS = 2000
P_MUTATION = 0.3
TOUR_K = 3
ELITE = 2  # number of top individuals carried over each generation

MAX_FITNESS = N * (N - 1) // 2  # C(N,2) non‑attacking pairs (goal for positive fitness)
Chromosome = Tuple[int, ...]

# Pick fitness function based on flag ---------------------------------------------------
fitness = fitness_fn_negative if args.neg else fitness_fn_positive

def order_one_xover(mom: Chromosome, dad: Chromosome) -> Chromosome:
    """Order‑1 crossover (OX1) preserves permutation semantics."""
    a, b = sorted(random.sample(range(N), 2))
    child = [-1] * N
    # copy dad slice
    child[a:b+1] = dad[a:b+1]
    # fill remaining with mom's genes keeping order
    fill = [gene for gene in mom if gene not in child]
    idx = 0
    for i in range(N):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return tuple(child)

def swap_mutate(chrom: Chromosome) -> Chromosome:
    i, j = random.sample(range(N), 2)
    lst = list(chrom)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)

def tournament(pop: List[Chromosome], k: int = TOUR_K) -> Chromosome:
    """Return best of k random individuals."""
    return max(random.sample(pop, k), key=fitness)

def random_chrom() -> Chromosome:
    lst = list(range(N))
    random.shuffle(lst)
    return tuple(lst)

def genetic_algorithm() -> Chromosome:
    population: List[Chromosome] = [random_chrom() for _ in range(POP_SIZE)]
    best = max(population, key=fitness)

    for gen in range(MAX_GENS):
        best = max(population, key=fitness)
        best_fit = fitness(best)
        if gen % 100 == 0 or (not args.neg and best_fit == MAX_FITNESS):
            print(f"Gen {gen:4d} | best fitness = {best_fit}")
        # goal check
        if (not args.neg and best_fit == MAX_FITNESS) or (args.neg and best_fit == 0):
            print("\nSolution found!")
            return best

        # --- next generation ------------------------------------------------
        new_pop: List[Chromosome] = sorted(population, key=fitness, reverse=True)[:ELITE]
        while len(new_pop) < POP_SIZE:
            mom = tournament(population)
            dad = tournament(population)
            child = order_one_xover(mom, dad)
            if random.random() < P_MUTATION:
                child = swap_mutate(child)
            new_pop.append(child)
        population = new_pop
    print("Generation limit reached; returning best‑so‑far.")
    return max(population, key=fitness)

# ── ASCII & plot ----------------------------------------------------

def print_board(chrom: Chromosome):
    for row in range(N):
        print(" ".join('Q' if chrom[row] == col else '·' for col in range(N)))
    print()

def plot_board(chrom: Chromosome):
    if plt is None:
        print("matplotlib not installed; ASCII board shown instead.")
        return
    plt.figure(figsize=(N/2, N/2))
    plt.title(f"{N}-Queens Solution")
    ax = plt.gca()
    for r in range(N):
        for c in range(N):
            color = 'white' if (r+c)%2==0 else 'lightgray'
            ax.add_patch(plt.Rectangle((c, N-r-1), 1, 1, edgecolor='black', facecolor=color))
    ax.scatter([chrom[r]+0.5 for r in range(N)], [N-r-0.5 for r in range(N)], s=250, marker='♛', color='red')
    ax.set_xlim(0, N); ax.set_ylim(0, N); ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
    plt.show()

# ── main --------------------------------------------------------------------
if __name__ == "__main__":
    solution = genetic_algorithm()
    print("\nBest permutation:", solution)
    print_board(solution)
    if args.plot:
        plot_board(solution)
