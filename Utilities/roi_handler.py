from PySide6.QtWidgets import (
    QGraphicsScene, QInputDialog, QGraphicsRectItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton
)
from PySide6.QtGui import QColor, QPen, QBrush, QImage, QPixmap
from PySide6.QtCore import Qt
import numpy as np
import os
from Utilities.logging_utils import log_message
from Utilities.display_handler import display_image


class MovableROI(QGraphicsRectItem):
    """A moveable ROI box that aligns with the displayed image's top-left corner."""
    def __init__(self, x, y, size, main_window, scale_factor, image_scene_x, image_scene_y):
        super().__init__((x - 1) * scale_factor + image_scene_x, (y - 1) * scale_factor + image_scene_y, 
                         size * scale_factor, size * scale_factor)
        self.main_window = main_window
        self.scale_factor = scale_factor
        self.image_scene_x = image_scene_x  # Top-left corner of image in scene
        self.image_scene_y = image_scene_y
        self.setBrush(QBrush(QColor(255, 255, 153, 100)))  # Light yellow fill
        self.setPen(QPen(Qt.yellow, 2))  # Yellow border
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)

    def mouseDoubleClickEvent(self, event):
        """On double-click, open ROI modification dialog with correct scaling."""
        scene_pos = self.sceneBoundingRect().topLeft()
        x_offset = int((scene_pos.x() - self.image_scene_x) / self.scale_factor) + 1
        y_offset = int((scene_pos.y() - self.image_scene_y) / self.scale_factor) + 1

        modify_roi_dialog(self.main_window, self, x_offset, y_offset, int(self.rect().width() / self.scale_factor))


def select_roi_size(main_window):
    """Prompt user for ROI size selection."""
    if not main_window.mat_data or "imlow" not in main_window.mat_data:
        log_message(main_window.ui, "Error: No data loaded.")
        return

    imlow = main_window.mat_data["imlow"]
    max_size = min(imlow.shape[0], imlow.shape[1])

    size, ok = QInputDialog.getInt(
        main_window, "Set ROI Size",
        f"Enter ROI size (64 to {max_size} pixels):",
        64, 64, max_size, 1
    )

    if ok:
        main_window.roi_size = size
        log_message(main_window.ui, f"ROI size set to {size} pixels.")
        display_image_with_roi(main_window)


def display_image_with_roi(main_window):
    """Display the first frame and overlay a moveable ROI box aligned to the displayed image."""
    if not main_window.mat_data or "imlow" not in main_window.mat_data:
        log_message(main_window.ui, "Error: Set ROI size first.")
        return

    imlow = main_window.mat_data["imlow"]
    scene = QGraphicsScene()
    image = imlow[:, :, 0]  # First frame

    # Normalize and convert image
    image = (image - image.min()) / (image.max() - image.min()) * 255
    image = image.astype(np.uint8)
    image = np.ascontiguousarray(image)

    height, width = image.shape
    q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(q_image)
    pixmap_item = scene.addPixmap(pixmap)

    # Get the displayed image's bounding box inside the scene
    main_window.ui.display_window.setScene(scene)
    main_window.ui.display_window.fitInView(pixmap_item, Qt.KeepAspectRatio)
    main_window.ui.display_window.setSceneRect(scene.itemsBoundingRect())

    image_scene_rect = pixmap_item.sceneBoundingRect()
    image_scene_x, image_scene_y = int(image_scene_rect.x()), int(image_scene_rect.y())

    # Scaling factor to match displayed image size
    scale_factor = image_scene_rect.width() / width  # Ensure correct scaling

    roi_size = main_window.roi_size
    init_x = max(1, min(50, width - roi_size))  # Ensure valid range
    init_y = max(1, min(50, height - roi_size))

    roi_box = MovableROI(init_x, init_y, roi_size, main_window, scale_factor, image_scene_x, image_scene_y)
    scene.addItem(roi_box)

    main_window.roi_box = roi_box
    main_window.roi_scale_factor = scale_factor
    main_window.image_scene_x = image_scene_x
    main_window.image_scene_y = image_scene_y


