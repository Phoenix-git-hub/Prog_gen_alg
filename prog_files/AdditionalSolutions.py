from python_tsp.exact import solve_tsp_brute_force
import numpy as np
import time
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Solution(ABC):
    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, name_of_method, place_on_screen):
        self.adjacency_matrix = adjacency_matrix
        self.coordinates_of_vertices = coordinates_of_vertices
        self.number_of_vertices = number_of_vertices
        self.name_of_method = name_of_method

        self.coordinates = place_on_screen
        if self.coordinates:
            self.coordinates = f'+{place_on_screen[0]}+{place_on_screen[1]}'

        self.distance = None
        self.permutation = None
        self.time = 0

    def start_solution(self):
        start_time = time.time()
        self.permutation, self.distance = self.solution()
        end_time = time.time()
        self.time = end_time - start_time

    def display_sol(self):
        if self.permutation is None:
            error_str = str(self.__class__.__name__) + \
                        ".start_solution must be called before " + str(self.__class__.__name__) + ".display_sol"
            raise Exception(error_str)
        else:
            # нужно переписать работу функции и сделать ее более понятной
            plt.figure(self.name_of_method, figsize=(4, 3)).clear()

            plt.get_current_fig_manager().window.wm_geometry(self.coordinates)
            plt.title(self.name_of_method)
            plt.ylim([0, 101])
            plt.xlim([0, 101])
            for i in self.coordinates_of_vertices:
                plt.scatter(i[0], i[1], color='red')
            for i in range(len(self.permutation) - 1):
                plt.plot([self.coordinates_of_vertices[self.permutation[i]][0],
                          self.coordinates_of_vertices[self.permutation[i + 1]][0]],
                         [self.coordinates_of_vertices[self.permutation[i]][1],
                          self.coordinates_of_vertices[self.permutation[i + 1]][1]], color='blue')

            plt.plot([self.coordinates_of_vertices[self.permutation[0]][0],
                      self.coordinates_of_vertices[self.permutation[-1]][0]],
                     [self.coordinates_of_vertices[self.permutation[0]][1],
                      self.coordinates_of_vertices[self.permutation[-1]][1]], color='blue')

    def output_parameters_to_console(self):
        print(f"{self.name_of_method}:")
        print('\tВремя -', self.time)
        print('\tДистанция -', self.distance)
        print('\tРешение -', self.permutation)

    @abstractmethod
    def solution(self):
        pass


class SolDynamicProgramming(Solution):
    # нудно переписать код
    def find_best_solution_by_dynamic_programming(self, start_town=0):
        set_of_possible_vertices = set(np.array([i for i in range(self.number_of_vertices)]))
        set_of_possible_vertices.remove(start_town)
        min_sol = 0
        best_solution = [start_town]
        vertex = start_town
        while set_of_possible_vertices:
            array_of_edges = [[i, self.adjacency_matrix[vertex][i]] for i in range(self.number_of_vertices)]

            for i in range(1, self.number_of_vertices):
                for j in range(self.number_of_vertices - i):
                    if array_of_edges[j][1] > array_of_edges[j + 1][1]:
                        array_of_edges[j], array_of_edges[j + 1] = array_of_edges[j + 1], array_of_edges[j]
            for i in array_of_edges:
                if i[0] in set_of_possible_vertices:
                    min_sol += i[1]
                    best_solution.append(i[0])
                    set_of_possible_vertices.remove(i[0])
                    vertex = i[0]
                    break
        min_sol += self.adjacency_matrix[best_solution[-1]][start_town]
        return best_solution, min_sol

    @abstractmethod
    def solution(self):
        pass


class SolutionByDynamicProgramming(SolDynamicProgramming):
    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, place_on_screen):
        name_of_method = "Solution by dynamic programming"
        super(SolutionByDynamicProgramming, self).__init__(adjacency_matrix, coordinates_of_vertices,
                                                           number_of_vertices, name_of_method, place_on_screen)

    def solution(self):
        permutation, distance = self.find_best_solution_by_dynamic_programming()
        return np.array(permutation), distance


class SolutionByDynamicProgWithAllVertices(SolDynamicProgramming):
    def __init__(self, adjacency_matrix, coordinates_of_vertices=0, number_of_vertices=0, place_on_screen=0):
        name_of_method = "Solution by greedy algorithm"
        super(SolutionByDynamicProgWithAllVertices, self).__init__(adjacency_matrix, coordinates_of_vertices,
                                                                   number_of_vertices, name_of_method,  place_on_screen)

    def set_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix

    def set_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def solution(self):
        permutation, distance = self.find_best_solution_by_dynamic_programming_al_v()
        return np.array(permutation), distance

    def find_best_solution_by_dynamic_programming_al_v(self):
        # нужно переписать код
        best_sol, min_sol = self.find_best_solution_by_dynamic_programming()
        for i in range(1, self.number_of_vertices):
            best_sol_n, min_sol_n = self.find_best_solution_by_dynamic_programming(i)
            if min_sol > min_sol_n:
                min_sol = min_sol_n
                best_sol = best_sol_n
        return best_sol, min_sol


class SolutionByBruteForceMethod(Solution):

    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, place_on_screen):
        name_of_method = "Solution by brute force method"
        super(SolutionByBruteForceMethod, self).__init__(adjacency_matrix, coordinates_of_vertices,
                                                         number_of_vertices, name_of_method, place_on_screen)

    def solution(self):
        permutation, distance = solve_tsp_brute_force(self.adjacency_matrix)
        return np.array(permutation), distance
