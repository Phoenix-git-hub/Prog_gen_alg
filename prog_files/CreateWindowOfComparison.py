import tkinter
import tkinter.messagebox
import tkinter.ttk


class WindowComparison:

    def __init__(self):
        self.name_window = "Окно сравнения(дополнительное)"

        self.window = tkinter.Toplevel()
        self.window.geometry('330x90+800+0')
        self.window.title(self.name_window)
        self.window.resizable(width=False, height=False)

        settings = ('number_of_comparisons')

        self.parameters = dict.fromkeys(settings)

        self.val_ent_number_of_comparisons = tkinter.StringVar(value='5')

    def basic_parameters(self):
        self.number_of_comparisons()

    def number_of_comparisons(self):
        lab_number_of_comparisons = tkinter.Label(self.window, text='Количество сравнений   -', font=("Arial Bold", 14))
        lab_number_of_comparisons.place(x=0, y=10, width=240, height=30)

        ent_number_of_comparisons = tkinter.Entry(self.window, width=10,
                                                  textvariable=self.val_ent_number_of_comparisons)
        ent_number_of_comparisons.place(x=248, y=12, width=60, height=30)

    def get_parameters(self):

        if self.val_ent_number_of_comparisons.get().isdigit():
            self.parameters['number_of_comparisons'] = int(self.val_ent_number_of_comparisons.get())
        else:
            tkinter.messagebox.showerror("Ошибка", "Неправильный формат для ввода данных")

        return self.parameters

    def deiconify(self):
        self.window.deiconify()

    def withdraw(self):
        self.window.withdraw()
