from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Utilities.display_handler import (
    display_single_raw_frame,
    display_all_raw_frames,
    display_single_raw_spectrum,
    display_all_raw_spectra,
    display_single_roi_image,
    display_all_roi_images,
    display_result_image
)


class DisplayOptionsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Display Options")
        self.setFixedSize(250, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        buttons = [
            ("Single raw frame", lambda: display_single_raw_frame(self.main_window)),
            ("All raw frames", lambda: display_all_raw_frames(self.main_window)),
            ("Single raw spectrum", lambda: display_single_raw_spectrum(self.main_window)),
            ("All raw spectra", lambda: display_all_raw_spectra(self.main_window)),
            ("Single ROI image", lambda: display_single_roi_image(self.main_window)),
            ("All ROI images", lambda: display_all_roi_images(self.main_window)),
            ("Amplitude result", lambda: display_result_image(self.main_window, result_type="amplitude")),
            ("Phase result", lambda: display_result_image(self.main_window, result_type="phase")),
            ("Pupil function", lambda: display_result_image(self.main_window, result_type="pupil")),
        ]

        for label, func in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(func)
            layout.addWidget(btn)

        self.setLayout(layout)
