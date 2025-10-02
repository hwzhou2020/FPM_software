import scipy.io
import mat73
import os

from PySide6.QtWidgets import QFileDialog, QApplication


def load_mat_file(parent):
    """Opens a file dialog to select and load a .mat file, then displays messages in Msg_window."""
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    start_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.isdir(start_dir):
        start_dir = os.getcwd()

    dialog = QFileDialog(parent, "Select a .mat file", start_dir, "MAT Files (*.mat);;All Files (*.*)")
    dialog.setOptions(options)
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setAcceptMode(QFileDialog.AcceptOpen)

    app = QApplication.instance()
    if app is not None:
        dialog.setPalette(app.palette())
        if app.styleSheet():
            dialog.setStyleSheet(app.styleSheet())

    if dialog.exec() == QFileDialog.Accepted:
        file_path = dialog.selectedFiles()[0]
    else:
        parent.ui.Msg_window.appendPlainText("No file selected.")
        return None

    # Store the file path for recent files
    parent.current_file_path = file_path
    parent.ui.Msg_window.appendPlainText(f"Loading file: {os.path.basename(file_path)}")

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
