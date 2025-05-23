import numpy as np
import torch
import torch_dct
import scipy.io as sio

def apic_reconstruction(I_low, kx, ky, NA, wavelength, dpix, padding=2):
    """
    Perform APIC complex field reconstruction.

    Parameters:
        I_low (np.ndarray): Stack of low-resolution intensity images (H x W x N)
        kx, ky (np.ndarray): Illumination wave vectors (N,)
        NA (float): Numerical aperture
        wavelength (float): Wavelength in um
        dpix (float): Pixel size at sample plane in um
        padding (int): Padding factor for high-resolution reconstruction

    Returns:
        amp (np.ndarray): Amplitude of reconstructed field
        phase (np.ndarray): Phase of reconstructed field
        pupil (np.ndarray): Reconstructed pupil function
    """
    # Convert inputs to torch tensors
    I_tensor = torch.from_numpy(I_low).float()
    kx = torch.from_numpy(kx).float()
    ky = torch.from_numpy(ky).float()

    # Basic Fourier-based reconstruction placeholder (replace with APIC logic)
    H, W, N = I_tensor.shape
    HR_shape = (H * padding, W * padding)
    recon = torch.zeros(HR_shape, dtype=torch.cfloat)
    pupil = torch.ones_like(recon)

    for i in range(N):
        shifted = torch.fft.fft2(I_tensor[:, :, i], s=HR_shape)
        recon += shifted

    recon /= N
    amp = torch.abs(recon)
    phase = torch.angle(recon)
    return amp.numpy(), phase.numpy(), pupil.numpy()