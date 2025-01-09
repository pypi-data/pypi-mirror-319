import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from pyside_ui_backpack.css.colors import Colors
from pyside_ui_backpack.widgets.push_button import PushButton

if __name__ == '__main__':
    # create a qt application
    app = QApplication(sys.argv)

    # create a main window
    main_window = QMainWindow()

    # set the size of the main window
    main_window.setMinimumSize(380, 400)

    main_window.show()

    # create a push button for every color in Colors
    for index, color in enumerate(Colors):
        push_button = PushButton(
            main_window, f'push_button {index}', color.name, (100, 30), color, True
        )
        column = index % 3
        row = index // 3
        push_button.move(20 + (column * 120), 20 + (row * 40))
        push_button.show()

    # start the event loop
    sys.exit(app.exec_())
