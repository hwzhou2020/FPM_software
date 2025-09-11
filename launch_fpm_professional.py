#!/usr/bin/env python3
"""
Professional FPM Software Launcher
Handles environment setup and launches the application with proper error handling
"""

import sys
import os
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = ['PySide6', 'numpy', 'scipy', 'psutil']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    print(f"Installing missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        return True
    except subprocess.CalledProcessError:
        return False

def launch_application():
    """Launch the FPM application"""
    try:
        # Import and run the main application
        from main import QApplication, MainWindow
        import sys
        
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("FPM Software")
        app.setApplicationVersion("2.0 Professional")
        app.setOrganizationName("Caltech Biophotonics Lab")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("✓ FPM Software Professional Edition launched successfully!")
        print("✓ Professional UI loaded with modern styling")
        print("✓ All features are ready to use")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"✗ Error launching application: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("FPM Software Professional Edition Launcher")
    print("=" * 60)
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        if install_dependencies(missing):
            print("✓ Dependencies installed successfully")
        else:
            print("✗ Failed to install dependencies")
            print("Please install manually: pip install " + " ".join(missing))
            return False
    else:
        print("✓ All dependencies are available")
    
    # Launch application
    print("Launching FPM Software...")
    return launch_application()

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
        sys.exit(1)
