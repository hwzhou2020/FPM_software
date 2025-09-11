#!/bin/bash

echo "========================================"
echo "    FPM Software Launcher"
echo "========================================"
echo
echo "NOTE: For the best experience with professional UI,"
echo "      use: python launch_fpm_professional.py"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Try to activate conda environment if available
if command_exists conda; then
    echo "Found conda, activating FPM environment..."
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate FPM_Application 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Environment activated successfully!"
        python main.py
        exit $?
    fi
fi

# Check for Python
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found!"
    echo "Please install Python 3.8+ or Anaconda/Miniconda"
    echo "Download from: https://www.python.org/downloads/"
    echo "or https://www.anaconda.com/products/distribution"
    exit 1
fi

echo "Starting FPM Software..."
echo "Python command: $PYTHON_CMD"
echo

$PYTHON_CMD main.py

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Failed to start FPM Software"
    echo "This might be due to missing dependencies."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi
