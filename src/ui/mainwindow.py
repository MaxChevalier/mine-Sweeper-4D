from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)
from PySide6.QtCore import Qt
from .case import Case


class MainWindows(QMainWindow):

    def __init__(self, game, game_size):
        super().__init__()
        self.game = game
        self.game_size = game_size

        cell_size = 30
        cell_separator = 5

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        W_zone = QVBoxLayout(central_widget)
        W_zone.setObjectName("W_zone")
        W_zone.setContentsMargins(0, 0, 0, 0)

        for w in range(game_size):
            Z_zone = QHBoxLayout()
            Z_zone.setObjectName("Z_zone" + str(w))
            Z_zone.setContentsMargins(0, 0, 0, 0)
            for z in range(game_size):
                grid = QWidget()
                Y_zone = QVBoxLayout()
                Y_zone.setObjectName("Y_zone" + str(w) + "." + str(z))
                Y_zone.setContentsMargins(0, 0, 0, 0)
                for y in range(game_size):
                    X_zone = QHBoxLayout()
                    X_zone.setObjectName(
                        "X_zone" + str(w) + "." + str(z) + "." + str(y)
                    )
                    X_zone.setContentsMargins(0, 0, 0, 0)
                    for x in range(game_size):
                        button = Case()
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
                        button.mousePressEvent = (
                            lambda event, button=button: self.ButtonAction(
                                event, button
                            )
                        )
                        button.setMaximumWidth(cell_size)
                        button.setMaximumHeight(cell_size)
                        button.setMinimumHeight(cell_size)
                        button.setMinimumWidth(cell_size)
                        X_zone.addWidget(button)
                    Y_zone.addLayout(X_zone)
                grid.setLayout(Y_zone)
                grid.setMaximumWidth((cell_size + cell_separator) * game_size)
                grid.setMaximumHeight((cell_size + cell_separator) * game_size)
                grid.setMinimumHeight((cell_size + cell_separator) * game_size)
                grid.setMinimumWidth((cell_size + cell_separator) * game_size)
                grid.setStyleSheet(
                    "background-color: #FFFFFF; border: 6px ridge #c2c2c2;"
                )
                grid.setContentsMargins(8, 8, 8, 8)
                Z_zone.addWidget(grid)
            W_zone.addLayout(Z_zone)

    def ButtonAction(self, event, button):
        if event.button() == Qt.LeftButton:
            self.setButtonTextAction(button)
        elif event.button() == Qt.RightButton:
            self.SetFlag(button)

    def setButtonTextAction(self, button):
        if button.text() != "":
            return
        name = button.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        number = self.game.table[coord[0]][coord[1]][coord[2]][coord[3]]
        button.default_background = "#DDDDDD"
        button.hoverButton("#FFFFFF")
        if number == -1:
            button.setText("💥")
        elif number == 0:
            button.setText("0")
            for w in range(-1, 2, 1):
                for z in range(-1, 2, 1):
                    for y in range(-1, 2, 1):
                        for x in range(-1, 2, 1):
                            if (
                                coord[0] + w >= 0
                                and coord[0] + w < self.game_size
                                and coord[1] + z >= 0
                                and coord[1] + z < self.game_size
                                and coord[2] + y >= 0
                                and coord[2] + y < self.game_size
                                and coord[3] + x >= 0
                                and coord[3] + x < self.game_size
                            ):
                                next_button = (
                                    button.parent()
                                    .parent()
                                    .findChild(
                                        QPushButton,
                                        "button"
                                        + str(coord[0] + w)
                                        + "."
                                        + str(coord[1] + z)
                                        + "."
                                        + str(coord[2] + y)
                                        + "."
                                        + str(coord[3] + x),
                                    )
                                )
                                if next_button and type(next_button) == Case:
                                    self.setButtonTextAction(next_button)
        else:
            button.setText(str(number))
            if number > 40:
                color = "#96%s00" % (
                    hex(int((150 / 40) * (40 - (number / 2))))[2:]
                    if len(hex(int((150 / 40) * (40 - (number / 2))))[2:]) > 1
                    else "0" + hex(int((150 / 40) * (40 - (number / 2))))[2:]
                )
            else:
                color = "#%s9600" % (
                    hex(int((150 / 40) * (number)))[2:]
                    if len(hex(int((150 / 40) * (number)))[2:]) > 1
                    else "0" + hex(int((150 / 40) * (number)))[2:]
                )
            button.setStyleSheet({"color": color, "font-weight": "bold"})

    def SetFlag(self, button):
        if button is not None:
            if button.text() == "":
                button.setText("🚩")
            elif button.text() == "🚩":
                button.setText("")
        else:
            print("No sender found.")
