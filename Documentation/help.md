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
│   │── file_handling.py       # Handles file loading & dialogs
│   │── logging_utils.py       # Manages message logging
│   │── image_display.py       # Image rendering & display functions
│   │── interactive_view.py    # Custom graphics view for zooming & panning
│   │── scalable_text.py       # Manages dynamic text scaling
│   │── data_handler.py        # UI field updates for .mat file variables
│   │── roi_display.py         # Handles ROI selection & movement ✅
│── Documentation/
│   |── HELP.md
|── ReadMe.md
│── .gitignore            # Ignore unnecessary files
│── .gitattributes
```

## 2. Data Format
