import os
import numpy as np
from PySide6.QtWidgets import QWidget
from WindowUI.SystemSpecsWindow_ui import Ui_SystemSpecsWindow
from Utilities.logging_utils import log_message


def format_scalar(value):
    """Convert single-element arrays/lists to scalars for display."""
    if isinstance(value, np.ndarray) and value.size == 1:
        return str(value.item())  # Convert array to scalar
    elif isinstance(value, list) and len(value) == 1:
        return str(value[0])  # Convert list to scalar
    elif isinstance(value, (int, float)):
        return str(value)  # Already a scalar
    else:
        return "Invalid Data"


class SystemSpecsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_SystemSpecsWindow()
        self.ui.setupUi(self)
        self.main_window = main_window  # Reference to the main window

        # Connect the confirm button to update data
        self.ui.Cfm_sys_butt.clicked.connect(self.confirm_specs)
        

    def load_system_specs(self):
        """Update System Specs UI fields from loaded .mat file data."""
        if self.main_window.mat_data is None:
            log_message(self.main_window.ui, "Error: No data loaded.")
            return

        # Extract values from mat_data safely
        mat_data = self.main_window.mat_data
        self.ui.mag.setText(format_scalar(mat_data.get("mag", "optional")))
        self.ui.NA.setText(format_scalar(mat_data.get("NA", "optional")))
        self.ui.pix_size.setText(format_scalar(mat_data.get("dpix_c", "optional")))
        self.ui.Lambda.setText(format_scalar(mat_data.get("lambda", "optional")))

        # Detect algorithms dynamically from the "Algorithms" folder
        detected_algorithms = self.detect_algorithms()
        self.populate_algorithm_list(detected_algorithms)

        # Validate NA_list and imlow consistency
        if "imlow" not in mat_data or not isinstance(mat_data["imlow"], np.ndarray):
            log_message(self.main_window.ui, "Error: imlow data is missing or corrupted.")
            self.ui.NA_list.setText("Error: imlow missing")
            return

        imlow = mat_data["imlow"]
        na_list = mat_data.get("NA_list", None)

        if isinstance(na_list, np.ndarray) and na_list.shape[0] == imlow.shape[2]:
            self.ui.NA_list.setText("loaded")
            log_message(self.main_window.ui, "NA_list is loaded correctly.")
        else:
            self.ui.NA_list.setText("Error: NA_list is not loaded correctly")
            log_message(self.main_window.ui, "Error: NA_list does not match the number of raw images.")

        # Load ROI values from `roi_params`
        if hasattr(self.main_window, "roi_params"):
            roi_x = self.main_window.roi_params.get("x_offset", 1)
            roi_y = self.main_window.roi_params.get("y_offset", 1)
            roi_size = self.main_window.roi_params.get("roi_size", 256)
            self.ui.ROIsltbox.setText(f"[{roi_x}, {roi_y}, {roi_size}, {roi_size}]")
        else:
            self.ui.ROIsltbox.setText("[1,1,256,256]")  # Default if no ROI is set  

    def detect_algorithms(self):
        """Scans the 'Algorithms' directory for subfolders and returns a sorted list of names."""
        algorithm_directory = "Algorithms"  # Path to the algorithm folder

        if not os.path.exists(algorithm_directory):
            return []
        
        return sorted(
            [
                folder for folder in os.listdir(algorithm_directory)
                if os.path.isdir(os.path.join(algorithm_directory, folder))
            ]
        )

    def populate_algorithm_list(self, algorithms):
        """Dynamically populate the algorithm combo box."""
        self.ui.AlgcomboBox.clear()
        self.ui.AlgcomboBox.addItems(algorithms)

        # Set the currently selected algorithm from main window
        if hasattr(self.main_window, "selected_algorithm"):
            index = self.ui.AlgcomboBox.findText(self.main_window.selected_algorithm)
            if index >= 0:
                self.ui.AlgcomboBox.setCurrentIndex(index)

    def update_algorithm_selection(self, algorithm_name):
        """Update algorithm selection in the combo box."""
        index = self.ui.AlgcomboBox.findText(algorithm_name)
        if index >= 0:
            self.ui.AlgcomboBox.setCurrentIndex(index)

    def update_roi_field(self, roi_text):
        """Updates the ROI selection field when the ROI is changed."""
        self.ui.ROIsltbox.setText(roi_text)

    def confirm_specs(self):
        """Update loaded .mat file data with values from UI fields and update menu tick."""
        if self.main_window.mat_data is None:
            log_message(self.main_window.ui, "Error: No data to update.")
            return

        # Update system specifications in `mat_data`
        self.main_window.mat_data["magnification"] = self.ui.mag.text()
        self.main_window.mat_data["NA"] = self.ui.NA.text()
        self.main_window.mat_data["pixel_size"] = self.ui.pix_size.text()
        self.main_window.mat_data["wavelength"] = self.ui.Lambda.text()

        # Update selected algorithm
        selected_algorithm = self.ui.AlgcomboBox.currentText()
        self.main_window.mat_data["algorithm"] = selected_algorithm
        self.main_window.select_algorithm(selected_algorithm)  # Update Main UI tick

        # Ensure `roi_params` is a dictionary before updating
        if not isinstance(self.main_window.roi_params, dict):
            self.main_window.roi_params = {"x_offset": 1, "y_offset": 1, "roi_size": 256}

        # Update ROI selection using `roi_params`
        try:
            roi_values = [int(i) for i in self.ui.ROIsltbox.text().strip("[]").split(",")]
            if len(roi_values) == 4:
                self.main_window.roi_params["x_offset"] = roi_values[0]
                self.main_window.roi_params["y_offset"] = roi_values[1]
                self.main_window.roi_params["roi_size"] = roi_values[2]
                log_message(self.main_window.ui, f"Updated ROI to {roi_values}")
            else:
                log_message(self.main_window.ui, "Error: Invalid ROI format.")
        except ValueError:
            log_message(self.main_window.ui, "Error: Invalid ROI input.")

        log_message(self.main_window.ui, "System specifications updated.")
        self.close()  # Close window after confirmation
