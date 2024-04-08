from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from src.gameData import GameData


class Case(QPushButton):
    def __init__(self, game_data: GameData, SetGameInformation, cell_size: int):
        super().__init__()
        self.SetGameInformation = SetGameInformation
        self.game_data = game_data
        self.style_dict = dict()
        self.cell_size = cell_size

        self.setMaximumWidth(cell_size)
        self.setMaximumHeight(cell_size)
        self.setMinimumHeight(cell_size)
        self.setMinimumWidth(cell_size)
        

        self.setStyleSheet(
            {
                "background-color": "#BDBDBD",
                "border-top": "4px solid #ffffff",
                "border-right": "4px solid #7b7b7b",
                "border-bottom": "4px solid #7b7b7b",
                "border-left": "4px solid #ffffff",
            }
        )  # Couleur de fond initiale

        self.mousePressEvent = lambda event: self.ButtonAction(event)

    def setStyleSheet(self, style):
        for key, value in style.items():
            self.style_dict[key] = value
        text = ""
        for key, value in self.style_dict.items():
            text += key + ": " + value + ";"
        super().setStyleSheet(text)

    def enterEvent(self, event):
        self.hoverButton(
            "#E0E0FF"
        )  # Appel de la fonction avec la couleur appropriée lors du survol

    def leaveEvent(self, event):
        self.hoverButton(
            "#BDBDBD"
        )  # Appel de la fonction avec la couleur appropriée lors de la sortie du survol

    def hoverButton(self, color):
        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        for w in range(-1, 2, 1):
            for z in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    for x in range(-1, 2, 1):
                        highlight_button = (
                            self.parent()
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
                        if highlight_button:
                            highlight_button.setStyleSheet({"background-color": color})

    def ButtonAction(self, event):
        if self.game_data.isGameOver:
            return
        if event.button() == Qt.LeftButton:
            self.setButtonTextAction()
            self.SetGameInformation()
            if (
                not self.game_data.isGameOver
                and self.game_data.discoverd
                == self.game_data.game_size["X"]
                * self.game_data.game_size["Y"]
                * self.game_data.game_size["Z"]
                * self.game_data.game_size["W"]
                - self.game_data.bombs
            ):
                self.game_data.isGameOver = True
        elif event.button() == Qt.RightButton:
            self.SetFlag()

    def setButtonTextAction(self):
        if self.text() != "":
            return
        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        number = self.game_data.game.table[coord[0]][coord[1]][coord[2]][coord[3]]
        self.setStyleSheet(
            {
                "border-top": "1px solid #7b7b7b",
                "border-right": "1px solid #7b7b7b",
                "border-bottom": "1px solid #7b7b7b",
                "border-left": "1px solid #7b7b7b",
            }
        )

        self.setMaximumWidth(self.cell_size)
        self.setMaximumHeight(self.cell_size)
        self.setMinimumHeight(self.cell_size)
        self.setMinimumWidth(self.cell_size)

        if number == -1:
            self.setText("💥")
            self.game_data.isGameOver = True
        elif number == 0:
            self.game_data.discoverd += 1
            self.setText("0")
            for w in range(-1, 2, 1):
                for z in range(-1, 2, 1):
                    for y in range(-1, 2, 1):
                        for x in range(-1, 2, 1):
                            if (
                                coord[0] + w >= 0
                                and coord[0] + w < self.game_data.game_size["W"]
                                and coord[1] + z >= 0
                                and coord[1] + z < self.game_data.game_size["Z"]
                                and coord[2] + y >= 0
                                and coord[2] + y < self.game_data.game_size["Y"]
                                and coord[3] + x >= 0
                                and coord[3] + x < self.game_data.game_size["X"]
                            ):
                                next_button = (
                                    self.parent()
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
                                    next_button.setButtonTextAction()
        else:
            self.setText(str(number))
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
            self.setStyleSheet({"color": color, "font-weight": "bold"})
            self.game_data.discoverd += 1

    def SetFlag(self):
        if self.text() == "":
            self.setText("🚩")
            self.game_data.flags += 1
        elif self.text() == "🚩":
            self.setText("")
            self.game_data.flags -= 1
        self.SetGameInformation()
