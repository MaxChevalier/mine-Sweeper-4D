from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget)
from PySide6.QtCore import Qt
from .case import Case

class MainWindows(QMainWindow):

    def __init__(self, game, game_size):
        super().__init__()
        self.game = game
        self.game_size = game_size

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        W_zone = QVBoxLayout(central_widget)
        W_zone.setObjectName(u"W_zone")
        W_zone.setContentsMargins(0, 0, 0, 0)

        for w in range(game_size):
            Z_zone = QHBoxLayout()
            Z_zone.setObjectName(u"Z_zone" + str(w))
            Z_zone.setContentsMargins(0, 0, 0, 0)
            for z in range(game_size):
                Y_zone = QVBoxLayout()
                Y_zone.setObjectName(u"Y_zone" + str(w) + "." + str(z))
                Y_zone.setContentsMargins(0, 0, 0, 0)
                for y in range(game_size):
                    X_zone = QHBoxLayout()
                    X_zone.setObjectName(u"X_zone" + str(w) + "." + str(z) + "." + str(y))
                    X_zone.setContentsMargins(0, 0, 0, 0)
                    for x in range(game_size):
                        button = Case()
                        button.setObjectName(u"button" + str(w) + "." + str(z) + "." + str(y) + "." + str(x))
                        button.mousePressEvent = lambda event, button=button: self.ButtonAction(event, button)
                        X_zone.addWidget(button)
                    Y_zone.addLayout(X_zone)
                Z_zone.addLayout(Y_zone)
            W_zone.addLayout(Z_zone)
            
    def ButtonAction(self, event, button):
        if event.button() == Qt.LeftButton:
            self.setButtonTextAction(button)
        elif event.button() == Qt.RightButton:
            self.SetFlag(button)
            
            
    def setButtonTextAction(self, button):
        if button.text() != "" : return
        name = button.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        number = self.game.table[coord[0]][coord[1]][coord[2]][coord[3]]
        if number == -1:
            button.setText('💥')
        else :
            button.setText(str(number))
        if number == 0:
            for w in range(-1,2,1):
                for z in range(-1,2,1):
                    for y in range(-1,2,1):
                        for x in range(-1,2,1):
                            if coord[0] + w >= 0 and coord[0] + w < self.game_size and coord[1] + z >= 0 and coord[1] + z < self.game_size and coord[2] + y >= 0 and coord[2] + y < self.game_size and coord[3] + x >= 0 and coord[3] + x < self.game_size:
                                next_button = button.parent().parent().findChild(QPushButton, "button" + str(coord[0] + w) + "." + str(coord[1] + z) + "." + str(coord[2] + y) + "." + str(coord[3] + x))
                                if next_button and type(next_button) == Case :
                                    self.setButtonTextAction(next_button)
                                    
    def SetFlag(self, button):
        if button is not None:
            if button.text() == "" :
                button.setText("🚩")
            elif button.text() == "🚩":
                button.setText("")
        else:
            print("No sender found.")
    

            
        
            
    