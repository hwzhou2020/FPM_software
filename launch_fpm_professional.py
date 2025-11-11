#!/usr/bin/env python3
"""
Professional FPM Software Launcher
Handles environment setup and launches the application with proper error handling
"""

import sys
import os
import re
import subprocess
from importlib import util as importlib_util
from importlib import metadata as importlib_metadata

def _version_tuple(version_str):
    """Convert a version string into a comparable tuple of integers."""
    parts = []
    for component in version_str.split('.'):
        match = re.match(r'(\d+)', component)
        if not match:
            break
        parts.append(int(match.group(1)))
    return tuple(parts)


def _compare_versions(lhs, rhs):
    """Return -1, 0, or 1 depending on the comparison outcome."""
    left_tuple = _version_tuple(lhs)
    right_tuple = _version_tuple(rhs)
    length = max(len(left_tuple), len(right_tuple))
    left_tuple += (0,) * (length - len(left_tuple))
    right_tuple += (0,) * (length - len(right_tuple))
    if left_tuple < right_tuple:
        return -1
    if left_tuple > right_tuple:
        return 1
    return 0


def _is_version_sufficient(installed, minimum):
    """Return True if the installed version is >= the minimum."""
    return _compare_versions(installed, minimum) >= 0


def _is_version_within_range(installed, minimum=None, maximum=None):
    """Return True if installed version satisfies the optional minimum/maximum bounds."""
    if minimum and _compare_versions(installed, minimum) < 0:
        return False
    if maximum and _compare_versions(installed, maximum) >= 0:
        return False
    return True


def _format_requirement(package_name, min_version=None, max_version=None):
    """Return a pip-style version specifier."""
    if min_version and max_version:
        return f"{package_name}>={min_version},<{max_version}"
    if min_version:
        return f"{package_name}>={min_version}"
    if max_version:
        return f"{package_name}<{max_version}"
    return package_name


def check_dependencies():
    """Return a list of pip package names (with version specs) that still need to be installed."""
    dependencies = [
        {'module': 'PySide6', 'package': 'PySide6'},
        {'module': 'numpy', 'package': 'numpy', 'min_version': '1.26.0', 'max_version': '2.0.0'},
        {'module': 'scipy', 'package': 'scipy', 'min_version': '1.11.0', 'max_version': '1.13.0'},
        {'module': 'psutil', 'package': 'psutil'},
        {'module': 'yaml', 'package': 'PyYAML'},  # PyYAML installs the yaml module
        {'module': 'mat73', 'package': 'mat73'},
        {'module': 'torch', 'package': 'torch'},
    ]

    missing_packages = []

    for dependency in dependencies:
        module_name = dependency['module']
        package_name = dependency['package']
        min_version = dependency.get('min_version')
        max_version = dependency.get('max_version')
        requirement = _format_requirement(package_name, min_version, max_version)

        if importlib_util.find_spec(module_name) is None:
            missing_packages.append(requirement)
            continue

        if min_version or max_version:
            try:
                installed_version = importlib_metadata.version(package_name)
            except importlib_metadata.PackageNotFoundError:
                missing_packages.append(requirement)
                continue

            if not _is_version_within_range(installed_version, min_version, max_version):
                missing_packages.append(requirement)

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
