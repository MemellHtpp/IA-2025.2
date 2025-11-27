import random

# ================================
# FINE-TUNING CONFIG
# (Aqui você ajusta os parâmetros!)
# ================================
USE_INITIAL_STATE = True
USE_MANHATTAN = True

INITIAL_STATE = [1, 4, 2,
                 3, 5, 0,
                 6, 7, 8]

GOAL_STATE = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]

POPULATION_SIZE = 150
MUTATION_RATE = 0.1
MAX_GENERATIONS = 2000
TOURNAMENT_SIZE = 5
# ================================


# Precomputação das posições do objetivo (para Manhattan)
GOAL_POSITIONS = {value: (i // 3, i % 3) for i, value in enumerate(GOAL_STATE)}


# Fitness 1: peças fora do lugar
def fitness_misplaced(state):
    return sum(1 for i in range(9) if state[i] != GOAL_STATE[i])


# Fitness 2: distância Manhattan
def fitness_manhattan(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        curr_row, curr_col = i // 3, i % 3
        goal_row, goal_col = GOAL_POSITIONS[tile]
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance


# Selecionador de fitness: agora baseado no fine-tuning
def fitness(state):
    if USE_MANHATTAN:
        return fitness_manhattan(state)
    return fitness_misplaced(state)


# Verifica solvabilidade
def is_solvable(puzzle):
    inv_count = sum(
        1 for i in range(8) for j in range(i + 1, 9)
        if puzzle[i] and puzzle[j] and puzzle[i] > puzzle[j]
    )
    return inv_count % 2 == 0


# Gera indivíduo válido
def generate_individual():
    state = list(range(9))
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return state


# Seleção por torneio
def select_parents(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    tournament.sort(key=fitness)
    return tournament[0], tournament[1]


# Crossover
def crossover(parent1, parent2):
    point = random.randint(1, 7)
    child = parent1[:point]
    for gene in parent2:
        if gene not in child:
            child.append(gene)
    return child


# Mutação
def mutate(individual):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(9), 2)
        individual[i], individual[j] = individual[j], individual[i]


# Algoritmo Genético
def genetic_algorithm():

    population = []

    # Se usar estado inicial fixo
    if USE_INITIAL_STATE:
        if not is_solvable(INITIAL_STATE):
            print("ERROR: Initial state is not solvable!")
            return None

        population.append(INITIAL_STATE.copy())

        while len(population) < POPULATION_SIZE:
            population.append(generate_individual())
    else:
        population = [generate_individual() for _ in range(POPULATION_SIZE)]

    # Loop evolutivo
    for generation in range(MAX_GENERATIONS):
        population.sort(key=fitness)
        best = population[0]
        print(f"Generation {generation} | Best fitness: {fitness(best)} | State: {best}")

        if fitness(best) == 0:
            print("Goal reached!")
            return best

        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = select_parents(population)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    print("Goal not reached within the generation limit.")
    return None


# Executa
if __name__ == "__main__":
    print("=== Genetic Algorithm for 8-Puzzle ===")
    print(f"Using Manhattan Distance: {USE_MANHATTAN}")
    print(f"Using predefined initial state: {USE_INITIAL_STATE}\n")

    solution = genetic_algorithm()

    if solution:
        print("\nFinal solution:", solution)