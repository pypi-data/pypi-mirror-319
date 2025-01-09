try:
    from PySide2.QtCore import QSize
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import (
        QApplication,
        QDialog,
        QLabel,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QStyle,
    )
except ImportError:
    from PySide6.QtCore import QSize
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import (
        QApplication,
        QDialog,
        QLabel,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QStyle,
    )


def inform_dialog(parent: QMainWindow, message: str, title: str = ''):
    """Open qt dialog box with a warning message."""
    msg_box = CustomSizeDialog(parent, message, title, QStyle.SP_MessageBoxInformation)
    msg_box.exec_()


def inform_dialog_small(parent: QMainWindow, message: str, title: str = ''):
    """Open qt dialog box with a warning message."""
    msg_box = QMessageBox(parent)
    msg_box.setStyleSheet('background: rgba(40, 40, 40, 255); color: rgba(255, 255, 255, 255);')
    msg_box.setWindowIcon(
        QIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))
    )
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Close)
    msg_box.exec_()


def warning_dialog(parent: QMainWindow, message: str, title: str = ''):
    """Open qt dialog box with a warning message."""
    msg_box = CustomSizeDialog(parent, message, title, QStyle.SP_MessageBoxWarning)
    msg_box.exec_()


def warning_dialog_small(parent: QMainWindow, error_message: str, title: str = ''):
    """Open qt dialog box with a warning message."""
    msg_box = QMessageBox(parent)
    msg_box.setStyleSheet('background: rgba(40, 40, 40, 255); color: rgba(255, 255, 255, 255);')
    msg_box.setWindowIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)))
    msg_box.setText(error_message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Close)
    msg_box.exec_()


class CustomSizeDialog(QDialog):
    def __init__(self, parent: QMainWindow, message: str, title: str, icon: QStyle.StandardPixmap):
        """Custom dialog box with a custom size."""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(300, 200)

        # icon & dark css
        style = QApplication.style()
        self.setWindowIcon(QIcon(style.standardIcon(icon)))
        self.setStyleSheet(
            'background: rgba(40, 40, 40, 255); \
                           color: rgba(255, 255, 255, 255); \
                           font-family: Segoe UI; font-size: 12px; '
        )

        # text info
        self.label = QLabel(parent=self, text=message)
        self.label.move(20, 20)
        self.label.show()

        # close button
        self.button = QPushButton(parent=self, text='Close')
        btn_size = QSize(130, 31)
        self.button.setMinimumSize(btn_size)
        self.button.setMaximumSize(btn_size)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.button.setSizePolicy(size_policy)
        self.button.setStyleSheet('background: rgb(60, 60, 60); color: rgb(240, 240, 240);')

        self.button.clicked.connect(self.close)
        self.button.move(150, 160)
        self.button.show()
