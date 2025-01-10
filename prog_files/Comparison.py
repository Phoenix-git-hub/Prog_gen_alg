from SolutionByGeneticAlgorithm import GeneticAlgorithm
from prog_files.WorkWithVertices import WorkWithVertices
import matplotlib.pyplot as plt
from prog_files import VisualizationProgression


class AlgorithmInformation:
    def __init__(self, number_of_generations):
        pass
class Comparison:
    def __init__(self, general_settings, settings_mandatory_alg, settings_additional_alg, settings_comparison_alg):
        self.general_settings = general_settings
        self.settings_mandatory_alg = settings_mandatory_alg
        self.settings_additional_alg = settings_additional_alg

        self.settings_comparison_alg = settings_comparison_alg

        method_of_generation_start_population_first_alg = self.settings_mandatory_alg[
            'method_of_generation_start_population']
        method_of_generation_start_population_second_alg = self.settings_additional_alg[
            'method_of_generation_start_population']

        self.number_of_comparisons = self.settings_comparison_alg['number_of_comparisons']

        measure_of_disorder = self.general_settings['measure_of_disorder']
        status_of_gen_adj_mat = self.general_settings['status_of_generation_adjacency_matrix']
        status_of_the_symmetry_adjacency_matrix = self.general_settings['status_of_the_symmetry_adjacency_matrix']

        self.population_size = general_settings['population_size']
        self.number_of_vertices = general_settings['number_of_vertices']
        self.number_of_generations = general_settings['number_of_generations']

        self.work_with_vertices = WorkWithVertices(self.number_of_vertices, status_of_gen_adj_mat,
                                                   measure_of_disorder, status_of_the_symmetry_adjacency_matrix)

        self.graph = VisualizationProgression.ProgressionGraph(2)
        self.dev_graph = VisualizationProgression.DeviationGrash(2)

        self.average_mean_val_1 = [0] * self.number_of_generations
        self.average_min_val_1 = [0] * self.number_of_generations
        self.average_mean_val_2 = [0] * self.number_of_generations
        self.average_min_val_2 = [0] * self.number_of_generations
        self.average_deviation_1 = [0] * self.number_of_generations
        self.average_deviation_2 = [0] * self.number_of_generations

        self.average_time_to_crossing_1 = 0
        self.average_time_to_mutation_1 = 0
        self.average_time_to_selection_1 = 0
        self.average_time_to_calculat_statistics_1 = 0
        self.average_full_time_1 = 0
        self.time_to_generate_first_pop_1 = 0
        self.similarity_to_parent_1 = [0, 0, 0]

        self.average_time_to_crossing_2 = 0
        self.average_time_to_mutation_2 = 0
        self.average_time_to_selection_2 = 0
        self.average_time_to_calculat_statistics_2 = 0
        self.average_full_time_2 = 0
        self.time_to_generate_first_pop_2 = 0
        self.similarity_to_parent_2 = [0, 0, 0]

        self.sum_division_1 = 0
        self.sum_division_2 = 0

        #все выделить в отдельные классы
        self.first_gen_alg = GeneticAlgorithm(self.population_size, self.number_of_generations,
                                              self.number_of_vertices, method_of_generation_start_population_first_alg)
        self.first_gen_alg.initialization_state_family_resemblance_analysis(
            self.settings_mandatory_alg['state_family_resemblance_analysis'])
        self.first_gen_alg.initialization_state_surfing(self.settings_mandatory_alg['state_surfing'])
        self.first_gen_alg.initialization_selection_method(self.settings_mandatory_alg['selection_method'])
        self.first_gen_alg.initialization_crossing_method(self.settings_mandatory_alg['crossing_method'])
        self.first_gen_alg.initialization_mutation_method(self.settings_mandatory_alg['mutation_method'])
        self.first_gen_alg.initialization_status_of_searching_parent(
            self.settings_mandatory_alg['status_of_searching_parent'])
        self.first_gen_alg.initialization_status_of_the_symmetry_adjacency_matrix(status_of_the_symmetry_adjacency_matrix)
        self.first_gen_alg.initialization_state_generation_similarity_analysis(self.settings_mandatory_alg['state_generation_similarity_analysis'])


        self.second_gen_alg = GeneticAlgorithm(self.population_size, self.number_of_generations,
                                               self.number_of_vertices, method_of_generation_start_population_second_alg)

        self.second_gen_alg.initialization_state_family_resemblance_analysis(
            self.settings_additional_alg['state_family_resemblance_analysis'])
        self.second_gen_alg.initialization_state_surfing(self.settings_additional_alg['state_surfing'])
        self.second_gen_alg.initialization_selection_method(self.settings_additional_alg['selection_method'])
        self.second_gen_alg.initialization_crossing_method(self.settings_additional_alg['crossing_method'])
        self.second_gen_alg.initialization_mutation_method(self.settings_additional_alg['mutation_method'])
        self.second_gen_alg.initialization_status_of_searching_parent(
            self.settings_additional_alg['status_of_searching_parent'])
        self.second_gen_alg.initialization_status_of_the_symmetry_adjacency_matrix(status_of_the_symmetry_adjacency_matrix)
        self.second_gen_alg.initialization_state_generation_similarity_analysis(self.settings_additional_alg['state_generation_similarity_analysis'])
    def start_comparison(self):

        for i in range(self.number_of_comparisons):
            print(i)

            adjacency_matrix = self.work_with_vertices.initialization_adjacency_matrix()

            self.first_gen_alg.set_adjacency_matrix(adjacency_matrix)
            self.second_gen_alg.set_adjacency_matrix(adjacency_matrix)

            self.first_gen_alg.start_solution()
            self.second_gen_alg.start_solution()

            # обернуть в какю-нибуть функцию срочно
            # поставить таймер на сбор данных

            self.average_time_to_crossing_1 += self.first_gen_alg.get_time_to_crossing()
            self.average_time_to_mutation_1 += self.first_gen_alg.get_time_to_mutation()
            self.average_time_to_selection_1 += self.first_gen_alg.get_time_to_selection()
            self.average_time_to_calculat_statistics_1 += self.first_gen_alg.get_time_to_calculat_statistics()
            self.average_full_time_1 += self.first_gen_alg.get_full_time()
            self.time_to_generate_first_pop_1 += self.first_gen_alg.get_time_to_generate_first_pop()
            self.sum_division_1 += self.first_gen_alg.get_deviation_numb()

            self.similarity_to_parent_1 = list(map(sum, zip(self.similarity_to_parent_1,
                                                       self.first_gen_alg.get_similarity_to_parent())))

            self.average_time_to_crossing_2 += self.second_gen_alg.get_time_to_crossing()
            self.average_time_to_mutation_2 += self.second_gen_alg.get_time_to_mutation()
            self.average_time_to_selection_2 += self.second_gen_alg.get_time_to_selection()
            self.average_time_to_calculat_statistics_2 += self.second_gen_alg.get_time_to_calculat_statistics()
            self.average_full_time_2 += self.second_gen_alg.get_full_time()
            self.time_to_generate_first_pop_2 += self.second_gen_alg.get_time_to_generate_first_pop()
            self.sum_division_2 += self.second_gen_alg.get_deviation_numb()

            self.similarity_to_parent_2 = list(map(sum, zip(self.similarity_to_parent_2,
                                                       self.second_gen_alg.get_similarity_to_parent())))

            mean_fitness_values_1 = self.first_gen_alg.get_mean_fitness_values()
            min_fitness_values_1 = self.first_gen_alg.get_min_fitness_values()
            deviation_values_1 = self.first_gen_alg.get_deviation_arr()

            mean_fitness_values_2 = self.second_gen_alg.get_mean_fitness_values()
            min_fitness_values_2 = self.second_gen_alg.get_min_fitness_values()
            deviation_values_2 = self.second_gen_alg.get_deviation_arr()

            for ind in range(self.number_of_generations):
                self.average_mean_val_1[ind] += mean_fitness_values_1[ind]
                self.average_min_val_1[ind] += min_fitness_values_1[ind]
                self.average_mean_val_2[ind] += mean_fitness_values_2[ind]
                self.average_min_val_2[ind] += min_fitness_values_2[ind]

                self.average_deviation_1[ind] += deviation_values_1[ind]
                self.average_deviation_2[ind] += deviation_values_2[ind]
                # блять тут и комментировать не надо
        for ind in range(self.number_of_generations):
            self.average_mean_val_1[ind] /= self.number_of_comparisons
            self.average_min_val_1[ind] /= self.number_of_comparisons
            self.average_mean_val_2[ind] /= self.number_of_comparisons
            self.average_min_val_2[ind] /= self.number_of_comparisons

            self.average_deviation_1[ind] /= self.number_of_comparisons
            self.average_deviation_2[ind] /= self.number_of_comparisons

        # блять все в новые функции
        self.average_time_to_crossing_1 /= self.number_of_comparisons
        self.average_time_to_mutation_1 /= self.number_of_comparisons
        self.average_time_to_selection_1 /= self.number_of_comparisons
        self.average_time_to_calculat_statistics_1 /= self.number_of_comparisons
        self.average_full_time_1 /= self.number_of_comparisons
        self.time_to_generate_first_pop_1 /= self.number_of_comparisons
        self.similarity_to_parent_1 = list(map(lambda a: a / self.number_of_comparisons,
                                               self.similarity_to_parent_1))

        self.average_time_to_crossing_2 /= self.number_of_comparisons
        self.average_time_to_mutation_2 /= self.number_of_comparisons
        self.average_time_to_selection_2 /= self.number_of_comparisons
        self.average_time_to_calculat_statistics_2 /= self.number_of_comparisons
        self.average_full_time_2 /= self.number_of_comparisons
        self.time_to_generate_first_pop_2 /= self.number_of_comparisons
        self.similarity_to_parent_2 = list(map(lambda a: a / self.number_of_comparisons,
                                               self.similarity_to_parent_2))

        print("Вычисления закончены")

    def visualization_progression(self):

        self.graph.set_min_mean_array([self.average_min_val_1, self.average_min_val_2], [self.average_mean_val_1, self.average_mean_val_2])
        self.graph.display()

    def visualization_deviation(self):

        self.dev_graph.set_deviation([self.average_deviation_1, self.average_deviation_2])
        self.dev_graph.display()

    def output_deviation_to_console(self):
        # MAPE
        dev_first_from_second = 0

        for i in range(self.number_of_generations):
            dev_first_from_second += abs((self.average_mean_val_2[i] - self.average_mean_val_1[i]) / ((self.average_mean_val_2[i] + self.average_mean_val_1[i]) / 2))
        dev_first_from_second /= self.number_of_generations
        dev_first_from_second *= 100

        print(f'Средняя абсолютная процентная ошибка лучшего решения со средним 1 алгоритма - {self.sum_division_1 /self.number_of_comparisons}')
        print(f'Средняя абсолютная процентная ошибка лучшего решения со средним 2 алгоритма - {self.sum_division_2 /self.number_of_comparisons}')
        print(f'Средняя абсолютная процентная ошибка двух алгоритмов - {dev_first_from_second}')


    def output_time_to_console(self):
        print(f'Среднее время первого - {self.average_full_time_1}, второго - {self.average_full_time_2}')
        print(f'Среднее время на скрещивание - {self.average_time_to_crossing_1}, второго - {self.average_time_to_crossing_2 }')
        print(f'Среднее время мутации - {self.average_time_to_mutation_1}, второго - {self.average_time_to_mutation_2}')
        print(f'Среднее время селекции - {self.average_time_to_selection_1}, второго - {self.average_time_to_selection_2 }')
        print(f'Среднее время калькулирование - {self.average_time_to_calculat_statistics_1}, второго - {self.average_time_to_calculat_statistics_2 }')
        print(f'Среднее время на создание первого поколения - {self.time_to_generate_first_pop_1}, второго - {self.time_to_generate_first_pop_2}')
        if self.settings_mandatory_alg['state_family_resemblance_analysis']:
            print()
            print('Схожесть родителей на потомков, для первого и второго')
            print(f'На основного родителя: {self.similarity_to_parent_1[0]}, {self.similarity_to_parent_2[0]}')
            print(f'На второстепенного родителя:{self.similarity_to_parent_1[1]}, {self.similarity_to_parent_2[1]}')
            print(f'На обоих родителей: {self.similarity_to_parent_1[2]}, {self.similarity_to_parent_2[2]}')

        print()