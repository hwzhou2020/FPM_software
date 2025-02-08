import os
import scipy.io
import mat73
import numpy as np
from .logging_utils import log_message
from PySide6.QtWidgets import QFileDialog


def open_file_dialog(main_window):
    """Open a file dialog to select a .mat file."""
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(
        main_window, "Open File", "", "MAT Files (*.mat);;All Files (*)", options=options
    )

    if file_name:
        main_window.ui.DataPath.setText(file_name)
        log_message(main_window.ui, f"Selected file: {os.path.basename(file_name)}")  # Display filename only


def load_mat_file(main_window):
    """Load .mat file based on its version (supports both v7.3 and earlier versions)."""
    file_path = main_window.ui.DataPath.text()

    if not os.path.exists(file_path):
        log_message(main_window.ui, "Error: File not found! Please select a valid .mat file.")
        return None

    file_name = os.path.basename(file_path)
    log_message(main_window.ui, f"Start loading .mat data: {file_name}")

    try:
        data = scipy.io.loadmat(file_path)
        log_message(main_window.ui, f"MAT file '{file_name}' loaded successfully (scipy.io).")
    except NotImplementedError:
        try:
            data = mat73.loadmat(file_path)
            log_message(main_window.ui, f"MAT file '{file_name}' loaded successfully (mat73).")
        except Exception as e:
            log_message(main_window.ui, f"Error: Failed to load MAT file '{file_name}': {str(e)}")
            return None

    required_keys = ['mag', 'NA', 'NA_list', 'lambda', 'dpix_c', 'imlow']
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        log_message(main_window.ui, f"Error: Missing keys in MAT file: {', '.join(missing_keys)}")
        return None

    mag = float(data['mag'].item()) if isinstance(data['mag'], np.ndarray) else data['mag']
    NA = float(data['NA'].item()) if isinstance(data['NA'], np.ndarray) else data['NA']
    lambda_ = float(data['lambda'].item()) if isinstance(data['lambda'], np.ndarray) else data['lambda']
    dpix_c = float(data['dpix_c'].item()) if isinstance(data['dpix_c'], np.ndarray) else data['dpix_c']
    NA_list = data['NA_list']
    imlow = data['imlow']

    if not isinstance(imlow, np.ndarray) or imlow.ndim != 3:
        log_message(main_window.ui, "Error: 'imlow' should be a 3D NumPy array.")
        return None

    return data, mag, NA, lambda_, dpix_c, NA_list, imlow
