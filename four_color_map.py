from random import choice
from itertools import chain
import random
import sys

# Parameters
mask = '1111111100000000'  # The reproduction mask.We ensure fairness by copying equal amount of bits from each parent.
colors = ['R', 'Y', 'G', 'B']  # The four allowed colours. Red,Yellow,Green,Blue.

# Use a dictionary to represent the adjacent areas, as seen in map.png
adjacency_dict = {0: [1, 2, 3, 12, 14, 15], 1: [0, 2, 4, 7, 8, 13, 14, 15], 2: [0, 1, 3, 4, 5], 3: [0, 2, 5, 12],
                  4: [1, 2, 5, 6, 8, 9],
                  5: [2, 3, 4, 6, 10, 12], 6: [4, 5, 9, 10], 7: [1, 8, 13], 8: [1, 4, 7, 9, 11, 13],
                  9: [4, 6, 8, 10, 11], 10: [5, 6, 9, 11, 12],
                  11: [8, 9, 10, 12, 13, 14], 12: [0, 3, 5, 10, 11, 14], 13: [1, 7, 8, 11, 14],
                  14: [0, 1, 11, 12, 13, 15], 15: [0, 1, 14]}


# Fitness function to evaluate the fitness of the chromosomes
# The function accepts a list of chromosomes.
# First,we build a dictionary with the fitness value for each chromosome, initialized to zero.
# For each chromosome in our population, and for each gene in each chromosome,fitness is increased by one WHEN:
# Two adjacent areas have different colours. So, the least possible fitness is 0 (all adjacent areas same colour),
# and the maximum is achieved when all adjacent vertices have a different colour. So it's 16.

def fitness_function(population):
    # Initialize the fitness dictionary.
    fitness_dict = {chromosome: 0 for chromosome in population}
    # Loop through chromosomes, and check if each gene is adjacent to the ones defined in the above adjacency_dict
    for chromosome in fitness_dict:
        for gene_index, gene in enumerate(chromosome):
            # Loop through adjacency_dict list elements. Can probably be made even more efficient, avoiding lists
            adj_genes = []
            for adj_index in adjacency_dict[gene_index]:
                adj_genes.append(chromosome[adj_index])
            if gene not in adj_genes:
                fitness_dict[chromosome] += 1

    return fitness_dict


# A simple single crossover function

def single_crossover(parent1, parent2, cur_mask):
    child1 = ''
    child2 = ''

    # Find last "1"in mask.
    i = cur_mask.rfind('1')
    # First child
    child1 += parent1[:i]
    child1 += parent2[i:]
    # Second child
    child2 += parent2[:i]
    child2 += parent1[i:]

    return child1, child2


# Randomly generate initial population of strings (representing chromosomes) of size popSize
# Then append them to a list of strings. This will be the initial population

def generate_initialpop(pop_size):
    chromosomes = []
    for x in range(pop_size):
        a_chrom = (''.join(choice(colors) for i in range(16)))
        chromosomes.append(a_chrom)
    return chromosomes


# Fitness proportionate selection function
# Uses typical roulette wheel selection as shown in the course's book

def weighted_choice(population):
    max_fit = sum(population.values())
    pick = random.uniform(0, max_fit)
    current = 0
    for chromosome, value in population.items():
        current += value
        if current > pick:
            return chromosome


def main():
    # Generate initial population and fitness score
    # Add a counter to count number of generations passed

    generations_passed = 0
    pop_size = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    init_population = generate_initialpop(pop_size)
    fitness = fitness_function(init_population)

    # Parents,children and new population.
    prod_chromosomes = []
    children = []
    new_population = []

    # Loop until fitness max is met.
    while max(fitness.values()) < 16:
        print('Iterating')
        generations_passed += 1
        new_population.clear()
        # Add fit chromosomes to population(50% population renewal)
        for i in range(int(pop_size / 2)):
            new_population.append(weighted_choice(fitness))
        # Add fit chromosomes to parent population(50% population reproduction)
        for i in range(int(pop_size / 2)):
            prod_chromosomes.append(weighted_choice(fitness))
        # Call crossover function to get children tuples from each pair
        for x in range(int(len(prod_chromosomes) / 2)):
            children.append(single_crossover(prod_chromosomes[x], prod_chromosomes[x + 1], cur_mask=mask))

        # Unpack the list of tuples to a list of strings-chromosomes.
        children = list(chain.from_iterable(children))
        # Add the children to the population.
        new_population = new_population + children
        # Random shuffle to select chromosomes to be mutated.
        random.shuffle(new_population)
        # Initialise mutated population list.
        mutated_population = []
        # Iterate through 1% of chromosomes in total population.
        # Mutation rate is 1%.
        for chromosome in new_population[0:int(pop_size / 100)]:
            # Pick a random gene from each chromosome to be mutated.
            random_gene = random.randint(0, len(chromosome) - 1)
            # Create a list without the color that will be mutated.
            new_colors = colors[:]
            # print(new_colors)
            # print(chromosome[random_gene])
            new_colors.remove(str(chromosome[random_gene]))
            # Form a new list of mutated chromosomes
            mutated_chromosome = '' + chromosome[:random_gene] + random.choice(new_colors) + chromosome[
                                                                                             random_gene + 1:]
            mutated_population.append(mutated_chromosome)
            new_colors.clear()
            # print('Next')
        # Replace chromosomes in old population with mutated ones
        new_population[0:int(pop_size / 100)] = mutated_population
        # Calculate fitness for the new population
        fitness = fitness_function(new_population)
        # Clear lists to avoid memory leak
        prod_chromosomes = []
        children = []
        # Calculate average fitness for the fitness dictionary
        count = 0
        _sum = 0
        for key in fitness:
            count += 1
            _sum += fitness[key]
        # Print results
        print("New population length is: ", len(new_population))
        print(fitness)
        print('Average fitness: ', _sum / count)
        print('Max fitness: ', max(fitness.values()))
    print("Winning chromosome: ", max(fitness, key=fitness.get), "Fitness is: ", max(fitness.values()))
    print("Generations passed: ", generations_passed)
    print("Initial population was: ", pop_size)


main()
