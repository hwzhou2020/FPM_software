from PySide6 import QtWidgets
from File_ui import Ui_MainWindow  # Import UI class
from Utilities.UIfunctions import open_file_dialog, load_mat_file, log_message  # Import new function

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.filebrowse.clicked.connect(lambda: open_file_dialog(self))  # Open file dialog
        self.ui.LoadData.clicked.connect(lambda: self.load_data())  # Load .mat file

    def load_data(self):
        """Load the .mat file and store the data."""
        self.mat_data = load_mat_file(self)  # Store loaded data in an attribute
        if self.mat_data:
            log_message(self.ui, "MAT file data loaded successfully.")  # Log success message

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

# (freqXY_calib-[xc,yc])*lambda = dpix_c / mag * ROIlength *NA_list
# 1/lambda*na_cal/(1/(imsize*dpix_c/mag)) = na_rp_cal