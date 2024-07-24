import numpy as np
from prog_files.AdditionalSolutions import Solution
from prog_files.MethodsOfCrossing import MethodsOfCrossing
from prog_files.MethodsOfMutation import MethodsOfMutation
from prog_files.MethodOfSelection import MethodsOfSelection
import matplotlib.pyplot as plt
import time

class GeneticAlgorithm(Solution):

    def __init__(self,  population_size, number_of_generations, number_of_vertices,
                 adjacency_matrix=None, coordinates_of_vertices=None, place_on_screen=None):

        self.crossing_method = None
        self.mutation_method = None
        self.selection_method = None

        self.number_of_generations = number_of_generations
        self.population_size = population_size

        #переименовать переменные
        self.meanFitnessValues = []
        self.minFitnessValues = []

        self.population = None

        name_of_method = "solution by genetic algorithm"
        super(GeneticAlgorithm, self).__init__(adjacency_matrix, coordinates_of_vertices, number_of_vertices,
                                               name_of_method, place_on_screen)

    def initialization_crossing_method(self, crossing_method):
        self.crossing_method = MethodsOfCrossing()
        self.crossing_method.initialize_number_of_vertices(self.number_of_vertices)
        self.crossing_method.initialize_population_size(self.population_size)
        self.crossing_method.initialize_method_of_crossing(crossing_method)

    def initialization_mutation_method(self, mutation_method):
        self.mutation_method = MethodsOfMutation()
        self.mutation_method.initialize_number_of_vertices(self.number_of_vertices)
        self.mutation_method.initialize_population_size(self.population_size)
        self.mutation_method.initialize_method_of_mutation(mutation_method)

    def initialization_selection_method(self, selection_method):
        #инициалиизация классов селеуции должна проходить в __init__
        self.selection_method = MethodsOfSelection()
        self.selection_method.initialize_number_of_vertices(self.number_of_vertices)
        self.selection_method.initialize_population_size(self.population_size)
        self.selection_method.initialize_method_of_selection(selection_method)
        self.selection_method.initialize_adjacency_matrix(self.adjacency_matrix)

    def initialization_status_of_searching_parent(self, searching_parent):
        self.crossing_method.initialize_status_of_searching_parent(searching_parent)

    def solution(self):
        permutation, distance = self.solution_gen_alg()
        return np.array(permutation), distance

    def solution_gen_alg(self):

        # поставить проверку на первое поколение
        # print(self.population)
        self.time_to_crossing = 0
        self.time_to_mutation = 0
        self.time_to_selection = 0
        self.time_to_calculat_statistics = 0
        self.full_time = 0

        self.meanFitnessValues.append(self.average_fitness_value(self.population))
        self.minFitnessValues.append(self.find_best(self.population)[1])

        start_full_time = time.perf_counter()
        for i in range(self.number_of_generations):
            # бухнуть декоратор ? ???

            start_time_to_crossing = time.perf_counter()
            new_population = self.crossing_method.do_crossing(self.population)
            end_time_to_crossing = time.perf_counter()
            self.time_to_crossing += end_time_to_crossing - start_time_to_crossing

            start_time_to_mutation = time.perf_counter()
            self.mutation_method.do_mutation(new_population)
            end_time_to_mutation = time.perf_counter()
            self.time_to_mutation += end_time_to_mutation - start_time_to_mutation

            # мы вичисляем фитнес значение два раза, когда происходит отбор и когда считаем среднее значение
            start_time_to_selection = time.perf_counter()
            self.selection_method.do_selection(self.population, new_population)
            end_time_to_selection = time.perf_counter()
            self.time_to_selection += end_time_to_selection - start_time_to_selection

            start_time_to_calculat_statistics = time.perf_counter()
            self.meanFitnessValues.append(self.average_fitness_value(self.population))
            self.minFitnessValues.append(self.find_best(self.population)[1])
            end_time_to_calculat_statistics = time.perf_counter()
            self.time_to_calculat_statistics += end_time_to_calculat_statistics - start_time_to_calculat_statistics
            del new_population

        end_full_time = time.perf_counter()
        self.full_time += end_full_time - start_full_time

        return self.find_best(self.population)

    def find_best(self, population):
        #нужно переписать код
        best_solution = population[0].copy()
        min_sol = self.fitness_function(population[0])
        for i in population:
            if (new := self.fitness_function(i)) < min_sol:
                min_sol = new
                best_solution = i.copy()
        return best_solution, min_sol

    def fitness_function(self, individual):
        # нужно переписать код
        sum_vertexes = 0
        for i in range(self.number_of_vertices - 1):
            sum_vertexes += self.adjacency_matrix[individual[i]][individual[i + 1]]

        sum_vertexes += self.adjacency_matrix[individual[- 1]][individual[0]]
        return sum_vertexes

    def average_fitness_value(self, population):
        sum_value = 0
        for individual in population:
            sum_value += self.fitness_function(individual)
        return sum_value // self.population_size

    def visualization_progression(self):
        plt.figure("Приспособленность").clear()
        plt.figure("Приспособленность")
        plt.plot(self.minFitnessValues, color='red')
        plt.plot(self.meanFitnessValues, color='green')
        plt.xlabel('Поколение')
        plt.ylabel('Макс/средняя приспособленность')
        plt.title('Зависимость максимальной и средней приспособленности от поколения')

    def get_mean_fitness_values(self):
        return self.meanFitnessValues

    def get_min_fitness_values(self):
        return self.minFitnessValues

    def get_time(self):
        # нужно написать какие паарметры и в каком порядке возвращает жтот метод
        return self.time_to_crossing, self.time_to_mutation, self.time_to_selection,\
            self.time_to_calculat_statistics, self.full_time

    def get_time_to_crossing(self):
        return self.time_to_crossing

    def get_time_to_mutation(self):
        return self.time_to_mutation

    def get_time_to_selection(self):
        return self.time_to_selection

    def get_time_to_calculat_statistics(self):
        return self.time_to_calculat_statistics

    def get_full_time(self):
        return self.full_time

    def get_average_time(self):
        average_time_to_crossing = self.time_to_crossing / self.number_of_generations
        average_time_to_mutation = self.time_to_mutation / self.number_of_generations
        average_time_to_selection = self.time_to_selection / self.number_of_generations
        average_time_to_calculat_statistics = self.time_to_calculat_statistics / self.number_of_generations
        average_full_time = self.full_time / self.number_of_generations

        return average_time_to_mutation, average_time_to_selection, \
            average_time_to_calculat_statistics, average_full_time, average_time_to_crossing

    def output_all_time_to_console(self):
        average_time_to_crossing = self.time_to_crossing / self.number_of_generations
        average_time_to_mutation = self.time_to_mutation / self.number_of_generations
        average_time_to_selection = self.time_to_selection / self.number_of_generations
        average_time_to_calculat_statistics = self.time_to_calculat_statistics / self.number_of_generations
        average_full_time = self.full_time / self.number_of_generations

        print('\n')
        print(f'Все время на программу: {self.full_time}, среднее: {average_full_time}')
        print(f'Время на скрещивание: {self.time_to_crossing}, среднее: {average_time_to_crossing}')
        print(f'Время на мутации: {self.time_to_mutation}, среднее: {average_time_to_mutation}')
        print(f'Время на отбор: {self.time_to_selection}, среднее: {average_time_to_selection}')
        print(f'Время на сбор статистики: {self.time_to_calculat_statistics}, среднее: {average_time_to_calculat_statistics}')
        print('\n')

    def set_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.selection_method.initialize_adjacency_matrix(self.adjacency_matrix)

    def set_population(self, population):
        self.population = population