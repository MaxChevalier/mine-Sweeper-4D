from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from .game_info import GameInfo
from ..models.gameData import GameData


class Case(QPushButton):
    def __init__(
        self,
        game_data: GameData,
        cell_size: int,
        game_info: GameInfo,
    ):
        super().__init__()
        self.game_data = game_data
        self.style_dict = dict()
        self.cell_size = cell_size
        self.game_info = game_info

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
        )

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
        if self.game_data.is_game_over:
            return
        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        for w in range(-1, 2, 1):
            for z in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    for x in range(-1, 2, 1):
                        self.set_hover_button_color(
                            [coord[0] + w, coord[1] + z, coord[2] + y, coord[3] + x],
                            color,
                        )

    def set_hover_button_color(self, coord, color):
        highlight_button = (
            self.parent()
            .parent()
            .findChild(
                QPushButton,
                "button"
                + str(coord[0])
                + "."
                + str(coord[1])
                + "."
                + str(coord[2])
                + "."
                + str(coord[3]),
            )
        )
        if highlight_button:
            highlight_button.setStyleSheet({"background-color": color})

    def ButtonAction(self, event):
        if self.game_data.is_game_over:
            return
        if event.button() == Qt.LeftButton:
            self.setButtonTextAction()
            if (
                not self.game_data.is_game_over
                and self.game_data.discoverd
                == self.game_data.game_size["X"]
                * self.game_data.game_size["Y"]
                * self.game_data.game_size["Z"]
                * self.game_data.game_size["W"]
                - self.game_data.bombs
            ):
                self.game_data.is_game_over = True
                self.game_info.set_emoji_win()
        elif event.button() == Qt.RightButton:
            self.SetFlag()

    def setButtonTextAction(self):
        if self.text() != "":
            return
        if not self.game_info.is_start:
            self.game_info.is_start = True
            self.game_info.start_timer()

        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        number = self.game_data.game.table[coord[0]][coord[1]][coord[2]][coord[3]]
        border = "1px solid #7b7b7b"
        self.setStyleSheet(
            {
                "border-top": border,
                "border-right": border,
                "border-bottom": border,
                "border-left": border,
            }
        )

        self.setMaximumWidth(self.cell_size)
        self.setMaximumHeight(self.cell_size)
        self.setMinimumHeight(self.cell_size)
        self.setMinimumWidth(self.cell_size)

        if number == -1:
            self.setStyleSheet({"background-color": "red"})
            self.reveal_bombs()
            self.game_data.is_game_over = True
            self.game_info.set_emoji_lose()
        elif number == 0:
            self.game_data.discoverd += 1
            self.setText("0")
            self.reveal_neighbors(coord)
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

    def reveal_neighbors(self, coord):
        for w in range(-1, 2, 1):
            for z in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    for x in range(-1, 2, 1):
                        self.reveal_neighbor(
                            [coord[0] + w, coord[1] + z, coord[2] + y, coord[3] + x]
                        )

    def reveal_neighbor(self, coord):
        if (
            coord[0] >= 0
            and coord[0] < self.game_data.game_size["W"]
            and coord[1] >= 0
            and coord[1] < self.game_data.game_size["Z"]
            and coord[2] >= 0
            and coord[2] < self.game_data.game_size["Y"]
            and coord[3] >= 0
            and coord[3] < self.game_data.game_size["X"]
        ):
            next_button = (
                self.parent()
                .parent()
                .findChild(
                    QPushButton,
                    "button"
                    + str(coord[0])
                    + "."
                    + str(coord[1])
                    + "."
                    + str(coord[2])
                    + "."
                    + str(coord[3]),
                )
            )
            if next_button and isinstance(next_button, Case):
                next_button.setButtonTextAction()

    def SetFlag(self):
        if not self.game_info.is_start:
            self.game_info.is_start = True
            self.game_info.start_timer()
        if self.text() == "":
            self.setText("🚩")
            self.game_data.flags += 1
        elif self.text() == "🚩":
            self.setText("")
            self.game_data.flags -= 1
        self.game_info.update_bombs_remaining()
        
    def reveal_bombs(self):
        for w in range(self.game_data.game_size["W"]):
            for z in range(self.game_data.game_size["Z"]):
                for y in range(self.game_data.game_size["Y"]):
                    for x in range(self.game_data.game_size["X"]):
                        button = (
                            self.parent()
                            .parent()
                            .findChild(
                                QPushButton,
                                "button" + str(w) + "." + str(z) + "." + str(y) + "." + str(x),
                            )
                        )
                        if button:
                            button.reveal_bomb()
    
    def reveal_bomb(self):
        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        if self.game_data.game.table[coord[0]][coord[1]][coord[2]][coord[3]] == -1 and self.text() != "🚩":
            self.setText("💣")
        elif self.text() == "🚩" and self.game_data.game.table[coord[0]][coord[1]][coord[2]][coord[3]] != -1:
            self.setText("❌")