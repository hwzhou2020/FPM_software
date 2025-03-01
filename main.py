from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QColor, QAction
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
from Utilities.system_specs_window import SystemSpecsWindow  # Import the System Specs window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FPMSoftware()
        self.ui.setupUi(self)

        self.mat_data = None  # Initialize data storage
        self.system_specs_window = None  # Initialize system specs window

        # **ROI parameters (Default ROI: [X-offset, Y-offset, ROI_size, ROI_size])**
        self.roi_params = {"x_offset": 1, "y_offset": 1, "roi_size": 256}


        # Define available algorithms (Easily expandable)
        self.algorithms = [
            "Gerchberg-Saxton",
            "EPRY Embedded pupil function recovery",
            "Gauss-Newton",
            "KK Kramers-Kronig relation",
            "APIC Angular Ptychographic Imaging with Closed-form method"
        ]


        # Replace default QGraphicsView with interactive view
        self.ui.display_window = ZoomableGraphicsView(self.ui.centralwidget)
        border_color = QColor(255, 255, 255)  # White border
        self.ui.display_window.setStyleSheet(f"border: 1px solid rgb({border_color.red()}, {border_color.green()}, {border_color.blue()});")
        self.ui.display_window.show()
        
        self.ui.gridLayout_3.addWidget(self.ui.display_window, 0, 0, 1, 1)

        # Connect buttons and menu actions to functions
        self.ui.load_butt.clicked.connect(self.load_data)
        self.ui.actionLoad_Data.triggered.connect(self.load_data)
        self.ui.actionShow_single_raw_frame.triggered.connect(self.show_single_raw_frame)
        self.ui.actionShow_all_raw_frames.triggered.connect(self.show_all_raw_frames)
        self.ui.actionSingle_raw_spectrum.triggered.connect(self.show_single_raw_spectrum)
        self.ui.actionAll_raw_spectrum.triggered.connect(self.show_all_raw_spectra)
        self.ui.actionSave_Messgaes.triggered.connect(self.export_messages)
        self.ui.actionClear_Messages.triggered.connect(self.clear_messages)
        self.ui.actionSystem_specs.triggered.connect(self.show_system_specs)  # Link to System Specs
        self.ui.actionSIngle_ROI.triggered.connect(self.show_single_roi_image)  # Single ROI frame
        self.ui.actionAll_ROI_images.triggered.connect(self.show_all_roi_images)  # All ROI frames

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

    def load_data(self):
        """Loads a .mat file and updates System Specs UI fields."""
        new_data = load_mat_file(self)  # Attempt to load a new file

        if new_data:
            self.mat_data = new_data
            self.ui.Msg_window.appendPlainText("New data loaded successfully.")

            # If the System Specs window exists, update values
            if self.system_specs_window:
                self.system_specs_window.load_system_specs()
        else:
            self.ui.Msg_window.appendPlainText("No new data loaded. Retaining previous data.")

    def show_single_raw_frame(self):
        """Calls the function to display a single raw frame."""
        display_single_raw_frame(self)

    def show_all_raw_frames(self):
        """Calls the function to display all raw frames."""
        display_all_raw_frames(self)

    def show_single_raw_spectrum(self):
        """Calls the function to display a single raw spectrum."""
        display_single_raw_spectrum(self)

    def show_all_raw_spectra(self):
        """Calls the function to display all raw spectra."""
        display_all_raw_spectra(self)

    def show_single_roi_image(self):
        """Displays a single ROI frame."""
        display_single_roi_image(self)

    def show_all_roi_images(self):
        """Displays all ROI frames sequentially."""
        display_all_roi_images(self)

    def export_messages(self):
        """Calls the function to export messages."""
        export_messages(self)

    def clear_messages(self):
        """Calls the function to clear messages."""
        clear_messages(self)

    def show_system_specs(self):
        """Opens the System Specs window and updates values."""
        if self.system_specs_window is None:
            self.system_specs_window = SystemSpecsWindow(self)

        # Update System Specs UI with current ROI values
        if hasattr(self, "roi_params"):
            roi_text = str(self.roi_params)
            self.system_specs_window.update_roi_field(roi_text)

        self.system_specs_window.load_system_specs()
        self.system_specs_window.show()


    def populate_algorithm_menu(self):
        """Dynamically populate the algorithm selection menu."""
        menu_algorithms = self.ui.menuAlgorithm_specs
        menu_algorithms.clear()  # Clear existing menu items

        for algorithm in self.algorithms:
            action = QAction(algorithm, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, alg=algorithm: self.select_algorithm(alg))
            self.algorithm_actions[algorithm] = action
            menu_algorithms.addAction(action)

        # Default selection
        self.selected_algorithm = self.algorithms[0]
        self.algorithm_actions[self.selected_algorithm].setChecked(True)

    def select_algorithm(self, algorithm_name):
        """Updates the selected algorithm and sets a tick in the menu bar."""
        self.selected_algorithm = algorithm_name

        # Clear all previous checks
        for action in self.algorithm_actions.values():
            action.setChecked(False)

        # Set the tick for the selected algorithm
        if algorithm_name in self.algorithm_actions:
            self.algorithm_actions[algorithm_name].setChecked(True)

        self.ui.Msg_window.appendPlainText(f"Algorithm selected: {algorithm_name}")

        # Update algorithm selection in system specs window if open
        if self.system_specs_window:
            self.system_specs_window.update_algorithm_selection(algorithm_name)

    def show_system_specs(self):
        """Opens the System Specs window and updates values."""
        if self.system_specs_window is None:
            self.system_specs_window = SystemSpecsWindow(self)

        # Update System Specs UI with current ROI values
        if hasattr(self, "roi_params"):
            roi_text = str(self.roi_params)
            self.system_specs_window.update_roi_field(roi_text)

        # Update algorithms dynamically
        self.system_specs_window.populate_algorithm_list(self.algorithms)

        self.system_specs_window.load_system_specs()
        self.system_specs_window.show()

if __name__ == "__main__":
    import sys  # Ensure sys is imported

    app = QApplication(sys.argv)  # Pass system arguments
    window = MainWindow()
    window.show()  # Show the main UI window
    sys.exit(app.exec())  # Start the event loop properly
