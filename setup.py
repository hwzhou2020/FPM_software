#!/usr/bin/env python3
"""
Setup script for FPM Software
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fpm-software",
    version="1.0.0",
    author="Haowen Zhou",
    author_email="",
    description="Fourier Ptychographic Microscopy reconstruction software",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/hwzhou2020/FPM_software",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "fpm-software=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.qss", "*.ui", "*.yml", "*.png", "*.jpg"],
    },
)
