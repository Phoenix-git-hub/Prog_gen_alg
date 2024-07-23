import tkinter
import tkinter.messagebox
import tkinter.ttk


class WindowComparison:

    def __init__(self):
        self.name_window = "Окно сравнения(дополнительное)"

        self.window = tkinter.Toplevel()
        self.window.geometry('330x200+800+0')
        self.window.title(self.name_window)
        self.window.resizable(width=False, height=False)

        settings = ('number_of_comparisons', 'generation_of_the_starting_population')

        self.parameters = dict.fromkeys(settings)

        self.val_ent_number_of_comparisons = tkinter.StringVar(value='20')
        self.val_generation_of_the_start_population = tkinter.StringVar(value='random_selection')

    def basic_parameters(self):
        self.number_of_comparisons()
        self.generation_of_the_starting_population()

    def number_of_comparisons(self):
        lab_number_of_comparisons = tkinter.Label(self.window, text='Количество сравнений   -', font=("Arial Bold", 14))
        lab_number_of_comparisons.place(x=0, y=10, width=240, height=30)

        ent_number_of_comparisons = tkinter.Entry(self.window, width=10,
                                                  textvariable=self.val_ent_number_of_comparisons)
        ent_number_of_comparisons.place(x=248, y=12, width=60, height=30)

    def generation_of_the_starting_population(self):
        lab = tkinter.Label(self.window, text='Генерация первого поколения ', font=("Arial Bold", 15))
        lab.place(x=10, y=50, width=280, height=60)

        random_selection = tkinter.Radiobutton(self.window, text='Случайным отбором',
                                               value='random_selection',
                                               variable=self.val_generation_of_the_start_population,
                                               font=("Arial Bold", 15))
        random_selection.place(x=0, y=110, width=250, height=30)

        in_ascending_order = tkinter.Radiobutton(self.window, text='В порядке возрастания', value='in_ascending_order',
                                                 variable=self.val_generation_of_the_start_population,
                                                 font=("Arial Bold", 15))
        in_ascending_order.place(x=13, y=140, width=250, height=30)

    def get_parameters(self):

        if self.val_ent_number_of_comparisons.get().isdigit():
            self.parameters['number_of_comparisons'] = int(self.val_ent_number_of_comparisons.get())
        else:
            tkinter.messagebox.showerror("Ошибка", "Неправильный формат для ввода данных")
        self.parameters['generation_of_the_starting_population'] = self.val_generation_of_the_start_population.get()

        return self.parameters

    def deiconify(self):
        self.window.deiconify()

    def withdraw(self):
        self.window.withdraw()
