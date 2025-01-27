from python_tsp.exact import solve_tsp_brute_force
import numpy as np
import time
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from math import inf
from random import shuffle

from numpy import exp
from random import sample, random

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class Solution(ABC):
    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, name_of_method, place_on_screen):
        self.adjacency_matrix = adjacency_matrix
        self.coordinates_of_vertices = coordinates_of_vertices
        self.number_of_vertices = number_of_vertices
        self.name_of_method = name_of_method
        self.time_to_calculat_statistics = 0

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
            plt.ylim([0, 201])
            plt.xlim([0, 201])
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
        print('\tВремя -', self.time - self.time_to_calculat_statistics)
        print('\tДистанция -', self.distance)
        print('\tРешение -', self.permutation)

    @abstractmethod
    def solution(self):
        pass

    def fitness_function(self, individual):
        sum_vertexes = 0
        for i in range(self.number_of_vertices - 1):
            sum_vertexes += self.adjacency_matrix[individual[i]][individual[i + 1]]

        sum_vertexes += self.adjacency_matrix[individual[- 1]][individual[0]]
        return sum_vertexes


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
        if distance != self.fitness_function(permutation):
            raise 'дистанция не совпадает с показанием'

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
        if distance != self.fitness_function(permutation):
            raise 'дистанция не совпадает с показанием'
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
        if distance != self.fitness_function(permutation):
            raise 'дистанция не совпадает с показанием'
        return np.array(permutation), distance


class SolutionByAntAlgorithm(Solution):

    def __init__(self, adjacency_matrix, coordinates_of_vertices=0, number_of_vertices=0, place_on_screen=0):
        name_of_method = "Solution by ant algorithm"
        super(SolutionByAntAlgorithm, self).__init__(adjacency_matrix, coordinates_of_vertices, number_of_vertices,
                                                     name_of_method, place_on_screen)
        self.init_ant_algorithm_parameters()

    def init_ant_algorithm_parameters(self):
        """Initializes the hyperparameters for the algorithm."""
        self.ants = 100
        self.iter = 20
        self.a = 1.5
        self.b = 1.2
        self.p = 0.6
        self.q = 10

    @staticmethod
    def select_i(selection):

        sum_num = sum(selection)
        if sum_num == 0:
            return len(selection) - 1
        tmp_num = random()
        prob = 0
        for i in range(len(selection)):
            prob += selection[i] / sum_num
            if prob >= tmp_num:
                return i

    def create_indx(self, pm):

        unvisited_indx = list(range(self.number_of_vertices))
        shuffle(unvisited_indx)
        visited_indx = [unvisited_indx.pop()]
        for _ in range(self.number_of_vertices - 1):
            i = visited_indx[-1]
            selection = []
            for j in unvisited_indx:
                selection.append(
                    (pm[i][j] ** self.a) * ((1 / max(self.adjacency_matrix[i][j], 10**-5)) ** self.b)
                )
            selected_i = SolutionByAntAlgorithm.select_i(selection)
            visited_indx.append(unvisited_indx.pop(selected_i)) # была какая-то ошибка
        visited_indx.append(visited_indx[0])
        return visited_indx

    def update_pm(self, pm, tmp_indx, tmp_leng):

        # l = len(pm)
        for i in range(self.number_of_vertices):
            for j in range(i, self.number_of_vertices):
                pm[i][j] *= 1 - self.p
                pm[j][i] *= 1 - self.p
        for i in range(self.ants):
            delta = self.q / tmp_leng[i]
            indx = tmp_indx[i]
            for j in range(self.number_of_vertices):
                pm[indx[j]][indx[j + 1]] += delta
                pm[indx[j + 1]][indx[j]] += delta

    # def _calculate_dist(self, individual: list[int]) -> float:
    #     # убрать этот метод у меня етсь отдельные для этот
    #     """Calculates the path length based on the index list of the distance matrix."""
    #     sum_vertexes = 0
    #     for i in range(len(individual) - 1):
    #         sum_vertexes += self.adjacency_matrix[individual[i]][individual[i + 1]]
    #
    #     # sum_vertexes += self.adjacency_matrix[individual[- 1]][individual[0]]
    #     return sum_vertexes
    def run(self):
        pm = [[1 for _ in range(self.number_of_vertices)] for _ in range(self.number_of_vertices)]
        res_indx = []
        res_leng = inf
        for _ in range(self.iter):
            tmp_indx = []
            tmp_leng = []
            for _ in range(self.ants):
                indx = self.create_indx(pm)
                tmp_indx.append(indx)
                tmp_leng.append(self.fitness_function(indx))
            self.update_pm(pm, tmp_indx, tmp_leng)
            best_leng = min(tmp_leng)
            if best_leng < res_leng:
                res_leng = best_leng
                res_indx = tmp_indx[tmp_leng.index(best_leng)]
                # print(res_indx, res_leng, self._calculate_dist(res_indx), self.fitness_function(res_indx[:-1]))

        res_indx = res_indx[:-1]
        res_leng = self.fitness_function(res_indx)
        return res_indx, res_leng

    def solution(self):
        permutation, distance = self.solve_ant_algorithm()
        # print(per)
        # print(distance, self.fitness_function(per), self._calculate_dist(per))
        if distance != self.fitness_function(permutation):
            # print(per)
            print(permutation)
            raise 'дистанция не совпадает с показанием'
        return np.array(permutation), distance

    def solve_ant_algorithm(self):
        best_sol, distance = self.run()
        return best_sol, distance


