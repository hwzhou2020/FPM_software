from PySide6 import QtWidgets
from File_ui import Ui_MainWindow
from Utilities import (
    open_file_dialog, load_mat_file, display_single_raw_image, display_all_raw_images,
    update_ui_fields, set_roi_size, preview_roi_image, preview_roi_sum,
    ZoomableGraphicsView, log_message
)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.imlow = None  # Initialize imlow
        self.roi_size = None  # Initialize ROI size
        self.roi_box = None  # Store ROI reference

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
        self.ui.SetROILen.clicked.connect(lambda: set_roi_size(self))
        self.ui.PreROISig.clicked.connect(lambda: preview_roi_image(self))  
        self.ui.PreROISum.clicked.connect(lambda: preview_roi_sum(self))


    def load_data(self):
        """Load the .mat file and update UI fields."""
        result = load_mat_file(self)
        if result:
            self.mat_data, self.mag, self.NA, self.lambda_, self.dpix_c, self.NA_list, self.imlow = result
            update_ui_fields(self)  # Update UI fields dynamically

    def update_roi_input(self, x, y, width, height):
        """Update the ROI input field after user sets position."""
        roi_text = f"[{x}, {y}, {width}, {height}]"
        self.ui.ROI.setText(roi_text)
        log_message(self.ui, f"ROI selected: {roi_text}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



## notes
# (freqXY_calib-[xc,yc])*lambda = dpix_c / mag * ROIlength *NA_list
# 1/lambda*na_cal/(1/(imsize*dpix_c/mag)) = na_rp_cal