from queens_fitness import *
import random

p_mutation = 0.2
num_of_generations = 100


def genetic_algorithm(population, fitness_fn, minimal_fitness, n):
    """Runs the genetic algorithm to solve the N-Queens problem."""
    max_fitness_reached = 0
    max_fitness_individual = None

    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))

        # Print only the best individual to keep output manageable
        fittest_individual = get_fittest_individual(population, fitness_fn)
        fitness = fitness_fn(fittest_individual)
        if fitness > max_fitness_reached:
            max_fitness_reached = fitness
            max_fitness_individual = fittest_individual

        print("Best individual: {} - fitness: {}".format(fittest_individual, fitness))
        print(f"Population size: {len(population)}")

        # Create a new population with fixed size to prevent unbounded growth
        new_population = set()

        # Select parents and create offspring
        selection_pool = list(population)
        # Limit population size if it gets too large
        if len(population) > 100:  # Limit pool size to prevent excessive growth
            selection_pool = select_top_individuals(population, fitness_fn, 100)

        for i in range(len(selection_pool) // 2):  # Create half as many offspring pairs as parents
            mother, father = random_selection(selection_pool, fitness_fn)
            child1, child2 = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child1 = mutate(child1, n)
            if random.uniform(0, 1) < p_mutation:
                child2 = mutate(child2, n)

            new_population.add(child1)
            new_population.add(child2)

        # Combine old and new population, then select top individuals
        combined_population = population.union(new_population)
        population = select_top_individuals(combined_population, fitness_fn, 100)  # Keep population size fixed

        # Check if we've found a solution
        fittest_individual = get_fittest_individual(population, fitness_fn)
        if minimal_fitness <= fitness_fn(fittest_individual):
            print(f"Solution found in generation {generation}!")
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    # Return the best solution found, even if it doesn't meet minimal_fitness
    return get_fittest_individual(population, fitness_fn)


def select_top_individuals(population, fitness_fn, n):
    """Select the top n individuals from the population based on fitness."""
    sorted_population = sorted(population, key=fitness_fn, reverse=True)
    return set(sorted_population[:n])


def print_population(population, fitness_fn):
    """Prints the population with their fitness values."""
    # Only print top 10 individuals to keep output manageable
    sorted_individuals = sorted(population, key=fitness_fn, reverse=True)
    for individual in sorted_individuals[:10]:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))
    if len(population) > 10:
        print(f"... and {len(population) - 10} more individuals")


def reproduce(mother, father):
    """Performs single-point crossover and returns two children."""
    crossover_point = random.randint(1, len(mother) - 1)
    child1 = mother[:crossover_point] + father[crossover_point:]
    child2 = father[:crossover_point] + mother[crossover_point:]
    return child1, child2


def mutate(individual, n):
    """Randomly changes one queen's row."""
    idx = random.randint(0, len(individual) - 1)
    new_row = random.randint(0, n - 1)
    mutated = list(individual)
    mutated[idx] = new_row
    return tuple(mutated)


def random_selection(population, fitness_fn):
    """Roulette-wheel selection based on fitness."""
    # Add 1 to all fitness values to handle case where all fitness values are 0
    population_list = list(population)
    fitness_values = [fitness_fn(ind) + 1 for ind in population_list]
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]

    selected = random.choices(population_list, weights=probabilities, k=2)
    return selected[0], selected[1]


def get_fittest_individual(iterable, func):
    """Returns the individual with the highest fitness."""
    return max(iterable, key=func)


def get_initial_population(n, count):
    """Generates an initial population of N-Queens solutions."""
    return set([
        tuple(random.randint(0, n - 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    """Runs the genetic algorithm for the N-Queens problem."""
    n = 8  # Number of queens
    minimal_fitness = 28  # Maximum number of non-attacking pairs for 8 queens

    initial_population = get_initial_population(n, 50)

    print(f"Starting genetic algorithm for {n}-queens problem")
    print(f"Looking for solution with fitness >= {minimal_fitness}")
    print(f"Initial population size: {len(initial_population)}")

    fittest = genetic_algorithm(initial_population, fitness_fn_positive, minimal_fitness, n)

    print('Fittest Individual: ' + str(fittest))
    print('Fitness: ' + str(fitness_fn_positive(fittest)))

    # Visualize the solution
    print("\nSolution visualization:")
    visualize_board(fittest, n)


def visualize_board(queens, n):
    """Visualize the chessboard with queens."""
    board = [['·' for _ in range(n)] for _ in range(n)]
    for col, row in enumerate(queens):
        board[row][col] = 'Q'

    for row in board:
        print(' '.join(row))


if __name__ == '__main__':
    main()