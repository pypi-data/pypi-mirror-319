import sys
import time

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton

from pyside_ui_backpack.widgets.wait_cursor import wait_cursor

if __name__ == '__main__':
    # create a qt application
    app = QApplication(sys.argv)

    # create a main window
    main_window = QMainWindow()

    # set the size of the main window
    main_window.setMinimumSize(200, 200)
    main_window.setMaximumSize(200, 200)

    main_window.show()

    # create a push button that calls a function when clicked
    button = QPushButton(main_window)
    button.setText('click me')
    button.move(20, 20)
    button.show()
    button.clicked.connect(lambda: long_running_function())

    @wait_cursor
    def long_running_function():
        for i in range(1, 4):
            button.setText(f'working... {i}')
            QApplication.processEvents()
            time.sleep(1)

        button.setText('click me')

    # create a push button that calls a function when clicked
    button2 = QPushButton(main_window)
    button2.setText('click me, function failed')
    button2.move(20, 120)
    # set the size of the push button
    button2.resize(160, 30)
    button2.show()
    button2.clicked.connect(lambda: function_that_fails())

    @wait_cursor
    def function_that_fails():
        for i in range(1, 4):
            button2.setText(f'working... {i}')
            QApplication.processEvents()
            time.sleep(1)
            raise Exception('function failed')

        button2.setText('click me, function failed')

    # start the event loop
    sys.exit(app.exec_())
