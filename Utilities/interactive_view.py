from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent


class ZoomableGraphicsView(QGraphicsView):
    """Custom QGraphicsView with zoom and pan functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.15

    def wheelEvent(self, event: QWheelEvent):
        """Zoom in/out using the mouse wheel."""
        zoom_in = event.angleDelta().y() > 0
        factor = self.zoom_factor if zoom_in else 1 / self.zoom_factor
        self.scale(factor, factor)
