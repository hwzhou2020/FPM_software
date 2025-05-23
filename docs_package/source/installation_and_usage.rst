Installation and Usage
======================

This guide explains how to set up and run the Fourier Ptychographic Microscopy (FPM) software.

Installation
------------

1. **Install Miniconda or Anaconda** (if not already installed):
   https://docs.conda.io/en/latest/miniconda.html

2. **Navigate to the `docs_package` directory** in your terminal and create the environment:

   .. code-block:: bash

       conda env create -f environment.yml

3. **Activate the environment**:

   .. code-block:: bash

       conda activate fpm_env

4. **Launch the software**:

   .. code-block:: bash

       python ../main.py

   Make sure you're inside the `docs_package` directory or adjust the path accordingly.

Usage
-----

Once the GUI launches, the software provides the following features via the menu bar:

- **File > Load Data**: Load raw microscopy data from `.mat` files.
- **Display > Single raw frame / All raw frames**: Visualize single or all raw images.
- **Display > Single/All raw spectra**: View Fourier transforms of the raw frames.
- **Display > ROI tools**: Select and inspect regions of interest.
- **Specs > System Specs / Algorithm Specs**: Set physical and algorithm parameters.
- **MessageBox > Clear Messages**: Clear status log output.

Each function is triggered by a combination of `QMenu` actions and handlers defined in `Utilities/*.py` and `WindowUI/*.py`.

Tips
----

- Supported `.mat` files must contain a `data["imlow"]` field with 3D image stacks.
- Spectral tools assume image data is real and non-negative.
- ROI selections are interactive and can be fine-tuned before reconstruction.