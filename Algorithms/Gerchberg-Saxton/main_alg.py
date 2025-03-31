import numpy as np
from scipy.ndimage import zoom
import torch
import os

def run_algorithm(system_params, roi_params, mat_data, log_callback=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Extract raw intensity images
    I_low = mat_data["imlow"].astype("float32")
    H, W, _ = I_low.shape

    # Extract ROI
    cx = roi_params.get("x_offset", W // 2)
    cy = roi_params.get("y_offset", H // 2)
    roi_size = roi_params.get("roi_size", 256)

    I_ROI = I_low[cy:cy + roi_size, cx:cx + roi_size, :]
    I_ROI = I_ROI[:roi_size, :roi_size, :]  # Ensures fixed size

    # Load system parameters
    NA = float(mat_data.get("NA", 0.1))
    dpix_cam = float(mat_data.get("dpix_c", 3.45))
    wavelength = float(mat_data.get("lambda", 0.5))
    mag = float(mat_data.get("mag", 10.0))
    NA_cal = float(mat_data.get("NA", NA))
    NA_cal_list = mat_data["NA_list"].astype("float32")

    dpix = dpix_cam / mag
    k0 = 2 * np.pi / wavelength
    kmax = NA_cal * k0

    # Parameters
    upsample = int(system_params.get("upsample", 3))
    alpha = float(system_params.get("alpha", 1.0))
    beta = float(system_params.get("beta", 0.1))
    num_iters = int(system_params.get("num_iters", 50))
    mode = system_params.get("mode", "all")
    tol = float(system_params.get("tol", 0.05))
    use_pupil_correction = False

    N = I_ROI.shape[0]
    N_up = N * upsample

    # Frequency grid
    Fxx1, Fyy1 = np.meshgrid(np.arange(-N_up // 2, N_up // 2), np.arange(-N_up // 2, N_up // 2))
    Fxx1 = Fxx1[0, :] / (N * dpix) * (2 * np.pi)
    Fyy1 = Fyy1[:, 0] / (N * dpix) * (2 * np.pi)

    # Sort by illumination angle
    u = -NA_cal_list[:, 0]
    v = -NA_cal_list[:, 1]
    NAillu = np.sqrt(u**2 + v**2)
    order = np.argsort(NAillu)
    u = u[order]
    v = v[order]
    I_ROI = I_ROI[:, :, order]
    NAillu = NAillu[order]

    # Select mode
    if mode == "bright":
        idx = np.where(NAillu <= NA + tol)[0]
    elif mode == "dark":
        idx = np.where(NAillu > NA + tol)[0]
    else:
        idx = np.arange(len(NAillu))

    u = u[idx]
    v = v[idx]
    I = I_ROI[:, :, idx]
    ID_len = len(idx)

    # LED positions in frequency space
    ledpos = np.zeros((ID_len, 2), dtype=int)
    for i in range(ID_len):
        ledpos[i, 0] = np.argmin(np.abs(Fxx1 - k0 * u[i]))
        ledpos[i, 1] = np.argmin(np.abs(Fyy1 - k0 * v[i]))

    # Normalize and define pupil function
    Isum = I / np.max(I)
    Fx1, Fy1 = np.meshgrid(np.arange(-N / 2, N / 2), np.arange(-N / 2, N / 2))
    Fxy2 = ((Fx1 / (N * dpix) * 2 * np.pi) ** 2 + (Fy1 / (N * dpix) * 2 * np.pi) ** 2)
    Pupil = np.zeros((N, N))
    Pupil[Fxy2 <= kmax**2] = 1
    Pupil0 = torch.from_numpy(Pupil.astype("float32")).to(device)

    # Initial guess
    o = np.sqrt(zoom(Isum[:, :, 0], upsample, order=1)).astype("complex64")
    O = torch.fft.fftshift(torch.fft.fft2(torch.from_numpy(o).to(device)))

    # Prepare tensors
    Pupil = Pupil0.clone().to(torch.complex64)
    Isum = torch.from_numpy(Isum).to(device)
    ledpos = torch.from_numpy(ledpos).to(device)
    PupilSUM = torch.zeros_like(O)
    error_bef = 1e10

    for iter in range(num_iters):
        error_now = 0

        if log_callback:
            log_callback(f"Iteration {iter+1}/{num_iters}...")

        for i in range(ID_len):
            uo, vo = ledpos[i]
            temp = O[vo - N // 2:vo + N // 2, uo - N // 2:uo + N // 2]
            OP_bef = temp * Pupil * Pupil0 / (upsample ** 2)
            o_bef = torch.fft.ifft2(torch.fft.fftshift(OP_bef))
            oI_bef = torch.abs(o_bef)**2
            oI_cap = Isum[:, :, i]

            if torch.mean(oI_cap) > 0.1 and torch.mean(oI_bef) > 0.1:
                o_aft = torch.sqrt(oI_cap) / torch.sqrt(oI_bef) * o_bef
            else:
                o_aft = o_bef

            OP_aft = torch.fft.fftshift(torch.fft.fft2(o_aft))
            OP_diff = OP_aft - OP_bef

            O[vo - N // 2:vo + N // 2, uo - N // 2:uo + N // 2] = temp + alpha * OP_diff * \
                torch.abs(Pupil) * torch.conj(Pupil) / torch.abs(Pupil).max() / \
                (torch.abs(Pupil) ** 2 + 1) * torch.conj(Pupil0)

            if use_pupil_correction:
                Pupil += beta * OP_diff * torch.abs(OP_bef) * torch.conj(OP_bef) / \
                    torch.abs(temp).max() / (torch.abs(OP_bef) ** 2 + 1000) * torch.conj(Pupil0)
            else:
                Pupil = Pupil0 * torch.exp(1j * torch.angle(Pupil))

            if iter == 0:
                PupilSUM[vo - N // 2:vo + N // 2, uo - N // 2:uo + N // 2] = Pupil0 + \
                    PupilSUM[vo - N // 2:vo + N // 2, uo - N // 2:uo + N // 2] * (torch.ones_like(Pupil0) - Pupil0.abs())
            else:
                O *= PupilSUM

            error_now += torch.sum((torch.abs(o_bef) - torch.sqrt(oI_cap)) ** 2)

        if iter > 0 and (error_bef - error_now) / error_bef < 0.01:
            alpha *= 0.5
            beta *= 0.5
            if alpha < 1e-4:
                break
        error_bef = error_now

    # Final reconstruction
    o = torch.fft.ifft2(torch.fft.fftshift(O))
    AmpReconFPM = torch.abs(o)
    PhaseReconFPM = torch.angle(o)

    return AmpReconFPM, PhaseReconFPM, Pupil
