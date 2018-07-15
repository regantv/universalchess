from PyQt5.QtWidgets import QWidget, QAction, qApp, QApplication, QLabel,QInputDialog,QCheckBox,QDialog, QComboBox,QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, pyqtSlot
from PyQt5.QtCore import Qt
import cv2
import numpy as np

import sys

class InitScreen(QDialog):
    def __init__(self,robot):
        
        super().__init__()
        self.robot = robot
        self.UI()
        
    def UI(self):
        self.setWindowTitle("Fen Clear?")
        self.setGeometry(300, 150, 250, 75)
        noBtn = QPushButton('No',self)
        noBtn.move(30,20)
        noBtn.show()
        yesBtn = QPushButton('Yes',self)
        yesBtn.move(150,20)
        yesBtn.show()
        noBtn.clicked.connect(self.Close)
        yesBtn.clicked.connect(self.Clear)
        
        self.show()
        
    def Close(self):
        self.close()
    
    def Clear(self):
        filename = 'player0.txt'
        file = open(filename,'w')
        file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        file.close()
        filename = 'player1.txt'
        file = open(filename,'w')
        file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        file.close()
        filename = 'player2.txt'
        file = open(filename,'w')
        file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        file.close()
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    robot = []
    ex = InitScreen(robot)
    
    sys.exit(app.exec_())
