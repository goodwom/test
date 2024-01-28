import sys
from PyQt6.QtCore import*
from PyQt6.QtGui import*
from PyQt6.QtWidgets import *

class KeyboardWidget (QWidget):
    keyPressed = pyqtSignal(str)

    def keyPressEvent(self, keyEvent):
        self.keyPressed.emit(keyEvent.text())

