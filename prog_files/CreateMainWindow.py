import tkinter
import tkinter.messagebox
import tkinter.ttk
from prog_files.AlgorithmWindow import AlgorithmWindow
from prog_files.CreateWindowOfComparison import WindowComparison


class MainWindow:
    def __init__(self, star_alg):

        self.window = tkinter.Tk()
        self.star_alg = star_alg

        self.state_dynamic = tkinter.BooleanVar(value=True)
        self.state_dynamic_all_vertices = tkinter.BooleanVar(value=True)
        self.state_brute_force = tkinter.BooleanVar(value=False)
        self.state_ant_algorithm = tkinter.BooleanVar(value=True)
        self.state_annealing_method = tkinter.BooleanVar(value=True)
        self.state_branch_and_bound = tkinter.BooleanVar(value=True)

        self.comparison_status = tkinter.StringVar(value='solo_test')
        self.status_of_generation_adjacency_matrix = tkinter.StringVar(value='generation_by_vertices')
        self.status_of_the_symmetry_adj_matrix = tkinter.StringVar(value='symmetric_adjacency_matrix')

        self.value_ent_number_of_vertices = tkinter.StringVar(value='17')
        self.value_ent_number_of_generations = tkinter.StringVar(value='10000')
        self.value_ent_population_size = tkinter.StringVar(value='20')
        self.value_ent_measure_of_disorder = tkinter.StringVar(value='0')
        self.name_file = tkinter.StringVar(value='')


        # вместо одного списка настроек нужно сделать несколько: solutions_settings, state_mode, gen_alg_settings
        settings = ('state_mode', 'status_of_generation_adjacency_matrix', 'state_dynamic',
                    'state_dynamic_all_vertices', 'state_brute_force', 'number_of_vertices',
                    'number_of_generations', 'population_size', 'measure_of_disorder',
                    'status_of_the_symmetry_adjacency_matrix', 'name_file')
        self.algorithm_parameters = dict.fromkeys(settings)

        place_1 = "+0+380"
        place_2 = "+500+380"

        self.window_mandatory_alg = AlgorithmWindow('Настройки обязательного алгоритма', place_1)
        self.window_mandatory_alg.basic_parameters()

        self.array_of_algorithms = [self.window_mandatory_alg]

        self.window_additional_alg = AlgorithmWindow('Настройки второго алгоритма(для сравнения)', place_2)
        self.window_additional_alg.basic_parameters()
        self.window_additional_alg.withdraw()

        self.window_comparison = WindowComparison()
        self.window_comparison.basic_parameters()
        self.window_comparison.withdraw()

    def create_main_window(self):
        self.settings_main_window()
        self.display_comparison_status()
        self.display_status_of_generation_adjacency_matrix()
        self.display_additional_solutions()
        self.display_general_parameters()
        self.display_start_btn()
        self.window.mainloop()

    def settings_main_window(self):
        self.window.geometry('800x350+0+0')
        self.window.title('Главное окно')
        self.window.resizable(width=False, height=False)

    def display_comparison_status(self):
        solo_test = tkinter.Radiobutton(self.window, text='Пробный тест одной сборки', value='solo_test',
                                        variable=self.comparison_status,
                                        font=("Arial Bold", 15), command=self.swap_mode)
        solo_test.place(x=10, y=0, width=280, height=60)

        comparison = tkinter.Radiobutton(self.window, text='Сравнение сборок', value='comparison',
                                         variable=self.comparison_status,
                                         font=("Arial Bold", 15), command=self.swap_mode)
        comparison.place(x=280, y=0, width=280, height=60)

        # lab_assemblies_number = tkinter.Label(self.window, text='Количество \nсборок-', font=("Arial Bold", 14))
        # lab_assemblies_number.place(x=580, y=10, width=110, height=60)
        # ent_assemblies_number = tkinter.Entry(self.window, width=10, textvariable=self.value_ent_assemblies_number)
        #
        # ent_assemblies_number.place(x=680, y=38, width=70, height=30)

    def display_status_of_generation_adjacency_matrix(self):
        generation_by_vertices = tkinter.Radiobutton(self.window, text='Генерация на основе вершин',
                                                     value='generation_by_vertices',
                                                     variable=self.status_of_generation_adjacency_matrix,
                                                     font=("Arial Bold", 15))
        generation_by_vertices.place(x=7, y=40, width=300, height=40)

        random_generation = tkinter.Radiobutton(self.window, text='Случайная генерация', value='random_generation',
                                                variable=self.status_of_generation_adjacency_matrix,
                                                font=("Arial Bold", 15))
        random_generation.place(x=320, y=40, width=240, height=40)

        random_generation = tkinter.Radiobutton(self.window, text='Скачать из файлы', value='download_from_a_file',
                                                variable=self.status_of_generation_adjacency_matrix,
                                                font=("Arial Bold", 15))
        random_generation.place(x=570, y=40, width=190, height=40)

        lab_name_file = tkinter.Label(self.window, text='Название файла -', font=("Arial Bold", 14))
        lab_name_file.place(x=530, y=20, width=160, height=20)

        ent_name_file = tkinter.Entry(self.window, width=10, textvariable=self.name_file)
        ent_name_file.place(x=690, y=20, width=100, height=20)


    def display_additional_solutions(self):
        title = tkinter.Label(self.window, text='Дополнительные решения:', font=("Arial Bold", 15))
        title.place(x=400, y=80, width=300, height=30)

        self.checkbutton_dynamic_programming()
        self.checkbutton_dynamic_programming_with_all_vertices()
        self.checkbutton_brute_force()
        self.checkbutton_ant_algorithm()
        self.checkbutton_annealing_method()
        self.checkbutton_branch_and_bound()

    def display_general_parameters(self):
        """The general parameters(number of vertices, generations and individuals in one generation)
         have been initialized and described here"""

        title = tkinter.Label(self.window, text='Общие параметры:', font=("Arial Bold", 15))
        title.place(x=2, y=75, width=200, height=45)

        self.number_of_vertices()
        self.number_of_generations()
        self.population_size()
        self.measure_of_disorder()
        self.symmetric_adjacency_matrix()

    def display_start_btn(self):
        save_btn = tkinter.Button(self.window, text="Let's goo", bg='white', font=("Arial Bold", 20),
                                  command=self.star_alg)
        save_btn.place(x=425, y=280, width=120, height=50)

    def number_of_vertices(self):
        lab_number_of_vertices = tkinter.Label(self.window, text='Количество городов-', font=("Arial Bold", 14))
        lab_number_of_vertices.place(x=16, y=115, width=200, height=30)

        ent_number_of_cities = tkinter.Entry(self.window, width=10, textvariable=self.value_ent_number_of_vertices)
        ent_number_of_cities.place(x=220, y=116, width=70, height=30)

    def number_of_generations(self):
        lab_number_of_generations = tkinter.Label(self.window, text='Количество поколений-', font=("Arial Bold", 14))
        lab_number_of_generations.place(x=15, y=155, width=220, height=30)

        ent_number_of_gen = tkinter.Entry(self.window, width=10, textvariable=self.value_ent_number_of_generations)
        ent_number_of_gen.place(x=236, y=156, width=70, height=30)

    def population_size(self):
        lab_population_size = tkinter.Label(self.window, text='Количество особей в поколение-', font=("Arial Bold", 14))
        lab_population_size.place(x=16, y=195, width=300, height=30)

        ent_population_size = tkinter.Entry(self.window, width=10, textvariable=self.value_ent_population_size)
        ent_population_size.place(x=320, y=195, width=70, height=30)

    def measure_of_disorder(self):

        lab_measure_of_disorder = tkinter.Label(self.window, text='Коэффициент хаоса -', font=("Arial Bold", 14))
        lab_measure_of_disorder.place(x=17, y=230, width=200, height=30)

        ent_measure_of_disorder = tkinter.Entry(self.window, width=10, textvariable=self.value_ent_measure_of_disorder)
        ent_measure_of_disorder.place(x=220, y=230, width=70, height=30)

    def symmetric_adjacency_matrix(self):

        solo_test = tkinter.Radiobutton(self.window, text='симметричная матрица', value='symmetric_adjacency_matrix',
                                        variable=self.status_of_the_symmetry_adj_matrix,
                                        font=("Arial Bold", 15))
        solo_test.place(x=20, y=270, width=250, height=25)

        comparison = tkinter.Radiobutton(self.window, text='ассиметричная матрица', value='asymmetric_adjacency_matrix',
                                         variable=self.status_of_the_symmetry_adj_matrix,
                                         font=("Arial Bold", 15))
        comparison.place(x=23, y=300, width=250, height=25)

    def checkbutton_dynamic_programming(self):
        checkbutton_dynamic_programming = tkinter.Checkbutton(self.window, text='жадный с одной вершиной',
                                                              font=("Arial Bold", 14),
                                                              variable=self.state_dynamic)
        checkbutton_dynamic_programming.place(x=451, y=113, width=270, height=25)

    def checkbutton_dynamic_programming_with_all_vertices(self):
        checkbutton_dynamic_prog_with_all_vertices = tkinter.Checkbutton(self.window,
                                                                         text='жадный со всеми вершинами',
                                                                         font=("Arial Bold", 14),
                                                                         variable=self.state_dynamic_all_vertices)
        checkbutton_dynamic_prog_with_all_vertices.place(x=438, y=140, width=320, height=35)

    def checkbutton_brute_force(self):
        checkbutton_brute_force = tkinter.Checkbutton(self.window, text='перебором', font=("Arial Bold", 14),
                                                      variable=self.state_brute_force)
        checkbutton_brute_force.place(x=418, y=175, width=200, height=25)

    def checkbutton_ant_algorithm(self):
        checkbutton_brute_force = tkinter.Checkbutton(self.window, text='муравьиный алгоритм', font=("Arial Bold", 14),
                                                      variable=self.state_ant_algorithm)
        checkbutton_brute_force.place(x=456, y=200, width=215, height=23)

    def checkbutton_annealing_method(self):
        checkbutton_brute_force = tkinter.Checkbutton(self.window, text='имитация отжига', font=("Arial Bold", 14),
                                                      variable=self.state_annealing_method)
        checkbutton_brute_force.place(x=433, y=226, width=215, height=23)

    def checkbutton_branch_and_bound(self):
        checkbutton_branch_and_bound = tkinter.Checkbutton(self.window, text='ветвей и границ', font=("Arial Bold", 14),
                                                      variable=self.state_branch_and_bound)
        checkbutton_branch_and_bound.place(x=428, y=250, width=215, height=23)

    def safe_settings(self):
        numb_of_ver = self.value_ent_number_of_vertices.get()
        numb_of_gen = self.value_ent_number_of_generations.get()
        pop_size = self.value_ent_population_size.get()
        meas_of_dis = self.value_ent_measure_of_disorder.get()

        # есть желание в будущем сделать функцию проверки и задокументировать ее
        if meas_of_dis.isdigit() and int(meas_of_dis) % 2 == 1:
            tkinter.messagebox.showerror("Неправильный формат для ввода данных",
                                         f'Параметр коэффициент хаоса(meas_of_dis должен быть четным')
        if numb_of_ver.isdigit() and numb_of_gen.isdigit() and pop_size.isdigit():
            if int(numb_of_ver) <= 100 or self.status_of_generation_adjacency_matrix.get() == 'download_from_a_file':
                settings = (('state_mode', self.comparison_status.get()),
                            ('status_of_generation_adjacency_matrix', self.status_of_generation_adjacency_matrix.get()),
                            ('state_dynamic', self.state_dynamic.get()),
                            ('state_dynamic_all_vertices', self.state_dynamic_all_vertices.get()),
                            ('state_brute_force', self.state_brute_force.get()),
                            ('state_ant_algorithm', self.state_ant_algorithm.get()),
                            ('state_annealing_method', self.state_annealing_method.get()),
                            ('state_branch_and_bound', self.state_branch_and_bound.get()),
                            ('status_of_the_symmetry_adjacency_matrix', self.status_of_the_symmetry_adj_matrix.get()),
                            ('number_of_vertices', int(numb_of_ver)),
                            ('number_of_generations', int(numb_of_gen)),
                            ('population_size', int(pop_size)), ('measure_of_disorder', int(meas_of_dis)),
                            ('name_file', self.name_file.get())
                            )
                self.algorithm_parameters.update(settings)
            else:
                tkinter.messagebox.showerror("Ошибка", "Количество городов не может быть больше 100")
        else:
            tkinter.messagebox.showerror("Ошибка", "Неправильный формат для ввода данных")

    def get_algorithm_parameters(self):
        self.safe_settings()
        return self.algorithm_parameters

    def get_settings_mandatory_alg(self):
        self.safe_settings()
        return self.window_mandatory_alg.get_parameters()

    def get_settings_additional_alg(self):
        self.safe_settings()
        if self.comparison_status.get() == 'comparison':
            return self.window_additional_alg.get_parameters()
        else:
            return None

    def get_settings_comparison_alg(self):
        self.safe_settings()
        if self.comparison_status.get() == 'comparison':
            return self.window_comparison.get_parameters()
        else:
            return None

    def swap_mode(self):
        if self.comparison_status.get() == 'comparison':
            self.window_additional_alg.deiconify()
            self.window_comparison.deiconify()
            # self.value_ent_assemblies_number.set('2')

        if self.comparison_status.get() == 'solo_test':
            self.window_additional_alg.withdraw()
            self.window_comparison.withdraw()
            # self.value_ent_assemblies_number.set('1')

    # def create_new_algorithm(self):
    #     window_additional_alg = AlgorithmWindow(f'Алгоритм номер {len(self.array_of_algorithms) + 1}', place="+500+380")
    #     window_additional_alg.basic_parameters()
    #     return window_additional_alg
    # def on_assemblies_number_change(self, *args):
    #     print(self.value_ent_assemblies_number.get())
    #
    #     if len(self.array_of_algorithms) < int(self.value_ent_assemblies_number.get()):
    #
    #         while len(self.array_of_algorithms) != int(self.value_ent_assemblies_number.get()):
    #             self.array_of_algorithms.append(self.create_new_algorithm())
    #
    #     if len(self.array_of_algorithms) > int(self.value_ent_assemblies_number.get()):
    #         while len(self.array_of_algorithms) != int(self.value_ent_assemblies_number.get()):
    #             self.array_of_algorithms.pop()
    #
    #     print(self.array_of_algorithms)



