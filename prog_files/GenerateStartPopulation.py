import numpy as np
import tkinter.messagebox
from AdditionalSolutions import SolutionByDynamicProgWithAllVertices
class GenStartPop:
    def __init__(self, number_of_vertices, population_size, method_of_generation_start_population):
        self.number_of_vertices = number_of_vertices
        self.method_of_generation_start_population = method_of_generation_start_population.get()
        self.population_size = population_size

    def generation_start_population(self, adjacency_matrix):
        if self.method_of_generation_start_population == 'random_gen':
            population = np.array([np.random.choice(self.number_of_vertices, self.number_of_vertices, replace=False)
                                   for _ in range(self.population_size)])
            return population
        elif self.method_of_generation_start_population == 'ordered_gen':
            population = np.zeros(shape=(self.population_size, self.number_of_vertices), dtype=int)
            for i in range(self.population_size):
                for j in range(self.number_of_vertices):
                    population[i][j] = j
            return population
        elif self.method_of_generation_start_population == 'greedy_algorithm_gen':
            sol_din_pr = SolutionByDynamicProgWithAllVertices(adjacency_matrix,
                                                              number_of_vertices=self.number_of_vertices)
            individual = sol_din_pr.solution()[0]
            population = np.array([individual for _ in range(self.population_size)])
            return population

        else:
            string = """Неизвестное значение self.settings_comparison_alg['generation_of_the_starting_population']
            класса 'WindowComparison'"""
            tkinter.messagebox.showerror("Ошибка", string)