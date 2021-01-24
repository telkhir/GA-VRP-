import random


class GenerationFactory:

    def __init__(self, genetic_problem):
        self.genetic_problem = genetic_problem

    def tournament_selection(self, genetic_problem, population, n_winners, k):
        winners = []
        for _ in range(n_winners):
            elements = random.sample(population, k)
            winners.append(min(elements, key=genetic_problem.fitness))
        return winners

    def cross_parents(self, genetic_problem, parents):
        children = []
        for i in range(0, len(parents), 2):
            children.extend(genetic_problem.crossover(parents[i], parents[i + 1]))
        return children

    def mutate(self, genetic_problem, population, prob):
        for item in population:
            genetic_problem.mutation(item, prob)
        return population
