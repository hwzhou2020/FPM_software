import scipy.io
import mat73
import os

from PySide6.QtWidgets import QFileDialog


def load_mat_file(parent):
    """Opens a file dialog to select and load a .mat file, then displays messages in Msg_window."""
    file_path, _ = QFileDialog.getOpenFileName(parent, "Select a .mat file", "", "MAT Files (*.mat);;All Files (*.*)")

    if not file_path:
        parent.ui.Msg_window.appendPlainText("No file selected.")
        return None

    parent.ui.Msg_window.appendPlainText(f"Loading file: {file_path}")

    try:
        # Attempt to read with scipy.io (works for v7 and older .mat files)
        data = scipy.io.loadmat(file_path)
        parent.ui.Msg_window.appendPlainText("File loaded successfully using scipy.io.")
    except NotImplementedError:
        # If scipy.io fails, try using mat73 (works for v7.3 files)
        try:
            data = mat73.loadmat(file_path)
            parent.ui.Msg_window.appendPlainText("File loaded successfully using mat73.")
        except Exception as e:
            parent.ui.Msg_window.appendPlainText(f"Failed to load .mat file: {e}")
            return None

    parent.ui.Msg_window.appendPlainText("Data successfully loaded into memory.")
    return data  # Returns the loaded dictionary for further processing
