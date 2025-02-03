import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 GUI Application")
        self.setGeometry(100, 100, 800, 600)
        
        label = QLabel("Hello, PySide6!", self)
        label.setGeometry(200, 200, 400, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())