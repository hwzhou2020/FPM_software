import os
import yaml
import webbrowser
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QColor, QAction, QIcon
from Main_ui import Ui_FPMSoftware
from Utilities.data_handler import load_mat_file
from Utilities.display_handler import (
    display_single_raw_frame,
    display_all_raw_frames,
    display_single_raw_spectrum,
    display_all_raw_spectra,
    display_single_roi_image,
    display_all_roi_images,
)
from Utilities.message_handler import export_messages, clear_messages
from Utilities.logging_utils import log_message
from Utilities.interactive_view import ZoomableGraphicsView
from Utilities.roi_handler import select_roi_size
from Utilities.system_specs_window import SystemSpecsWindow  
from Utilities.parameter_dialog import ParameterDialog  
from WindowUI.DisplayOptionsWindow import DisplayOptionsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FPMSoftware()
        self.ui.setupUi(self)
        self.setWindowTitle("FPM Software")
        self.setWindowIcon(QIcon("icons/FPM_icon.png"))
        doc_path = os.path.abspath("docs_package/build/html/index.html")
        self.ui.actionSoftware_Guide.triggered.connect(lambda: webbrowser.open(f"file://{doc_path}"))


        self.mat_data = None  # Initialize data storage
        self.system_specs_window = None  # Initialize system specs window

        # **ROI parameters (Default ROI: [X-offset, Y-offset, ROI_size, ROI_size])**
        self.roi_params = {"x_offset": 1, "y_offset": 1, "roi_size": 256}

        # **Scan for algorithm subfolders dynamically**
        self.algorithm_directory = "Algorithms"  # Directory where algorithms are stored
        self.algorithms = self.detect_algorithms()  # Automatically fetch algorithms

        # Replace default QGraphicsView with interactive view
        self.ui.display_window = ZoomableGraphicsView(self.ui.centralwidget)
        border_color = QColor(255, 255, 255)  # White border
        self.ui.display_window.setStyleSheet(f"border: 1px solid rgb({border_color.red()}, {border_color.green()}, {border_color.blue()});")
        self.ui.display_window.show()

        self.ui.gridLayout_3.addWidget(self.ui.display_window, 0, 0, 1, 1)

        # Connect buttons and menu actions to functions
        self.ui.load_butt.clicked.connect(self.load_data)
        self.ui.actionLoad_Data.triggered.connect(self.load_data)
        self.ui.actionSave_Messgaes.triggered.connect(self.export_messages)
        self.ui.actionClear_Messages.triggered.connect(self.clear_messages)
        self.ui.actionSystem_specs.triggered.connect(self.show_system_specs)
        self.ui.actionSIngle_ROI.triggered.connect(self.show_single_roi_image)
        self.ui.actionAll_ROI_images.triggered.connect(self.show_all_roi_images)
        self.ui.run_butt.clicked.connect(self.run_selected_algorithm)
        self.ui.display_butt.clicked.connect(self.show_display_options)
        self.ui.actionSoftware_Guide = QAction("Software Guide", self)
        self.ui.menuHelp.addAction(self.ui.actionSoftware_Guide)


        # Connect ROI selection button
        self.ui.roi_butt.clicked.connect(lambda: select_roi_size(self))

        # Ensure algorithm menu items are checkable
        self.ui.actionGerchberg_Saxton.setCheckable(True)
        self.ui.actionEPRY.setCheckable(True)
        self.ui.actionGauss_Newton.setCheckable(True)
        self.ui.actionKramers_Kronig.setCheckable(True)
        self.ui.actionAPIC.setCheckable(True)

        # Dynamically populate the algorithm menu
        self.algorithm_actions = {}
        self.populate_algorithm_menu()

    def show_display_options(self):
        self.display_options_window = DisplayOptionsWindow(self)
        self.display_options_window.show()

    def load_data(self):
        new_data = load_mat_file(self)
        if new_data:
            self.mat_data = new_data
            self.ui.Msg_window.appendPlainText("New data loaded successfully.")
            if self.system_specs_window:
                self.system_specs_window.load_system_specs()
        else:
            self.ui.Msg_window.appendPlainText("No new data loaded. Retaining previous data.")

    def show_single_raw_frame(self):
        display_single_raw_frame(self)

    def show_all_raw_frames(self):
        display_all_raw_frames(self)

    def show_single_raw_spectrum(self):
        display_single_raw_spectrum(self)

    def show_all_raw_spectra(self):
        display_all_raw_spectra(self)

    def show_single_roi_image(self):
        display_single_roi_image(self)

    def show_all_roi_images(self):
        display_all_roi_images(self)

    def export_messages(self):
        export_messages(self)

    def clear_messages(self):
        clear_messages(self)

    def show_system_specs(self):
        if self.system_specs_window is None:
            self.system_specs_window = SystemSpecsWindow(self)
        if hasattr(self, "roi_params"):
            roi_text = str(self.roi_params)
            self.system_specs_window.update_roi_field(roi_text)
        self.system_specs_window.populate_algorithm_list(self.algorithms)
        self.system_specs_window.load_system_specs()
        self.system_specs_window.show()

    def detect_algorithms(self):
        if not os.path.exists(self.algorithm_directory):
            return []
        return sorted([
            folder for folder in os.listdir(self.algorithm_directory)
            if os.path.isdir(os.path.join(self.algorithm_directory, folder))
        ])

    def populate_algorithm_menu(self):
        menu_algorithms = self.ui.menuAlgorithm_specs
        menu_algorithms.clear()
        for algorithm in self.algorithms:
            shortened_name = algorithm.split(" ")[0]
            action = QAction(shortened_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, alg=algorithm: self.select_algorithm(alg))
            self.algorithm_actions[algorithm] = action
            menu_algorithms.addAction(action)
        if self.algorithms:
            self.selected_algorithm = self.algorithms[0]
            self.algorithm_actions[self.selected_algorithm].setChecked(True)

    def select_algorithm(self, algorithm_name):
        self.selected_algorithm = algorithm_name
        for action in self.algorithm_actions.values():
            action.setChecked(False)
        if algorithm_name in self.algorithm_actions:
            self.algorithm_actions[algorithm_name].setChecked(True)
        self.ui.Msg_window.appendPlainText(f"Algorithm selected: {algorithm_name}")
        if self.system_specs_window:
            self.system_specs_window.update_algorithm_selection(algorithm_name)
        config_path = os.path.join("Algorithms", algorithm_name, "config.yml")
        if os.path.exists(config_path):
            dialog = ParameterDialog(algorithm_name, parent=self)
            dialog.show()

    def load_algorithm_config(self, algorithm_name):
        config_path = os.path.join("Algorithms", algorithm_name, "config.yml")
        if not os.path.exists(config_path):
            return None
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def run_selected_algorithm(self):
        if not self.selected_algorithm:
            log_message(self.ui, "No algorithm selected.")
            return
        try:
            module_path = f"Algorithms.{self.selected_algorithm}.main_alg"
            run_module = __import__(module_path, fromlist=["run_algorithm"])
            run_algorithm = getattr(run_module, "run_algorithm")
            Amp, Phase, Pupil = run_algorithm(
                system_params=self.algorithm_parameters,
                roi_params=self.roi_params,
                mat_data=self.mat_data,
                log_callback=lambda msg: self.ui.Msg_window.appendPlainText(msg)
            )
            log_message(self.ui, f"{self.selected_algorithm} executed successfully.")
            # Store results for display
            self.reconstruction_result = {
                "amplitude": Amp.cpu().numpy() if hasattr(Amp, "cpu") else Amp,
                "phase": Phase.cpu().numpy() if hasattr(Phase, "cpu") else Phase,
                "pupil": Pupil.cpu().numpy() if hasattr(Pupil, "cpu") else Pupil,
            }

        except Exception as e:
            log_message(self.ui, f"Algorithm run failed: {e}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    with open("fancy_dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
