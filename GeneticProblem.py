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

            for _ in self.vehicles:
                # number of served trips for this vehicle
                served_trips_nb = random.randrange(0, 2)
                # sample this number from the mandatory trips
                trips_to_serve = random.sample(left_trips, served_trips_nb)

                homes, works = [], []
                for trip in trips_to_serve:
                    homes.append(trip[0])
                    works.append(trip[1])

                # get unique values only
                homes = [i for n, i in enumerate(homes) if i not in homes[:n]]
                works = [i for n, i in enumerate(works) if i not in works[:n]]
                journey = random.sample(homes, len(homes)) + random.sample(works, len(works))
                journeys.append(journey)

                # remove served trips from left_trips
                left_trips = [trip for trip in left_trips if trip not in trips_to_serve]

            if len(left_trips) > 1:
                left_trips_copy = left_trips.copy()
                for trip in left_trips:
                    trip_exist = False
                    for journey in journeys:
                        if trip[0] in journey and trip[1] in journey:
                            trip_exist = True
                            left_trips_copy.remove(trip)
                            break
                    if trip_exist is False:
                        # add the trip to any journey
                        my_journeys_idx = []
                        #for idx, journey in enumerate(journeys):
                        #    if trip[0] in journey or trip[1] in journey:
                        #        my_journeys_idx.append(idx)
                        if len(my_journeys_idx) != 0:
                            pos = random.choice(my_journeys_idx)
                        else:
                            pos = random.randrange(0, len(journeys))
                        first_ixd_W = 0
                        #for j, item in enumerate(journeys[pos]):
                        #    if "W" in item:
                        #        first_ixd_W = j
                        #        break
                        #if first_ixd_W != 0:
                        #    journeys[pos].insert(random.randrange(0, first_ixd_W), trip[0])
                        #    journeys[pos].insert(random.randrange(first_ixd_W, len(journeys[pos])), trip[1])
                        #else:
                        #    journeys[pos].insert(first_ixd_W, trip[0])
                        #    journeys[pos].insert(first_ixd_W+1, trip[1])
                        journeys[pos].insert(0, trip[0])
                        journeys[pos].insert(len(journeys[pos]), trip[1])


            # delete redandent w in a chromosome
            for trip in self.mandatory_trips:
                journey_of_existance = []
                journey_ixd = []
                for i, journey in enumerate(journeys):
                    if trip[0] in journey and trip[1] in journey:
                        journey_of_existance.append(journey)
                        journey_ixd.append(i)
                if len(journey_ixd) != 0:
                    journeys_idx_to_drop_trip_from = random.sample(journey_ixd, len(journey_ixd)-1)
                    for ixd in journeys_idx_to_drop_trip_from:
                        # remove trip
                        journeys[ixd] = [x for x in journeys[ixd] ]# if x != trip[1] and x != trip[0]]

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
        #for i in range(0, len(chromosome)-1):
        #    if chromosome[i] not in self.vehicles and chromosome[i+1] not in self.vehicles:
        #        fitness_value += self.distances[chromosome[i], chromosome[i+1]]

        vehicles_trip_list, _ = self.split_at_values(chromosome, self.vehicles)

        ## methode 2 : fitness is max distance of trips
        trips_distances = []
        for vehicleTrip in vehicles_trip_list:
            distance = 0
            nb_stops = len(vehicleTrip)
            if nb_stops != 0:
                for i in range(0, len(vehicleTrip) - 1):
                    distance += self.distances[vehicleTrip[i], vehicleTrip[i + 1]]
            trips_distances.append(distance)

        fitness_value = max(trips_distances)
        #fitness_value = sum(trips_distances)

        ## for each mandatory trips, at least one vehicle is serving it
        for mandatory_trip in self.mandatory_trips:
            trip_exist = False
            for vehicleTrip in vehicles_trip_list:
                if mandatory_trip[0] in vehicleTrip and mandatory_trip[1] in vehicleTrip:
                    trip_exist = True

            if trip_exist is False:
                fitness_value += 1000000
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


