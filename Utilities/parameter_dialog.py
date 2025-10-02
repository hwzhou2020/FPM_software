import os
import yaml
from PySide6.QtWidgets import (
    QDialog, QGroupBox, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QApplication
)
from PySide6.QtCore import Qt


class ParameterDialog(QDialog):
    def __init__(self, algorithm_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{algorithm_name} Parameters")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.algorithm_name = algorithm_name
        self.config = self.load_config()
        self.param_inputs = {}  # Store QLineEdit widgets for each param

        self.setup_ui()
        self._apply_current_stylesheet()

    def load_config(self):
        config_path = os.path.join("Algorithms", self.algorithm_name, "config.yml")
        if not os.path.exists(config_path):
            QMessageBox.critical(self, "Error", f"Configuration file not found: {config_path}")
            return {}

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.param_box = QGroupBox("Algorithm Parameters")
        param_layout = QVBoxLayout()

        parameters = self.config.get("parameters", {})
        help_texts = self.config.get("help", {})

        for key, info in parameters.items():
            hlayout = QHBoxLayout()
            label = QLabel(info.get("label", key))
            default_val = info.get("default", "")
            edit = QLineEdit(str(default_val))
            tooltip = help_texts.get(key, "")
            if tooltip:
                edit.setToolTip(tooltip)
            hlayout.addWidget(label)
            hlayout.addWidget(edit)
            self.param_inputs[key] = edit
            param_layout.addLayout(hlayout)

        self.param_box.setLayout(param_layout)
        layout.addWidget(self.param_box)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm)
        layout.addWidget(confirm_button)

    def _apply_current_stylesheet(self):
        app = QApplication.instance()
        if app is not None:
            self.setStyleSheet(app.styleSheet())
            self.setPalette(app.palette())

    def confirm(self):
        params = {}
        for key, edit in self.param_inputs.items():
            try:
                value = edit.text().strip()
                param_type = self.config["parameters"][key]["type"]
                if param_type == "int":
                    params[key] = int(value)
                elif param_type == "float":
                    params[key] = float(value)
                elif param_type == "bool":
                    params[key] = value.lower() in ["true", "1"]
                else:
                    params[key] = value
            except Exception as e:
                QMessageBox.warning(self, "Invalid Input", f"Parameter '{key}' is invalid: {e}")
                return

        self.parent().algorithm_parameters = params
        self.accept()

    def closeEvent(self, event):
        parent = self.parent()
        if parent is not None and hasattr(parent, "parameter_dialog"):
            if parent.parameter_dialog is self:
                parent.parameter_dialog = None
        super().closeEvent(event)
