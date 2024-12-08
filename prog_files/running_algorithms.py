from prog_files.CreateMainWindow import MainWindow
import tkinter.messagebox
import SoloTest
from prog_files.Comparison import Comparison
import matplotlib.pyplot as plt

class RunningAlgorithm:

    def __init__(self):
        self.settings_mandatory_alg = None
        self.settings_additional_alg = None
        self.general_settings = None
        self.settings_comparison_alg = None

        self.window = MainWindow(self.star_alg)
        self.window.create_main_window()

    def star_alg(self):
        self.save_settings()
        state_mode = self.general_settings['state_mode']
        if state_mode == 'solo_test':
            solution = SoloTest.Solution(self.general_settings, self.settings_mandatory_alg)
            solution.start_solving()
            solution.display()
        elif state_mode == 'comparison':
            comparison = Comparison(self.general_settings, self.settings_mandatory_alg,
                                    self.settings_additional_alg, self.settings_comparison_alg)
            comparison.start_comparison()
            comparison.output_time_to_console()
            comparison.output_deviation_to_console()
            comparison.visualization_progression()
            comparison.visualization_deviation()

        else:
            tkinter.messagebox.showerror("Ошибка", "Неизвестное значение 'settings['state_mode']' класса 'MainWindow'")
        plt.show()

    def save_settings(self):
        self.settings_mandatory_alg = self.window.get_settings_mandatory_alg()
        self.settings_additional_alg = self.window.get_settings_additional_alg()
        self.general_settings = self.window.get_algorithm_parameters()
        self.settings_comparison_alg = self.window.get_settings_comparison_alg()


if __name__ == "__main__":
    lo = RunningAlgorithm()
