import sys
from src.game import Game
from PySide6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QHBoxLayout)
from PySide6.QtCore import (QRect, Slot)

@Slot()
def setButtonText():
    button = app.sender()  # Get the button that sent the signal
    print("Button clicked:", button)  # Debugging
    if button is not None:
        name = button.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        button.setText(str(game.table[coord[0]][coord[1]][coord[2]][coord[3]]))
    else:
        print("No sender found.")

app = QApplication(sys.argv)

game_size = 4
bombs = 50
game = Game(game_size, bombs)

box = QWidget()
box.setObjectName(u"box")
box.setGeometry(QRect(380, 240, 330, 261))

W_zone = QVBoxLayout()
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
                button = QPushButton()
                button.setObjectName(u"button" + str(w) + "." + str(z) + "." + str(y) + "." + str(x))
                button.clicked.connect(setButtonText)
                # button.setText(str(game.table[w][z][y][x]))
                X_zone.addWidget(button)
            Y_zone.addLayout(X_zone)
        Z_zone.addLayout(Y_zone)
    W_zone.addLayout(Z_zone)
box.setLayout(W_zone)
box.show()

sys.exit(app.exec())
