# FPM Software Installation Guide

## 🚀 Quick Installation (Recommended)

### Option 1: One-Click Auto-Installer
```bash
# Clone the repository
git clone https://github.com/hwzhou2020/FPM_software.git
cd FPM_software

# Run the auto-installer (handles everything automatically)
python install_fpm.py

# Launch the software
python main.py
```

### Option 2: Launcher Scripts (Easiest)
**Windows:**
```bash
# Just double-click this file or run in command prompt
run_fpm.bat
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x run_fpm.sh
./run_fpm.sh
```

### Option 3: Using Conda (For Scientific Computing)
```bash
# Create environment from the provided environment file
conda env create -f docs_package/environment.yml
conda activate fpm_env

# Run the software
python main.py
```

### Option 4: Manual pip Installation
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
