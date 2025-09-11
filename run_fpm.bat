@echo off
echo ========================================
echo    FPM Software Launcher
echo ========================================
echo.
echo NOTE: For the best experience with professional UI,
echo       use: launch_fpm_professional.bat
echo.

REM Try to find Python in common locations
set PYTHON_PATH=""

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% == 0 (
    echo Found conda, activating FPM environment...
    call conda activate FPM_Application
    if %errorlevel% == 0 (
        echo Environment activated successfully!
        python main.py
        goto :end
    )
)

REM Check Anaconda installation
if exist "C:\Users\%USERNAME%\anaconda3\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\anaconda3\python.exe"
    echo Found Anaconda Python
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set PYTHON_PATH="C:\ProgramData\Anaconda3\python.exe"
    echo Found Anaconda Python
) else if exist "C:\Users\%USERNAME%\miniconda3\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\miniconda3\python.exe"
    echo Found Miniconda Python
) else (
    echo Checking system Python...
    python --version >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON_PATH="python"
        echo Found system Python
    )
)

if %PYTHON_PATH% == "" (
    echo.
    echo ERROR: Python not found!
    echo Please install Python 3.8+ or Anaconda/Miniconda
    echo Download from: https://www.python.org/downloads/
    echo or https://www.anaconda.com/products/distribution
    echo.
    pause
    goto :end
)

echo.
echo Starting FPM Software...
echo Python path: %PYTHON_PATH%
echo.

%PYTHON_PATH% main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start FPM Software
    echo This might be due to missing dependencies.
    echo Please run: pip install -r requirements.txt
    echo.
    pause
)

:end
