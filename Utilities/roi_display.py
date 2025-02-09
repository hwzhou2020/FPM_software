from PySide6.QtWidgets import QGraphicsScene, QInputDialog, QGraphicsRectItem
from PySide6.QtGui import QImage, QPixmap, QColor, QPen, QBrush
from PySide6.QtCore import Qt
import numpy as np
from .logging_utils import log_message


class MovableROI(QGraphicsRectItem):
    """A moveable ROI box that can be dragged around the image."""
    def __init__(self, x, y, size, main_window):
        super().__init__(x, y, size, size)
        self.main_window = main_window  # Store reference to MainWindow
        self.setBrush(QBrush(QColor(255, 255, 153, 100)))  # Light yellow
        self.setPen(QPen(Qt.yellow, 2))  # Yellow border
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)

    def mouseDoubleClickEvent(self, event):
        """On double-click, store the final ROI position and update UI."""
        x, y = int(self.x()), int(self.y())
        size = int(self.rect().width())

        # Ensure ROI stays within bounds
        max_x = self.main_window.imlow.shape[1] - size
        max_y = self.main_window.imlow.shape[0] - size
        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        self.main_window.update_roi_input(x, y, size, size) 


def set_roi_size(main_window):
    """Prompt user to enter ROI size and validate input."""
    if main_window.imlow is None:
        log_message(main_window.ui, "Error: No data loaded. Please load a .mat file first.")
        return

    max_size = main_window.imlow.shape[0]  # Max ROI size based on imlow dimensions
    size, ok = QInputDialog.getInt(
        main_window, "Set ROI size",
        f"Enter ROI size (64 to {max_size} pixels):",
        64, 64, max_size, 1  # Default=64, min=64, max=max_size, step=1
    )

    if ok:
        main_window.roi_size = size  # Store in main window
        log_message(main_window.ui, f"ROI size set to {size} pixels.")
        display_image_with_roi(main_window)


def display_image_with_roi(main_window):
    """Display the first imlow image and overlay a moveable ROI box."""
    if main_window.imlow is None or main_window.roi_size is None:
        log_message(main_window.ui, "Error: Set ROI size first.")
        return

    scene = QGraphicsScene()
    image = main_window.imlow[:, :, 0]  # First frame

    # Normalize image
    image = (image - image.min()) / (image.max() - image.min()) * 255
    image = image.astype(np.uint8)
    image = np.ascontiguousarray(image)

    # Convert NumPy array to QImage
    height, width = image.shape
    q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)
    pixmap_item = scene.addPixmap(pixmap)  # Add image to scene

    # Create a moveable ROI box at (50,50) initially
    roi_size = main_window.roi_size
    roi_box = MovableROI(50, 50, roi_size, main_window) 
    scene.addItem(roi_box)

    # Set scene to graphicsView
    main_window.ui.graphicsView.setScene(scene)
    main_window.ui.graphicsView.fitInView(pixmap_item, Qt.KeepAspectRatio)
    main_window.ui.graphicsView.setSceneRect(scene.itemsBoundingRect())

    # Store reference to ROI box
    main_window.roi_box = roi_box


def update_roi_input(main_window, x, y, width, height):
    """Update the ROI input field after user sets position."""
    roi_text = f"[{x}, {y}, {width}, {height}]"
    main_window.ui.ROI.setText(roi_text)
    log_message(main_window.ui, f"ROI selected: {roi_text}")


def preview_roi_image(main_window):
    """Display a selected frame with the ROI region highlighted."""
    if main_window.imlow is None:
        log_message(main_window.ui, "Error: No data loaded. Load data first.")
        return

    if main_window.roi_box is None:
        log_message(main_window.ui, "Error: Set ROI first.")
        return

    # Get the ROI dimensions from UI
    roi_text = main_window.ui.ROI.text()
    try:
        roi_values = [int(i) for i in roi_text.strip("[]").split(",")]
        if len(roi_values) != 4:
            raise ValueError
        x_offset, y_offset, width, height = roi_values
    except ValueError:
        log_message(main_window.ui, "Error: Invalid ROI format.")
        return

    num_frames = main_window.imlow.shape[2]  # Total frames in imlow

    # Prompt user for frame selection
    frame, ok = QInputDialog.getInt(
        main_window, "Select Frame",
        f"Enter frame number (1 to {num_frames}):",
        1, 1, num_frames, 1  # Default value, min, max, step
    )

    if not ok:
        return  # User canceled input

    # Extract the selected frame
    full_image = main_window.imlow[:, :, frame-1]

    # Ensure the ROI stays within bounds
    max_x = full_image.shape[1] - width
    max_y = full_image.shape[0] - height
    x_offset = min(max(x_offset, 0), max_x)
    y_offset = min(max(y_offset, 0), max_y)

    # Crop the ROI region
    roi_image = full_image[y_offset:y_offset+height, x_offset:x_offset+width]

    # Normalize image to [0, 255] range
    roi_image = (roi_image - roi_image.min()) / (roi_image.max() - roi_image.min()) * 255
    roi_image = roi_image.astype(np.uint8)
    roi_image = np.ascontiguousarray(roi_image)  # Ensure memory layout

    # Convert NumPy array to QImage
    q_image = QImage(roi_image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)

    # Display image in graphicsView
    scene = QGraphicsScene()
    scene.addPixmap(pixmap)

    # Update graphicsView
    main_window.ui.graphicsView.setScene(scene)
    main_window.ui.graphicsView.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
    main_window.ui.graphicsView.setSceneRect(scene.itemsBoundingRect())

    # Log result
    log_message(main_window.ui, f"Displaying ROI from frame {frame}.")


def preview_roi_sum(main_window):
    """Compute and display the sum of imlow in the selected ROI region."""
    if main_window.imlow is None:
        log_message(main_window.ui, "Error: No data loaded. Load data first.")
        return

    if main_window.roi_box is None:
        log_message(main_window.ui, "Error: Set ROI first.")
        return

    # Get the ROI dimensions from UI
    roi_text = main_window.ui.ROI.text()
    try:
        roi_values = [int(i) for i in roi_text.strip("[]").split(",")]
        if len(roi_values) != 4:
            raise ValueError
        x_offset, y_offset, width, height = roi_values
    except ValueError:
        log_message(main_window.ui, "Error: Invalid ROI format.")
        return

    # Extract and sum the ROI across all frames
    full_image_stack = main_window.imlow[y_offset:y_offset+height, x_offset:x_offset+width, :]
    summed_image = np.sum(full_image_stack, axis=2)  # Sum across frames

    # Normalize summed image to [0, 255]
    summed_image = (summed_image - summed_image.min()) / (summed_image.max() - summed_image.min()) * 255
    summed_image = summed_image.astype(np.uint8)
    summed_image = np.ascontiguousarray(summed_image)  # Ensure memory layout

    # Convert NumPy array to QImage
    q_image = QImage(summed_image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)

    # Display image in graphicsView
    scene = QGraphicsScene()
    scene.addPixmap(pixmap)

    # Update graphicsView
    main_window.ui.graphicsView.setScene(scene)
    main_window.ui.graphicsView.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
    main_window.ui.graphicsView.setSceneRect(scene.itemsBoundingRect())

    # Log result
    log_message(main_window.ui, f"Displaying summed ROI over all frames.")
