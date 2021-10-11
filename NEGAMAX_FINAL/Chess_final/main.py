# Fait en binome dans le cadre d'un projet informatique


import sys
from PyQt5 import QtWidgets
from gui import Game, Player
from pieces import *
from board import *

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = Game()
    app.exec_()
    sys.exit(app.exec_())
