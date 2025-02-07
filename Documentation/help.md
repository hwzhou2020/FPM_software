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

```plaintext
FPM software/
│── my_package/           # Package directory
│   ├── __init__.py       # Package initializer
│   ├── module1.py        # First module
│── tests/                # Tests directory
│   ├── test_module1.py   # Test file
│── setup.py              # Packaging instructions
│── README.md             # Documentation
│── requirements.txt      # Dependencies (optional)
│── LICENSE               # License file (optional)
│── .gitignore            # Ignore unnecessary files
```

## 2. Data Format