class SolutionAnnealingMethod(Solution):

    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, place_on_screen):
        name_of_method = "Solution by annealing method"
        super(SolutionAnnealingMethod, self).__init__(adjacency_matrix, coordinates_of_vertices, number_of_vertices,
                                                      name_of_method, place_on_screen)

        self.init_hyperparameters()

    def init_hyperparameters(self):
        self.iter = 200000
        self.t = 100
        self.g = 0.6
        # iter = 20000, t = 100, g = 0.6

    # def _calculate_dist(self, individual: list[int]) -> float:
    #     # убрать этот метод у меня етсь отдельные для этот
    #     """Calculates the path length based on the index list of the distance matrix."""
    #     sum_vertexes = 0
    #     for i in range(len(individual) - 1):
    #         sum_vertexes += self.adjacency_matrix[individual[i]][individual[i + 1]]
    #
    #     sum_vertexes += self.adjacency_matrix[individual[- 1]][individual[0]]
    #     return sum_vertexes

    def solution(self):

        permutation, distance = self.run()

        if distance != self.fitness_function(permutation):
            raise 'дистанция не совпадает с показанием'
        return np.array(permutation), distance

    def is_acceptable(self, prb_leng, tmp_leng):
            # print(self.t, exp(-(prb_leng - tmp_leng) / self.t), -(prb_leng - tmp_leng) / self.t)
        try:
            prob = min(1, exp(-(prb_leng - tmp_leng) / self.t))
        except Exception:
            prob = 0
            if prb_leng - tmp_leng < 0:
                prob = 1
        if prob > random():
            return True

        return False

    def run(self):

        tmp_indx = [i for i in range(self.number_of_vertices)] + [0]
        tmp_leng = self.fitness_function(tmp_indx)
        res_indx = tmp_indx.copy()
        res_leng = tmp_leng
        for _ in range(self.iter):
            i, j = sample(range(1, self.number_of_vertices), 2)
            prb_indx = tmp_indx.copy()
            prb_indx[i], prb_indx[j] = prb_indx[j], prb_indx[i]
            prb_leng = self.fitness_function(prb_indx)
            if self.is_acceptable(prb_leng, tmp_leng):
                tmp_indx = prb_indx
                tmp_leng = prb_leng
            if tmp_leng < res_leng:
                res_indx = tmp_indx
                res_leng = tmp_leng
            self.t *= self.g
        res_indx = res_indx[:-1]
        res_leng = self.fitness_function(res_indx)
        return res_indx, res_leng


class SolutionByBranchAndBound(Solution):
    def __init__(self, adjacency_matrix, coordinates_of_vertices, number_of_vertices, place_on_screen):
        name_of_method = "Solution by branch and bound"
        super(SolutionByBranchAndBound, self).__init__(adjacency_matrix, coordinates_of_vertices,
                                                         number_of_vertices, name_of_method, place_on_screen)

    def solution(self):
        permutation, distance = self.solve_by_branch_and_bound()
        if distance != self.fitness_function(permutation):
            raise 'дистанция не совпадает с показанием'
        return np.array(permutation), distance

    def calculate_lower_bound(self, route):
        bound = 0
        remaining_cities = [i for i in range(self.number_of_vertices) if i not in route]

        for i in range(1, len(route)):
            bound += self.adjacency_matrix[route[i - 1]][route[i]]

        if remaining_cities:
            bound += min(self.adjacency_matrix[route[-1]][city] for city in remaining_cities)
            for city in remaining_cities:
                if len(remaining_cities) > 1:
                    bound += min(self.adjacency_matrix[city][i] for i in remaining_cities if i != city)
                else:
                    bound += self.adjacency_matrix[city][route[0]]
        return bound
    
    def solve_by_branch_and_bound(self):

        best_tour = None

        best_cost = float('inf')

        stack = [((0,), 0)]

        while stack:
            route, dist = stack.pop()

            if len(route) == self.number_of_vertices:
                dist += self.adjacency_matrix[route[-1]][route[0]]  # Complete the route
                if dist < best_cost:
                    best_cost = dist
                    best_tour = route
            else:
                remaining_cities = [i for i in range(self.number_of_vertices) if i not in route]
                for city in remaining_cities:
                    new_tour = route + (city,)
                    new_cost = dist + self.adjacency_matrix[route[-1]][city]
                    lower_bound = self.calculate_lower_bound(new_tour)

                    if lower_bound < best_cost:
                        stack.append((new_tour, new_cost))

        return best_tour, best_cost

