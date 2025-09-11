#!/usr/bin/env python3
"""
FPM Software Auto-Installer
Automatically installs dependencies and sets up the environment
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ ERROR: pip is not available")
        print("   Please install pip: https://pip.pypa.io/en/stable/installation/")
        return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    # Map package names to their import names
    required_packages = {
        "numpy": "numpy",
        "scipy": "scipy", 
        "PySide6": "PySide6",
        "PyYAML": "yaml",  # PyYAML imports as 'yaml'
        "mat73": "mat73",
        "torch": "torch",
        "matplotlib": "matplotlib",
        "h5py": "h5py"
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - missing")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0, missing_packages

def create_conda_env():
    """Create conda environment if conda is available"""
    try:
        subprocess.check_call(["conda", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Conda detected")
        
        # Check if environment already exists
        result = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)
        if "FPM_Application" in result.stdout:
            print("✅ FPM_Application environment already exists")
            return True
        
        print("📦 Creating conda environment...")
        subprocess.check_call([
            "conda", "create", "-n", "FPM_Application", 
            "python=3.10", "-y"
        ])
        print("✅ Conda environment created")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  Conda not available, using pip installation")
        return False

def main():
    """Main installation process"""
    import sys
    
    # Check for test mode
    test_mode = "--test" in sys.argv
    
    print("=" * 50)
    print("    FPM Software Auto-Installer")
    if test_mode:
        print("    (TEST MODE - No packages will be installed)")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_pip():
        return False
    
    if not test_mode:
        # Try to create conda environment
        conda_available = create_conda_env()
        
        if conda_available:
            print("\n🔄 Activating conda environment...")
            print("   Please run: conda activate FPM_Application")
            print("   Then run: python main.py")
        else:
            # Install with pip
            if not install_requirements():
                return False
    else:
        print("\n🧪 Test mode: Skipping package installation")
        conda_available = False
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    all_installed, missing = check_dependencies()
    
    if not all_installed:
        if test_mode:
            print(f"\n⚠️  Test mode: {len(missing)} packages would need to be installed")
            print(f"   Missing: {', '.join(missing)}")
        else:
            print(f"\n❌ Missing packages: {', '.join(missing)}")
            print("   Please install them manually:")
            print(f"   pip install {' '.join(missing)}")
            return False
    
    if test_mode:
        print("\n✅ Test completed successfully!")
        print("   All dependencies are available or can be installed.")
    else:
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        if conda_available:
            print("   1. Activate environment: conda activate FPM_Application")
            print("   2. Run software: python main.py")
        else:
            print("   1. Run software: python main.py")
            print("   2. Or use launcher: run_fpm.bat (Windows) / run_fpm.sh (Linux/Mac)")
    
    print("\n💡 For help, see INSTALL.md or press F1 in the application")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Installation failed. Please check the errors above.")
        sys.exit(1)
