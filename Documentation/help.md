# FPM Software Help Guide (v2.0 Professional)

## Overview
This guide summarizes the most common tasks in the Professional Edition of the FPM Software: installing the app, loading data, running reconstructions, and saving or reloading results.

---

## Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/hwzhou2020/FPM_software.git
   cd FPM_software
   ```
2. **Launch the professional UI**
   ```bash
   python launch_fpm_professional.py
   ```
   If the splash screen causes a `QPaintDevice` warning, run `python launch_fpm_no_splash.py` instead.

---

## Loading Data
- Click **Load** (or press `Ctrl+O`).
- The dialog now opens in the bundled `data/` folder by default.
- Select a `.mat` data set. The app validates the required fields (`imlow`, `NA_list`, etc.) and reports issues in the message window.

### Recent Files
Successfully loaded files are tracked in the recent file list and can be reopened quickly via the **Specs → Load Specs** menu.

---

## Running a Reconstruction
1. Load data as described above.
2. Choose an algorithm from **Specs → Algorithm specs**.
3. (Optional) Adjust algorithm parameters when prompted.
4. Click **Run** or press `Ctrl+R`.
5. Monitor progress in the status bar; logs stream into the message window.
6. The amplitude result displays automatically when processing finishes.

### Viewing Other Outputs
Use **Display → …** or the Help menu actions to view raw frames, spectra, amplitude, phase, or pupil results after a reconstruction completes.

---

## Saving & Reloading Results
- After a successful run, the **Save** button and **File → Save Results** become available.
- Results are written to the `Results/` folder inside the repository (created automatically). The save file contains amplitude, phase, pupil arrays, algorithm parameters, ROI info, and the source data name.
- To open a saved result later, choose **File → Load Results** and select the `.mat` or `.npy` archive. The reconstruction data and metadata are restored and ready for display.

---

## Keyboard Shortcuts
- `Ctrl+O` – Load data
- `Ctrl+R` – Run selected algorithm
- `Ctrl+Shift+S` – Set save directory
- `Ctrl+Q` – Exit the application
- `F1` – Open documentation

---

## Troubleshooting
- **No output after loading** – Ensure the `.mat` file contains the required `imlow` (3D) and `NA_list` (2D) arrays.
- **Memory errors** – Reduce ROI size or algorithm upsampling parameters.
- **Torch not installed** – Rerun `python install_fpm.py` on macOS; the installer now handles Apple Silicon wheels automatically.
- **GUI issues** – Launch with `launch_fpm_no_splash.py` to bypass animated splash screens.

For full API documentation and detailed UI notes see:
- `INSTALL.md`
- `PROFESSIONAL_UI_IMPROVEMENTS.md`
- `docs_package/build/html/index.html`
