@echo off
echo ========================================
echo FPM Software Professional Edition
echo (No Splash Screen Version)
echo ========================================
echo.

REM Try to find Python in the FPM_Application environment
set PYTHON_PATH=C:\Users\Holoz\anaconda3\envs\FPM_Application\python.exe

REM Check if the Python path exists
if exist "%PYTHON_PATH%" (
    echo Using Python: %PYTHON_PATH%
    echo.
    "%PYTHON_PATH%" launch_fpm_no_splash.py
) else (
    echo Python not found at: %PYTHON_PATH%
    echo Trying system Python...
    echo.
    python launch_fpm_no_splash.py
)

echo.
echo Application closed.
pause
