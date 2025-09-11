# FPM Software - Fourier Ptychographic Microscopy

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://pypi.org/project/PySide6/)

A comprehensive software package for Fourier Ptychographic Microscopy (FPM) reconstruction algorithms with an intuitive graphical user interface.

## 🚀 Quick Start

### Option 1: One-Click Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/hwzhou2020/FPM_software.git
cd FPM_software

# Run the auto-installer
python install_fpm.py

# Launch the software
python main.py
```

### Option 2: Use Launcher Scripts
**Windows:**
```bash
# Double-click or run in command prompt
run_fpm.bat
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x run_fpm.sh
./run_fpm.sh
```

### Option 3: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Test your installation (optional)
python test_installation.py

# Run the software
python main.py
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 8GB RAM minimum (16GB recommended for large datasets)
- **GPU**: Optional but recommended for faster processing (CUDA-compatible)

## 🎯 Features

### Core Functionality
- **Multiple Algorithms**: Gerchberg-Saxton, EPRY, Gauss-Newton, Kramers-Kronig, APIC
- **Interactive GUI**: Modern PySide6 interface with dark theme
- **Data Loading**: Support for MATLAB .mat files (v7 and v7.3)
- **ROI Selection**: Interactive region of interest selection
- **Real-time Display**: Zoom, pan, and navigate through image stacks

### User Experience
- **Keyboard Shortcuts**: Ctrl+O (Load), Ctrl+R (Run), F1 (Help)
- **Progress Indicators**: Real-time progress bars and status updates
- **Auto-display**: Amplitude results shown automatically after reconstruction
- **Error Handling**: Clear, user-friendly error messages
- **Data Validation**: Comprehensive .mat file structure validation

### Advanced Features
- **GPU Acceleration**: PyTorch-based algorithms with CUDA support
- **Parameter Configuration**: YAML-based algorithm parameter management
- **Export Functionality**: Save results in multiple formats
- **Documentation**: Built-in help system and comprehensive guides

## 📦 Dependencies

### Core Dependencies
- **PySide6**: GUI framework
- **NumPy & SciPy**: Scientific computing
- **PyTorch**: Deep learning framework for algorithms
- **mat73**: MATLAB file support
- **PyYAML**: Configuration management

### Optional Dependencies
- **OpenCV**: Enhanced image processing
- **scikit-image**: Additional image analysis tools
- **tqdm**: Progress bars

## 🛠️ Installation Methods

### Method 1: Conda (Recommended for Scientific Computing)
```bash
# Create environment from provided file
conda env create -f docs_package/environment.yml
conda activate fpm_env
python main.py
```

### Method 2: pip Installation
```bash
pip install -r requirements.txt
python main.py
```

### Method 3: Development Installation
```bash
pip install -e .
python main.py
```

## 📖 Usage

1. **Load Data**: Click "Load" or press Ctrl+O to load .mat files
2. **Select ROI**: Use the ROI button to select region of interest
3. **Choose Algorithm**: Go to Specs → Algorithm specs to select algorithm
4. **Configure Parameters**: Set algorithm-specific parameters
5. **Run Reconstruction**: Click "Run" or press Ctrl+R
6. **View Results**: Amplitude results display automatically

## 📁 Data Format

The software expects .mat files containing:
- **`imlow`**: 3D array (H×W×N) of low-resolution intensity images
- **`NA_list`**: Illumination numerical aperture coordinates
- **`NA`**: System numerical aperture
- **`dpix_c`**: Camera pixel size
- **`lambda`**: Wavelength
- **`mag`**: Magnification

## 🐛 Troubleshooting

### Common Issues

**Python not found:**
```bash
# Install Python from https://www.python.org/downloads/
# Or use Anaconda: https://www.anaconda.com/products/distribution
```

**Import errors:**
```bash
pip install -r requirements.txt
```

**Test your installation:**
```bash
python test_installation.py
```

**GUI not displaying:**
```bash
# Linux: Install X11
sudo apt-get install python3-tk

# Run with debug mode
python -X dev main.py
```

**Memory issues:**
- Reduce ROI size
- Lower upsampling factor
- Close other applications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Haowen Zhou** - Caltech Biophotonics Lab
- Website: https://hwzhou2020.github.io/
- GitHub: [@hwzhou2020](https://github.com/hwzhou2020)

## 🙏 Acknowledgments

- Caltech Biophotonics Lab
- PySide6 development team
- Scientific Python community

## 📚 Documentation

- [Installation Guide](INSTALL.md)
- [User Manual](docs_package/build/html/index.html)
- [API Reference](docs_package/build/html/modules.html)

---
