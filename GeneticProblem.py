import random
from random import randrange
from time import time


class GeneticProblem(object):

    def __init__(self, genes, individuals_length):
        self.genes = genes
        self.individuals_length = individuals_length

    def initial_population(self, initial_population_size, vehicles, all_stations):
        initial_population = []
        for _ in range(initial_population_size):
            chromosome = []
            for vehicle in vehicles:
                vehicle_stops_nb = random.randrange(0, len(all_stations))
                trip = random.sample(list(all_stations), vehicle_stops_nb)
                chromosome += [vehicle]
                chromosome += trip
            initial_population.append(chromosome)
        return initial_population

    def mutation(self, chromosome, prob):
        def inversion_mutation(chromosome_aux):
            chromosome = chromosome_aux

            index1 = randrange(0, len(chromosome))
            index2 = randrange(index1, len(chromosome))

            chromosome_mid = chromosome[index1:index2]
            chromosome_mid.reverse()

            chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]

            return chromosome_result

        print(chromosome)
        vehiclesTripList, indices = split_at_values(chromosome, vehicles)
        i = 0
        for vehicleTrip in vehiclesTripList:
            if len(vehicleTrip) >= 2:
                if random.random() < prob:
                    aux = inversion_mutation(vehicleTrip)
                    chromosome[indices[i] + 1:indices[i + 1]] = aux
            i += 1
        print(chromosome)
        return chromosome

    def crossover(self, parent1, parent2):
        pos = random.randrange(1, min(len(parent1), len(parent2)))
        child1 = parent1[:pos] + parent2[pos:]
        child2 = parent2[:pos] + parent1[pos:]
        list_childs = process_vehicle_repeated(child1, child2)
        list_childs1 = process_gen_repeated_in_trip(list_childs[0], list_childs[1])
        # list_childs2 = process_vehicle_absent(list_childs1[0], list_childs1[1])
        # print(list_childs2[0])
        # print(list_childs2[1])
        return list_childs1

    def decodeVRP(chromosome):
        decoded_list = []
        for k in chromosome:
            if k in vehicles:
                decoded_list.append(frontier)
            else:
                decoded_list.append(k)
        return decoded_list

    def fitnessVRP(chromosome):
        def split_at_values(lst, values):
            indices = [i for i, x in enumerate(lst) if x in values]
            size = len(lst)
            res = [lst[i: j] for i, j in
                   zip([0] + [x + 1 for x in indices], indices + ([size] if indices[-1] != size else []))]
            return res

        fitness_value = 0
        # methode1 : finettes s the sum of distances in a chromosome
        # for i in range(0, len(chromosome)-1):
        #    if chromosome[i] not in vehicles and chromosome[i+1] not in vehicles:
        #        fitness_value += distances[chromosome[i], chromosome[i+1]]
        print(chromosome)

        vehiclesTripList = split_at_values(chromosome, vehicles)
        # methode 2 : fitness is max distance of trips
        tripDistances = []
        for vehicleTrip in vehiclesTripList:

            distance = 0
            nbStops = len(vehicleTrip)
            if nbStops != 0:
                for i in range(0, len(vehicleTrip) - 1):
                    distance += distances[vehicleTrip[i], vehicleTrip[i + 1]]
                tripDistances.append(distance)
            else:
                tripDistances.append(distance)
        fitness_value = max(tripDistances)

        for vehicleTrip in vehiclesTripList:
            nbStops = len(vehicleTrip)
            if nbStops != 0:

                # trip must start by Home:
                if 'W' in vehicleTrip[0]:
                    fitness_value += 100000
                # each trip must contain Hs and Ws
                H_exist = False
                W_exist = False
                for stop in vehicleTrip:
                    if "W" in stop:
                        W_exist = True
                    if "H" in stop:
                        H_exist = True
                if H_exist == False or W_exist == False:
                    fitness_value += 100000

                # if W is before H this is not a valid chromosome, should have a very big distance (bad fitness)
                for i in range(0, nbStops - 1):
                    if "W" in vehicleTrip[i] and "H" in vehicleTrip[i + 1]:
                        fitness_value += 100000
                        break

        return fitness_value

    def totalDistanceVRP(chromosome):
        def split_at_values(lst, values):
            indices = [i for i, x in enumerate(lst) if x in values]
            size = len(lst)
            res = [lst[i: j] for i, j in
                   zip([0] + [x + 1 for x in indices], indices + ([size] if indices[-1] != size else []))]
            return res

        total_distance = 0

        for i in range(0, len(chromosome) - 1):
            if chromosome[i] not in vehicles and chromosome[i + 1] not in vehicles:
                total_distance += distances[chromosome[i], chromosome[i + 1]]

        return total_distance


