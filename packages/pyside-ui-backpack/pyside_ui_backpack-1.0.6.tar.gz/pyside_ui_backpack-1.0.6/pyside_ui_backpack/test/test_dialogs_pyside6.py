import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

from pyside_ui_backpack import dialogs

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
    button.setText('information')
    button.move(20, 20)
    button.show()
    button.clicked.connect(
        lambda: dialogs.inform_dialog(
            main_window, 'this is an inform dialog', 'Title for inform dialog'
        )
    )

    # create a push button that calls a function when clicked
    button_info_default = QPushButton(main_window)
    button_info_default.setText('information small')
    button_info_default.move(20, 60)
    button_info_default.show()
    button_info_default.clicked.connect(
        lambda: dialogs.inform_dialog_small(
            main_window, 'this is an inform dialog', 'Title for inform dialog'
        )
    )

    # warning dialog button
    button2 = QPushButton(main_window)
    button2.setText('warning')
    button2.move(20, 100)
    button2.show()
    button2.clicked.connect(
        lambda: dialogs.warning_dialog(
            main_window, 'this is a warning dialog', 'Title for warning dialog'
        )
    )

    # warning dialog small button
    button_warning_small = QPushButton(main_window)
    button_warning_small.setText('warning small')
    button_warning_small.move(20, 140)
    button_warning_small.show()
    button_warning_small.clicked.connect(
        lambda: dialogs.warning_dialog_small(
            main_window, 'this is a warning dialog', 'Title for warning dialog'
        )
    )

    # start the event loop
    sys.exit(app.exec())
