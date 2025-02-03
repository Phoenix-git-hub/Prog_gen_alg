import random
import numpy as np


class MethodsOfSelection:
    def __init__(self):
        # пожалуй нужно сделать файл config куда я положу общие данные для всего кода
        self.possible_names_of_selection = ('selection_of_the_best', 'roulette_selection', 'tournament_with_parent',
                                            'random_tournament_selection')
        self.name_of_selection = dict.fromkeys(self.possible_names_of_selection)

        self.name_of_selection['selection_of_the_best'] = self.selection_of_the_best
        self.name_of_selection['roulette_selection'] = self.roulette_selection
        self.name_of_selection['tournament_with_parent'] = self.tournament_with_parent
        self.name_of_selection['random_tournament_selection'] = self.random_tournament_selection

        self.number_of_vertices = None
        self.selection_method = None
        self.population_size = None
        self.adjacency_matrix = None
        self.parent_index = None

    def initialize_method_of_selection(self, name_of_method):

        if name_of_method not in self.possible_names_of_selection:
            error_str = f'nonexistent name of crossing'
            raise Exception(error_str)

        self.selection_method = self.name_of_selection[name_of_method]

    def initialize_fitness_function(self, fitness_function):
        self.fitness_function = fitness_function

    def initialize_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def initialize_population_size(self, population_size):
        self.population_size = population_size

    def initialize_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix

    def do_selection(self, population, new_population, parent_index = None):

        self.parent_index = parent_index
        return self.selection_method(population, new_population)

    def selection_of_the_best(self, population, new_population):
        #все переписать
        candidate_fitness = [[i, self.fitness_function(new_population[i])] for i in range(self.population_size)]
        population_fitness = [[i, self.fitness_function(population[i])] for i in range(self.population_size)]

        for i in range(1, self.population_size):
            for j in range(self.population_size - i):
                if population_fitness[j][1] < population_fitness[j + 1][1]:
                    a = population_fitness[j].copy()
                    population_fitness[j] = population_fitness[j + 1].copy()
                    population_fitness[j + 1] = a

        for i in range(1, self.population_size):
            for j in range(self.population_size - i):
                if candidate_fitness[j][1] > candidate_fitness[j + 1][1]:
                    a = candidate_fitness[j].copy()
                    candidate_fitness[j] = candidate_fitness[j + 1].copy()
                    candidate_fitness[j + 1] = a

        index = 0
        for i in candidate_fitness:
            if i[1] < population_fitness[index][1]:
                population[population_fitness[index][0]] = new_population[i[0]].copy()
                index += 1

    def roulette_selection(self, population, new_population):


        value_fitness = np.array([0] * self.population_size * 2, dtype='float64')
        flag_min_val = True
        min_val = 0
        flag_max_val = True
        max_val = 0

        for i in range(self.population_size):
            val = self.fitness_function(population[i])
            value_fitness[i] = val

            if flag_min_val or min_val > val:
                flag_min_val = False
                min_val = val
            if flag_max_val or max_val < val:
                max_val = val
                flag_max_val = False

        for i in range(self.population_size):

            val = self.fitness_function(new_population[i])
            value_fitness[i + self.population_size] = val

            if flag_min_val or min_val > val:
                min_val = val
                flag_min_val = False
            if flag_max_val or max_val < val:
                max_val = val
                flag_max_val = False
        if min_val == max_val:
            min_val -= 0.000001

        elit = np.argsort(value_fitness)[:int(self.population_size / 1.3)]

        value_fitness = np.delete(value_fitness, elit)

        # этот коэфицент надо настраивать
        ratio_1 = 1000 / (-max_val + min_val)
        ratio_2 = 1 - (ratio_1 * max_val)

        sum_value = 0
        # print('до изменений')
        # print(value_fitness)
        # print()
        for i in range(self.population_size * 2 - len(elit)):
            value_fitness[i] = value_fitness[i] * ratio_1 + ratio_2
            sum_value += value_fitness[i]
        # print('val')
        # print(value_fitness)
        # print()
        value_fitness /= value_fitness.sum()

        # print(value_fitness)
        # print()
        ind = np.random.choice([i for i in range(self.population_size * 2) if i not in elit],
                               self.population_size - len(elit),  replace=False,
                               p=value_fitness)
        ind = np.concatenate((elit, ind))
        set_ind = set([i for i in range(self.population_size)])
        replace_ind = []
        for i in ind:
            if i < self.population_size:
                set_ind.discard(i)
            else:
                replace_ind.append(i)

        for i in replace_ind:
            index = set_ind.pop()
            population[index] = new_population[i % self.population_size].copy()

    def tournament_with_parent(self, population, new_population):

        if self.parent_index is None:
            raise 'Неопределен параметр self.parent_index в турнирном отборе с родителем'

        candidate_fitness = [self.fitness_function(candidate) for candidate in new_population]
        population_fitness = [self.fitness_function(candidate) for candidate in population]
        for i in range(self.population_size):
            if population_fitness[i] > candidate_fitness[i]:
                population[i] = new_population[i].copy()

    def random_tournament_selection(self, population, new_population):

        candidate_fitness = [self.fitness_function(candidate) for candidate in new_population]
        population_fitness = [self.fitness_function(candidate) for candidate in population]

        acceptable_candidates = [i for i in range(self.population_size)]

        for i in range(self.population_size):
            random_individual = acceptable_candidates.pop(random.randrange(len(acceptable_candidates)))
            if population_fitness[i] > candidate_fitness[random_individual]:
                population[i] = new_population[random_individual].copy()

