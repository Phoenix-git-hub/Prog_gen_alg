import numpy as np
import math
import tkinter.messagebox
import random


class WorkWithVertices:
    #нужно поэтапно, по сеттерам передавать параметры
    def __init__(self, number_of_vertices, status_of_generation_adjacency_matrix,
                 measure_of_disorder, status_of_the_symmetry_adjacency_matrix):

        self.status_of_the_symmetry_adjacency_matrix = status_of_the_symmetry_adjacency_matrix
        self.measure_of_disorder = measure_of_disorder
        self.number_of_vertices = number_of_vertices
        self.status_of_generation_adjacency_matrix = status_of_generation_adjacency_matrix
        self.coordinates_of_vertices = None

    def initialization_coordinates_of_vertices(self):
        self.coordinates_of_vertices = np.random.choice(101, size=[self.number_of_vertices, 2], replace=False)

    def get_coordinates_of_vertices(self):
        return self.coordinates_of_vertices

    def initialization_adjacency_matrix(self):
        #не во всех случаях надо инициализировать координаты вершин в дальнейшем надо изменить
        self.initialization_coordinates_of_vertices()

        if self.status_of_generation_adjacency_matrix == 'generation_by_vertices':
            return self.generation_adjacency_matrix()
        elif self.status_of_generation_adjacency_matrix == 'random_generation':
            return self.random_generation_adjacency_matrix()
        else:
            str_error = "Неизвестное значение 'settings['status_of_generation_adjacency_matrix']' класса 'MainWindow'"
            tkinter.messagebox.showerror("Ошибка", str_error)

    def generation_adjacency_matrix(self):

        adjacency_matrix = np.zeros((self.number_of_vertices, self.number_of_vertices), dtype='int16')
        # мэйби переписать рабочий код
        ind_i = 0
        for i in self.coordinates_of_vertices:
            ind_j = ind_i + 1
            for j in self.coordinates_of_vertices[ind_i + 1:]:
                distance = round(math.sqrt((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2))
                adjacency_matrix[ind_i][ind_j] = distance
                adjacency_matrix[ind_j][ind_i] = distance
                ind_j += 1
            ind_i += 1
        #это нужно переписать аыамыаы
        return self.checking_for_symmetry(self.make_mess(adjacency_matrix.copy()))

    def random_generation_adjacency_matrix(self):
        num_of_ver = self.number_of_vertices
        adjacency_matrix = np.random.randint(100, size=(num_of_ver, num_of_ver), dtype='int16')

        return self.checking_for_symmetry(self.make_mess(adjacency_matrix.copy()))
    #переписать логику, нужно чтото сделать в следствии симметрии и не только
    #переименовать все self.measure_of_disorder = measure_of_disorder в mess

    def make_mess(self, adjacency_matrix):
        if self.measure_of_disorder == 0:
            return adjacency_matrix.copy()
        for i in range(self.number_of_vertices):
            for j in range(self.number_of_vertices):
                k = random.random()
                if k < 0.5:
                    a = (2 * k)**(1/(self.measure_of_disorder + 1))
                else:
                    a = (1/(2 * (1 - k)))**(1/(self.measure_of_disorder + 1))
                adjacency_matrix[i][j] = adjacency_matrix[i][j] * a
        return adjacency_matrix.copy()

    def checking_for_symmetry(self, adjacency_matrix):
        if self.status_of_the_symmetry_adjacency_matrix == 'symmetric_adjacency_matrix':
            for i in range(self.number_of_vertices):
                for j in range(i):
                    adjacency_matrix[i][j] = adjacency_matrix[j][i]
        return adjacency_matrix
