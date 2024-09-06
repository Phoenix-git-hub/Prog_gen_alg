import SolutionByGeneticAlgorithm
from prog_files import AdditionalSolutions
import matplotlib.pyplot as plt
from prog_files.WorkWithVertices import WorkWithVertices

class Solution:

    def __init__(self, general_settings, settings_gen_alg):

        self.general_settings = general_settings
        self.settings_gen_alg = settings_gen_alg
        self.places_on_screen = {"upper left": (740, 0), "upper right": (1140, 0),
                                 "lower left": (740, 370), "lower right": (1140, 370)}
        self.position_screen = ["upper right", "lower right", "lower left", "upper left",
                                "upper right", "lower right", "lower left", "upper left"]

        numb_of_ver = self.general_settings['number_of_vertices']
        status_of_gen_adj_mat = self.general_settings['status_of_generation_adjacency_matrix']
        measure_of_disorder = self.general_settings['measure_of_disorder']
        status_of_the_symmetry_adjacency_matrix = self.general_settings['status_of_the_symmetry_adjacency_matrix']

        self.work_with_vertices = WorkWithVertices(numb_of_ver, status_of_gen_adj_mat,
                                                   measure_of_disorder, status_of_the_symmetry_adjacency_matrix)

        self.sol_brute_force = None
        self.sol_by_dynamic_prog = None
        self.sol_dynamic_all_vertices = None
        self.sol_by_genetic_algorithm = None
        self.sol_by_ant_algorithm = None
        self.sol_by_annealing_method = None

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

    def pattern_add_sol(self, state, name_sol):
        if state:
            self.sol_brute_force = name_sol(self.adjacency_matrix, self.coordinates_of_vertices,
                                            self.number_of_vertices, self.places_on_screen[self.position_screen.pop()])
            self.sol_brute_force.start_solution()
            self.sol_brute_force.display_sol()
            self.sol_brute_force.output_parameters_to_console()

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
                                                                                    self.places_on_screen[self.position_screen.pop()])

        self.sol_by_genetic_algorithm.initialization_selection_method(self.settings_gen_alg['selection_method'])
        self.sol_by_genetic_algorithm.initialization_crossing_method(self.settings_gen_alg['crossing_method'])
        self.sol_by_genetic_algorithm.initialization_mutation_method(self.settings_gen_alg['mutation_method'])

        self.sol_by_genetic_algorithm.initialization_status_of_searching_parent(
            self.settings_gen_alg['status_of_searching_parent'])

        self.sol_by_genetic_algorithm.start_solution()

        self.sol_by_genetic_algorithm.display_sol()
        self.sol_by_genetic_algorithm.output_parameters_to_console()
        print()
        self.sol_by_genetic_algorithm.visualization_progression()
        self.sol_by_genetic_algorithm.output_deviation_to_console()
        self.sol_by_genetic_algorithm.output_all_time_to_console()

    @staticmethod
    def display():
        plt.show()
