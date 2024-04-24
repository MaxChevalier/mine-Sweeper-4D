from PySide6.QtWidgets import QLCDNumber

class GameInfoLCDNumber (QLCDNumber):
    
    def __init__(self):
        super().__init__()
        
        self.setDigitCount(3)
        self.setFixedHeight(50)
        self.setFixedWidth(80)
        self.setStyleSheet(
            "QLCDNumber { background-color: black; color: red; border: none; }"
        )
        self.setSegmentStyle(QLCDNumber.Flat)