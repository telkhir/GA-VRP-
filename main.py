import random
from time import time
from DataReader import DataReader
from GeneticProblem import GeneticProblem
from GenerationFactory import GenerationFactory

# nb_generations: nb of times we will produce a generation (includes tournament, cross over and mutation )
# ratio_cross : ratio of the total population to be crossed over and mutated
# prob_mutate : mutation probability
# k: number of participants on the selection tournaments.
initial_population_size, nb_generations, ratio_cross, prob_mutate, k = 500, 100, 0.8, 0.05, 2

if __name__ == "__main__":

    # reading the data from the excel file
    dataReader = DataReader("data/data_transportationPb_mini.xlsx")
    data = dataReader.read_data()

    # creating the list of vehicle names
    vehicles = ['vehicle' + str(i) for i in range(0, int(data["nb_vehicles"]))]
    stations = list(data["all_stations"])
    distances = data["distances"]
    mandatory_trips = data["trips"]

    # How many time to run the whole algo
    problem_instances = 10
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
        print("Solution: {0}, Fitness: {1}, TotalDistance: {2}".format(bestChromosome,
                                                                       genetic_problem.fitness(bestChromosome),
                                                                       genetic_problem.total_distance(bestChromosome)))
    t1 = time()
    print("\n")
    print("Total time: ", (t1 - t0), " secs.\n")

