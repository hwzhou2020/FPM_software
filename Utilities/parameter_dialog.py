import os
import yaml
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class ParameterDialog(QWidget):
    def __init__(self, algorithm_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{algorithm_name} Parameters")
        self.setWindowFlag(Qt.Window)  # Make it a floating window
        self.setFixedSize(400, 300)

        self.algorithm_name = algorithm_name
        self.config = self.load_config()
        self.param_inputs = {}  # Store QLineEdit widgets for each param

        self.setup_ui()

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
        self.close()