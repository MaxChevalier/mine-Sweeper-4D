# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from src.mainWindow import MainWindows
from PySide6.QtWidgets import QApplication

game_size = {"X": 3, "Y": 3, "Z": 3, "W": 3}
bombs = 5


app = QApplication(sys.argv)

main_wind = MainWindows(game_size, bombs)
main_wind.show()

sys.exit(app.exec())
