#!/usr/bin/env python3
"""
FPM Software Launcher (No Splash Screen)
Launches the application without splash screen to avoid paint device issues
"""

import sys
import os
import subprocess

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
    """Launch the FPM application without splash screen"""
    try:
        # Import and run the main application
        from main import QApplication, MainWindow
        import sys
        
        app = QApplication(sys.argv)
        
        # Set application properties
        app.setApplicationName("FPM Software")
        app.setApplicationVersion("2.0 Professional")
        app.setOrganizationName("Caltech Biophotonics Lab")
        
        # Create and show main window (no splash screen)
        window = MainWindow()
        window.show()
        
        print("[OK] FPM Software Professional Edition launched successfully!")
        print("[OK] Professional UI loaded with modern styling")
        print("[OK] All features are ready to use")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"[ERROR] Error launching application: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("FPM Software Professional Edition Launcher (No Splash)")
    print("=" * 60)
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        if install_dependencies(missing):
            print("[OK] Dependencies installed successfully")
        else:
            print("[ERROR] Failed to install dependencies")
            print("Please install manually: pip install " + " ".join(missing))
            return False
    else:
        print("[OK] All dependencies are available")
    
    # Launch application
    print("Launching FPM Software...")
    return launch_application()

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
        sys.exit(1)
