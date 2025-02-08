import numpy as np
from .logging_utils import log_message


def format_scalar(value):
    """Convert single-element arrays/lists to scalars for display."""
    if isinstance(value, np.ndarray) and value.size == 1:
        return str(value.item())  # Convert array to scalar
    elif isinstance(value, list) and len(value) == 1:
        return str(value[0])  # Convert list to scalar
    elif isinstance(value, (int, float)):
        return str(value)  # Already a scalar
    else:
        return "Invalid Data"


def update_ui_fields(main_window):
    """Update UI fields with loaded .mat file data and validate NA_list."""
    if main_window.mat_data is None:
        log_message(main_window.ui, "Error: No data loaded.")
        return

    # Update UI fields
    main_window.ui.mag.setText(format_scalar(main_window.mag))  # Magnification
    main_window.ui.NA.setText(format_scalar(main_window.NA))  # NA values
    main_window.ui.pix_size.setText(format_scalar(main_window.dpix_c))  # Pixel size
    main_window.ui.Lambda.setText(format_scalar(main_window.lambda_))  # Wavelength

    # Validate NA_list and imlow consistency
    if main_window.imlow is None or not isinstance(main_window.imlow, np.ndarray):
        log_message(main_window.ui, "Error: imlow data is missing or corrupted.")
        main_window.ui.NA_list.setText("Error: imlow missing")
        return

    if isinstance(main_window.NA_list, np.ndarray) and main_window.NA_list.shape[0] == main_window.imlow.shape[2]:
        main_window.ui.NA_list.setText("loaded")
        log_message(main_window.ui, "NA_list is loaded correctly.")
    else:
        main_window.ui.NA_list.setText("Error: NA_list is not loaded correctly")
        log_message(main_window.ui, "Error: NA_list does not match the number of raw images.")
