"""
Professional About Dialog for FPM Software
Provides a modern, informative about dialog with software information
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTextEdit, QScrollArea, QWidget)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

class ProfessionalAboutDialog(QDialog):
    """Professional about dialog with modern design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_about_dialog()
        
    def setup_about_dialog(self):
        """Set up the about dialog"""
        self.setWindowTitle("About FPM Software")
        self.setFixedSize(500, 600)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Apply professional styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a1a,
                    stop:0.5 #1e1e1e,
                    stop:1 #252525
                );
                color: #e8e8e8;
            }
            QLabel {
                color: #e8e8e8;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2,
                    stop:1 #357abd
                );
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2,
                    stop:1 #4a8acd
                );
            }
            QTextEdit {
                background: #1a1a1a;
                color: #e8e8e8;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 9pt;
            }
        """)
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title section
        title_layout = QVBoxLayout()
        
        # Software title
        title_label = QLabel("FPM Software")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4a90e2; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Fourier Ptychographic Microscopy Reconstruction")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #b8b8b8;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle_label)
        
        # Version
        version_label = QLabel("Professional Edition v2.0")
        version_font = QFont("Segoe UI", 10)
        version_label.setFont(version_font)
        version_label.setStyleSheet("color: #888888;")
        version_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(version_label)
        
        main_layout.addLayout(title_layout)
        
        # Information section
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        
        info_content = """
FPM Software is a professional-grade application for Fourier Ptychographic Microscopy (FPM) reconstruction. 

Key Features:
• Advanced reconstruction algorithms (Gerchberg-Saxton, EPRY, Gauss-Newton, Kramers-Kronig, APIC)
• Interactive image display with zoom and pan capabilities
• Professional user interface with modern styling
• Comprehensive data analysis and visualization tools
• Support for various data formats and batch processing
• Real-time system monitoring and progress tracking

Technical Specifications:
• Built with PySide6 (Qt6) for cross-platform compatibility
• Optimized for scientific computing with NumPy and SciPy
• GPU acceleration support via PyTorch
• Professional documentation and help system

This software is designed for researchers, scientists, and engineers working in the field of computational microscopy and biomedical imaging.
        """
        
        info_text.setPlainText(info_content)
        main_layout.addWidget(info_text)
        
        # Credits section
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setMaximumHeight(120)
        
        credits_content = """
Development Team:
• Lead Developer: Haowen Zhou
• Institution: Caltech Biophotonics Lab
• Website: https://hwzhou2020.github.io/

Acknowledgments:
• Caltech Biophotonics Laboratory
• Open source community contributors
• Scientific computing libraries (NumPy, SciPy, PyTorch, Qt)

License: MIT License
© 2024 Caltech Biophotonics Lab
        """
        
        credits_text.setPlainText(credits_content)
        main_layout.addWidget(credits_text)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)
        
        # Center the dialog
        self.center_dialog()
        
    def center_dialog(self):
        """Center the dialog on the parent window"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)

def show_about_dialog(parent=None):
    """Show the professional about dialog"""
    dialog = ProfessionalAboutDialog(parent)
    dialog.exec()
