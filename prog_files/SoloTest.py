import SolutionByGeneticAlgorithm
from prog_files import AdditionalSolutions
import matplotlib.pyplot as plt
from prog_files.WorkWithVertices import WorkWithVertices


class PositionOnScreen:
    def __init__(self):
        self.coordinates = {"upper left": (740, 0), "upper right": (1140, 0),
                            "lower left": (740, 370), "lower right": (1140, 370)}
        self.next_position = {"upper left": "lower left", "lower left": "upper right",
                              "upper right": "lower right", "lower right": "upper left"}
        self.now_position = "upper left"

    def get(self):
        coordinates = self.coordinates[self.now_position]
        self.now_position = self.next_position[self.now_position]
        return coordinates


class Solution:
    def __init__(self, general_settings, settings_gen_alg):

        self.general_settings = general_settings
        self.settings_gen_alg = settings_gen_alg

        self.position_screen = PositionOnScreen()

        numb_of_ver = self.general_settings['number_of_vertices']
        status_of_gen_adj_mat = self.general_settings['status_of_generation_adjacency_matrix']
        measure_of_disorder = self.general_settings['measure_of_disorder']
        status_of_the_symmetry_adjacency_matrix = self.general_settings['status_of_the_symmetry_adjacency_matrix']

        self.work_with_vertices = WorkWithVertices(numb_of_ver, status_of_gen_adj_mat,
                                                   measure_of_disorder, status_of_the_symmetry_adjacency_matrix)

        self.adjacency_matrix = self.work_with_vertices.initialization_adjacency_matrix()
        self.coordinates_of_vertices = self.work_with_vertices.get_coordinates_of_vertices()
        self.number_of_vertices = numb_of_ver

        import numpy as np
        np.set_printoptions(threshold=np.inf)

        print(self.coordinates_of_vertices)
        print(self.adjacency_matrix)

    def start_solving(self):

        self.solve_by_genetic_algorithm()

        self.pattern_add_sol(self.general_settings['state_brute_force'], AdditionalSolutions.SolutionByBruteForceMethod)
        self.pattern_add_sol(self.general_settings['state_dynamic_all_vertices'], AdditionalSolutions.SolutionByDynamicProgWithAllVertices)
        self.pattern_add_sol(self.general_settings['state_dynamic'], AdditionalSolutions.SolutionByDynamicProgramming)
        self.pattern_add_sol(self.general_settings['state_ant_algorithm'], AdditionalSolutions.SolutionByAntAlgorithm)
        self.pattern_add_sol(self.general_settings['state_annealing_method'], AdditionalSolutions.SolutionAnnealingMethod)

        self.pattern_add_sol(self.general_settings['state_branch_and_bound'],
                             AdditionalSolutions.SolutionByBranchAndBound)


    def pattern_add_sol(self, state, name_sol):
        if state:
            sol = name_sol(self.adjacency_matrix, self.coordinates_of_vertices,
                           self.number_of_vertices, self.position_screen.get())
            sol.start_solution()
            sol.display_sol()
            sol.output_parameters_to_console()

    def solve_by_genetic_algorithm(self):
        number_of_generations = self.general_settings['number_of_generations']
        population_size = self.general_settings['population_size']
        method_of_generation_start_pop = self.settings_gen_alg['method_of_generation_start_population']

        self.sol_by_genetic_algorithm = SolutionByGeneticAlgorithm.GeneticAlgorithm(population_size,
                                                                                    number_of_generations,
                                                                                    self.number_of_vertices,
                                                                                    method_of_generation_start_pop,
                                                                                    self.adjacency_matrix,
                                                                                    self.coordinates_of_vertices,
                                                                                    self.position_screen.get())

        self.sol_by_genetic_algorithm.initialization_state_surfing(self.settings_gen_alg['state_surfing'])
        self.sol_by_genetic_algorithm.initialization_selection_method(self.settings_gen_alg['selection_method'])
        self.sol_by_genetic_algorithm.initialization_crossing_method(self.settings_gen_alg['crossing_method'])
        self.sol_by_genetic_algorithm.initialization_mutation_method(self.settings_gen_alg['mutation_method'])

        self.sol_by_genetic_algorithm.initialization_status_of_searching_parent(
            self.settings_gen_alg['status_of_searching_parent'])

        self.sol_by_genetic_algorithm.start_solution()

        self.sol_by_genetic_algorithm.display_sol()
        self.sol_by_genetic_algorithm.display_deviation()
        self.sol_by_genetic_algorithm.output_parameters_to_console()
        print()
        self.sol_by_genetic_algorithm.visualization_progression()
        self.sol_by_genetic_algorithm.output_deviation_to_console()
        self.sol_by_genetic_algorithm.output_all_time_to_console()

    @staticmethod
    def display():
        plt.show()
