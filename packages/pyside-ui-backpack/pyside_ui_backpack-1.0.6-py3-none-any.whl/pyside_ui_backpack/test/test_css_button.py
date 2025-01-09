import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton

from pyside_ui_backpack import Colors, style_push_button

if __name__ == '__main__':
    # create a qt application
    app = QApplication(sys.argv)

    # create a main window
    main_window = QMainWindow()

    # set the size of the main window
    main_window.setMinimumSize(200, 200)
    main_window.setMaximumSize(200, 200)

    main_window.show()

    # test button 1
    button = QPushButton(main_window)
    button.setText('information')
    button.move(20, 20)
    style_push_button(main_window, button, Colors.BG_BLUE)
    button.show()

    # test button 2
    button = QPushButton(main_window)
    button.setText('warning')
    button.move(20, 60)
    style_push_button(main_window, button, Colors.DARK_ORANGE)
    button.show()

    # start the event loop
    sys.exit(app.exec_())
