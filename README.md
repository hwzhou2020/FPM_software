# FPM Software - Fourier Ptychographic Microscopy

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://pypi.org/project/PySide6/)
[![Professional UI](https://img.shields.io/badge/UI-Professional%20Edition-purple.svg)](#)

A comprehensive software package for Fourier Ptychographic Microscopy (FPM) reconstruction algorithms with a **professional, modern graphical user interface**.

## 🚀 Quick Start

### Option 1: Professional Launcher (Recommended)
```bash
# Clone the repository
git clone https://github.com/hwzhou2020/FPM_software.git
cd FPM_software

# Run the professional launcher (handles dependencies automatically)
python launch_fpm_professional.py

# If you encounter "QPaintDevice" errors, use the no-splash version:
python launch_fpm_no_splash.py
```

### Option 2: One-Click Installation
```bash
# Run the auto-installer
python install_fpm.py

# Launch the software
python main.py
```

### Option 3: Use Launcher Scripts
**Windows:**
```bash
# Professional launcher (recommended)
launch_fpm_professional.bat

# No-splash version (if you get paint device errors)
launch_fpm_no_splash.bat

# Or standard launcher
run_fpm.bat
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x run_fpm.sh
./run_fpm.sh
```

### Option 4: Manual Installation
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

### 🎨 Professional User Interface
- **Modern Design**: Professional dark theme with blue accents and gradients
- **Enhanced Status Bar**: Real-time system monitoring (RAM usage, time)
- **Professional Splash Screen**: Animated loading with progress indicators
- **About Dialog**: Comprehensive software information and credits
- **Enhanced Buttons**: Professional icons and helpful tooltips
- **Responsive Layout**: Optimized for different screen sizes

### 🔬 Core Functionality
- **Multiple Algorithms**: Gerchberg-Saxton, EPRY, Gauss-Newton, Kramers-Kronig, APIC
- **Interactive GUI**: Modern PySide6 interface with professional styling
- **Data Loading**: Support for MATLAB .mat files (v7 and v7.3)
- **ROI Selection**: Interactive region of interest selection
- **Real-time Display**: Zoom, pan, and navigate through image stacks

### 🚀 User Experience
- **Keyboard Shortcuts**: Ctrl+O (Load), Ctrl+R (Run), F1 (Help)
- **Progress Indicators**: Professional progress bars with gradients
- **Auto-display**: Amplitude results shown automatically after reconstruction
- **Error Handling**: Clear, user-friendly error messages with color coding
- **Data Validation**: Comprehensive .mat file structure validation
- **System Monitoring**: Live RAM usage and performance tracking

### ⚡ Advanced Features
- **GPU Acceleration**: PyTorch-based algorithms with CUDA support
- **Parameter Configuration**: YAML-based algorithm parameter management
- **Export Functionality**: Save results in multiple formats
- **Documentation**: Built-in help system and comprehensive guides
- **Professional Branding**: Consistent branding throughout the application

## 📦 Dependencies

### Core Dependencies
- **PySide6**: GUI framework with professional theming
- **NumPy & SciPy**: Scientific computing
- **PyTorch**: Deep learning framework for algorithms
- **mat73**: MATLAB file support
- **PyYAML**: Configuration management
- **psutil**: System resource monitoring

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

### Getting Started
1. **Launch**: Run `python launch_fpm_professional.py` for the best experience
2. **Load Data**: Click "📁 Load Data" or press Ctrl+O to load .mat files
3. **Select ROI**: Use the "🎯 ROI" button to select region of interest
4. **Choose Algorithm**: Go to Specs → Algorithm specs to select algorithm
5. **Configure Parameters**: Set algorithm-specific parameters
6. **Run Reconstruction**: Click "▶ Run" or press Ctrl+R
7. **View Results**: Amplitude results display automatically

### Professional Features
- **System Monitoring**: Watch real-time RAM usage in the status bar
- **Progress Tracking**: Professional progress bars with gradients
- **Status Messages**: Color-coded success/error/warning messages
- **Help System**: Press F1 or use Help menu for assistance
- **About Dialog**: View software information and credits

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

**QPaintDevice errors:**
```bash
# Use the no-splash version to avoid paint device issues
python launch_fpm_no_splash.py

# Or on Windows:
launch_fpm_no_splash.bat
```

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

## 🎨 Professional UI Features

The FPM Software now features a **Professional Edition** with modern, commercial-grade user interface:

### Visual Design
- **Modern Dark Theme**: Professional color scheme with blue accents (#4a90e2)
- **Gradient Effects**: Subtle gradients for depth and visual appeal
- **Enhanced Typography**: Segoe UI font family for clean, modern text
- **Rounded Corners**: 6px border radius for contemporary appearance
- **Professional Icons**: Emoji-based icons for better visual recognition

### Enhanced User Experience
- **Professional Splash Screen**: Animated loading with progress indicators
- **Real-time Status Bar**: Live system monitoring (RAM usage, time)
- **Color-coded Messages**: Success (green), error (red), warning (yellow)
- **Professional Progress Bars**: Gradient progress indicators
- **Enhanced Tooltips**: Helpful descriptions for all UI elements

### System Integration
- **Application Metadata**: Professional branding and version information
- **Window Management**: Automatic centering and optimal sizing
- **Error Handling**: Graceful fallbacks for all new features
- **Cross-platform**: Optimized for Windows, macOS, and Linux

### Professional Features
- **About Dialog**: Comprehensive software information and credits
- **System Monitoring**: Live RAM usage and performance tracking
- **Professional Launcher**: Enhanced startup with dependency checking
- **Clean CSS**: Qt-compatible styling without warnings

## 📚 Documentation

- [Installation Guide](INSTALL.md)
- [Professional UI Guide](PROFESSIONAL_UI_IMPROVEMENTS.md)
- [User Manual](docs_package/build/html/index.html)
- [API Reference](docs_package/build/html/modules.html)

---
