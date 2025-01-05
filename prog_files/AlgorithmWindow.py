import tkinter
import tkinter.messagebox
import tkinter.ttk


class AlgorithmWindow:

    def __init__(self, name_window, place):
        self.window = tkinter.Toplevel()
        self.window.geometry('500x350' + place)
        self.window.title(name_window)
        self.window.resizable(width=False, height=False)

        settings = ('crossing_method', 'mutation_method', 'selection_method', 'status_of_searching_parent',
                    'method_of_generation_start_population', 'state_surfing', 'state_family_resemblance_analysis')
        self.parameters = dict.fromkeys(settings)

        self.status_of_searching_parent = tkinter.StringVar(value='random_search')

        self.method_of_generation_start_population = tkinter.StringVar(value='random_gen')
        self.state_surfing = tkinter.StringVar(value='none_surf')
        self.state_family_resemblance_analysis = tkinter.BooleanVar(value=False)

        self.crossing_methods = ('crossing_pass', 'two_point_crossing', 'orderly_crossing_OX1',
                                 'one_point_crossing_OX1', 'crossover_ordered_ss', 'cycle_crossover',
                                 'crossover_order_bb', 'crossover_order_OX5', 'crossover_order_OX1_upgrade',
                                 'crossover_ordered_ox_s', 'crossover_ordered_ox_b', 'partially_matched_crossover',
                                 'one_point_crossing_bb', 'greedy_crossover', 'crossover_order_OX5_upgrade')
        self.value_crossing_methods = tkinter.StringVar(value=self.crossing_methods[1])

        self.mutation_methods = ('mutation_pass', 'mutation_turning_180_g', 'mutation_by_exchange',
                                 'mutation_by_shuffling', 'mutations_with_probability',
                                 'module_based_mutation', 'm2_based_mutation')
        self.value_mutation_methods = tkinter.StringVar(value=self.mutation_methods[0])

        self.selection_methods = ('selection_of_the_best', 'roulette_selection', 'tournament_with_parent',
                                  'random_tournament_selection')
        self.value_selection_methods = tkinter.StringVar(value=self.selection_methods[0])

    def basic_parameters(self):
        lab = tkinter.Label(self.window, text='Обязательные параметры:', font=("Arial Bold", 15))
        lab.place(x=8, y=10, width=250, height=30)

        self.display_crossing_methods()
        self.display_mutation_methods()
        self.display_selection_methods()
        self.gene_surfing_status()
        self.display_status_of_searching_parent()
        self.display_family_resemblance_analysis()

        self.display_method_of_generation_start_population()

    def display_family_resemblance_analysis(self):
        checkbutton = tkinter.Checkbutton(self.window, text='аналитика семейного\n сходства', font=("Arial Bold", 13),
                                          variable=self.state_family_resemblance_analysis)
        checkbutton.place(x=260, y=7, width=215, height=35)

    def gene_surfing_status(self):
        # checkbutton = tkinter.Checkbutton(self.window, text='сёрфинг ген', font=("Arial Bold", 14),
        #                                   variable=self.state_surfing)
        # checkbutton.place(x=10, y=300, width=150, height=25)

        lab = tkinter.Label(self.window, text='Параметры серфинга:', font=("Arial Bold", 14))
        lab.place(x=10, y=290, width=200, height=25)

        none_surf = tkinter.Radiobutton(self.window, text='нету', value='none_surf',
                                        variable=self.state_surfing, font=("Arial Bold", 14))
        none_surf.place(x=215, y=295, width=60, height=18)

        none_surf = tkinter.Radiobutton(self.window, text='сёрф всей популяции', value='surf_all_pop',
                                        variable=self.state_surfing, font=("Arial Bold", 14))
        none_surf.place(x=275, y=295, width=230, height=18)

        none_surf = tkinter.Radiobutton(self.window, text='случайный', value='random_surf',
                                        variable=self.state_surfing, font=("Arial Bold", 14))
        none_surf.place(x=30, y=315, width=116, height=18)

        none_surf = tkinter.Radiobutton(self.window, text='случайный_2', value='random_surf_on_random_val',
                                        variable=self.state_surfing, font=("Arial Bold", 14))
        none_surf.place(x=170, y=315, width=145, height=21)

        none_surf = tkinter.Radiobutton(self.window, text='по четности', value='even_surf',
                                        variable=self.state_surfing, font=("Arial Bold", 14))
        none_surf.place(x=320, y=315, width=130, height=21)

    def display_method_of_generation_start_population(self):
        lab = tkinter.Label(self.window, text='Метод генерации первого поколения:', font=("Arial Bold", 15))
        lab.place(x=40, y=195, width=350, height=20)

        random_gen = tkinter.Radiobutton(self.window, text='случайно', value='random_gen',
                                         variable=self.method_of_generation_start_population, font=("Arial Bold", 15))
        random_gen.place(x=40, y=217, width=120, height=20)

        ordered_gen = tkinter.Radiobutton(self.window, text='последовательно', value='ordered_gen',
                                          variable=self.method_of_generation_start_population,
                                          font=("Arial Bold", 15))
        ordered_gen.place(x=170, y=217, width=190, height=25)

        greedy_algorithm_gen = tkinter.Radiobutton(self.window, text='на основе жадного алгоритма',
                                                   value='greedy_algorithm_gen',
                                                   variable=self.method_of_generation_start_population,
                                                   font=("Arial Bold", 15))
        greedy_algorithm_gen.place(x=44, y=240, width=300, height=25)

        greedy_algorithm_gen = tkinter.Radiobutton(self.window, text='муравьиный алгоритм',
                                                   value='ant_algorithm_gen',
                                                   variable=self.method_of_generation_start_population,
                                                   font=("Arial Bold", 15))
        greedy_algorithm_gen.place(x=9, y=270, width=300, height=17)

    def display_status_of_searching_parent(self):
        lab = tkinter.Label(self.window, text='Статус поиска родителей:', font=("Arial Bold", 15))
        lab.place(x=40, y=145, width=240, height=25)

        random_search = tkinter.Radiobutton(self.window, text='случайный', value='random_search',
                                            variable=self.status_of_searching_parent, font=("Arial Bold", 15))
        random_search.place(x=290, y=147, width=120, height=20)

        ordered_search = tkinter.Radiobutton(self.window, text='упорядоченный', value='ordered_search',
                                             variable=self.status_of_searching_parent, font=("Arial Bold", 15))
        ordered_search.place(x=288, y=167, width=170, height=25)

    def display_crossing_methods(self):
        lab_crossing_methods = tkinter.Label(self.window, text='Метод скрещивания -', font=("Arial Bold", 15))
        lab_crossing_methods.place(x=15, y=43, width=250, height=30)

        combobox_crossing_methods = tkinter.ttk.Combobox(self.window, font=("Arial Bold", 11),
                                                         textvariable=self.value_crossing_methods,
                                                         values=self.crossing_methods)
        combobox_crossing_methods.place(x=244, y=45, width=220, height=30)

    def display_mutation_methods(self):
        lab_mutation_methods = tkinter.Label(self.window, text='Метод мутации    -', font=("Arial Bold", 15))
        lab_mutation_methods.place(x=2, y=76, width=250, height=30)

        combobox_mutation_methods = tkinter.ttk.Combobox(self.window, font=("Arial Bold", 11),
                                                         textvariable=self.value_mutation_methods,
                                                         values=self.mutation_methods)
        combobox_mutation_methods.place(x=244, y=79, width=220, height=30)

    def display_selection_methods(self):
        lab_selection_methods = tkinter.Label(self.window, text='Метод отбора     -', font=("Arial Bold", 15))
        lab_selection_methods.place(x=0, y=109, width=250, height=30)

        combobox_display_selection_methods = tkinter.ttk.Combobox(self.window, font=("Arial Bold", 11),
                                                                  textvariable=self.value_selection_methods,
                                                                  values=self.selection_methods)
        combobox_display_selection_methods.place(x=244, y=111, width=220, height=30)

    def get_parameters(self):
        self.parameters['crossing_method'] = self.value_crossing_methods.get()
        self.parameters['mutation_method'] = self.value_mutation_methods.get()
        self.parameters['selection_method'] = self.value_selection_methods.get()
        self.parameters['status_of_searching_parent'] = self.status_of_searching_parent.get()
        self.parameters['method_of_generation_start_population'] = self.method_of_generation_start_population.get()
        self.parameters['state_surfing'] = self.state_surfing.get()
        self.parameters['state_family_resemblance_analysis'] = self.state_family_resemblance_analysis.get()

        return self.parameters

    def deiconify(self):
        self.window.deiconify()

    def withdraw(self):
        self.window.withdraw()
