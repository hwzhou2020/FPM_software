"""
Professional Status Bar Enhancement for FPM Software
Provides enhanced status bar with progress indicators, system info, and professional styling
"""

from PySide6.QtWidgets import QStatusBar, QProgressBar, QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
import psutil
import time

class ProfessionalStatusBar(QStatusBar):
    """Enhanced status bar with professional styling and functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_professional_status_bar()
        
    def setup_professional_status_bar(self):
        """Set up the professional status bar components"""
        # Set basic styling
        self.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a2a,
                    stop:1 #1f1f1f
                );
                color: #b8b8b8;
                border-top: 1px solid #3a3a3a;
                padding: 4px;
                font-size: 9pt;
                font-weight: 500;
            }
        """)
        
        # Create status widgets
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #00ff88; font-weight: 600;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #2a2a2a;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                text-align: center;
                color: #ffffff;
                font-weight: 500;
                height: 16px;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2,
                    stop:1 #28a745
                );
                border-radius: 3px;
            }
        """)
        self.progress_bar.setVisible(False)
        
        # System info widgets
        self.memory_label = QLabel()
        self.memory_label.setStyleSheet("color: #888888; font-size: 8pt;")
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #888888; font-size: 8pt;")
        
        # Add widgets to status bar
        self.addWidget(self.status_label, 1)
        self.addPermanentWidget(self.memory_label)
        self.addPermanentWidget(self.time_label)
        self.addPermanentWidget(self.progress_bar)
        
        # Set up system monitoring
        self.setup_system_monitoring()
        
    def setup_system_monitoring(self):
        """Set up system resource monitoring"""
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.update_system_info)
        self.system_timer.start(2000)  # Update every 2 seconds
        
        # Time update timer
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Update every second
        
        # Initial update
        self.update_system_info()
        self.update_time()
        
    def update_system_info(self):
        """Update system resource information"""
        try:
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Color code based on usage
            if memory_percent < 70:
                color = "#00ff88"  # Green
            elif memory_percent < 90:
                color = "#ffc107"  # Yellow
            else:
                color = "#dc3545"  # Red
                
            self.memory_label.setText(f"RAM: {memory_used:.1f}/{memory_total:.1f}GB ({memory_percent:.0f}%)")
            self.memory_label.setStyleSheet(f"color: {color}; font-size: 8pt;")
            
        except Exception:
            self.memory_label.setText("RAM: N/A")
            
    def update_time(self):
        """Update current time display"""
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(f"Time: {current_time}")
        
    def show_progress(self, message="Processing...", maximum=100):
        """Show progress bar with message"""
        self.status_label.setText(message)
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
    def update_progress(self, value, message=None):
        """Update progress bar value"""
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
            
    def hide_progress(self, message="Ready"):
        """Hide progress bar and show completion message"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(message)
        
    def show_message(self, message, timeout=3000):
        """Show a temporary message"""
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, self.reset_message)
            
    def reset_message(self):
        """Reset message to Ready safely"""
        try:
            if self.status_label and not self.status_label.isHidden():
                self.status_label.setText("Ready")
        except RuntimeError:
            # Label was deleted, ignore
            pass
            
    def show_success(self, message):
        """Show success message in green"""
        self.status_label.setText(f"[OK] {message}")
        self.status_label.setStyleSheet("color: #00ff88; font-weight: 600;")
        QTimer.singleShot(3000, self.reset_status_style)
        
    def show_error(self, message):
        """Show error message in red"""
        self.status_label.setText(f"[ERROR] {message}")
        self.status_label.setStyleSheet("color: #dc3545; font-weight: 600;")
        QTimer.singleShot(5000, self.reset_status_style)
        
    def show_warning(self, message):
        """Show warning message in yellow"""
        self.status_label.setText(f"[WARNING] {message}")
        self.status_label.setStyleSheet("color: #ffc107; font-weight: 600;")
        QTimer.singleShot(4000, self.reset_status_style)
        
    def reset_status_style(self):
        """Reset status label style safely"""
        try:
            if self.status_label and not self.status_label.isHidden():
                self.status_label.setStyleSheet("color: #00ff88; font-weight: 600;")
        except RuntimeError:
            # Label was deleted, ignore
            pass
