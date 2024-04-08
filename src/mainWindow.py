from PySide6.QtWidgets import QPushButton, QMainWindow, QStatusBar, QMessageBox
from .gameData import GameData
from src.table import Table
from .game import Game


class MainWindows(QMainWindow):

    game_data = GameData()

    def __init__(self, game_size, bombs):
        super().__init__()

        self.SetMenu()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.UpdateConfig(game_size, bombs)

    def SetMenu(self):
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

    def CreateInterface(self):
        central = Table(self.game_data, self.SetGameInformation)
        self.setCentralWidget(central)

    def SetGameInformation(self):
        self.status_bar.showMessage(
            "Discoverd: %d/%d       Flags: %d/%d"
            % (
                self.game_data.discoverd,
                self.game_data.game_size["X"]
                * self.game_data.game_size["Y"]
                * self.game_data.game_size["Z"]
                * self.game_data.game_size["W"]
                - self.game_data.bombs,
                self.game_data.flags,
                self.game_data.bombs,
            )
        )

    def RestartGame(self):
        self.game_data.game = Game(self.game_data.game_size, self.game_data.bombs)
        self.game_data.isGameOver = False
        self.game_data.flags = 0
        self.game_data.discoverd = 0
        self.CreateInterface()
        self.SetGameInformation()

    def UpdateConfig(self, game_size, bombs):
        self.game_data.game_size = game_size
        self.game_data.bombs = bombs
        self.RestartGame()

    def About(self):
        QMessageBox.information(
            self,
            "About",
            "This is a Minesweeper game in 4D made with PySide6 by Maxime Chevalier",
        )
