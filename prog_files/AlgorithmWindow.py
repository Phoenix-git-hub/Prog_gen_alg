import tkinter
import tkinter.messagebox
import tkinter.ttk


class AlgorithmWindow:

    def __init__(self, name_window, place):
        self.window = tkinter.Toplevel()
        self.window.geometry('500x300' + place)
        self.window.title(name_window)
        self.window.resizable(width=False, height=False)

        settings = ('crossing_method', 'mutation_method', 'selection_method', 'status_of_searching_parent')
        self.parameters = dict.fromkeys(settings)

        self.status_of_searching_parent = tkinter.StringVar(value='random_search')

        self.crossing_methods = ('crossing_pass', 'two_point_crossing', 'orderly_crossing_OX1',
                                 'one_point_crossing_OX1', 'displayed_crossing', 'cycle_crossover',
                                 'crossover_order_OX', 'crossover_order_OX5')
        self.value_crossing_methods = tkinter.StringVar(value=self.crossing_methods[1])

        self.mutation_methods = ('mutation_pass', 'mutation_turning_180_g', 'mutation_by_exchange',
                                 'mutation_by_shuffling')
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
        self.display_status_of_searching_parent()



    def display_status_of_searching_parent(self):
        lab = tkinter.Label(self.window, text='Статус поиска родителей:', font=("Arial Bold", 15))
        lab.place(x=40, y=145, width=240, height=20)

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

        return self.parameters

    def deiconify(self):
        self.window.deiconify()

    def withdraw(self):
        self.window.withdraw()
