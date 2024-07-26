from SolutionByGeneticAlgorithm import GeneticAlgorithm
from prog_files.WorkWithVertices import WorkWithVertices
import matplotlib.pyplot as plt

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

        self.average_mean_val_1 = [0] * self.number_of_generations
        self.average_min_val_1 = [0] * self.number_of_generations
        self.average_mean_val_2 = [0] * self.number_of_generations
        self.average_min_val_2 = [0] * self.number_of_generations

        self.average_time_to_crossing_1 = 0
        self.average_time_to_mutation_1 = 0
        self.average_time_to_selection_1 = 0
        self.average_time_to_calculat_statistics_1 = 0
        self.average_full_time_1 = 0
        self.time_to_generate_first_pop_1 = 0

        self.average_time_to_crossing_2 = 0
        self.average_time_to_mutation_2 = 0
        self.average_time_to_selection_2 = 0
        self.average_time_to_calculat_statistics_2 = 0
        self.average_full_time_2 = 0
        self.time_to_generate_first_pop_2 = 0

        #все выделить в отдельные классы
        self.first_gen_alg = GeneticAlgorithm(self.population_size, self.number_of_generations,
                                              self.number_of_vertices, method_of_generation_start_population_first_alg)

        self.first_gen_alg.initialization_selection_method(self.settings_mandatory_alg['selection_method'])
        self.first_gen_alg.initialization_crossing_method(self.settings_mandatory_alg['crossing_method'])
        self.first_gen_alg.initialization_mutation_method(self.settings_mandatory_alg['mutation_method'])
        self.first_gen_alg.initialization_status_of_searching_parent(
            self.settings_mandatory_alg['status_of_searching_parent'])

        self.second_gen_alg = GeneticAlgorithm(self.population_size, self.number_of_generations,
                                               self.number_of_vertices, method_of_generation_start_population_second_alg)

        self.second_gen_alg.initialization_selection_method(self.settings_additional_alg['selection_method'])
        self.second_gen_alg.initialization_crossing_method(self.settings_additional_alg['crossing_method'])
        self.second_gen_alg.initialization_mutation_method(self.settings_additional_alg['mutation_method'])
        self.second_gen_alg.initialization_status_of_searching_parent(
            self.settings_additional_alg['status_of_searching_parent'])




    def start_comparison(self):

        for i in range(self.number_of_comparisons):
            print(i)

            adjacency_matrix = self.work_with_vertices.initialization_adjacency_matrix()

            self.first_gen_alg.set_adjacency_matrix(adjacency_matrix)
            self.second_gen_alg.set_adjacency_matrix(adjacency_matrix)

            self.first_gen_alg.start_solution()
            self.second_gen_alg.start_solution()

            # обернуть в какю-нибуть функцию срочно

            self.average_time_to_crossing_1 += self.first_gen_alg.get_time_to_crossing()
            self.average_time_to_mutation_1 += self.first_gen_alg.get_time_to_mutation()
            self.average_time_to_selection_1 += self.first_gen_alg.get_time_to_selection()
            self.average_time_to_calculat_statistics_1 += self.first_gen_alg.get_time_to_calculat_statistics()
            self.average_full_time_1 +=self.first_gen_alg.get_full_time()
            self.time_to_generate_first_pop_1 += self.first_gen_alg.get_time_to_generate_first_pop()

            self.average_time_to_crossing_2 += self.second_gen_alg.get_time_to_crossing()
            self.average_time_to_mutation_2 += self.second_gen_alg.get_time_to_mutation()
            self.average_time_to_selection_2 += self.second_gen_alg.get_time_to_selection()
            self.average_time_to_calculat_statistics_2 += self.second_gen_alg.get_time_to_calculat_statistics()
            self.average_full_time_2 += self.second_gen_alg.get_full_time()
            self.time_to_generate_first_pop_2 += self.second_gen_alg.get_time_to_generate_first_pop()

            mean_fitness_values_1 = self.first_gen_alg.get_mean_fitness_values()
            min_fitness_values_1 = self.first_gen_alg.get_min_fitness_values()

            mean_fitness_values_2 = self.second_gen_alg.get_mean_fitness_values()
            min_fitness_values_2 = self.second_gen_alg.get_min_fitness_values()

            for ind in range(self.number_of_generations):
                self.average_mean_val_1[ind] += mean_fitness_values_1[ind]
                self.average_min_val_1[ind] += min_fitness_values_1[ind]
                self.average_mean_val_2[ind] += mean_fitness_values_2[ind]
                self.average_min_val_2[ind] += min_fitness_values_2[ind]
        # блять тут и комментировать не надо
        for ind in range(self.number_of_generations):
            self.average_mean_val_1[ind] /= self.number_of_comparisons
            self.average_min_val_1[ind] /= self.number_of_comparisons
            self.average_mean_val_2[ind] /= self.number_of_comparisons
            self.average_min_val_2[ind] /= self.number_of_comparisons

        # блять все в новые функции
        self.average_time_to_crossing_1 /= self.number_of_comparisons
        self.average_time_to_mutation_1 /= self.number_of_comparisons
        self.average_time_to_selection_1 /= self.number_of_comparisons
        self.average_time_to_calculat_statistics_1 /= self.number_of_comparisons
        self.average_full_time_1 /= self.number_of_comparisons
        self.time_to_generate_first_pop_1 /= self.number_of_comparisons

        self.average_time_to_crossing_2 /= self.number_of_comparisons
        self.average_time_to_mutation_2 /= self.number_of_comparisons
        self.average_time_to_selection_2 /= self.number_of_comparisons
        self.average_time_to_calculat_statistics_2 /= self.number_of_comparisons
        self.average_full_time_2 /= self.number_of_comparisons
        self.time_to_generate_first_pop_2 /= self.number_of_comparisons

        print("Вычисления закончены")

    def visualization_progression(self):
        plt.figure('Сравнение двух функций').clear()
        plt.plot(self.average_mean_val_1, color='blue')
        plt.plot(self.average_min_val_1, '--', color='b')
        plt.plot(self.average_mean_val_2, color='red')
        plt.plot(self.average_min_val_2, '--', color='red')

        plt.xlabel('Поколение')
        plt.ylabel('средняя приспособленность')
        plt.title("blue - первый случай, red - второй \n штрих - лучшие значение, прямая - среднее")

        plt.show()

    def output_deviation_to_console(self):
        # MSPE
        dev_min_from_mean_1 = 0
        dev_min_from_mean_2 = 0

        for i in range(self.number_of_generations):
            dev_min_from_mean_1 += ((self.average_mean_val_1[i] - self.average_min_val_1[i]) / self.average_min_val_1[i]) ** 2
            dev_min_from_mean_2 += ((self.average_mean_val_2[i] - self.average_min_val_2[i]) / self.average_min_val_1[i]) ** 2

        dev_min_from_mean_1 /= self.number_of_generations
        dev_min_from_mean_2 /= self.number_of_generations
        dev_min_from_mean_1 *= 100
        dev_min_from_mean_2 *= 100

        print(f'Среднеквадратичная ошибка в процентах первого алгоритма - {dev_min_from_mean_1}')
        print(f'Среднеквадратичная ошибка в процентах второго алгоритма - {dev_min_from_mean_2}')

    def output_time_to_console(self):
        print(f'Среднее время первого - {self.average_full_time_1}, второго - {self.average_full_time_2}')
        print(f'Среднее время на скрещивание - {self.average_time_to_crossing_1}, второго - {self.average_time_to_crossing_2 }')
        print(f'Среднее время мутации - {self.average_time_to_mutation_1}, второго - {self.average_time_to_mutation_2}')
        print(f'Среднее время селекции - {self.average_time_to_selection_1}, второго - {self.average_time_to_selection_2 }')
        print(f'Среднее время калькулирование - {self.average_time_to_calculat_statistics_1}, второго - {self.average_time_to_calculat_statistics_2 }')
        print(f'Среднее время на создание первого поколения - {self.time_to_generate_first_pop_1}, второго - {self.time_to_generate_first_pop_2}')
        print()