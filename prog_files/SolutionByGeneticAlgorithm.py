import numpy as np
from prog_files.AdditionalSolutions import Solution
from prog_files.MethodsOfCrossing import MethodsOfCrossing
from prog_files.MethodsOfMutation import MethodsOfMutation
from prog_files.MethodOfSelection import MethodsOfSelection
import matplotlib.pyplot as plt
import time

import tkinter.messagebox
from AdditionalSolutions import SolutionByDynamicProgWithAllVertices
from AdditionalSolutions import SolutionByAntAlgorithm

class GeneticAlgorithm(Solution):

    def __init__(self,  population_size, number_of_generations, number_of_vertices,
                 method_of_generation_start_population, adjacency_matrix=None,
                 coordinates_of_vertices=None, place_on_screen=None):

        self.crossing_method = None
        self.mutation_method = None
        self.selection_method = None

        self.number_of_generations = number_of_generations
        self.population_size = population_size
        self.method_of_generation_start_population = method_of_generation_start_population.get()
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
        self.selection_method.initialize_fitness_function(self.fitness_function)

    def initialization_status_of_searching_parent(self, searching_parent):
        self.crossing_method.initialize_status_of_searching_parent(searching_parent)

    def solution(self):
        permutation, distance = self.solution_gen_alg()
        return np.array(permutation), distance

    def solution_gen_alg(self):
        #gjcnfdbnm ghjdthre yf yfkbxbt gthdjuj gjrjktybz
        # поставить проверку на первое поколение
        # print(self.population)
        self.meanFitnessValues = []
        self.minFitnessValues = []

        self.time_to_crossing = 0
        self.time_to_mutation = 0
        self.time_to_selection = 0
        self.time_to_calculat_statistics = 0
        self.full_time = 0
        self.time_to_generate_first_pop = 0

        start_full_time = time.perf_counter()
        start_gen_first_pop = time.perf_counter()
        self.generation_start_population()
        end_gen_first_pop = time.perf_counter()
        self.time_to_generate_first_pop += end_gen_first_pop - start_gen_first_pop

        st = time.perf_counter()
        self.meanFitnessValues.append(self.average_fitness_value(self.population))
        self.minFitnessValues.append(self.find_best(self.population)[1])
        ed = time.perf_counter()
        self.time_to_calculat_statistics += ed - st

        correct_sol = True

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
            correct_sol = self.check_solution(self.population) and correct_sol
            end_time_to_calculat_statistics = time.perf_counter()
            self.time_to_calculat_statistics += end_time_to_calculat_statistics - start_time_to_calculat_statistics

            # with open('.txt', 'a') as f:
            #     f.write('0000000000' + str(i) + '\n')
            #     for item in self.population:
            #         f.write(str(item) + '\n')
            #     f.write('\n')
            # del new_population

        end_full_time = time.perf_counter()
        self.full_time += end_full_time - start_full_time
        if not correct_sol:
            print(self.population)
            string = """в решение присутствует ошибка
                        класс 'SolutionByGeneticAlgoritm'"""
            tkinter.messagebox.showerror("Ошибка", string)
        return self.find_best(self.population)

    def check_solution(self, population):
        all_v = [1]
        for individual in population:
            all_v = set([k for k in range(self.number_of_vertices)])
            for j in individual:
                if j in all_v:
                    all_v.discard(j)
                else:
                    return False
        if len(all_v) > 0:
            return False

        return True

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
            self.time_to_calculat_statistics, self.full_time, self.time_to_generate_first_pop

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
            average_time_to_calculat_statistics, average_full_time, average_time_to_crossing,

    def get_time_to_generate_first_pop(self):
        return self.time_to_generate_first_pop

    def get_deviation(self):

        dev_min_from_mean = 0
        for i in range(self.number_of_generations):
            dev_min_from_mean += abs((self.meanFitnessValues[i] - self.minFitnessValues[i]) / self.minFitnessValues[i])
        dev_min_from_mean /= self.number_of_generations
        dev_min_from_mean *= 100

        return dev_min_from_mean

    def output_deviation_to_console(self):
        # у меня операция по расчету выполняется в двух разных местах, это по хорошему убрать
        dev_min_from_mean = 0
        for i in range(self.number_of_generations):
            dev_min_from_mean += abs((self.meanFitnessValues[i] - self.minFitnessValues[i]) / self.minFitnessValues[i])
        dev_min_from_mean /= self.number_of_generations
        dev_min_from_mean *= 100

        print(f'Среднеквадратичная разница лучшего со средним решением в процентах ГА - {dev_min_from_mean}')

    def output_all_time_to_console(self):
        # переделать
        average_time_to_crossing = self.time_to_crossing / self.number_of_generations
        average_time_to_mutation = self.time_to_mutation / self.number_of_generations
        average_time_to_selection = self.time_to_selection / self.number_of_generations
        average_time_to_calculat_statistics = self.time_to_calculat_statistics / self.number_of_generations

        print(f'Все время на программу: {self.full_time}')
        print(f'Время на скрещивание: {self.time_to_crossing}, за итерацию: {average_time_to_crossing}')
        print(f'Время на мутации: {self.time_to_mutation}, за итерацию: {average_time_to_mutation}')
        print(f'Время на отбор: {self.time_to_selection}, за итерацию: {average_time_to_selection}')
        print(f'Время на сбор статистики: {self.time_to_calculat_statistics}, за итерацию: {average_time_to_calculat_statistics}')
        print(f'Время на генерацию первого поколения: {self.time_to_generate_first_pop}')
        print('\n')

    def set_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.selection_method.initialize_adjacency_matrix(self.adjacency_matrix)

    def set_population(self, population):
        self.population = population

    def generation_start_population(self):
        print(self.method_of_generation_start_population)
        del self.population
        # нужно создать тест на наличие матрици смежности
        if self.method_of_generation_start_population == 'random_gen':
            self.population = np.array([np.random.choice(self.number_of_vertices, self.number_of_vertices, replace=False)
                                   for _ in range(self.population_size)])
        elif self.method_of_generation_start_population == 'ordered_gen':
            self.population = np.zeros(shape=(self.population_size, self.number_of_vertices), dtype=int)
            for i in range(self.population_size):
                for j in range(self.number_of_vertices):
                    self.population[i][j] = j
        elif self.method_of_generation_start_population == 'greedy_algorithm_gen':
            sol_din_pr = SolutionByDynamicProgWithAllVertices(self.adjacency_matrix,
                                                              number_of_vertices=self.number_of_vertices)
            individual = sol_din_pr.solution()[0]
            self.population = np.array([individual for _ in range(self.population_size)])

        elif self.method_of_generation_start_population == 'ant_algorithm_gen':
            sol_ant_algorithm = SolutionByAntAlgorithm(self.adjacency_matrix, number_of_vertices=self.number_of_vertices)
            individual = sol_ant_algorithm.solution()[0]
            self.population = np.array([individual for _ in range(self.population_size)])

        else:
            string = """Неизвестное значение self.settings_comparison_alg['generation_of_the_starting_population']
            класса 'SolutionByGeneticAlgoritm'"""
            tkinter.messagebox.showerror("Ошибка", string)