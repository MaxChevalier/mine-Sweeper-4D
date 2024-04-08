from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt

from src.gameData import GameData
from .case import Case


class Table(QWidget):
    def __init__(self, game_data: GameData, SetGameInformation):
        super().__init__()

        cell_size = 30
        cell_separator = 40

        grid_size = [
            (cell_size) * game_data.game_size["X"] + 23,
            (cell_size) * game_data.game_size["Y"] + 23,
        ]

        game_table = QWidget()

        W_zone = QVBoxLayout(game_table)
        W_zone.setObjectName("W_zone")
        W_zone.setContentsMargins(0, 0, 0, 0)

        for w in range(game_data.game_size["W"]):
            Z_zone = QHBoxLayout()
            Z_zone.setObjectName("Z_zone" + str(w))
            Z_zone.setContentsMargins(0, 0, 0, 0)
            for z in range(game_data.game_size["Z"]):

                grid = QWidget()
                Y_zone = QVBoxLayout()
                Y_zone.setObjectName("Y_zone" + str(w) + "." + str(z))
                Y_zone.setContentsMargins(0, 0, 0, 0)
                Y_zone.setSpacing(2)
                for y in range(game_data.game_size["Y"]):
                    X_zone = QHBoxLayout()
                    X_zone.setObjectName(
                        "X_zone" + str(w) + "." + str(z) + "." + str(y)
                    )
                    X_zone.setContentsMargins(0, 0, 0, 0)
                    X_zone.setSpacing(2)
                    for x in range(game_data.game_size["X"]):
                        button = Case(game_data, SetGameInformation, cell_size)
                        button.setObjectName(
                            "button"
                            + str(w)
                            + "."
                            + str(z)
                            + "."
                            + str(y)
                            + "."
                            + str(x)
                        )
                        X_zone.addWidget(button)
                    Y_zone.addLayout(X_zone)
                grid.setLayout(Y_zone)

                grid.setMaximumWidth(grid_size[0])
                grid.setMaximumHeight(grid_size[1])
                grid.setMinimumHeight(grid_size[1])
                grid.setMinimumWidth(grid_size[0])
                grid.setStyleSheet(
                    "border: 10px ridge #d0d0d0;\
                    background: transparent;"
                )
                grid.setContentsMargins(10, 10, 10, 10)

                Z_zone.addWidget(grid)
            W_zone.addLayout(Z_zone)
        self.setLayout(W_zone)
