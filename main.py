from PySide6 import QtWidgets
from File_ui import Ui_MainWindow
from Utilities import open_file_dialog, load_mat_file, display_single_raw_image, display_all_raw_images, update_ui_fields, ZoomableGraphicsView



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.imlow = None  # Initialize imlow

        # Replace default graphicsView with ZoomableGraphicsView
        if self.ui.DisplayImage.layout() is None:
            from PySide6.QtWidgets import QVBoxLayout
            self.ui.DisplayImage.setLayout(QVBoxLayout())  # Assign a vertical layout

        self.ui.graphicsView = ZoomableGraphicsView(self)
        self.ui.DisplayImage.layout().addWidget(self.ui.graphicsView)

        # Connect buttons to functions
        self.ui.filebrowse.clicked.connect(lambda: open_file_dialog(self))
        self.ui.LoadData.clicked.connect(self.load_data)
        self.ui.Display1raw.clicked.connect(lambda: display_single_raw_image(self))
        self.ui.Displayallraw.clicked.connect(lambda: display_all_raw_images(self))

    def load_data(self):
        """Load the .mat file and update UI fields."""
        result = load_mat_file(self)
        if result:
            self.mat_data, self.mag, self.NA, self.lambda_, self.dpix_c, self.NA_list, self.imlow = result
            update_ui_fields(self)  # Update UI fields dynamically


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()




## notes
# (freqXY_calib-[xc,yc])*lambda = dpix_c / mag * ROIlength *NA_list
# 1/lambda*na_cal/(1/(imsize*dpix_c/mag)) = na_rp_cal