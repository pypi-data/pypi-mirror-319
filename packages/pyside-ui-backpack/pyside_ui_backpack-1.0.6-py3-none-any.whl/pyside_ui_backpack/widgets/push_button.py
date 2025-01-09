try:
    from PySide2.QtCore import QSize
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import (
        QGraphicsDropShadowEffect,
        QMainWindow,
        QPushButton,
        QSizePolicy,
    )
except ImportError:
    from PySide6.QtCore import QSize
    from PySide6.QtGui import QColor
    from PySide6.QtWidgets import (
        QGraphicsDropShadowEffect,
        QMainWindow,
        QPushButton,
        QSizePolicy,
    )

from pyside_ui_backpack.css.colors import Colors


class PushButton(QPushButton):
    def __init__(
        self,
        parent: QMainWindow = None,
        qt_name: str = 'push_button',
        text: str = 'button',
        size: tuple = None,
        color: Colors = Colors.GREY,
        shadow: bool = True,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        """ creates a custom QPushButton widget

        Args:
            parent (ui): parent ui class. Defaults to None.
            qt_name (str): qt widget name. Defaults to 'button'.
            text (str, optional): button text. Defaults to 'button'.
            size (int tuple, optional): widget size. Defaults to None.
            color (Colors, optional): color theme. Defaults to Colors.GRAY.
            shadow (bool, optional): applies shadow. Defaults to True.
        """
        self.setObjectName(qt_name)

        # text
        self.setText(text)

        # size
        if size:
            btn_size = QSize(size[0], size[1])
            self.setMinimumSize(btn_size)
            self.setMaximumSize(btn_size)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.setSizePolicy(size_policy)

        # css & color theme
        css = """
            QPushButton {
                background-color: %s;
                color: %s;
                border-radius: 3;
                font-size: 12px;
                font-family: Segoe UI;
                font-weight: bold;
            }

            QPushButton:hover {
                border: 1px solid rgb(235, 235, 235);
            }

            QPushButton:pressed {
                background-color: rgb(60, 60, 60);
            }
        """ % (color.value.background_color, color.value.foreground_color)

        self.setStyleSheet(css)

        # shadow
        if shadow:
            shadow = QGraphicsDropShadowEffect(parent)
            shadow.setBlurRadius(6)
            shadow.setOffset(4)
            shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(shadow)
