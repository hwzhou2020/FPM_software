import time
import numpy as np
from PySide6.QtGui import QImage, QPixmap, QColor, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem, QInputDialog, QApplication, QGraphicsView, QGraphicsTextItem
from PySide6.QtCore import Qt
from Utilities.logging_utils import log_message


def mat2gray(image):
    """Normalize image to range [0, 255] for display."""
    image = image - np.min(image)
    if np.max(image) > 0:
        image = image / np.max(image) * 255
    return image.astype(np.uint8)


def compute_spectrum(image):
    """Compute the log-transformed spectrum of an image."""
    spectrum = np.fft.fftshift(np.fft.fft2(image))
    spectrum = np.log(1 + np.abs(spectrum))
    return mat2gray(spectrum)


def display_image(ui, image, frame_number=None, total_frames=None):
    """Display an image in `display_window` with dynamic scaling and fixed-size frame number overlay."""
    scene = QGraphicsScene()
    height, width = image.shape

    # Normalize and convert image to 8-bit grayscale
    image = (image - image.min()) / (image.max() - image.min()) * 255
    image = image.astype(np.uint8)
    image = np.ascontiguousarray(image)  # Ensure C-contiguous memory

    q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)
    pixmap_item = scene.addPixmap(pixmap)

    # Add frame number overlay with a fixed size
    if frame_number is not None:
        text_item = QGraphicsTextItem(f"Frame {frame_number + 1}/{total_frames}")
        text_item.setDefaultTextColor(QColor("#F38181"))  # Soft coral color
        text_font = QFont("Arial", 16)
        text_font.setBold(True)
        text_item.setFont(text_font)

        # Ensure text size remains fixed regardless of zoom level
        text_item.setFlag(QGraphicsTextItem.ItemIgnoresTransformations, True)

        # Add text to scene and position it in the top-left corner
        scene.addItem(text_item)
        text_item.setPos(10, 10)

    # Update display window
    ui.display_window.setScene(scene)
    ui.display_window.setSceneRect(scene.itemsBoundingRect())
    ui.display_window.fitInView(pixmap_item, Qt.KeepAspectRatio)

    # Enable zooming and dragging
    ui.display_window.setDragMode(QGraphicsView.ScrollHandDrag)
    ui.display_window.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)


