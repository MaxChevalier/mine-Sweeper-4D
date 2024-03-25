import sys
from src.game import Game
from src.ui.mainwindow import MainWindows
from PySide6.QtWidgets import QApplication

game_size = 3
bombs = 10
game = Game(game_size, bombs)


app = QApplication(sys.argv)

main_wind = MainWindows(game, game_size)
main_wind.show()

sys.exit(app.exec())
