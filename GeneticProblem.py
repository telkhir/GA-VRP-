import random
from random import randrange
import numpy as np

class GeneticProblem(object):

    def __init__(self, vehicles, stations, distances, mandatory_trips):
        self.vehicles = vehicles
        self.stations = stations
        self.distances = distances
        self.mandatory_trips = mandatory_trips

    def initial_population(self, initial_population_size):
        initial_population = []
        for _ in range(initial_population_size):
            chromosome = []
            journeys = []
            left_trips = self.mandatory_trips.copy()

            for vehicle in self.vehicles:
                # number of served trips for this vehicle
                served_trips_nb = random.randrange(0, len(left_trips))
                # sample this number from the mandatory trips
                trips_to_serve = random.sample(left_trips, served_trips_nb)

                homes, works = [], []
                for trip in trips_to_serve:
                    homes.append(trip[0])
                    works.append(trip[1])
                homes = [i for n, i in enumerate(homes) if i not in homes[:n]]
                works = [i for n, i in enumerate(works) if i not in works[:n]]
                journey = random.sample(homes, len(homes)) + random.sample(works, len(works))
                journeys.append(journey)

                # remove served trips from left_trips
                left_trips = [trip for trip in left_trips if trip not in trips_to_serve]

            if len(left_trips) > 1:
                for trip in left_trips:
                    # add the trip to any journey
                    pos = random.randrange(0, len(journeys))
                    journeys[pos].insert(0, trip[0])
                    journeys[pos].insert(len(journeys[pos]), trip[1])

            for vehicle, journey in zip(self.vehicles, journeys):
                chromosome += [vehicle]
                chromosome += [i for n, i in enumerate(journey) if i not in journey[:n]]  # unique values only

            initial_population.append(chromosome)
        return initial_population

    def mutation(self, chromosome, prob):
        def inversion_mutation(chromosome_aux):
            chromosome = chromosome_aux

            #index1 = randrange(0, len(chromosome))
            #index2 = randrange(index1, len(chromosome))

            #chromosome_mid = chromosome[index1:index2+1]
            #chromosome_mid.reverse()

            #chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2+1:]
            chromosome.reverse()
            return chromosome

        vehicles_trip_list, indices = self.split_at_values(chromosome, self.vehicles)
        chromosome_copy = chromosome.copy()
        for i, vehicleTrip in enumerate(vehicles_trip_list):
            if len(vehicleTrip) >= 2:
                if random.random() < prob:
                    first_ixd_W = 0
                    for j, item in enumerate(vehicleTrip):
                        if "W" in item:
                            first_ixd_W = j
                            break
                    aux_homes = vehicleTrip[:first_ixd_W]
                    aux_works = vehicleTrip[first_ixd_W:]
                    if len(vehicleTrip[:first_ixd_W]) >= 2:
                        aux_homes = inversion_mutation(vehicleTrip[:first_ixd_W])
                    if len(vehicleTrip[first_ixd_W:]) >= 2:
                        aux_works = inversion_mutation(vehicleTrip[first_ixd_W:])

                    chromosome_copy[indices[i] + 1: indices[i + 1] if i + 1 <= len(indices) - 1 else len(chromosome_copy)] = aux_homes + aux_works

        return chromosome

    def crossover(self, parent1, parent2):

        trips_parent1, _ = self.split_at_values(parent1, self.vehicles)
        trips_parent2, _ = self.split_at_values(parent2, self.vehicles)

        trips_child1 = trips_parent1.copy()
        trips_child2 = trips_parent2.copy()

        idx_vehicle_trip_to_cross = random.randrange(0, len(self.vehicles))

        trips_child1[idx_vehicle_trip_to_cross] = trips_parent2[idx_vehicle_trip_to_cross]
        trips_child2[idx_vehicle_trip_to_cross] = trips_parent1[idx_vehicle_trip_to_cross]

        child1 = [[vehicle] + trip for vehicle, trip in zip(self.vehicles, trips_child1)]
        child2 = [[vehicle] + trip for vehicle, trip in zip(self.vehicles, trips_child2)]

        # flatten the lists
        child1_flatten = [item for items in child1 for item in items]
        child2_flatten = [item for items in child2 for item in items]
        return [child1_flatten, child2_flatten]

    def fitness(self, chromosome):
        fitness_value = 0
        # methode1 : finettes s the sum of distances in a chromosome
        # for i in range(0, len(chromosome)-1):
        #    if chromosome[i] not in vehicles and chromosome[i+1] not in vehicles:
        #        fitness_value += distances[chromosome[i], chromosome[i+1]]

        vehicles_trip_list, _ = self.split_at_values(chromosome, self.vehicles)

        # methode 2 : fitness is max distance of trips
        trips_distances = []
        for vehicleTrip in vehicles_trip_list:
            distance = 0
            nb_stops = len(vehicleTrip)
            if nb_stops != 0:
                for i in range(0, len(vehicleTrip) - 1):
                    distance += self.distances[vehicleTrip[i], vehicleTrip[i + 1]]
            trips_distances.append(distance)

        fitness_value = max(trips_distances)

        for vehicleTrip in vehicles_trip_list:
            nb_stops = len(vehicleTrip)
            if nb_stops != 0:
                # trip must start by Home:
                if 'W' in vehicleTrip[0]:
                    fitness_value += 200000

                # each trip must contain Hs and Ws
                H_exist = False
                W_exist = False
                for stop in vehicleTrip:
                    if "W" in stop:
                        W_exist = True
                        break
                    if "H" in stop:
                        H_exist = True
                        break
                if H_exist is False or W_exist is False:
                    fitness_value += 200000

                # if W is before H this is not a valid chromosome, should have a very big distance (bad fitness)
                for i in range(0, nb_stops - 1):
                    if "W" in vehicleTrip[i] and "H" in vehicleTrip[i + 1]:
                        fitness_value += 100000
                        break

        # for each mandatory trips, at least one vehicle is serving it
        for mandatory_trip in self.mandatory_trips:
            trip_exist = False
            for vehicleTrip in vehicles_trip_list:
                if mandatory_trip[0] in vehicleTrip and mandatory_trip[1] in vehicleTrip:
                    trip_exist = True
                    break
                else:
                    continue
            if not trip_exist:
                fitness_value += 10000000
                break

        return fitness_value

    def total_distance(self, chromosome):
        total_distance = 0

        for i in range(0, len(chromosome) - 1):
            if chromosome[i] not in self.vehicles and chromosome[i + 1] not in self.vehicles:
                total_distance += self.distances[chromosome[i], chromosome[i + 1]]

        return total_distance

    def split_at_values(self, lst, values):
        indices = [i for i, x in enumerate(lst) if x in values]
        size = len(lst)
        res = [lst[indices[i] + 1: indices[i + 1] if i + 1 <= len(indices) - 1 else size] for i in
               range(0, len(indices))]
        return res, indices


