from PySide6.QtWidgets import (QPushButton)

class Case(QPushButton):
    def __init__(self):
        super().__init__()
        self.style_dict = dict()
        
        self.setStyleSheet({
            "background-color": "#FFFFFF",
            "width": "30px",
            "height": "30px",
            })  # Couleur de fond initiale
        
    def setStyleSheet(self, style):
        for key, value in style.items():
            self.style_dict[key] = value
        text = ""
        for key, value in self.style_dict.items():
            text += key + ": " + value + ";"
        super().setStyleSheet(text)
        

    def enterEvent(self, event):
        self.hoverButton("#CCCCFF")  # Appel de la fonction avec la couleur appropriée lors du survol

    def leaveEvent(self, event):
        self.hoverButton("#FFFFFF")  # Appel de la fonction avec la couleur appropriée lors de la sortie du survol
        
    def hoverButton(self, color):
        name = self.objectName()
        coord = [int(i) for i in name[6:].split(".")]
        for w in range(-1,2,1):
            for z in range(-1,2,1):
                for y in range(-1,2,1):
                    for x in range(-1,2,1):
                        highlight_button = self.parent().parent().findChild(QPushButton, "button" + str(coord[0] + w) + "." + str(coord[1] + z) + "." + str(coord[2] + y) + "." + str(coord[3] + x))
                        if highlight_button :
                            highlight_button.setStyleSheet({"background-color": color})
        