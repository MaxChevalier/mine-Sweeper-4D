from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont
from time import sleep
from threading import Thread

from .game_info_LCD import GameInfoLCDNumber

class GameInfo (QWidget):
    time = 0
    is_start = False
    
    def __init__(self, game_data):
        super().__init__()
        self.game_data = game_data
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.bombs_ui = GameInfoLCDNumber()
        
        
        self.emoji_ui = QPushButton()
        self.emoji_ui.setFont(QFont("Segoe UI Emoji", 50))
        self.emoji_ui.setStyleSheet("QPushButton { border: none; }")
        
        self.time_ui = GameInfoLCDNumber()
        
        layout.addWidget(self.bombs_ui)
        layout.addWidget(self.emoji_ui)
        layout.addWidget(self.time_ui)
        
        self.update_bombs_remaining()
        self.time_ui.display(0)
        self.set_emoji_default()
        
    
    ################ Emoji ################
    
    def set_emoji_win(self):
        self.set_emoji("😎")
        
    def set_emoji_lose(self):
        self.set_emoji("😵")
    
    def set_emoji_default(self):
        self.set_emoji("😊")
        
    def set_emoji(self, emoji):
        self.emoji_ui.setText(emoji)
        
        
    ################ Bombs ################
    
    def update_bombs_remaining(self):
        self.bombs_ui.display(self.game_data.bombs - self.game_data.flags)
        
        
    ################ Timer ################
    
    def add_time(self, time):
        sleep(1)
        while not self.game_data.is_game_over:
            self.time += time
            self.time_ui.display(self.time)
            sleep(1)

    def start_timer(self):
        self.thread = Thread(target=self.add_time, args=(1,))
        self.thread.start()
        
    def stop_timer(self):
        self.game_data.is_game_over = True
        self.time = 0
        self.time_ui.display(self.time)
            