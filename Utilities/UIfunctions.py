import os
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QGraphicsScene
import scipy.io
import mat73

def log_message(ui, message):
    """Append messages to MsgBox."""
    ui.MsgBox.appendPlainText(message)  # Append new messages to MsgBox


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

    file_name = os.path.basename(file_path)  # Extract filename from path
    log_message(main_window.ui, f"Start loading .mat data: {file_name}")  # Show filename in log

    try:
        # Try loading with scipy.io (supports all versions except v7.3)
        data = scipy.io.loadmat(file_path)
        log_message(main_window.ui, f"MAT file '{file_name}' loaded successfully (scipy.io).")
    except NotImplementedError:
        try:
            # If scipy.io fails, try loading with mat73 (for v7.3 files)
            data = mat73.loadmat(file_path)
            log_message(main_window.ui, f"MAT file '{file_name}' loaded successfully (mat73).")
        except Exception as e:
            log_message(main_window.ui, f"Error: Failed to load MAT file '{file_name}': {str(e)}")
            return None

    return data  # Return the loaded .mat data dictionary
