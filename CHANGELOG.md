# Changelog

All notable changes to the FPM Software project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- **Core FPM Algorithms**: Gerchberg-Saxton, EPRY, Gauss-Newton, Kramers-Kronig, APIC
- **Modern GUI**: PySide6-based interface with dark theme
- **Data Loading**: Support for MATLAB .mat files (v7 and v7.3)
- **Interactive Display**: Zoom, pan, and navigate through image stacks
- **ROI Selection**: Interactive region of interest selection
- **Real-time Progress**: Progress bars and status updates during processing
- **Auto-display**: Amplitude results shown automatically after reconstruction
- **Keyboard Shortcuts**: Ctrl+O (Load), Ctrl+R (Run), F1 (Help), Ctrl+Q (Quit)
- **Data Validation**: Comprehensive .mat file structure validation
- **Error Handling**: Clear, user-friendly error messages
- **Export Functionality**: Save results and messages
- **Documentation**: Built-in help system and comprehensive guides

### Enhanced
- **User Experience**: Professional UI with status bar and smart button states
- **Installation**: Multiple installation methods (auto-installer, launchers, conda, pip)
- **Cross-platform**: Support for Windows, macOS, and Linux
- **GPU Acceleration**: PyTorch-based algorithms with CUDA support
- **Parameter Management**: YAML-based algorithm configuration

### Technical
- **Modular Architecture**: Clean separation of algorithms, utilities, and UI
- **Type Safety**: Improved error handling and validation
- **Memory Management**: Efficient data processing and cleanup
- **Testing**: Automated testing with GitHub Actions
- **CI/CD**: Continuous integration and deployment pipeline

### Documentation
- **README**: Comprehensive project overview and quick start guide
- **Installation Guide**: Step-by-step installation instructions
- **API Documentation**: Sphinx-generated documentation
- **Examples**: Demo data and usage examples
- **Troubleshooting**: Common issues and solutions

### Installation
- **Auto-installer**: `python install_fpm.py` handles everything automatically
- **Launcher Scripts**: `run_fpm.bat` (Windows) and `run_fpm.sh` (Linux/Mac)
- **Conda Support**: Environment file for scientific computing setups
- **pip Installation**: Standard Python package installation
- **Development Mode**: `pip install -e .` for contributors

---

## Future Releases

### Planned Features
- [ ] Batch processing for multiple datasets
- [ ] Additional FPM algorithms
- [ ] MATLAB code integration
- [ ] Advanced visualization tools
- [ ] Plugin system for custom algorithms
- [ ] Cloud processing capabilities
- [ ] Performance optimizations
- [ ] Extended export formats

### Known Issues
- Some algorithms (EPRY, Gauss-Newton, Kramers-Kronig) are placeholder implementations
- APIC algorithm needs full implementation
- Memory usage could be optimized for very large datasets

---

**For detailed information about each release, see the [GitHub Releases](https://github.com/hwzhou2020/FPM_software/releases) page.**