def modify_roi_dialog(main_window, roi_box, x_offset, y_offset, size):
    """Dialog to modify ROI parameters and update position dynamically."""
    imlow = main_window.mat_data["imlow"]
    max_x, max_y = imlow.shape[1], imlow.shape[0]

    dialog = QDialog(main_window)
    dialog.setWindowTitle("Modify ROI Parameters")

    layout = QHBoxLayout()

    # ROI Controls
    controls_layout = QVBoxLayout()
    x_label, y_label, size_label = QLabel("X-Offset (px):"), QLabel("Y-Offset (px):"), QLabel("ROI Size (px):")
    x_spin, y_spin, size_spin = QSpinBox(), QSpinBox(), QSpinBox()

    # Set limits
    size_spin.setRange(64, min(max_x, max_y))
    x_spin.setRange(1, max_x - size + 1)
    y_spin.setRange(1, max_y - size + 1)

    x_spin.setValue(x_offset)
    y_spin.setValue(y_offset)
    size_spin.setValue(size)

    confirm_btn = QPushButton("Confirm")

    # Instructional Image
    img_label = QLabel()
    img_path = os.path.join(os.getcwd(), "icons", "ROI_instruct.jpg")

    if os.path.exists(img_path):
        img = QPixmap(img_path).scaled(200, 200, Qt.KeepAspectRatio)
        img_label.setPixmap(img)
    else:
        img_label.setText("Image not found")

    # Update ROI dynamically
    def update_roi():
        """Updates the position of the yellow ROI box dynamically."""
        new_x_offset = x_spin.value()
        new_y_offset = y_spin.value()
        new_size = size_spin.value()

        # Ensure ROI stays within bounds
        max_x_offset = max_x - new_size + 1
        max_y_offset = max_y - new_size + 1
        new_x_offset = min(max(1, new_x_offset), max_x_offset)
        new_y_offset = min(max(1, new_y_offset), max_y_offset)

        x_spin.setValue(new_x_offset)
        y_spin.setValue(new_y_offset)
        size_spin.setValue(new_size)

        roi_box.setRect((new_x_offset - 1) * main_window.roi_scale_factor + main_window.image_scene_x, 
                        (new_y_offset - 1) * main_window.roi_scale_factor + main_window.image_scene_y, 
                        new_size * main_window.roi_scale_factor, 
                        new_size * main_window.roi_scale_factor)

        main_window.ui.display_window.scene().update()

    x_spin.valueChanged.connect(update_roi)
    y_spin.valueChanged.connect(update_roi)
    size_spin.valueChanged.connect(update_roi)

    confirm_btn.clicked.connect(lambda: apply_roi_changes(main_window, roi_box, x_spin.value(), y_spin.value(), size_spin.value(), dialog))

    controls_layout.addWidget(x_label)
    controls_layout.addWidget(x_spin)
    controls_layout.addWidget(y_label)
    controls_layout.addWidget(y_spin)
    controls_layout.addWidget(size_label)
    controls_layout.addWidget(size_spin)
    controls_layout.addWidget(confirm_btn)

    layout.addLayout(controls_layout)
    layout.addWidget(img_label)
    
    dialog.setLayout(layout)
    dialog.exec()



def apply_roi_changes(main_window, roi_box, x_offset, y_offset, size, dialog):
    """Apply changes, update ROI parameters, System Specs UI, and display the first frame."""
    # Update ROI parameters in main_window
    main_window.roi_params = [x_offset, y_offset, size, size]  # Store in MainWindow

    # Log the update
    roi_text = f"[{x_offset}, {y_offset}, {size}, {size}]"
    main_window.ui.Msg_window.appendPlainText(f"ROI modified: {roi_text}")
    log_message(main_window.ui, f"ROI modified: {roi_text}")

    # If System Specs window is open, update ROI display field
    if main_window.system_specs_window:
        main_window.system_specs_window.update_roi_field(roi_text)  # Call update function

    # Display the first frame with the new ROI
    display_first_roi_frame(main_window, x_offset, y_offset, size)
    dialog.accept()



def display_first_roi_frame(main_window, x_offset, y_offset, size):
    """Extract and display the first frame of the ROI."""
    imlow = main_window.mat_data["imlow"]
    roi_image = imlow[y_offset:y_offset + size, x_offset:x_offset + size, 0]
    display_image(main_window.ui, roi_image, frame_number=0, total_frames=1)
