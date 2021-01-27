import random
from time import time
from DataReader import DataReader
from GeneticProblem import GeneticProblem
from GenerationFactory import GenerationFactory
import pprint

# initial_population_size: number of chromosomes in the initial population
# nb_generations: nb of times we will produce a generation (includes tournament, cross over and mutation )
# ratio_cross : ratio of the total population to be crossed over and mutated
# prob_mutate : mutation probability
# k: number of participants on the selection tournaments.
initial_population_size, nb_generations, ratio_cross, prob_mutate, k = 200, 100, 0.8, 0.05, 2

# How many time to run the whole algo: for mini and small: 10 is enough, for big :100
problem_instances = 10
DATA_PATH = "data/data_transportationPb_mini.xlsx"


if __name__ == "__main__":

    # reading the data from the excel file
    dataReader = DataReader(DATA_PATH)
    data = dataReader.read_data()

    data["nb_vehicles"] = 9

    # creating the list of vehicle names
    vehicles = ['vehicle' + str(i) for i in range(0, int(data["nb_vehicles"]))]
    stations = list(data["all_stations"])
    distances = data["distances"]
    mandatory_trips = data["trips"]
    best_results = []

    print("EXECUTING ", problem_instances, " INSTANCES ")
    genetic_problem = GeneticProblem(vehicles, stations, distances, mandatory_trips)
    generation_factory = GenerationFactory(genetic_problem)
    t0 = time()

    for _ in range(0, problem_instances):
        # Generate initial population
        new_population = genetic_problem.initial_population(initial_population_size)

        # Define the n_parents to transform and n_direct (parents that will not be transformed)
        n_parents = round(initial_population_size * ratio_cross)
        n_parents = (n_parents if n_parents % 2 == 0 else n_parents - 1)
        n_directs = initial_population_size - n_parents

        # Produce Generations
        for i in range(nb_generations):
            #print("######## Directs")
            directs = generation_factory.tournament_selection(genetic_problem, new_population, n_directs, k)
            #print("######## Crosses")
            crosses = generation_factory.cross_parents(genetic_problem,
                                                       generation_factory.tournament_selection(genetic_problem,
                                                                                               new_population,
                                                                                               n_parents, k))
            #print("######## Mutation")
            mutations = generation_factory.mutate(genetic_problem, crosses, prob_mutate)
            new_population = directs + mutations

        # Get the best solution chromosome
        bestChromosome = min(new_population, key=genetic_problem.fitness)
        if genetic_problem.fitness(bestChromosome) < 10000:
            best_results.append({"Chromosome": bestChromosome, "fitness": genetic_problem.fitness(bestChromosome),
                                 "total_distance": genetic_problem.total_distance(bestChromosome)})
        print("Solution: {0}, Fitness: {1}, TotalDistance: {2}".format(bestChromosome,
                                                                       genetic_problem.fitness(bestChromosome),
                                                                       genetic_problem.total_distance(bestChromosome)))
    print("########################################")
    for solution in best_results:
        print("Valid Solution: ", solution)
    print("########################################")
    best_solution = min(best_results, key=lambda x: x["fitness"])
    print("Best Solution: ")
    print("Fitness: ", best_solution["fitness"])
    print("Total Distance: ", best_solution["total_distance"])
    print("Journeys:")
    journeys, indices = genetic_problem.split_at_values(best_solution["Chromosome"], genetic_problem.vehicles)
    for journey, vehicle in zip(journeys, genetic_problem.vehicles):
        print([vehicle] + journey)

    t1 = time()
    print("\n")
    print("Total time: ", (t1 - t0), " secs.\n")

