#!/usr/bin/python
import random
import csv
import argparse

# class to handle benefit and weight of items
class item:
    def __init__(self, benefit, weight, name):
        self.benefit = benefit
        self.weight = weight
        self.name = name

    def __str__(self):
        return "{}: ({}, {})".format(self.name, self.benefit, self.weight)

    def __repr__(self):
        return "{}: ({}, {})".format(self.name, self.benefit, self.weight)

# class to handle population members
class pop_member:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = None

    def __str__(self):
        return "Genes: {}\tFitness: {}".format(self.genes, self.fitness)

    def __repr__(self):
        return "Genes: {}\tFitness: {}".format(self.genes, self.fitness)

# method to generate a memeber of the population given the member's total genes
def generate_member(total_genes):
    genes = []
    for i in range(total_genes):
        genes.append(random.randint(0,1))

    return pop_member(genes)

# method to generate a population given the genes and size
def generate_population(pop_size, total_genes):
    population = []
    for i in range(pop_size):
        population.append(generate_member(total_genes))

    return population

# get the fitness of all memebers of the population
def fitness(pop, items, limit):
    for member in pop:
        mem_benefit = 0
        mem_weight = 0
        for i in range(len(member.genes)):
            if (member.genes[i]):
                mem_weight+=items[i].weight
                mem_benefit+=items[i].benefit

        if mem_weight > limit:
            member.fitness = -1
        else:
            member.fitness = mem_benefit

# method to crossover two parents into two children
def crossover(parent1, parent2):
    cross_point = random.randint(1, len(parent1)-2)
    child1 = list(parent1)
    child2 = list(parent2)
    for x in range(cross_point, len(parent1)):
        child1[x] = parent2[x]
        child2[x] = parent1[x]

    return child1, child2

# method to mutate a member
def mutate(member):
    mutate_point = random.randint(0, len(member)-1)
    member[mutate_point] ^= 1

def print_details(genes, gens, cross_chance, mut_chance, exit_reason):
    print("--------------------------------------------------")
    print("Total Gene Count: {}".format(genes))
    print("Max Generations: {}".format(gens))
    print("Chance for Crossover: {}".format(cross_chance))
    print("Chance for Mutation: {}".format(mut_chance))
    print(exit_reason)

def print_solution(genes, items):
    print("--------------------------------------------------")
    solution = []
    for x in range(len(items)):
        if genes[x]:
            solution.append(items[x].name)

    print("Get the following items: {}".format(solution))

def find_solution(pop_size, items, cross_chance, mut_chance, max_weight, max_gens, survival_rate, exit_rate, gen_updates):
    pop = generate_population(pop_size, len(items))
    new_members = int(round(pop_size - (pop_size*survival_rate)))
    exit_members = int(round(pop_size - (pop_size*exit_rate)))

    for gen in range(max_gens):
        # crossover if you get the right chance
        if random.uniform(0, 1) < cross_chance:
            parent1_id = random.randint(0, pop_size - 1)
            parent2_id = random.randint(0, pop_size - 1)
            crossover(pop[0].genes, pop[1].genes)

        # mutate if you get the right chance
        if random.uniform(0, 1) < mut_chance:
            mut_id = random.randint(0, pop_size - 1)
            mutate(pop[mut_id].genes)

        # calculate population fitness
        fitness(pop, items, max_weight)

        # sort the population
        pop.sort(key= lambda x: x.fitness, reverse=True)
        most_fit = pop[0]

        # print an update if it is the correct interval
        if gen % gen_updates == 0:
            print("Gen #{}  \tMost Fit Genes: {}\tHighest Fitness Value: {}".format(gen+1, most_fit.genes, most_fit.fitness))

        # if a certain % of the population agrees, exit
        exit_hits = 0
        for x in range(exit_members):
            if pop[x].fitness != most_fit.fitness:
                break
            exit_hits+=1
        if exit_hits == exit_members:
            print_details(len(items), max_gens, cross_chance, mut_chance, "Exiting on gen #{} due to over {} of the population being the same fitness".format(gen + 1, exit_rate))
            return most_fit

        # replace the lowest end of the population with new random members
        for x in range(new_members):
            pop.pop()
        for x in range(new_members):
            pop.append(generate_member(len(items)))

    print_details(len(items), max_gens, cross_chance, mut_chance, "Exiting due to reaching max generation #{}".format(max_gens))
    return pop[0]

# load the item data from a csv file
def load_data(filename):
    items = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        for value in data:
            items.append(item(float(value[1]), float(value[2]), value[0]))
    return items

# parser arguments to make running the program easier
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--population", help="the total population size (default 50)")
parser.add_argument("-f", "--filename", help="the location of the data file (defaults to knapsack.data)")
parser.add_argument("-c", "--crossover", help="crossover chance (defualts to .67)")
parser.add_argument("-m", "--mutation", help="mutation chance (defaults to .05")
parser.add_argument("-w", "--weight", help="max weight that cannot be passed (defaults to 22 for knapsack data)")
parser.add_argument("-g", "--gens", help="max gens before program stops (defaults to 1000)")
parser.add_argument("-s", "--survival", help="the top percent of the generation that will survive (defaults to .75)")
parser.add_argument("-e", "--exitrate", help="the percent of the population that has the same rate that will cause an early exit (defaults to .5)")
parser.add_argument("-u", "--updates", help="how many generations you recieve updates (defaults to 10)")
args = parser.parse_args()

if args.population:
    population = int(args.population)
else:
    population = 50

if args.filename:
    filename = args.filename
else:
    filename = "knapsack.data"

if args.crossover:
    crossrate=float(args.crossover)
else:
    crossrate=.67

if args.mutation:
    mutrate=float(args.mutation)
else:
    mutrate=.05

if args.weight:
    weight=float(args.weight)
else:
    weight=22

if args.gens:
    gens=int(args.gens)
else:
    gens=1000

if args.survival:
    survival=float(args.survival)
else:
    survival=.75

if args.exitrate:
    exit_rate=float(args.exitrate)
else:
    exit_rate=.5

if args.updates:
    updates=int(args.updates)
else:
    updates=20

# load data using the args filename
items = load_data(filename)

# find and print the most fit
most_fit = find_solution(population, items, crossrate, mutrate, weight, gens, survival, exit_rate, updates)
print_solution(most_fit.genes, items)
