from time import sleep
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from .game_info import GameInfo
from ..models.gameData import GameData
from .table import Table

class MainWindows(QMainWindow):

    game_data = GameData()

    def __init__(self, game_size, bombs):
        super().__init__()

        self.SetMenu()
        
        central = QWidget()
        self.setCentralWidget(central)
        self.central_layout = QVBoxLayout(central)
        self.game_info = QWidget()
        self.table = QWidget()

        self.UpdateConfig(game_size, bombs)

    def SetMenu(self):
        game_menu = self.menuBar().addMenu("Game")
        restart = game_menu.addAction("Restart")
        restart.triggered.connect(self.RestartGame)

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
        about = help_menu.addAction("About")
        about.triggered.connect(self.About)

    def CreateInterface(self):
        self.game_info = GameInfo(self.game_data)
        self.game_info.emoji_ui.clicked.connect(self.RestartGame)
        self.table = Table(self.game_data, self.game_info)
        for i in reversed(range(self.central_layout.count())): 
            self.central_layout.itemAt(i).widget().setParent(None)
        self.central_layout.addWidget(self.game_info)
        self.central_layout.addWidget(self.table)

    def RestartGame(self):
        if isinstance(self.game_info, GameInfo):
            self.game_info.stop_timer()
        self.game_data.game = None
        self.game_data.is_game_over = False
        self.game_data.flags = 0
        self.game_data.discoverd = 0
        self.CreateInterface()

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
        
    def closeEvent(self, event):
        if isinstance(self.game_info, GameInfo):
            self.game_info.stop_timer() # Arrêter le thread lorsque l'application se ferme
            sleep(1) # Attendre 1 seconde pour laisser le temps au thread de s'arrêter
        
    
