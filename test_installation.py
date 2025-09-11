#!/usr/bin/env python3
"""
FPM Software Installation Test
Run this script to verify your installation is working correctly.

NOTE: For the best experience with professional UI,
      use: python launch_fpm_professional.py
"""

import sys
import os

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[ERROR] Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("   Python 3.8 or higher is required")
        return False
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def test_imports():
    """Test that all required packages can be imported"""
    required_packages = {
        "numpy": "numpy",
        "scipy": "scipy", 
        "PySide6": "PySide6",
        "PyYAML": "yaml",
        "mat73": "mat73",
        "torch": "torch",
        "matplotlib": "matplotlib",
        "h5py": "h5py"
    }
    
    print("\n[INFO] Testing package imports...")
    failed_imports = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"[OK] {package_name}")
        except ImportError:
            print(f"[MISSING] {package_name}")
            failed_imports.append(package_name)
    
    return len(failed_imports) == 0, failed_imports

def test_file_structure():
    """Test that all required files exist"""
    print("\n[INFO] Testing file structure...")
    required_files = [
        "main.py",
        "requirements.txt", 
        "README.md",
        "LICENSE",
        "install_fpm.py",
        "run_fpm.bat",
        "run_fpm.sh"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            print(f"[MISSING] {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def test_main_module():
    """Test that main.py can be parsed"""
    print("\n[INFO] Testing main module...")
    try:
        with open("main.py", "r") as f:
            code = f.read()
        compile(code, "main.py", "exec")
        print("[OK] main.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"[ERROR] main.py has syntax errors: {e}")
        return False
    except FileNotFoundError:
        print("[ERROR] main.py not found")
        return False

def test_demo_data():
    """Test that demo data exists"""
    print("\n[INFO] Testing demo data...")
    demo_file = "data/Demo_data/FPM_SiemensStar_Demo.mat"
    if os.path.exists(demo_file):
        print(f"[OK] Demo data found: {demo_file}")
        return True
    else:
        print(f"[MISSING] Demo data: {demo_file}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("    FPM Software Installation Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test Python version
    if test_python_version():
        tests_passed += 1
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    if imports_ok:
        tests_passed += 1
    
    # Test file structure
    files_ok, missing_files = test_file_structure()
    if files_ok:
        tests_passed += 1
    
    # Test main module
    if test_main_module():
        tests_passed += 1
    
    # Test demo data
    if test_demo_data():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"    Test Results: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("[SUCCESS] All tests passed! Your FPM Software installation is ready.")
        print("\n[INFO] Next steps:")
        print("   RECOMMENDED: python launch_fpm_professional.py (Professional UI)")
        print("   Alternative: python main.py")
        print("   Or use launcher: run_fpm.bat (Windows) / run_fpm.sh (Linux/Mac)")
        print("   Demo data: data/Demo_data/FPM_SiemensStar_Demo.mat")
        return True
    else:
        print("[ERROR] Some tests failed. Please check the issues above.")
        
        if failed_imports:
            print(f"\n[INFO] To install missing packages:")
            print(f"   pip install {' '.join(failed_imports)}")
        
        if missing_files:
            print(f"\n[INFO] Missing files: {', '.join(missing_files)}")
            print("   Make sure you're in the correct directory")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
