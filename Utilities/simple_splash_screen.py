"""
Simple Splash Screen for FPM Software
A lightweight splash screen that avoids paint device issues
"""

import sys
import time
from PySide6.QtWidgets import QSplashScreen, QApplication
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor, QPen
from PySide6.QtCore import Qt, QTimer, QRect

class SimpleSplashScreen(QSplashScreen):
    """Simple splash screen without complex animations"""
    
    def __init__(self):
        # Create a simple pixmap for the splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(26, 26, 26))  # Dark background
        
        # Draw static content
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background gradient
        from PySide6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor(26, 26, 26))
        gradient.setColorAt(0.5, QColor(30, 30, 30))
        gradient.setColorAt(1, QColor(37, 37, 37))
        painter.fillRect(QRect(0, 0, 600, 400), gradient)
        
        # Title
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(74, 144, 226))  # Blue color
        painter.drawText(QRect(0, 80, 600, 50), Qt.AlignCenter, "FPM Software")
        
        # Subtitle
        subtitle_font = QFont("Segoe UI", 12)
        painter.setFont(subtitle_font)
        painter.setPen(QColor(200, 200, 200))
        painter.drawText(QRect(0, 130, 600, 30), Qt.AlignCenter, 
                        "Fourier Ptychographic Microscopy Reconstruction")
        
        # Version
        version_font = QFont("Segoe UI", 10)
        painter.setFont(version_font)
        painter.setPen(QColor(150, 150, 150))
        painter.drawText(QRect(0, 160, 600, 20), Qt.AlignCenter, "Professional Edition v2.0")
        
        # Loading text
        loading_font = QFont("Segoe UI", 11)
        painter.setFont(loading_font)
        painter.setPen(QColor(0, 255, 136))  # Green color
        painter.drawText(QRect(0, 250, 600, 30), Qt.AlignCenter, "Loading...")
        
        # Footer
        footer_font = QFont("Segoe UI", 8)
        painter.setFont(footer_font)
        painter.setPen(QColor(120, 120, 120))
        painter.drawText(QRect(0, 370, 600, 20), Qt.AlignCenter, 
                        "Caltech Biophotonics Lab • Designed by Haowen Zhou")
        
        painter.end()
        
        super().__init__(pixmap)
        
        # Set window properties
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def show_splash(self, duration=2000):
        """Show the splash screen for a specified duration"""
        self.show()
        QApplication.processEvents()
        
        # Simple timer-based display
        start_time = time.time()
        while time.time() - start_time < duration / 1000:
            QApplication.processEvents()
            time.sleep(0.01)
            
        self.close()

def show_simple_splash():
    """Show the simple splash screen"""
    splash = SimpleSplashScreen()
    splash.show_splash(2000)  # Show for 2 seconds
    return splash
