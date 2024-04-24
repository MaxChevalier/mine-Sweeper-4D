from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from ..models.gameData import GameData
from .case import Case
from .game_info import GameInfo


class Table(QWidget):
    def __init__(self, game_data: GameData, game_info: GameInfo):
        super().__init__()

        cell_size = 30

        grid_size = [
            (cell_size) * game_data.game_size["X"] + 20,
            (cell_size) * game_data.game_size["Y"] + 20,
        ]

        game_table = QWidget()

        w_zone = QVBoxLayout(game_table)
        w_zone.setObjectName("w_zone")
        w_zone.setContentsMargins(0, 0, 0, 0)

        for w in range(game_data.game_size["W"]):
            z_zone = QHBoxLayout()
            z_zone.setObjectName("z_zone" + str(w))
            z_zone.setContentsMargins(0, 0, 0, 0)
            for z in range(game_data.game_size["Z"]):

                grid = QWidget()
                y_zone = QVBoxLayout()
                y_zone.setObjectName("y_zone" + str(w) + "." + str(z))
                y_zone.setContentsMargins(0, 0, 0, 0)
                y_zone.setSpacing(0)
                for y in range(game_data.game_size["Y"]):
                    x_zone = QHBoxLayout()
                    x_zone.setObjectName(
                        "x_zone" + str(w) + "." + str(z) + "." + str(y)
                    )
                    x_zone.setContentsMargins(0, 0, 0, 0)
                    x_zone.setSpacing(0)
                    for x in range(game_data.game_size["X"]):
                        button = Case(game_data, cell_size, game_info)
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
                        x_zone.addWidget(button)
                    y_zone.addLayout(x_zone)
                grid.setLayout(y_zone)

                grid.setMaximumWidth(grid_size[0])
                grid.setMaximumHeight(grid_size[1])
                grid.setMinimumHeight(grid_size[1])
                grid.setMinimumWidth(grid_size[0])
                grid.setStyleSheet(
                    "border: 10px ridge #d0d0d0;\
                    background: transparent;"
                )
                grid.setContentsMargins(10, 10, 10, 10)

                z_zone.addWidget(grid)
            w_zone.addLayout(z_zone)
        self.setLayout(w_zone)
