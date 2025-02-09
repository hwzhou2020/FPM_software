import time
import numpy as np
from PySide6.QtGui import QImage, QPixmap, QColor, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem, QInputDialog, QGraphicsView, QApplication
from PySide6.QtCore import Qt
from Utilities.logging_utils import log_message
from Utilities.scalable_text import ZoomEventFilter


def display_image(ui, image, frame_number=None, total_frames=None):
    """Display an image in graphicsView and scale text dynamically when zooming."""
    scene = QGraphicsScene()
    height, width = image.shape

    image = (image - image.min()) / (image.max() - image.min()) * 255
    image = image.astype(np.uint8)
    image = np.ascontiguousarray(image)

    q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)
    pixmap_item = scene.addPixmap(pixmap)

    if frame_number is not None:
        text_item = QGraphicsSimpleTextItem(f"Frame {frame_number + 1}/{total_frames}")
        text_item.setBrush(QColor("#F38181"))  # Soft coral color
        text_item.setFont(QFont("Arial", 14))
        scene.addItem(text_item)
        text_item.setPos(10, 10)

        zoom_filter = ZoomEventFilter(text_item, ui.graphicsView)
        ui.graphicsView.viewport().installEventFilter(zoom_filter)

    ui.graphicsView.setScene(scene)
    ui.graphicsView.setSceneRect(scene.itemsBoundingRect())
    ui.graphicsView.fitInView(pixmap_item, Qt.KeepAspectRatio)

    # ✅ Corrected Drag Mode Assignment
    ui.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)  # Correct reference

    ui.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    zoom_filter.update_scale()


def display_single_raw_image(main_window):
    """Prompt user for frame number and display the selected raw image."""
    if main_window.imlow is None:
        log_message(main_window.ui, "Error: No data loaded. Please load a .mat file first.")
        return

    num_frames = main_window.imlow.shape[2]  # Number of frames in imlow

    frame, ok = QInputDialog.getInt(
        main_window, "Select Frame",
        f"Enter frame number (1 to {num_frames}):",
        1, 1, num_frames, 1  # Default value, min value, max value, step
    )

    if ok:
        log_message(main_window.ui, f"Displaying frame {frame} of {num_frames}.")
        display_image(main_window.ui, main_window.imlow[:, :, frame-1], frame_number=frame, total_frames=num_frames)



def display_all_raw_images(main_window):
    """Display all raw images sequentially with a 0.1s delay and show frame number."""
    if main_window.imlow is None:
        log_message(main_window.ui, "Error: No data loaded. Please load a .mat file first.")
        return

    num_frames = main_window.imlow.shape[2]
    log_message(main_window.ui, f"Displaying all {num_frames} frames sequentially.")

    for i in range(num_frames):
        log_message(main_window.ui, f"Displaying frame {i + 1} of {num_frames}.")
        display_image(main_window.ui, main_window.imlow[:, :, i], frame_number=i, total_frames=num_frames)
        
        QApplication.processEvents()  
        time.sleep(0.1)  # Delay of 0.1s between frames
