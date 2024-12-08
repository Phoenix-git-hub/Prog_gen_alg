import matplotlib.pyplot as plt
from abc import ABC
class Graph(ABC):
    def __init__(self, number_of_algorithms):

        self.number_of_algorithms = number_of_algorithms

        self.array_colors = ['b', 'r', 'g', 'm']

class ProgressionGraph(Graph):
    def __init__(self, number_of_algorithms):

        super(ProgressionGraph, self).__init__(number_of_algorithms)

        self.array_fix_col = [self.lighten_color(i, 0.5) for i in self.array_colors]

    def set_min_mean_array(self, array_min_fitness_values, array_mean_fitness_values):
        self.array_min_fitness_values = array_min_fitness_values
        self.array_mean_fitness_values = array_mean_fitness_values
        self.detect_raise()

    def display(self):

        self.create_window()

        for i in range(len(self.array_min_fitness_values)):
            plt.plot(self.array_mean_fitness_values[i], color=self.array_colors[i])
            plt.plot(self.array_min_fitness_values[i], '--', color=self.array_fix_col[i])

    def detect_raise(self):
        if len(self.array_min_fitness_values) > len(self.array_colors):
            raise ValueError(f'класс ProgressionGraph: количество допустимых цветов меньше чем количество сборок')

        if len(self.array_min_fitness_values) != len(self.array_mean_fitness_values):
            raise ValueError(f'класс ProgressionGraph: размерности массивов array_min_fitness_Values)'
                  f' array_mean_fitness_values не совпадают ')

        if len(self.array_min_fitness_values[0]) != len(self.array_mean_fitness_values[0]):
            raise ValueError(f'класс ProgressionGraph: размерности массивов array_min_fitness_Values)'
                  f' array_mean_fitness_values не совпадают ')

        if self.number_of_algorithms != len(self.array_min_fitness_values):
            raise ValueError(f'класс ProgressionGraph: размерность массивов array_min_fitness_values и '
                  f'array_mean_fitness_values не совпадают с заданным')

    def create_window(self):
        if type(self.number_of_algorithms) != int:
            raise ValueError(f'Значение параметра number_of_algorithms из класса ProgressionGraph равно'
                             f' {self.number_of_algorithms}, эта переменная должна быть целым числом')

        elif self.number_of_algorithms == 1:
            plt.figure("Приспособленность").clear()
            plt.figure("Приспособленность")
            plt.xlabel('Поколение')
            plt.ylabel('Макс/средняя приспособленность')
            plt.title('Зависимость максимальной и средней приспособленности от поколения')

        elif self.number_of_algorithms == 2:
            plt.figure('Сравнение двух функций').clear()
            plt.figure('Сравнение двух функций')
            plt.xlabel('Поколение')
            plt.ylabel('средняя приспособленность')
            plt.title("blue - первый случай, red - второй \n штрих - лучшие значение, прямая - среднее")

        elif self.number_of_algorithms > 2:
            # идет работа

            plt.figure("Сравнение многих сборок").clear()
            plt.figure("Сравнение многих сборок")

            plt.xlabel('Поколение')
            plt.ylabel('средняя приспособленность')
            plt.title("Штрих - лучшие значение, прямая - среднее, синий - 1,\n красный - 2, зеленый - 3, пурпурный - 4")

        elif self.number_of_algorithms <= 0:
            raise ValueError(f'Значение параметра number_of_algorithms из класса ProgressionGraph равно'
                             f' {self.number_of_algorithms}, это число не может быть меньше 1')

        else:
            raise ValueError(f'Непредвиденное значение number_of_algorithms из класса ProgressionGraph, равно'
                             f' {self.number_of_algorithms}')

    def lighten_color(self, color, amount=0.5):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.

        Examples:
        >> lighten_color('g', 0.3)
        >> lighten_color('#F034A3', 0.6)
        >> lighten_color((.3,.55,.1), 0.5)
        """
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


class DeviationGrash(Graph):
    def set_deviation(self, deviation):
        self.deviation = deviation

    def display(self):

        self.create_window()

        for i in range(len(self.deviation)):

            plt.plot(self.deviation[i], self.array_colors[i])

    @staticmethod
    def create_window():
        plt.figure("Отклонение среднего от минимального").clear()
        plt.figure("Отклонение среднего от минимального")
        plt.xlabel('Поколение')
        plt.ylabel('Разница')
        plt.title("Отклонение среднего от минимального")




