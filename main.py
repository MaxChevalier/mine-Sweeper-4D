# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from src.widget.mainWindow import MainWindows
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen

game_size = {"X": 3, "Y": 3, "Z": 3, "W": 3}
bombs = 5


app = QApplication(sys.argv)

main_window = MainWindows(game_size, bombs)
main_window.show()

center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
geo = main_window.frameGeometry()
geo.moveCenter(center)
main_window.move(geo.topLeft())

sys.exit(app.exec())
