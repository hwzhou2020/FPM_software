# FPM Software Installation Guide

## 🚀 Quick Installation (Recommended)

### Option 1: Professional Launcher (Best Experience)
```bash
# Clone the repository
git clone https://github.com/hwzhou2020/FPM_software.git
cd FPM_software

# Run the professional launcher (handles dependencies + professional UI)
python launch_fpm_professional.py
```

### Option 2: One-Click Auto-Installer
```bash
# Run the auto-installer (handles everything automatically)
python install_fpm.py

# Launch the software
python main.py
```

### Option 3: Launcher Scripts (Easiest)
**Windows:**
```bash
# Professional launcher (recommended)
launch_fpm_professional.bat

# Or standard launcher
run_fpm.bat
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x run_fpm.sh
./run_fpm.sh
```

### Option 4: Using Conda (For Scientific Computing)
```bash
# Create environment from the provided environment file
conda env create -f docs_package/environment.yml
conda activate fpm_env

# Run the software
python main.py
```

### Option 5: Manual pip Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the software
python main.py
```

### Option 5: Development Installation
```bash
# Install in development mode
pip install -e .

# Run the software
python main.py
```

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 8GB RAM minimum (16GB recommended for large datasets)
- **GPU**: Optional but recommended for faster processing (CUDA-compatible)

## Dependencies

The software requires the following key packages:
- **PySide6**: GUI framework
- **NumPy & SciPy**: Scientific computing
- **PyTorch**: Deep learning framework for algorithms
- **mat73**: MATLAB file support
- **PyYAML**: Configuration management

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'torch'**
   ```bash
   pip install torch torchvision torchaudio
   ```

2. **MATLAB file loading issues**
   ```bash
   pip install mat73
   ```

3. **GUI not displaying properly**
   - Ensure you have a display server running (X11 on Linux)
   - Try running with: `python -X dev main.py`

4. **Memory issues with large datasets**
   - Reduce ROI size
   - Lower upsampling factor
   - Close other applications

### Getting Help

- Check the documentation in `docs_package/build/html/`
- Review the help file: `Documentation/help.md`
- Press F1 in the application for built-in help

## Development Setup

For developers who want to contribute:

```bash
# Clone the repository
git clone https://github.com/hwzhou2020/FPM_software.git
cd FPM_software

# Create development environment
conda env create -f docs_package/environment.yml
conda activate fpm_env

# Install in development mode
pip install -e .

# Run tests (when available)
python -m pytest tests/
```

## License

This software is provided under the MIT License. See LICENSE file for details.

## macOS Troubleshooting

If you are running on macOS and the installer reports missing packages such as 	orch or mat73, try the following:

1. Make sure you are using Python 3.9+ that ships with the latest pip (python3 --version).
2. Run the auto-installer again:
   `ash
   python3 install_fpm.py
   `
3. If PyTorch is still missing on Apple Silicon (M1/M2):
   `ash
   python3 -m pip install torch --index-url https://download.pytorch.org/whl/metal
   `
   For Intel-based Macs use:
   `ash
   python3 -m pip install torch --index-url https://download.pytorch.org/whl/cpu
   `
4. Re-install mat73 explicitly if needed:
   `ash
   python3 -m pip install mat73
   `
5. Verify the install:
   `ash
   python3 -m pip check
   python3 -m pip show torch mat73
   `

After these steps, re-run the launcher (python3 launch_fpm_professional.py) to confirm the application starts without missing-module errors.
