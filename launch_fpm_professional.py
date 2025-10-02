#!/usr/bin/env python3
"""
Professional FPM Software Launcher
Handles environment setup and launches the application with proper error handling
"""

import sys
import os
import subprocess
from importlib import util as importlib_util

def check_dependencies():
    """Return a list of pip package names that still need to be installed."""
    dependencies = {
        'PySide6': 'PySide6',
        'numpy': 'numpy',
        'scipy': 'scipy',
        'psutil': 'psutil',
        'yaml': 'PyYAML',  # PyYAML installs the yaml module
        'mat73': 'mat73',
        'torch': 'torch',
    }
    missing_packages = []

    for module_name, package_name in dependencies.items():
        if importlib_util.find_spec(module_name) is None:
            missing_packages.append(package_name)

    # Remove duplicates while preserving order
    seen = set()
    unique_missing = []
    for package in missing_packages:
        if package not in seen:
            seen.add(package)
            unique_missing.append(package)

    return unique_missing

def install_dependencies(packages):
    """Install missing dependencies"""
    print(f"Installing missing packages: {', '.join(packages)}")
    success = True
    for package in packages:
        cmd = [sys.executable, '-m', 'pip', 'install', package]
        if package == 'torch':
            import platform
            system = platform.system().lower()
            machine = platform.machine().lower()
            if system == 'darwin':
                index_url = 'https://download.pytorch.org/whl/metal' if machine in ('arm64', 'arm64e') else 'https://download.pytorch.org/whl/cpu'
                cmd.extend(['--index-url', index_url])
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            success = False
            print(f"[ERROR] Failed to install {package} automatically")
    return success

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
    print("FPM Software Professional Edition Launcher")
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
