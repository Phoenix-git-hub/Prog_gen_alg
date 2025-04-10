import numpy as np
from prog_files.AdditionalSolutions import Solution
from prog_files.MethodsOfCrossing import MethodsOfCrossing
from prog_files.MethodsOfMutation import MethodsOfMutation
from prog_files.MethodOfSelection import MethodsOfSelection
from prog_files import VisualizationProgression
import time
import random

import tkinter.messagebox
from AdditionalSolutions import SolutionByDynamicProgWithAllVertices
from AdditionalSolutions import SolutionByAntAlgorithm
from AdditionalSolutions import SolutionAnnealingMethod
from AdditionalSolutions import SolutionByDynamicProgramming


class GeneticAlgorithm(Solution):

    def __init__(self,  population_size, number_of_generations, number_of_vertices,
                 method_of_generation_start_population, adjacency_matrix=None,
                 coordinates_of_vertices=None, place_on_screen=None):

        self.crossing_method = None
        self.mutation_method = None
        self.selection_method = None
        self.state_surfing = None
        self.state_family_resemblance_analysis = None
        self.status_of_the_symmetry_adjacency_matrix = None
        self.state_generation_similarity_analysis = None

        self.number_of_generations = number_of_generations
        self.population_size = population_size
        self.method_of_generation_start_population = method_of_generation_start_population
        #переименовать переменные
        self.meanFitnessValues = []
        self.minFitnessValues = []

        self.acceptable_surfing_names = {'none_surf', 'surf_all_pop', 'random_surf', 'random_surf_on_random_val',
                                         'even_surf'}

        self.population = None
        self.graph = VisualizationProgression.ProgressionGraph(1)
        self.dev_graph = VisualizationProgression.DeviationGrash(1)

        name_of_method = "solution by genetic algorithm"
        super(GeneticAlgorithm, self).__init__(adjacency_matrix, coordinates_of_vertices, number_of_vertices,
                                               name_of_method, place_on_screen)

    def initialization_state_surfing(self, state):
        if state not in self.acceptable_surfing_names:
            string = """недопустимое значение парамерта state_surfing'"""
            tkinter.messagebox.showerror("Ошибка", string)

        self.state_surfing = state

    def initialization_state_family_resemblance_analysis(self, state):
        self.state_family_resemblance_analysis = state

    def initialization_status_of_the_symmetry_adjacency_matrix(self, state):
        self.status_of_the_symmetry_adjacency_matrix = state

    def initialization_state_generation_similarity_analysis(self, state):
        self.state_generation_similarity_analysis = state


    def initialization_crossing_method(self, crossing_method):
        self.crossing_method = MethodsOfCrossing()
        self.crossing_method.initialize_number_of_vertices(self.number_of_vertices)
        self.crossing_method.initialize_population_size(self.population_size)
        self.crossing_method.initialize_method_of_crossing(crossing_method)

        if self.adjacency_matrix is not None:
            self.crossing_method.initialize_adjacency_matrix(self.adjacency_matrix)

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
        # тут должны быть все проверки
        if self.status_of_the_symmetry_adjacency_matrix is None:
            raise 'параметр self.status_of_the_symmetry_adjacency_matrix класса SolutionByGeneticAlgorithm не был инициализирован'

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
        self.time_to_surf_gen =  0

        start_full_time = time.perf_counter()
        start_gen_first_pop = time.perf_counter()
        self.generation_start_population()
        end_gen_first_pop = time.perf_counter()
        self.time_to_generate_first_pop += end_gen_first_pop - start_gen_first_pop

        st = time.perf_counter()
        self.generation_similarity_analytics(0)

        self.meanFitnessValues.append(self.average_fitness_value(self.population))
        self.minFitnessValues.append(self.find_best(self.population)[1])
        ed = time.perf_counter()
        self.time_to_calculat_statistics += ed - st

        correct_sol = True

        self.avg_similarity_to_the_primary_parent = 0
        self.avg_similarity_to_the_second_parent = 0
        self.avg_similarities_to_both_parents = 0

        for i in range(self.number_of_generations - 1):
            # бухнуть декоратор ? ???
            # print('поколение ')
            # print(self.population)
            # print()
            start_time_to_crossing = time.perf_counter()
            new_population = self.crossing_method.do_crossing(self.population)
            end_time_to_crossing = time.perf_counter()
            self.time_to_crossing += end_time_to_crossing - start_time_to_crossing

            parent_index = self.crossing_method.get_parent_index()

            start_time_to_mutation = time.perf_counter()
            self.mutation_method.do_mutation(new_population)
            end_time_to_mutation = time.perf_counter()

            self.time_to_mutation += end_time_to_mutation - start_time_to_mutation

            if self.state_family_resemblance_analysis:
                start_time_to_calculat_statistics = time.perf_counter()

                if self.population_size != len(parent_index):
                    raise 'self.population_size != len(parent_index) такого не должно быть'

                for ind in range(1, self.population_size, 2):
                    set1 = set()
                    set2 = set()
                    for j in range(self.number_of_vertices):
                        set1.add((self.population[parent_index[ind]][j-1], self.population[parent_index[ind]][j]))
                        set2.add((self.population[parent_index[ind - 1]][j-1], self.population[parent_index[ind-1]][j]))

                    similarity_to_the_primary_parent = 0
                    similarity_to_the_second_parent = 0
                    similarities_to_both_parents = 0

                    for j in range(self.number_of_vertices):
                        if (new_population[parent_index[ind]][j-1], new_population[parent_index[ind]][j]) in set1 and (new_population[parent_index[ind]][j-1], new_population[parent_index[ind]][j]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j - 1]) in set1 and (new_population[parent_index[ind]][j - 1], new_population[parent_index[ind]][j]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind]][j - 1], new_population[parent_index[ind]][j]) in set1 and (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j - 1]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j - 1]) in set1 and (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j - 1]) in set2:
                            similarities_to_both_parents += 1
                        elif (new_population[parent_index[ind]][j-1], new_population[parent_index[ind]][j]) in set1:
                            similarity_to_the_primary_parent += 1
                        elif (new_population[parent_index[ind]][j-1], new_population[parent_index[ind]][j]) in set2:
                            similarity_to_the_second_parent += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix':
                            if (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j-1]) in set1:
                                similarity_to_the_primary_parent += 1
                            elif (new_population[parent_index[ind]][j], new_population[parent_index[ind]][j-1]) in set2:
                                similarity_to_the_second_parent += 1

                        if (new_population[parent_index[ind-1]][j-1], new_population[parent_index[ind-1]][j]) in set1 and (new_population[parent_index[ind-1]][j-1], new_population[parent_index[ind-1]][j]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind - 1]][j], new_population[parent_index[ind - 1]][j - 1]) in set1 and (new_population[parent_index[ind - 1]][j - 1], new_population[parent_index[ind - 1]][j]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind - 1]][j - 1], new_population[parent_index[ind - 1]][j]) in set1 and (new_population[parent_index[ind - 1]][j], new_population[parent_index[ind - 1]][j - 1]) in set2:
                            similarities_to_both_parents += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix' and (new_population[parent_index[ind - 1]][j], new_population[parent_index[ind - 1]][j - 1]) in set1 and (new_population[parent_index[ind - 1]][j], new_population[parent_index[ind - 1]][j - 1]) in set2:
                            similarities_to_both_parents += 1
                        elif (new_population[parent_index[ind-1]][j-1], new_population[parent_index[ind-1]][j]) in set1:
                            similarity_to_the_second_parent += 1
                        elif (new_population[parent_index[ind-1]][j-1], new_population[parent_index[ind-1]][j]) in set2:
                            similarity_to_the_primary_parent += 1
                        elif self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix':
                            if (new_population[parent_index[ind-1]][j], new_population[parent_index[ind-1]][j-1]) in set1:
                                similarity_to_the_second_parent += 1
                            elif (new_population[parent_index[ind-1]][j], new_population[parent_index[ind-1]][j-1]) in set2:
                                similarity_to_the_primary_parent += 1

                    similarity_to_the_primary_parent /= self.number_of_vertices
                    similarity_to_the_second_parent /= self.number_of_vertices
                    similarities_to_both_parents /= self.number_of_vertices

                    # print(similarity_to_the_primary_parent, similarity_to_the_second_parent)

                    self.avg_similarity_to_the_primary_parent += similarity_to_the_primary_parent
                    self.avg_similarity_to_the_second_parent += similarity_to_the_second_parent
                    self.avg_similarities_to_both_parents += similarities_to_both_parents

                if self.population_size % 2 == 1:
                    ind = self.population_size - 1
                    set1 = set()
                    for j in range(self.number_of_vertices):
                        set1.add((self.population[parent_index[ind]][j-1], self.population[parent_index[ind]][j]))
                    similarity_to_the_primary_parent = 0
                    for j in range(self.number_of_vertices):
                        if (new_population[parent_index[ind]][j-1], new_population[parent_index[ind]][j]) in set1:
                            similarity_to_the_primary_parent += 1
                    similarity_to_the_primary_parent /= self.number_of_vertices
                    self.avg_similarity_to_the_primary_parent += similarity_to_the_primary_parent

                end_time_to_calculat_statistics = time.perf_counter()
                self.time_to_calculat_statistics += end_time_to_calculat_statistics - start_time_to_calculat_statistics
            # #
            # print(self.population)
            # print()
            # print(new_population)
            # print()

            # мы вичисляем фитнес значение два раза, когда происходит отбор и когда считаем среднее значение
            start_time_to_selection = time.perf_counter()
            self.selection_method.do_selection(self.population, new_population, parent_index)
            end_time_to_selection = time.perf_counter()
            self.time_to_selection += end_time_to_selection - start_time_to_selection

            st = time.perf_counter()
            self.generation_similarity_analytics(i + 1)
            ed = time.perf_counter()
            self.time_to_calculat_statistics += ed - st


            self.population_surf()

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

        self.avg_similarity_to_the_primary_parent /= self.population_size
        self.avg_similarity_to_the_second_parent /= self.population_size
        self.avg_similarities_to_both_parents /= self.population_size

        #

        if self.number_of_generations != 0:
            self.avg_similarity_to_the_primary_parent /= self.number_of_generations
            self.avg_similarity_to_the_second_parent /= self.number_of_generations
            self.avg_similarities_to_both_parents /= self.number_of_generations

        # if self.state_family_resemblance_analysis:
        #     print(self.avg_similarity_to_the_primary_parent, self.avg_similarity_to_the_second_parent,
        #           self.avg_similarities_to_both_parents)

        end_full_time = time.perf_counter()
        self.full_time += end_full_time - start_full_time
        if not correct_sol:
            print(self.population)
            string = """в решение присутствует ошибка
                        класс 'SolutionByGeneticAlgoritm'"""
            tkinter.messagebox.showerror("Ошибка", string)
        return self.find_best(self.population)

    def population_surf(self):
        start_surf_gen = time.perf_counter()
        if self.state_surfing == None:
            string = """неопределен параметр self.state_surfing'"""
            tkinter.messagebox.showerror("Ошибка", string)
        elif self.state_surfing == 'surf_all_pop':
            for ind in range(self.population_size):
                # print(self.population[ind], end='')
                self.population[ind] = np.roll(self.population[ind], 1).copy()
                # print(self.population[ind])
        elif self.state_surfing == 'random_surf':
            for ind in range(self.population_size):
                if random.random() > 0.5:
                    # print(self.population[ind], end='')
                    self.population[ind] = np.roll(self.population[ind], 1).copy()
                    # print(self.population[ind])
                else:
                    # print(self.population[ind], end='')
                    self.population[ind] = np.roll(self.population[ind], -1).copy()
                    # print(self.population[ind])

        elif self.state_surfing == 'random_surf_on_random_val':
            for ind in range(self.population_size):

                surf_ind = int(random.random() * 10 + 1)
                # print(surf_ind)
                # print(self.population[ind], end='')
                self.population[ind] = np.roll(self.population[ind], surf_ind).copy()
                # print(self.population[ind])
        elif self.state_surfing == 'even_surf':

            for ind in range(self.population_size):
                # print(self.population[ind], end='')
                if ind % 2 == 0:
                    self.population[ind] = np.roll(self.population[ind], 1).copy()
                else:
                    self.population[ind] = np.roll(self.population[ind], -1).copy()
                # print(self.population[ind])

        end_surf_gen = time.perf_counter()
        self.time_to_surf_gen += end_surf_gen - start_surf_gen
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

        self.graph.set_min_mean_array([self.minFitnessValues], [self.meanFitnessValues])

        self.graph.display()

    def display_deviation(self):

        deviation = [0] * self.number_of_generations
        for i in range(self.number_of_generations):
            deviation[i] = self.meanFitnessValues[i] - self.minFitnessValues[i]

        self.dev_graph.set_deviation([deviation])
        self.dev_graph.display()

    def get_similarity_to_parent(self):
        return self.avg_similarity_to_the_primary_parent, self.avg_similarity_to_the_second_parent, self.avg_similarities_to_both_parents
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

    def get_deviation_numb(self):

        dev_min_from_mean = 0
        for i in range(self.number_of_generations):
            dev_min_from_mean += abs((self.meanFitnessValues[i] - self.minFitnessValues[i]) / self.minFitnessValues[i])
        if self.number_of_generations != 0:
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

    def get_deviation_arr(self):
        deviation = [0] * self.number_of_generations
        for i in range(self.number_of_generations):
            deviation[i] = self.meanFitnessValues[i] - self.minFitnessValues[i]
        return deviation

    def output_all_time_to_console(self):
        # переделать
        average_time_to_crossing = self.time_to_crossing / self.number_of_generations
        average_time_to_mutation = self.time_to_mutation / self.number_of_generations
        average_time_to_selection = self.time_to_selection / self.number_of_generations
        average_time_to_calculat_statistics = self.time_to_calculat_statistics / self.number_of_generations
        average_time_surf_gen = self.time_to_surf_gen / self.number_of_generations

        print(f'Все время на программу: {self.full_time}')
        print(f'Время на скрещивание: {self.time_to_crossing}, за итерацию: {average_time_to_crossing}')
        print(f'Время на мутации: {self.time_to_mutation}, за итерацию: {average_time_to_mutation}')
        print(f'Время на отбор: {self.time_to_selection}, за итерацию: {average_time_to_selection}')
        print(f'Время на сбор статистики: {self.time_to_calculat_statistics}, за итерацию: {average_time_to_calculat_statistics}')
        print(f'Время на генерацию первого поколения: {self.time_to_generate_first_pop}')
        print(f'Время на серф ген: {self.time_to_surf_gen}, за итерацию: {average_time_surf_gen}')
        print()
        if self.state_family_resemblance_analysis:
            print(self.avg_similarity_to_the_primary_parent, self.avg_similarity_to_the_second_parent,
                  self.avg_similarities_to_both_parents)
        print('\n')

    def set_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.selection_method.initialize_adjacency_matrix(self.adjacency_matrix)
        self.crossing_method.initialize_adjacency_matrix(self.adjacency_matrix)

    def set_population(self, population):
        self.population = population

    def generation_start_population(self):
        del self.population
        # нужно создать тест на наличие матрици смежности
        # адинаковый алгоритм, заменить его на один код и словарь
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

        elif self.method_of_generation_start_population == 'the_greedy_algorithm_with_one_vertex' :

            sol_dynamic_programming = SolutionByDynamicProgramming(self.adjacency_matrix, number_of_vertices=self.number_of_vertices)
            individual = sol_dynamic_programming.solution()[0]
            self.population = np.array([individual for _ in range(self.population_size)])

        elif self.method_of_generation_start_population == 'simulated annealing':
            sol_annealing_method = SolutionAnnealingMethod(self.adjacency_matrix, number_of_vertices=self.number_of_vertices)
            individual = sol_annealing_method.solution()[0]
            self.population = np.array([individual for _ in range(self.population_size)])
        else:
            string = """Неизвестное значение self.settings_comparison_alg['generation_of_the_starting_population']
            класса 'SolutionByGeneticAlgoritm'"""
            tkinter.messagebox.showerror("Ошибка", string)

    def generation_similarity_analytics(self, ind_gen):
        # работа с популяцией
        if self.state_generation_similarity_analysis == None:
            raise 'self.state_generation_similarity_analysis не инициализирован'


        verification_generation = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 100]
        if ind_gen in verification_generation:
            if self.state_generation_similarity_analysis.get():
                if self.status_of_the_symmetry_adjacency_matrix:
                   print(self.generation_similarity_analytics_for_symmetry_adjacency_matrix())
                else:
                    self.generation_similarity_analytics_for_not_symmetry_adjacency_matrix()

    def generation_similarity_analytics_for_symmetry_adjacency_matrix(self):
        numb_connections = (self.number_of_vertices * (self.number_of_vertices - 1)) // 2

        city_connections = {}

        for individ in self.population:
            for ind in range(self.number_of_vertices):

                connection = f'{individ[ind-1]}-{individ[ind]}'
                connection_2 = f'{individ[ind]}-{individ[ind - 1]}'
                if connection in city_connections:
                    city_connections[connection] += 1
                elif connection_2 in city_connections:
                    city_connections[connection_2] += 1
                else:
                    city_connections[connection] = 1

        return len(city_connections) / numb_connections

    def generation_similarity_analytics_for_not_symmetry_adjacency_matrix(self):

        numb_connections = self.number_of_vertices * (self.number_of_vertices - 1)

        city_connections = {}

        for individ in self.population:
            for ind in range(self.number_of_vertices):

                connection = f'{individ[ind-1]}-{individ[ind]}'
                if connection in city_connections:
                    city_connections[connection] += 1
                else:
                    city_connections[connection] = 1

        return len(city_connections) / numb_connections