def display_single_raw_frame(main_window):
    """Prompt user for a frame number and display the selected raw image in `display_window`."""
    if not hasattr(main_window, "mat_data") or main_window.mat_data is None:
        main_window.ui.Msg_window.appendPlainText("Error: No data loaded. Please load a .mat file first.")
        return

    if "imlow" not in main_window.mat_data:
        main_window.ui.Msg_window.appendPlainText("Error: 'imlow' not found in .mat file.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]  # Number of frames in `imlow`

    # Ask the user for the frame number
    frame, ok = QInputDialog.getInt(
        main_window, "Select Frame",
        f"Enter frame number (1 to {num_frames}):",
        1, 1, num_frames, 1  # Default value, min value, max value, step
    )

    if ok:
        main_window.ui.Msg_window.appendPlainText(f"Displaying frame {frame} of {num_frames}.")
        display_image(main_window.ui, imlow[:, :, frame - 1], frame_number=frame-1, total_frames=num_frames)


def display_all_raw_frames(main_window):
    """Display all raw images sequentially in `display_window` with a short delay."""
    if not hasattr(main_window, "mat_data") or main_window.mat_data is None:
        main_window.ui.Msg_window.appendPlainText("Error: No data loaded. Please load a .mat file first.")
        return

    if "imlow" not in main_window.mat_data:
        main_window.ui.Msg_window.appendPlainText("Error: 'imlow' not found in .mat file.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]

    main_window.ui.Msg_window.appendPlainText(f"Displaying all {num_frames} frames sequentially.")

    for i in range(num_frames):
        main_window.ui.Msg_window.appendPlainText(f"Displaying frame {i + 1} of {num_frames}.")
        display_image(main_window.ui, imlow[:, :, i], frame_number=i, total_frames=num_frames)

        QApplication.processEvents()  # Allow UI updates
        time.sleep(0.1)  # Delay between frames


def display_single_raw_spectrum(main_window):
    """Prompt user for a frame number and display the spectrum of the selected raw image in `display_window`."""
    if not hasattr(main_window, "mat_data") or main_window.mat_data is None:
        main_window.ui.Msg_window.appendPlainText("Error: No data loaded. Please load a .mat file first.")
        return

    if "imlow" not in main_window.mat_data:
        main_window.ui.Msg_window.appendPlainText("Error: 'imlow' not found in .mat file.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]  # Number of frames in `imlow`

    # Ask the user for the frame number
    frame, ok = QInputDialog.getInt(
        main_window, "Select Frame",
        f"Enter frame number (1 to {num_frames}):",
        1, 1, num_frames, 1  # Default value, min value, max value, step
    )

    if ok:
        main_window.ui.Msg_window.appendPlainText(f"Displaying spectrum of frame {frame} of {num_frames}.")
        spectrum = compute_spectrum(imlow[:, :, frame - 1])
        display_image(main_window.ui, spectrum, frame_number=frame-1, total_frames=num_frames)


def display_all_raw_spectra(main_window):
    """Display all raw image spectra sequentially with a delay in `display_window`."""
    if not hasattr(main_window, "mat_data") or main_window.mat_data is None:
        main_window.ui.Msg_window.appendPlainText("Error: No data loaded. Please load a .mat file first.")
        return

    if "imlow" not in main_window.mat_data:
        main_window.ui.Msg_window.appendPlainText("Error: 'imlow' not found in .mat file.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]

    main_window.ui.Msg_window.appendPlainText(f"Displaying spectra of all {num_frames} frames sequentially.")

    for i in range(num_frames):
        main_window.ui.Msg_window.appendPlainText(f"Displaying spectrum of frame {i + 1} of {num_frames}.")
        spectrum = compute_spectrum(imlow[:, :, i])
        display_image(main_window.ui, spectrum, frame_number=i, total_frames=num_frames)

        QApplication.processEvents()  # Allow UI updates
        time.sleep(0.1)  # Delay between frames


def display_single_roi_image(main_window):
    """Displays a single ROI frame from the selected region."""
    if not main_window.mat_data or "imlow" not in main_window.mat_data:
        log_message(main_window.ui, "Error: No data loaded.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]  # Total frames

    if not hasattr(main_window, "roi_params") or not isinstance(main_window.roi_params, dict):
        log_message(main_window.ui, "Error: No ROI selected.")
        return

    roi_x = main_window.roi_params.get("x_offset", 1)
    roi_y = main_window.roi_params.get("y_offset", 1)
    roi_size = main_window.roi_params.get("roi_size", 256)

    roi_image = imlow[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size, 0]  # First frame

    log_message(main_window.ui, f"Displaying ROI frame 1 of {num_frames}.")
    display_image(main_window.ui, roi_image, frame_number=0, total_frames=num_frames)



def display_all_roi_images(main_window):
    """Displays all ROI frames sequentially with a 0.1s delay."""
    if not main_window.mat_data or "imlow" not in main_window.mat_data:
        log_message(main_window.ui, "Error: No data loaded.")
        return

    imlow = main_window.mat_data["imlow"]
    num_frames = imlow.shape[2]  # Total frames

    if not hasattr(main_window, "roi_params") or not isinstance(main_window.roi_params, dict):
        log_message(main_window.ui, "Error: No ROI selected.")
        return

    roi_x = main_window.roi_params.get("x_offset", 1)
    roi_y = main_window.roi_params.get("y_offset", 1)
    roi_size = main_window.roi_params.get("roi_size", 256)

    for i in range(num_frames):
        roi_image = imlow[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size, i]

        log_message(main_window.ui, f"Displaying ROI frame {i+1} of {num_frames}.")
        display_image(main_window.ui, roi_image, frame_number=i, total_frames=num_frames)

        QApplication.processEvents()
        time.sleep(0.1)



def display_result_image(main_window, result_type="amplitude"):

    if not hasattr(main_window, "reconstruction_result"):
        log_message(main_window.ui, "Error: No reconstruction results available.")
        return

    image = main_window.reconstruction_result.get(result_type)
    if image is None:
        log_message(main_window.ui, f"Error: {result_type} result not found.")
        return

    # Convert pupil to phase for display
    if result_type == "pupil":
        image = np.angle(image)

    # if it is all zeros, just display zeros to avoid division by zero
    if np.all(image == 0):
        log_message(main_window.ui, "Warning: Result image is all zeros. Displaying zero image.")
        image_uint8 = np.zeros_like(image)
    else:
        # Normalize and convert to 8-bit image
        image = (image - np.min(image)) / (np.max(image) - np.min(image) + 1e-8) * 255
        image_uint8 = image.astype(np.uint8)
        image_uint8 = np.ascontiguousarray(image_uint8)  # Ensure memory layout

    display_image(main_window.ui, image_uint8, frame_number=None, total_frames=None)
    # h, w = image.shape
    # q_image = QImage(image_uint8.data, w, h, w, QImage.Format_Grayscale8)
    # pixmap = QPixmap.fromImage(q_image)

    # # Create scene and add image
    # scene = QGraphicsScene()
    # pixmap_item = scene.addPixmap(pixmap)

    # # Add title overlay
    # # title = result_type.capitalize() + " result"
    # # text_item = QGraphicsSimpleTextItem(title)
    # # text_item.setBrush(QColor("#4A90E2"))
    # # text_item.setFont(QFont("Arial", 16))
    # # text_item.setPos(10, 10)
    # # scene.addItem(text_item)

    # # Display
    # main_window.ui.display_window.setScene(scene)
    # main_window.ui.display_window.setSceneRect(scene.itemsBoundingRect())
    # main_window.ui.display_window.fitInView(pixmap_item, Qt.KeepAspectRatio)
    # main_window.ui.display_window.setDragMode(QGraphicsView.ScrollHandDrag)
    # main_window.ui.display_window.setTransformationAnchor(main_window.ui.display_window.AnchorUnderMouse)

    # log_message(main_window.ui, f"Displayed {title}.")
