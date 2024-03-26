# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from src.mainWindow import MainWindows
from PySide6.QtWidgets import QApplication

game_size = 5
bombs = 10
game = Game(game_size, bombs)


app = QApplication(sys.argv)

main_wind = MainWindows(game_size, bombs)
main_wind.show()

sys.exit(app.exec())
