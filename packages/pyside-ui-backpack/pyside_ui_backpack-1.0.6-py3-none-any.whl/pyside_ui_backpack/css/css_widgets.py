"""Arcane2 Widgets CSS."""
try:
    from PySide2.QtWidgets import (
        QCheckBox,
        QComboBox,
        QGroupBox,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMenu,
    )
except ImportError:
    from PySide6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QGroupBox,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMenu,
    )


main_css = """

    QPushButton {
        color: rgb(230, 230, 230);
        font: bold;
        font-size: 12px;
    }

    QMainWindow {
        background: red;
    }

    QDialog {
        background: rgb(40, 40, 40);
    }

    QWidget {
        font-family : Segoe UI;
        font-style : normal;
    }

    QFrame {
        color: rgb(40,40,40);
    }

    QLabel {
        background: rgb(60,60,60);
        color: white;
    }

    QLineEdit {
        color: white;
        background-color: rgb(30,30,30);
    }

    QCheckBox {
        color: rgb(230, 230, 230);
    }

    QCheckBox:indicator:checked
    {
        background-color: rgb(52, 152, 219);
        border: 1px solid rgb(50, 50, 50);
    }

    QCheckBox:indicator:disabled
    {
        color: rgb(100,100,100);
        background-color: rgb(100, 100, 100);
        border: 1px solid rgb(100, 100, 100);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator
    {
        background-color: rgb(50,50,50);
        border: 1px solid rgb(120,120,120);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator:hover
    {
        border: 1px solid rgb(200, 200, 200);
    }

    """

qmenu_css = """
    QMenuBar {
        background: rgb(50,50,50);
        color: rgb(250,250,250);
    }

    QMenuBar:item {
        background: rgb(50,50,50);
        color: rgb(250,250,250);
    }

    QMenu:separator {
        height: 1px;
        background: rgb(60,60,60);
    }
    """

# lite progress bar, transparent background, blue line
pb_bar_lite_css = """
        QProgressBar {
            background: rgb(0, 0, 0, 0);
            color: rgb(235, 235, 235);
            border-style: none;
            text-align: center;
            }
        QProgressBar::chunk {
            background-color: rgb(46, 134, 193);
            margin: 9px;
            border-radius: 10px;
            }
        """


combobox_css = """
    /* base css */
    QComboBox {
        font-family : Segoe UI;
        font-size : 12px;
        font-style : normal;
        border-radius: 1;
        border-style: solid;
        subcontrol-origin: padding;
        subcontrol-position: top right;
        padding: 1px 0px 1px 6px;
    }

    QComboBox::drop-down {
        width: 20px;
        border: 0px;
        background: rgb(40, 40, 40);
        border-color: rgb(60, 60, 60);
        border-left-style:solid;
        border-top-style: none;
        border-bottom-style: none;
        border-right-style: none;
    }

    QComboBox::drop-down:hover {
    }

    /* arrow icon on rest state */
    QComboBox::down-arrow {
        width: 16; height: 16px;
        background: rgb(0, 0, 0, 0);
        image: url(:/dd_left);
    }

    QComboBox::down-arrow:hover {
        image: url(:/dd_hover);
    }

    /* arrow icon when opened */
    QComboBox::down-arrow:on {
        image: url(:/dd_down);
    }

    /* main window when is closed or not editable (in rest state)*/
    QComboBox:!editable, QComboBox:!open {
        background: rgb(40, 40, 40);
        color: rgb(220, 220, 200);
    }

    /* arrow icon when windows is on focus */
    /* main window when opened for selection */
    QComboBox:open {
        /*background: red;*/
    }

    /* items inside cbox */
    QComboBox QAbstractItemView {
        border: 1px solid darkgray;
        selection-background-color: rgb(230, 230, 230);
        selection-color: rgb(30, 30, 30);
        background: rgb(50, 50, 50);
        color: rgb(230, 230, 230);
        outline: none;
    }

    """

radio_css = """
    QRadioButton {
        color: rgb(230, 230, 230);
    }
    """

groupbox_white_css = """
    QGroupBox {
        font: bold;
        border: 1px solid silver;
        border-radius: 6px;
        margin-top: 3px;
        background: rgb(60, 60, 60);
    }
    QGroupBox:title {
        subcontrol-origin: margin;
        left: 10px;
        padding: -5px 5px 0px 5px;
    }
        """

checkbox_css = """
    QCheckBox {
        color: rgb(230, 230, 230);
    }

    QCheckBox:indicator:checked {
        background-color: rgb(52, 152, 219);
        border: 1px solid rgb(50, 50, 50);
    }

    QCheckBox:indicator:disabled {
        color: rgb(100,100,100);
        background-color: rgb(100, 100, 100);
        border: 1px solid rgb(100, 100, 100);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator {
        background-color: rgb(50,50,50);
        border: 1px solid rgb(120,120,120);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator:hover {
        border: 1px solid rgb(200, 200, 200);
    }
    """

qlistwidget_css = """
    QListWidget {
        background-color: rgb(40, 40, 40);
        color: rgb(220, 220, 220);
    }
    """

qlineedit_css = """
        background-color: rgb(40, 40, 40);
        color: rgb(220, 220, 220);
    """


def load_css(window: QMainWindow):
    """Find widgets and loads css. Use this method to apply the entire css style to the ui."""
    for widget in window.findChildren(QGroupBox):
        widget.setStyleSheet(groupbox_white_css)

    for widget in window.findChildren(QCheckBox):
        widget.setStyleSheet(checkbox_css)

    for widget in window.findChildren(QComboBox):
        widget.setStyleSheet(combobox_css)

    for widget in window.findChildren(QLineEdit):
        widget.setStyleSheet(qlineedit_css)

    for widget in window.findChildren(QListWidget):
        widget.setStyleSheet(qlistwidget_css)

    for widget in window.findChildren(QMenu):
        widget.setStyleSheet(qmenu_css)
