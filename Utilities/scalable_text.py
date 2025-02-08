from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtCore import QObject, QEvent


class ZoomEventFilter(QObject):
    """Handles zoom events and updates text scaling."""
    def __init__(self, text_item, graphics_view):
        super().__init__(graphics_view)
        self.text_item = text_item
        self.graphics_view = graphics_view
        self.base_font_size = 16

    def eventFilter(self, obj, event):
        if event.type() == QEvent.GraphicsSceneWheel:
            self.update_scale()
        return super().eventFilter(obj, event)

    def update_scale(self):
        view_transform = self.graphics_view.transform().m11()
        font = QFont("Arial", int(self.base_font_size / view_transform), QFont.Bold)
        self.text_item.setFont(font)
