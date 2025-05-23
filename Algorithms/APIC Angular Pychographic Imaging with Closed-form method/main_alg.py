import numpy as np
from .apic_core import apic_reconstruction
import yaml
import os

def run_algorithm(system_params, roi_params, mat_data, log_callback=None, progress_callback=None):
    I_low = mat_data["imlow"].astype("float32")
    H, W, _ = I_low.shape

    cx = roi_params.get("x_offset", W // 2)
    cy = roi_params.get("y_offset", H // 2)
    roi_size = roi_params.get("roi_size", 256)

    I_ROI = I_low[cy:cy + roi_size, cx:cx + roi_size, :]
    I_ROI = I_ROI[:roi_size, :roi_size, :]

    NA = float(mat_data.get("NA", 0.1))
    dpix_cam = float(mat_data.get("dpix_c", 3.45))
    wavelength = float(mat_data.get("lambda", 0.5))
    mag = float(mat_data.get("mag", 10.0))
    dpix = dpix_cam / mag

    # kx, ky generation
    NA_list = mat_data["NA_list"]
    kx = NA_list[:, 0] * 2 * np.pi / wavelength
    ky = NA_list[:, 1] * 2 * np.pi / wavelength

    if progress_callback:
        progress_callback(10)

    amp, phase, pupil = apic_reconstruction(I_ROI, kx, ky, NA, wavelength, dpix)

    if progress_callback:
        progress_callback(100)

    return amp, phase, pupil