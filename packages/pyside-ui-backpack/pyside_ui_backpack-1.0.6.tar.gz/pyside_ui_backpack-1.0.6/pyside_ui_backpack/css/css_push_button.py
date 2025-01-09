try:
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QPushButton
except ImportError:
    from PySide6.QtGui import QColor
    from PySide6.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QPushButton

from pyside_ui_backpack.css.colors import Colors


def style_push_button(
    qt_window: QMainWindow,
    button: QPushButton,
    color: Colors = Colors.GREY,
    shadow: bool = True,
):
    """Apply style to a QPushButton widget.

    Colors are:
            red for red/white
            orange for orange/black
            disabled for gray/gray
            blue for blue/white
            green for green/black
            lightgrey for lightgrey/white
            black for dark-gray/white
            gray for gray/white (default)

    shadow is a boolean to enable/disable shadow effect

    Args:
        qt_window (QMainWindow): parent QMainWindow
        button (QPushButton): QPushButton widget
        color (Colors, optional): color theme. Defaults to Colors.GRAY.
        shadow (bool, optional): enable/disable shadow effect. Defaults to True.
    """

    css_basic_btn = """
        color:{};
        background:{};
        font-size:12px;
        font-family:Segoe UI;
        """.format(color.value.foreground_color, color.value.background_color)

    button.setStyleSheet(css_basic_btn)

    if shadow:
        shadow = QGraphicsDropShadowEffect(qt_window)
        shadow.setBlurRadius(6)
        shadow.setOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        button.setGraphicsEffect(shadow)
