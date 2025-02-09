# HELP Guide for FPM software

## Introduction
This tutorial will guide you through installation, demo and background knowledge for Fourier ptychographic microscopy.

---

## Prerequisites
Ensure you have:
- Python 3.6+
- `pip` and `setuptools` installed
- Basic knowledge of Python
- A desktop GPU is recommended but not necessary

---

## 1. Project Structure

```
FPM_software/
│── main.py
│── File_ui.py
│── File.ui
│── Utilities/
│   │── __init__.py
│   │── data_handler.py        # UI field updates for .mat file variables
│   │── file_handling.py       # Handles file loading & dialogs
│   │── image_display.py       # Image rendering & display functions
│   │── interactive_view.py    # Custom graphics view for zooming & panning
|   │── logging_utils.py       # Manages message logging
│   │── roi_display.py         # Handles ROI selection & movement 
│   │── scalable_text.py       # Manages dynamic text scaling
│── Documentation/
│   |── HELP.md
│── Algorithms/                # Contains all different algorithm modules
│   |── APIC Angular Pychographic Imaging with Closed-form method/
│   |── EPRY Embedded pupil function recovery/
│   |── Gauss-Newton/
│   |── Gerchberg-Saxton/
│   |── KK Kramers-Kronig/
|── ReadMe.md
│── .gitignore            # Ignore unnecessary files
│── .gitattributes
```

## 2. Data Format
