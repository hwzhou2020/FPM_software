"""
Professional Splash Screen for FPM Software
Provides a modern, animated splash screen during application startup
"""

import sys
import time
from PySide6.QtWidgets import QSplashScreen, QApplication
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor, QPen
from PySide6.QtCore import Qt, QTimer, QRect

class ProfessionalSplashScreen(QSplashScreen):
    """Professional splash screen with modern design and animations"""
    
    def __init__(self):
        # Create a pixmap for the splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(26, 26, 26))  # Dark background
        
        super().__init__(pixmap)
        
        # Set window properties
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Animation properties
        self.progress = 0
        self.loading_text = "Initializing FPM Software..."
        self.version_text = "Professional Edition v2.0"
        self.is_closing = False
        
        # Create the splash screen content
        self.create_splash_content()
        
        # Set up animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Update every 50ms
        
    def create_splash_content(self):
        """Create the visual content of the splash screen"""
        try:
            # Create a new pixmap to avoid paint device conflicts
            new_pixmap = QPixmap(600, 400)
            new_pixmap.fill(QColor(26, 26, 26))  # Dark background
            
            painter = QPainter(new_pixmap)
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
            painter.drawText(QRect(0, 160, 600, 20), Qt.AlignCenter, self.version_text)
            
            # Loading text
            loading_font = QFont("Segoe UI", 11)
            painter.setFont(loading_font)
            painter.setPen(QColor(0, 255, 136))  # Green color
            painter.drawText(QRect(0, 250, 600, 30), Qt.AlignCenter, self.loading_text)
            
            # Progress bar background
            progress_bg_rect = QRect(100, 300, 400, 20)
            painter.setPen(QPen(QColor(60, 60, 60), 2))
            painter.setBrush(QColor(40, 40, 40))
            painter.drawRoundedRect(progress_bg_rect, 10, 10)
            
            # Progress bar fill
            progress_width = int(400 * (self.progress / 100))
            if progress_width > 0:
                progress_rect = QRect(100, 300, progress_width, 20)
                progress_gradient = QLinearGradient(100, 300, 100 + progress_width, 320)
                progress_gradient.setColorAt(0, QColor(74, 144, 226))
                progress_gradient.setColorAt(1, QColor(40, 167, 69))
                painter.setBrush(progress_gradient)
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(progress_rect, 10, 10)
            
            # Progress percentage
            painter.setFont(QFont("Segoe UI", 9))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(QRect(0, 330, 600, 20), Qt.AlignCenter, f"{self.progress}%")
            
            # Footer
            footer_font = QFont("Segoe UI", 8)
            painter.setFont(footer_font)
            painter.setPen(QColor(120, 120, 120))
            painter.drawText(QRect(0, 370, 600, 20), Qt.AlignCenter, 
                            "Caltech Biophotonics Lab • Designed by Haowen Zhou")
            
            painter.end()
            
            # Update the splash screen with the new pixmap
            self.setPixmap(new_pixmap)
            
        except Exception as e:
            # If painting fails, just continue without updating
            print(f"Splash screen painting error: {e}")
            pass
        
    def update_animation(self):
        """Update the animation progress"""
        if self.is_closing:
            return
            
        self.progress += 2
        
        # Update loading text based on progress
        if self.progress < 20:
            self.loading_text = "Loading core modules..."
        elif self.progress < 40:
            self.loading_text = "Initializing algorithms..."
        elif self.progress < 60:
            self.loading_text = "Setting up user interface..."
        elif self.progress < 80:
            self.loading_text = "Loading professional theme..."
        elif self.progress < 95:
            self.loading_text = "Finalizing setup..."
        else:
            self.loading_text = "Ready!"
            
        try:
            if not self.is_closing:
                self.create_splash_content()
        except Exception:
            # If painting fails, just continue
            pass
        
        if self.progress >= 100:
            self.timer.stop()
            self.is_closing = True
            QTimer.singleShot(500, self.safe_close)  # Close after 500ms delay
            
    def safe_close(self):
        """Safely close the splash screen"""
        try:
            self.is_closing = True
            self.timer.stop()
            self.hide()
            self.close()
        except Exception:
            # If close fails, just hide
            try:
                self.hide()
            except Exception:
                pass
            
    def show_splash(self, duration=3000):
        """Show the splash screen for a specified duration"""
        self.show()
        QApplication.processEvents()
        
        # Simulate loading time
        start_time = time.time()
        while time.time() - start_time < duration / 1000:
            QApplication.processEvents()
            time.sleep(0.01)
            
        self.close()

def show_professional_splash():
    """Show the professional splash screen"""
    splash = ProfessionalSplashScreen()
    splash.show_splash(3000)  # Show for 3 seconds
    return splash
