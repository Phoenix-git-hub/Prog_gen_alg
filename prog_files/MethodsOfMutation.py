import random
import math

class MethodsOfMutation:

    def __init__(self):
        # пожалуй нужно сделать файл config куда я положу общие данные для всего кода
        self.possible_names_of_mutation = ('mutation_pass', 'mutation_turning_180_g', 'mutation_by_exchange',
                                           'mutation_by_shuffling', 'mutations_with_probability',
                                           'module_based_mutation', 'm2_based_mutation')
        self.name_of_mutation = dict.fromkeys(self.possible_names_of_mutation)

        self.name_of_mutation['mutation_pass'] = self.mutation_pass
        self.name_of_mutation['mutation_turning_180_g'] = self.mutation_turning_180_g
        self.name_of_mutation['mutation_by_exchange'] = self.mutation_by_exchange
        self.name_of_mutation['mutation_by_shuffling'] = self.mutation_by_shuffling
        self.name_of_mutation['mutations_with_probability'] = self.mutations_with_probability
        self.name_of_mutation['module_based_mutation'] = self.module_based_mutation
        self.name_of_mutation['m2_based_mutation'] = self.m2_based_mutation
        self.number_of_vertices = None
        self.mutation_method = None
        self.population_size = None

    def initialize_method_of_mutation(self, name_of_method):

        if name_of_method not in self.possible_names_of_mutation:
            error_str = f'nonexistent name of mutation'
            raise Exception(error_str)

        self.mutation_method = self.name_of_mutation[name_of_method]

    def initialize_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def initialize_population_size(self, population_size):
        self.population_size = population_size

    def do_mutation(self, population):
        return self.mutation_method(population)

    @staticmethod
    def mutation_pass(population):
        pass

    def mutation_turning_180_g(self, population):
        # все очевидно, я посмотрел должно рпавильно работать
        # ++++++++
        for individual in population:
            first_limit = random.randrange(0, self.number_of_vertices)
            second_limit = random.randrange(0, self.number_of_vertices)
            if second_limit < first_limit:
                a = first_limit
                first_limit = second_limit
                second_limit = a
            individual[first_limit:second_limit + 1] = individual[first_limit:second_limit + 1][::-1].copy()

    def mutation_by_exchange(self, population):
        for i in range(self.population_size):
            first_el = random.randrange(0, self.number_of_vertices)
            second_el = random.randrange(0, self.number_of_vertices)
            population[i][first_el], population[i][second_el] = population[i][second_el], population[i][first_el]

    def mutation_by_shuffling(self, population):

        for individual in population:
            first_limit = random.randrange(0, self.number_of_vertices)
            second_limit = random.randrange(0, self.number_of_vertices)
            if second_limit < first_limit:
                a = first_limit
                first_limit = second_limit
                second_limit = a

            rand_num = random.randint(0, 1)

            if rand_num == 0:

                val_last_el = individual[first_limit]
                individual[first_limit] = individual[second_limit]

                for index in range(first_limit, second_limit):
                    val_this_el = individual[index + 1]
                    individual[index + 1] = val_last_el

                    val_last_el = val_this_el
            else:
                val_last_el = individual[second_limit]
                individual[second_limit] = individual[first_limit]

                for index in range(second_limit, first_limit, -1):
                    val_this_el = individual[index - 1]
                    individual[index - 1] = val_last_el

                    val_last_el = val_this_el

    def mutations_with_probability(self, population):
        probability1 = [math.sin(i * (1/(self.number_of_vertices - 1)) * math.pi)
                        for i in range(self.number_of_vertices)]
        probability2 = [abs(math.cos(i * (1/(self.number_of_vertices - 1)) * math.pi))
                        for i in range(self.number_of_vertices)]

        index = [i for i in range(self.number_of_vertices)]

        for individual in population:

            first_el = random.choices(index, weights=probability1)
            second_el = random.choices(index, weights=probability2)

            individual[first_el], individual[second_el] =\
                individual[second_el], individual[first_el]

    def module_based_mutation(self, population):
        probability1 = [abs(i /(self.number_of_vertices - 1) - 0.5)
                        for i in range(self.number_of_vertices)]
        probability2 = [-abs(i /(self.number_of_vertices - 1) - 0.5) + 1
                        for i in range(self.number_of_vertices)]

        index = [i for i in range(self.number_of_vertices)]

        for individual in population:

            first_el = random.choices(index, weights=probability1)
            second_el = random.choices(index, weights=probability2)

            individual[first_el], individual[second_el] =\
                individual[second_el], individual[first_el]

    def m2_based_mutation(self, population):
        probability1 = [2 * abs(i / (self.number_of_vertices - 1) - 0.5)
                        for i in range(self.number_of_vertices)]
        probability2 = [-2 * abs(i / (self.number_of_vertices - 1) - 0.5) + 1
                        for i in range(self.number_of_vertices)]

        index = [i for i in range(self.number_of_vertices)]

        for individual in population:

            first_el = random.choices(index, weights=probability1)
            second_el = random.choices(index, weights=probability2)

            individual[first_el], individual[second_el] =\
                individual[second_el], individual[first_el]


