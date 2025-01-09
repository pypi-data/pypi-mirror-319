from typing import Callable

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication


def wait_cursor(method: Callable) -> Callable:
    """Qt wait cursor decorator.

    Note:
        The wait cursor will be set for the duration of the method call.
        The method must be a function or a method of a class.

    Use QApplication.processEvents() to update the UI while the wait cursor is active.
    """

    def wrapper(*args, **kwargs):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()

        try:
            r = method(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()

        return r

    return wrapper
