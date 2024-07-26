import random


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

    def initialize_method_of_selection(self, name_of_method):

        if name_of_method not in self.possible_names_of_selection:
            error_str = f'nonexistent name of crossing'
            raise Exception(error_str)

        self.selection_method = self.name_of_selection[name_of_method]

    def initialize_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def initialize_population_size(self, population_size):
        self.population_size = population_size

    def initialize_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix

    def do_selection(self, population, new_population):
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

        # сделать с помощью choise numpy
        value_fitness = dict()

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

        ratio_1 = 20 / (max_val - min_val)
        ratio_2 = -1*(ratio_1 * min_val)

        for key, item in value_fitness.items():
            value_fitness[key] = item*ratio_1 + ratio_2

        for i in range(self.population_size):
            ind = random.choices(list(value_fitness.keys()), weights=list(value_fitness.values()),  k=1)[0]
            del value_fitness[ind]

        pop = list(value_fitness.keys())

        for i in range(1, self.population_size):
            for j in range(self.population_size - i):
                if pop[j] > pop[j + 1]:
                    a = pop[j]
                    pop[j] = pop[j +1]
                    pop[j+1] = a

        for i in range(self.population_size):
            if pop[i] < self.population_size:
                population[i] = population[pop[i]].copy()
            else:
                population[i] = new_population[pop[i]-self.population_size].copy()



        # candidate_fitness_1 = [self.fitness_function(candidate) for candidate in new_population]
        # population_fitness_1 = [self.fitness_function(candidate) for candidate in population]
        #
        # sum_can = sum(candidate_fitness_1)
        # sum_pop = sum(population_fitness_1)
        #
        # candidate_fitness = [(sum_can / fit) * 100 - 400 for fit in candidate_fitness_1]
        # population_fitness = [(sum_pop / fit) * 100 - 400 for fit in population_fitness_1]
        #
        # sum_can = sum(candidate_fitness)
        # sum_pop = sum(population_fitness)
        #
        # candidate_fitness = [fit / sum_can for fit in candidate_fitness]
        # population_fitness = [fit / sum_pop for fit in population_fitness]
        #
        # free = [1] * self.number_of_vertices
        #
        # for i in range(1, self.number_of_vertices, 2):
        #     free[i] = population[np.random.choice(self.number_of_vertices, p=population_fitness)].copy()
        #     free[i - 1] = new_population[np.random.choice(self.number_of_vertices, p=candidate_fitness)].copy()
        #
        # if self.number_of_vertices % 2 == 1:
        #     free[-1] = population[np.random.choice(self.number_of_vertices, p=population_fitness)].copy()
        #
        # j = 0
        # for i in free:
        #     population[j] = i.copy()
        #     j += 1
        #
        # size = len(new_population)
        # for candidate in range(size):
        #     for ind_population in range(size):
        #         if candidate_fitness[candidate] < population_fitness[ind_population]:
        #             population[ind_population] = new_population[candidate].copy()
        #             break

    def tournament_with_parent(self, population, new_population):
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

    def fitness_function(self, individual):
        # нужно переписать код
        sum_vertexes = 0
        for i in range(self.number_of_vertices - 1):
            sum_vertexes += self.adjacency_matrix[individual[i]][individual[i + 1]]

        sum_vertexes += self.adjacency_matrix[individual[0]][individual[self.number_of_vertices - 1]]
        return sum_vertexes
