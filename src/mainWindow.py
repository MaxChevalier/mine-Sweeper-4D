from math import ceil
from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QStatusBar,
    QMessageBox
)
from PySide6.QtCore import Qt
from .case import Case
from .game import Game


class MainWindows(QMainWindow):
    
    game : Game
    game_size : dict
    isGameOver : bool
    bombs : int
    flags : int
    discoverd : int

    def __init__(self, game_size, bombs):
        super().__init__()
        
        game_menu = self.menuBar().addMenu("Game")
        Restart = game_menu.addAction("Restart")
        Restart.triggered.connect(self.RestartGame)
        
        config_menu = self.menuBar().addMenu("Config")
        pre_config_game = [
            {"size": {"X": 3, "Y": 3, "Z": 3, "W": 3}, "Bombs": 5},
            {"size": {"X": 3, "Y": 3, "Z": 3, "W": 3}, "Bombs": 25},
            {"size": {"X": 4, "Y": 4, "Z": 4, "W": 4}, "Bombs": 10},
            {"size": {"X": 4, "Y": 4, "Z": 4, "W": 4}, "Bombs": 40},
            {"size": {"X": 5, "Y": 5, "Z": 5, "W": 5}, "Bombs": 15},
            {"size": {"X": 5, "Y": 5, "Z": 5, "W": 5}, "Bombs": 75},
        ]
        for config_game in pre_config_game:
            action = config_menu.addAction(
                "%dx%dx%dx%d - %d bombs"
                % (
                    config_game["size"]["X"],
                    config_game["size"]["Y"],
                    config_game["size"]["Z"],
                    config_game["size"]["W"],
                    config_game["Bombs"],
                )
            )
            action.triggered.connect(
                lambda checked=False, config_game=config_game: self.UpdateConfig(
                    config_game["size"], config_game["Bombs"]
                )
            )
        
        help_menu = self.menuBar().addMenu("Help")
        About = help_menu.addAction("About")
        About.triggered.connect(self.About)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.UpdateConfig(game_size, bombs)

        
    
    def CreateInterface(self):
        cell_size = 30
        cell_separator = 5
        
        game_table = QWidget()
        
        W_zone = QVBoxLayout(game_table)
        W_zone.setObjectName("W_zone")
        W_zone.setContentsMargins(0, 0, 0, 0)

        for w in range(self.game_size["W"]):
            Z_zone = QHBoxLayout()
            Z_zone.setObjectName("Z_zone" + str(w))
            Z_zone.setContentsMargins(0, 0, 0, 0)
            for z in range(self.game_size["Z"]):
                grid = QWidget()
                Y_zone = QVBoxLayout()
                Y_zone.setObjectName("Y_zone" + str(w) + "." + str(z))
                Y_zone.setContentsMargins(0, 0, 0, 0)
                for y in range(self.game_size["Y"]):
                    X_zone = QHBoxLayout()
                    X_zone.setObjectName(
                        "X_zone" + str(w) + "." + str(z) + "." + str(y)
                    )
                    X_zone.setContentsMargins(0, 0, 0, 0)
                    for x in range(self.game_size["X"]):
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
                grid.setMaximumWidth((cell_size + cell_separator) * self.game_size["X"])
                grid.setMaximumHeight((cell_size + cell_separator) * self.game_size["Y"])
                grid.setMinimumHeight((cell_size + cell_separator) * self.game_size["Y"])
                grid.setMinimumWidth((cell_size + cell_separator) * self.game_size["X"])
                grid.setStyleSheet(
                    "background-color: #FFFFFF; border: 6px ridge #c2c2c2;"
                )
                grid.setContentsMargins(8, 8, 8, 8)
                Z_zone.addWidget(grid)
            W_zone.addLayout(Z_zone)
            
        self.setCentralWidget(game_table)

        self.setCentralWidget(game_table)

    def ButtonAction(self, event, button):
        if self.isGameOver: return
        if event.button() == Qt.LeftButton:
            self.setButtonTextAction(button)
            self.SetGameInformation()
            if not self.isGameOver and self.discoverd == self.game_size["X"] * self.game_size["Y"] * self.game_size["Z"] * self.game_size["W"] - self.bombs:
                    self.isGameOver = True
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
            self.isGameOver = True
        elif number == 0:
            self.discoverd += 1
            button.setText("0")
            for w in range(-1, 2, 1):
                for z in range(-1, 2, 1):
                    for y in range(-1, 2, 1):
                        for x in range(-1, 2, 1):
                            if (
                                coord[0] + w >= 0
                                and coord[0] + w < self.game_size["W"]
                                and coord[1] + z >= 0
                                and coord[1] + z < self.game_size["Z"]
                                and coord[2] + y >= 0
                                and coord[2] + y < self.game_size["Y"]
                                and coord[3] + x >= 0
                                and coord[3] + x < self.game_size["X"]
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
            self.discoverd += 1

    def SetFlag(self, button):
        if button is not None:
            if button.text() == "":
                button.setText("🚩")
                self.flags += 1
            elif button.text() == "🚩":
                button.setText("")
                self.flags -= 1
            self.SetGameInformation()
        else:
            print("No sender found.")
            
    def SetGameInformation(self):
        self.status_bar.showMessage("Discoverd: %d/%d       Flags: %d/%d" % (self.discoverd, self.game_size["X"] * self.game_size["Y"] * self.game_size["Z"] * self.game_size["W"] - self.bombs, self.flags, self.bombs))
        
    def RestartGame(self):
        self.game = Game(self.game_size, self.bombs)
        self.isGameOver = False
        self.flags = 0
        self.discoverd = 0
        self.CreateInterface()
        self.SetGameInformation()
    
    def UpdateConfig(self, game_size, bombs):
        self.game_size = game_size
        self.bombs = bombs
        self.RestartGame()
        
    def About(self):
        QMessageBox.information(self, "About", "This is a Minesweeper game in 4D made with PySide6 by Maxime Chevalier")
