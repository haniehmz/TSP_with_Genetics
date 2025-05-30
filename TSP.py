
import random

def read(filename='in.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0])
        matrix = []
        for line in lines[1:]:
            matrix.append([int(x) for x in line.strip().split()])
    return n, matrix


def path_length(path, matrix):
    length = 0
    for i in range(len(path)):
        a = path[i]
        b = path[(i + 1) % len(path)]  
        dist = matrix[a][b]
        if dist == -1:
            return float('inf')  
        length += dist
    return length


def generate(n, size):
    popu = []
    for _ in range(size):
        new_path = list(range(n))
        random.shuffle(new_path)
        popu.append(new_path)
    return popu

def selection(population, matrix):
    fitness = []
    for path in population:
        length = path_length(path, matrix)
        fitnes = 1 / length if length > 0 else float('inf')
        fitness.append(fitnes)

    total_fitness = sum(fitness)
    prob = [f / total_fitness for f in fitness]

    selected = random.choices(population, weights=prob, k=1)[0]
    return selected

def crossover(parent1, parent2):
    size = len(parent1)
    end = random.randint(1,size-1)
    child = [-1] * size
    child[:end] = parent1[:end]
    pointer = end
    for gene in parent2:
        if gene not in child:
           child[pointer] = gene
           pointer += 1
    return child


def mutation(path, rate=0.1):
    if random.random() < rate:
        a, b = random.sample(range(len(path)), 2)
        path[a], path[b] = path[b], path[a]

def genetic(n, matrix, pop_size=100, generations=100):
    population = generate(n, pop_size)
    best = min(population, key=lambda p: path_length(p, matrix))

    for _ in range(generations):
        new_population = []
        for _ in range(pop_size):
            parent1 = selection(population, matrix)
            parent2 = selection(population, matrix)
            child = crossover(parent1, parent2)
            mutation(child)
            new_population.append(child)
        population = new_population
        current_best = min(population, key=lambda p: path_length(p, matrix))
        if path_length(current_best, matrix) < path_length(best, matrix):
            best = current_best

    return best, path_length(best, matrix)

if __name__ == '__main__':
    n, matrix = read()
    best, mind = genetic(n, matrix)
    best = [x + 1 for x in best]
    print(' '.join(map(str, best)))
    print(mind)