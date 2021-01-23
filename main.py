import random
from random import randrange
from time import time
from DataReader import DataReader
from GeneticProblem import GeneticProblem


def new_generation_t(genetic_problem, k, population, n_parents, n_directs, prob_mutate):

    def tournament_selection(genetic_problem, population, n, k):
        winners = []
        for _ in range(n):
            elements = random.sample(population, k)
            winners.append(min(elements, key=genetic_problem.fitness))
        return winners

    def cross_parents(genetic_problem, parents):
        childs = []
        for i in range(0, len(parents), 2):
            childs.extend(genetic_problem.crossover(parents[i], parents[i + 1]))
        return childs

    def mutate(genetic_problem, population, prob):
        for i in population:
            genetic_problem.mutation(i, prob)
        return population

    print("##############################directs")
    directs = tournament_selection(Problem_Genetic, population, n_directs, k)
    print("##############################Crosses")
    crosses = cross_parents(Problem_Genetic,
                            tournament_selection(Problem_Genetic, population, n_parents, k))
    # print("##############################mutattion")
    # mutations = mutate(Problem_Genetic, crosses, prob_mutate)
    new_generation = directs + crosses

    return new_generation



if __name__ == "__main__":

    # reading the data from the excel file
    dataReader = DataReader("data/data_transportationPb_mini.xlsx")
    data = dataReader.read_data()

    # creating the list of vehicle names
    vehicles = ['vehicle' + str(i) for i in range(0, int(data["nb_vehicles"]))]
    frontier = "######"

    # How many time to run the whole algo
    problem_instances = 1
    print("EXECUTING ", problem_instances, " INSTANCES ")
    genetic_problem = GeneticProblem(list(data["all_stations"]) + vehicles[:-1], len(list(data["all_stations"])))

    print("------------------------- Executing VRP ----------------------------- \n")
    print("Frontier = ", frontier)
    print("")
    t0 = time()
    initial_population_size = 10
    # nb of times we will produce a generation (this includes tournemenet, cross over and mutation for each generation)
    nb_generations = 100
    # ratio of the total population to be crossed over and mutated
    ratio_cross = 0.8
    # mutation probability
    prob_mutate = 0.05
    for _ in range(0, problem_instances):
        # Generate initial population
        population = genetic_problem.initial_population(initial_population_size, vehicles, data["all_stations"])

        n_parents = round(initial_population_size * ratio_cross)
        n_parents = (n_parents if n_parents % 2 == 0 else n_parents - 1)
        n_directs = initial_population_size - n_parents
        print("n_of parent to cross ", n_parents)

        # generate generations
        for _ in range(nb_generations):
            population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)

        bestChromosome = min(population, key=Problem_Genetic.fitness)
        # print("Chromosome: ", bestChromosome)
        genotype = Problem_Genetic.decode(bestChromosome)
        print(
            "Solution: {0}, Fitness: {1}, TotalDistance: {2}".format(genotype, Problem_Genetic.fitness(bestChromosome),
                                                                     Problem_Genetic.total_distance(bestChromosome)))
        return (genotype, Problem_Genetic.fitness(bestChromosome))
        #genetic_algorithm_t(VRP_PROBLEM, 2, min, 2, 10, 0.8, 0.05)
    t1 = time()
    print("\n")
    print("Total time: ", (t1 - t0), " secs.\n")

