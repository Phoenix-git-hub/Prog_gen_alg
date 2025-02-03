import random
import numpy as np


class MethodsOfCrossing:
    # подбор особей для скрещивания нудно сделать случайным
    def __init__(self):
        # пожалуй нужно сделать файл config куда я положу общие данные для всего кода
        # нужно переименовать названия переменных two_point_crossing на crossover или посмотреть в словаре что коректне
        self.possible_names_of_crossing = ('crossing_pass', 'two_point_crossing', 'orderly_crossing_OX1',
                                           'one_point_crossing_OX1', 'crossover_ordered_ss', 'cycle_crossover',
                                           'crossover_order_bb', 'crossover_order_OX5', 'crossover_order_OX1_upgrade',
                                           'crossover_ordered_ox_s', 'crossover_ordered_ox_b',
                                           'partially_matched_crossover', 'one_point_crossing_bb', 'greedy_crossover',
                                           'crossover_order_OX5_upgrade', 'crossover_ox3')

        self.name_of_crossing = dict.fromkeys(self.possible_names_of_crossing)

        self.name_of_crossing['crossing_pass'] = self.crossing_pass
        self.name_of_crossing['two_point_crossing'] = self.two_point_crossing
        self.name_of_crossing['orderly_crossing_OX1'] = self.orderly_crossing_ox1
        self.name_of_crossing['one_point_crossing_OX1'] = self.one_point_crossing_ox1
        self.name_of_crossing['crossover_ordered_ss'] = self.crossover_ordered_ss
        self.name_of_crossing['cycle_crossover'] = self.cycle_crossover
        self.name_of_crossing['crossover_order_bb'] = self.crossover_order_bb
        self.name_of_crossing['crossover_order_OX1_upgrade'] = self.crossover_order_ox1_upgrade
        self.name_of_crossing['crossover_ordered_ox_s'] = self.crossover_ordered_ox_s
        self.name_of_crossing['crossover_ordered_ox_b'] = self.crossover_ordered_ox_b
        self.name_of_crossing['crossover_order_OX5'] = self.crossover_order_ox5
        self.name_of_crossing['partially_matched_crossover'] = self.partially_matched_crossover
        self.name_of_crossing['one_point_crossing_bb'] = self.one_point_crossing_bb
        self.name_of_crossing['greedy_crossover'] = self.greedy_crossover
        self.name_of_crossing['crossover_order_OX5_upgrade'] = self.crossover_order_ox5_upgrade
        self.name_of_crossing['crossover_ox3'] = self.crossover_ox3
        self.parent_index = None

        self.population = None
        self.new_population = None

        self.number_of_vertices = None
        self.crossing_method = None
        self.population_size = None
        self.searching_parent = None
        self.adjacency_matrix = None

    def random_search(self):
        self.parent_index = []
        indexes = [i for i in range(self.population_size)]

        while len(indexes) > 1:

            ind_1 = random.randrange(len(indexes))
            index_1 = indexes.pop(ind_1)

            ind_2 = random.randrange(len(indexes))
            index_2 = indexes.pop(ind_2)

            self.crossing_method(index_1, index_2)

            self.parent_index.append(index_1)
            self.parent_index.append(index_2)
        if len(indexes) == 1:
            self.parent_index.append(indexes[0])


    def ordered_search(self):
        # можно написать генератор для self.parent_index. ЭЭто глобально не на что не повлияет,
        # но я думаю так код работает быстрее
        self.parent_index = []
        for index in range(1, self.population_size, 2):
            self.crossing_method(index, index - 1)
            self.parent_index.append(index)
            self.parent_index.append(index - 1)
        if self.population_size % 2 == 1:
            self.parent_index.append(self.population_size - 1)

    def get_parent_index(self):
        return self.parent_index

    def initialize_status_of_searching_parent(self, searching_parent):
        if searching_parent == 'random_search':
            self.searching_parent = self.random_search
        elif searching_parent == 'ordered_search':
            self.searching_parent = self.ordered_search
        else:
            error_str = f'nonexistent name of status_of_searching_parent'
            raise Exception(error_str)

    def initialize_method_of_crossing(self, name_of_method):

        if name_of_method not in self.possible_names_of_crossing:
            error_str = f'nonexistent name of crossing'
            raise Exception(error_str)

        self.crossing_method = self.name_of_crossing[name_of_method]

    def initialize_number_of_vertices(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices

    def initialize_population_size(self, population_size):
        self.population_size = population_size

    def initialize_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix

    def do_crossing(self, population):
        self.population = population
        self.new_population = self.population.copy()
        self.searching_parent()
        return self.new_population


    @staticmethod
    def crossing_pass(ind_1, ind_2):
        pass

    def two_point_crossing(self, index, index_2):
        '''
        первое это не скрещивание а мутация
        мы разворачиваем часть списка
        при этом родители никак не скрещиваются

        '''
        pop = self.population
        new_pop = self.new_population

        first_limit = random.randrange(0, self.number_of_vertices)
        second_limit = random.randrange(0, self.number_of_vertices)
        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        new_pop[index][first_limit:second_limit + 1] = pop[index][first_limit:second_limit + 1][::-1].copy()

        first_limit = random.randrange(0, self.number_of_vertices)
        second_limit = random.randrange(0, self.number_of_vertices)
        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        new_pop[index_2][first_limit:second_limit + 1] = pop[index_2][first_limit:second_limit + 1][::-1].copy()

    def orderly_crossing_ox1(self, index, index_2):
        '''Начинает запонять со второй точки разрыва'''
        # Начинает считывать с самого начала особи
        '''Дефолтное упорядоченное скрещивание из книжки (Га на python) старая
        '''
        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()

        set_1 = set(parent_1[first_limit:second_limit])
        set_2 = set(parent_2[first_limit:second_limit])

        ind_1 = second_limit
        ind_2 = second_limit
        for i in range(self.number_of_vertices):
            if ind_1 >= self.number_of_vertices:
                ind_1 = 0
            if parent_2[i] in set_1:
                set_1.discard(parent_2[i])
            else:
                self.new_population[index][ind_1] = parent_2[i]
                ind_1 += 1

            if ind_2 >= self.number_of_vertices:
                ind_2 = 0
            if parent_1[i] in set_2:
                set_2.discard(parent_1[i])
            else:
                self.new_population[index_2][ind_2] = parent_1[i]
                ind_2 += 1

    def one_point_crossing_ox1(self, index, index_2):
        '''
        Как предыдущее но одноточечное
        '''
        section_point = random.randrange(0, self.number_of_vertices)
        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()
        set_1 = set(parent_1[:section_point])
        set_2 = set(parent_2[:section_point])
        ind_1 = 0
        ind_2 = 0

        for i in range(self.number_of_vertices):
            if parent_2[i] in set_1:
                set_1.discard(parent_2[i])
            else:
                self.new_population[index][section_point + ind_1] = parent_2[i]
                ind_1 += 1

            if parent_1[i] in set_2:
                set_2.discard(parent_1[i])
            else:
                self.new_population[index_2][section_point + ind_2] = parent_1[i]
                ind_2 += 1

    def crossover_ordered_ss(self, index, index_2):
        # как двухточечное скрешивание OX1 но заполение начинается с начала, и смотреть начинает с начала
        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()

        set_1 = set(parent_1[first_limit:second_limit])
        set_2 = set(parent_2[first_limit:second_limit])

        ind_1 = 0
        ind_2 = 0
        raz_lim_1 = 0
        raz_lim_2 = 0
        for i in range(self.number_of_vertices):
            if ind_1 == first_limit:
                raz_lim_1 = second_limit - first_limit
            if parent_2[i] in set_1:
                set_1.discard(parent_2[i])
            else:
                self.new_population[index][raz_lim_1 + ind_1] = parent_2[i]
                ind_1 += 1

            if ind_2 == first_limit:
                raz_lim_2 = second_limit - first_limit
            if parent_1[i] in set_2:
                set_2.discard(parent_1[i])
            else:
                self.new_population[index_2][raz_lim_2 + ind_2] = parent_1[i]
                ind_2 += 1

    def cycle_crossover(self, index, index_2):

        parent_1 = self.population[index_2].copy()
        parent_2 = self.population[index].copy()
        #print(f"родитель_1 : {parent_1}, родитель_2 : {parent_2}")
        sketch = [-1] * self.number_of_vertices

        flag = 1

        for i in range(self.number_of_vertices):

            if sketch[i] == -1:

                sketch[i] = flag
                stop = parent_1[i]
                num = parent_2[i]
                while num != stop:
                    ind = np.where(parent_1 == num)[0][0]
                    num = parent_2[ind]
                    sketch[ind] = flag

                if flag == 1:
                    flag = 0
                else:
                    flag = 1

        for i in range(self.number_of_vertices):

            if sketch[i] == 0:
                number = self.new_population[index][i]
                self.new_population[index][i] = self.new_population[index_2][i]
                self.new_population[index_2][i] = number

        #print(f"потомок_1 : { new_population[index - 1]}, потомок_2 : {new_population[index]}")

    def crossover_order_bb(self, index, index_2):

        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        #print(f'first_limit: {first_limit}, second_limit: {second_limit}')
        parent_2 = self.population[index].copy()
        parent_1 = self.population[index_2].copy()

        set_2 = set(parent_2[first_limit:second_limit])
        set_1 = set(parent_1[first_limit:second_limit])

        ind_1 = second_limit
        ind_2 = second_limit
        ind_ch = second_limit
        for i in range(self.number_of_vertices):
            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices

            if ind_1 >= self.number_of_vertices:
                ind_1 = 0
            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
            else:
                self.new_population[index][ind_1] = parent_1[ind_ch + i]
                ind_1 += 1

            if ind_2 >= self.number_of_vertices:
                ind_2 = 0
            if parent_2[ind_ch + i] in set_1:
                set_1.discard(parent_2[ind_ch + i])
            else:
                self.new_population[index_2][ind_2] = parent_2[ind_ch + i]
                ind_2 += 1

    def crossover_order_ox1_upgrade(self, index, index_2):
        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit
        parent_2 = self.population[index].copy()
        parent_1 = self.population[index_2].copy()

        set_2 = set(parent_2[first_limit:second_limit])
        set_1 = set(parent_1[first_limit:second_limit])

        ind_1 = 0
        ind_2 = 0
        ind_ch = second_limit
        raz_lim_1 = 0
        raz_lim_2 = 0
        for i in range(self.number_of_vertices):
            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices

            if ind_1 == first_limit:
                raz_lim_1 = second_limit - first_limit
            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
            else:
                self.new_population[index][raz_lim_1 + ind_1] = parent_1[ind_ch + i]
                ind_1 += 1

            if ind_2 == first_limit:
                raz_lim_2 = second_limit - first_limit
            if parent_2[ind_ch + i] in set_1:
                set_1.discard(parent_2[ind_ch + i])
            else:
                self.new_population[index_2][raz_lim_2 + ind_2] = parent_2[ind_ch + i]
                ind_2 += 1

    def crossover_ordered_ox_s(self, index, index_2):
        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()

        set_1 = set(parent_1[first_limit:second_limit])
        set_2 = set(parent_2[first_limit:second_limit])

        ind_1 = first_limit
        ind_2 = first_limit
        for i in range(self.number_of_vertices):

            if parent_2[i] in set_1:
                self.new_population[index][ind_1] = parent_2[i]
                ind_1 += 1
                set_1.discard(parent_2[i])
            if parent_1[i] in set_2:
                set_2.discard(parent_1[i])
                self.new_population[index_2][ind_2] = parent_1[i]
                ind_2 += 1

    def crossover_ordered_ox_b(self, index, index_2):

        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()

        set_1 = set(parent_1[first_limit:second_limit])
        set_2 = set(parent_2[first_limit:second_limit])

        ind_1 = first_limit
        ind_2 = first_limit
        ind_ch = second_limit
        for i in range(self.number_of_vertices):

            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices

            if parent_2[ind_ch + i] in set_1:
                self.new_population[index][ind_1] = parent_2[ind_ch + i]
                ind_1 += 1
                set_1.discard(parent_2[ind_ch + i])

            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
                self.new_population[index_2][ind_2] = parent_1[ind_ch + i]
                ind_2 += 1

    def crossover_order_ox5(self, index, index_2):
        parent_2 = self.population[index].copy()
        parent_1 = self.population[index_2].copy()

        set_of_limits = set()

        while len(set_of_limits) != 4:
            limit = random.randrange(0, self.number_of_vertices + 1)
            if limit not in set_of_limits:
                set_of_limits.add(limit)

        list_of_limits = list(set_of_limits)

        list_of_limits.sort()

        lim_1 = list_of_limits[0]
        lim_2 = list_of_limits[1]
        lim_3 = list_of_limits[2]
        lim_4 = list_of_limits[3]

        # lim_1 = 1
        # lim_2 = 3
        # lim_3 = 5
        # lim_4 = 8

        # print(lim_1, lim_2, lim_3, lim_4)

        set_2 = set(np.concatenate((parent_2[lim_1:lim_2], parent_2[lim_3:lim_4])))
        set_1 = set(np.concatenate((parent_1[lim_1:lim_2], parent_1[lim_3:lim_4])))


        ind_1 = lim_4
        ind_2 = lim_4
        ind_ch = lim_4
        for i in range(self.number_of_vertices):
            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices

            if ind_1 >= self.number_of_vertices:
                ind_1 = 0

            if ind_1 == lim_1:
                ind_1 += lim_2 - lim_1

            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
            else:
                self.new_population[index][ind_1] = parent_1[ind_ch + i]
                ind_1 += 1

            if ind_2 >= self.number_of_vertices:
                ind_2 = 0

            if ind_2 == lim_1:
                ind_2 += lim_2 - lim_1

            if parent_2[ind_ch + i] in set_1:
                set_1.discard(parent_2[ind_ch + i])
            else:
                self.new_population[index_2][ind_2] = parent_2[ind_ch + i]
                ind_2 += 1

    def partially_matched_crossover(self, index, index_2):
        first_limit = random.randrange(0, self.number_of_vertices + 1)
        second_limit = random.randrange(0, self.number_of_vertices + 1)

        if second_limit < first_limit:
            first_limit, second_limit = second_limit, first_limit

        for i in range(first_limit, second_limit):

            i_1, = np.where(self.new_population[index] == self.population[index_2][i])
            i_2, = np.where(self.new_population[index_2] == self.population[index][i])

            self.new_population[index][i_1] = self.new_population[index][i]
            self.new_population[index_2][i_2] = self.new_population[index_2][i]

            self.new_population[index][i] = self.population[index_2][i]
            self.new_population[index_2][i] = self.population[index][i]

    def one_point_crossing_bb(self, index, index_2):

        section_point = random.randrange(0, self.number_of_vertices)
        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()
        set_1 = set(parent_1[:section_point])
        set_2 = set(parent_2[:section_point])
        ind_1 = 0
        ind_2 = 0
        ind_ch = section_point
        for i in range(self.number_of_vertices):
            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices
            if parent_2[i + ind_ch] in set_1:
                set_1.discard(parent_2[ind_ch + i])
            else:
                self.new_population[index][section_point + ind_1] = parent_2[i + ind_ch]
                ind_1 += 1

            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
            else:
                self.new_population[index_2][section_point + ind_2] = parent_1[i + ind_ch]
                ind_2 += 1

    def greedy_crossover(self, index, index_2):
        if self.adjacency_matrix is None:
            print(self.population[index], self.population[index_2])
            raise 'параметр self.adjacency_matrix не был инициализирован'

        first_section_point = random.randrange(0, self.number_of_vertices)
        second_selection_point = random.randrange(0, self.number_of_vertices)

        i = 0
        last_el = first_section_point
        self.new_population[index][i] = self.population[index][last_el]
        i += 1
        set_into_the_solution_1 = set()
        set_into_the_solution_1.add(self.population[index][last_el])

        while i != self.number_of_vertices:

            z1 = (last_el + 1) % self.number_of_vertices
            z2 = (np.where(self.population[index_2] == self.population[index][last_el])[0][0] + 1) % self.number_of_vertices
            if self.population[index_2][z2] in set_into_the_solution_1 and self.population[index][z1] in set_into_the_solution_1:
                if self.population[index_2][z2] != self.population[index][z1]:
                    for j in range(self.number_of_vertices):
                        if self.population[index][j] not in set_into_the_solution_1:

                            self.new_population[index][i] = self.population[index][j]
                            set_into_the_solution_1.add(self.population[index][j])
                            last_el = j
                            i += 1
                            break
                else:
                    last_el = z1
                    # print(first_section_point)
                    # print(self.population[index], self.population[index_2])
                    # print(self.new_population[index])
                    # print(self.population[index])


                continue
            elif self.population[index_2][z2] in set_into_the_solution_1:
                self.new_population[index][i] = self.population[index][z1]
                set_into_the_solution_1.add(self.population[index][z1])
                last_el = z1
            elif self.population[index][z1] in set_into_the_solution_1:
                self.new_population[index][i] = self.population[index_2][z2]
                set_into_the_solution_1.add(self.population[index_2][z2])
                last_el = np.where(self.population[index] == self.population[index_2][z2])[0][0]
            else:
                if self.adjacency_matrix[self.population[index][last_el]][self.population[index][z1]] \
                        > self.adjacency_matrix[self.population[index][last_el]][self.population[index_2][z2]]:
                    self.new_population[index][i] = self.population[index_2][z2]
                    set_into_the_solution_1.add(self.population[index_2][z2])
                    last_el = np.where(self.population[index] == self.population[index_2][z2])[0][0]
                else:
                    self.new_population[index][i] = self.population[index][z1]
                    set_into_the_solution_1.add(self.population[index][z1])
                    last_el = z1
            i += 1


        i = 0
        last_el = second_selection_point
        self.new_population[index_2][i] = self.population[index_2][last_el]
        i += 1
        set_into_the_solution_2 = set()
        set_into_the_solution_2.add(self.population[index_2][last_el])

        while i != self.number_of_vertices:

            z1 = (last_el + 1) % self.number_of_vertices
            z2 = (np.where(self.population[index] == self.population[index_2][last_el])[0][0] + 1) % self.number_of_vertices

            if self.population[index][z2] in set_into_the_solution_2 and self.population[index_2][z1] in set_into_the_solution_2:
                if self.population[index][z2] != self.population[index_2][z1]:
                    for j in range(self.number_of_vertices):
                        if self.population[index_2][j] not in set_into_the_solution_2:
                            last_el = j
                            self.new_population[index_2][i] = self.population[index_2][j]
                            set_into_the_solution_2.add(self.population[index_2][j])
                            i += 1
                            break

                else:
                    last_el = z1
                continue
            elif self.population[index][z2] in set_into_the_solution_2:
                self.new_population[index_2][i] = self.population[index_2][z1]
                set_into_the_solution_2.add(self.population[index_2][z1])

                last_el = z1
            elif self.population[index_2][z1] in set_into_the_solution_2:
                self.new_population[index_2][i] = self.population[index][z2]
                set_into_the_solution_2.add(self.population[index][z2])

                last_el = np.where(self.population[index_2] == self.population[index][z2])[0][0]

            else:
                if self.adjacency_matrix[self.population[index_2][last_el]][self.population[index_2][z1]] \
                        > self.adjacency_matrix[self.population[index_2][last_el]][self.population[index][z2]]:
                    self.new_population[index_2][i] = self.population[index][z2]
                    set_into_the_solution_2.add(self.population[index][z2])
                    last_el = np.where(self.population[index_2] == self.population[index][z2])[0][0]
                else:
                    self.new_population[index_2][i] = self.population[index_2][z1]
                    set_into_the_solution_2.add(self.population[index_2][z1])
                    last_el = z1
            i += 1
    def crossover_order_ox5_upgrade(self, index, index_2):

        parent_2 = self.population[index].copy()
        parent_1 = self.population[index_2].copy()

        set_of_limits = set()

        while len(set_of_limits) != 4:
            limit = random.randrange(0, self.number_of_vertices + 1)
            if limit not in set_of_limits:
                set_of_limits.add(limit)

        list_of_limits = list(set_of_limits)

        list_of_limits.sort()

        lim_1 = list_of_limits[0]
        lim_2 = list_of_limits[1]
        lim_3 = list_of_limits[2]
        lim_4 = list_of_limits[3]
        #
        # lim_1 = 1
        # lim_2 = 3
        # lim_3 = 5
        # lim_4 = 8

        # print(lim_1, lim_2, lim_3, lim_4)

        set_2 = set(np.concatenate((parent_2[lim_1:lim_2], parent_2[lim_3:lim_4])))
        set_1 = set(np.concatenate((parent_1[lim_1:lim_2], parent_1[lim_3:lim_4])))


        ind_1 = 0
        ind_2 = 0
        ind_ch = lim_4
        for i in range(self.number_of_vertices):
            if ind_ch + i >= self.number_of_vertices:
                ind_ch -= self.number_of_vertices

            if ind_1 >= self.number_of_vertices:
                ind_1 = 0

            if ind_1 == lim_1:
                ind_1 += lim_2 - lim_1
            if ind_1 == lim_3:
                ind_1 += lim_4 - lim_3

            if parent_1[ind_ch + i] in set_2:
                set_2.discard(parent_1[ind_ch + i])
            else:
                self.new_population[index][ind_1] = parent_1[ind_ch + i]
                ind_1 += 1

            if ind_2 >= self.number_of_vertices:
                ind_2 = 0

            if ind_2 == lim_1:
                ind_2 += lim_2 - lim_1
            if ind_2 == lim_3:
                ind_2 += lim_4 - lim_3

            if parent_2[ind_ch + i] in set_1:
                set_1.discard(parent_2[ind_ch + i])
            else:
                self.new_population[index_2][ind_2] = parent_2[ind_ch + i]
                ind_2 += 1

    def crossover_ox3(self, index, index_2):
        lim1_first_par = random.randrange(0, self.number_of_vertices + 1)
        lim2_first_par = random.randrange(0, self.number_of_vertices + 1)

        lim1_second_par = random.randrange(0, self.number_of_vertices + 1)
        lim2_second_par = random.randrange(0, self.number_of_vertices + 1)

        if lim2_first_par < lim1_first_par:
            lim1_first_par, lim2_first_par = lim2_first_par, lim1_first_par

        parent_1 = self.population[index].copy()
        parent_2 = self.population[index_2].copy()

        set_1 = set(parent_1[lim1_first_par:lim2_first_par])
        set_2 = set(parent_2[lim1_second_par:lim2_second_par])

        ind_1 = lim2_first_par
        ind_2 = lim2_second_par

        for i in range(self.number_of_vertices):
            if ind_1 >= self.number_of_vertices:
                ind_1 = 0
            if parent_2[i] in set_1:
                set_1.discard(parent_2[i])
            else:
                self.new_population[index][ind_1] = parent_2[i]
                ind_1 += 1

            if ind_2 >= self.number_of_vertices:
                ind_2 = 0
            if parent_1[i] in set_2:
                set_2.discard(parent_1[i])
            else:
                self.new_population[index_2][ind_2] = parent_1[i]
                ind_2 += 1

# CS = MethodsOfCrossing()
# CS.initialize_number_of_vertices(5)
# CS.initialize_population_size(2)
# CS.initialize_method_of_crossing('partially_matched_crossover')
# CS.initialize_status_of_searching_parent('ordered_search')
# pop = np.array([np.array([1, 2, 3, 4, 5]), np.array([4, 3, 5, 1, 2])])
#
# print(CS.do_crossing(pop))