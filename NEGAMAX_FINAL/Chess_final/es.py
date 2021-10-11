'''

'''
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from board import *
import time

from gui import QtBoard

"""
E.essai("e2","e4",Pion("blanc"))
E.essai("e7","e6",Pion("noir"))
E.essai("d2","d4",Pion("blanc"))
E.essai("d7","d5",Pion("noir"))
E.essai("b1","d2",Cavalier("blanc"))
E.essai("g8","f6",Cavalier("noir"))
E.essai("e4","d5",Pion("blanc"))
"""


def on_clik():
    E = Echiquier()
    app = QtWidgets.QApplication(sys.argv)
    jeu = QtBoard(E)
    jeu.show()
    sys.exit(app.exec_())

#
# class QtBoard(QtWidgets.QMainWindow):
#     '''
#     This class allows to create the board
#     '''
#
#     def __init__(self, echequier):
#         super().__init__()
#         self.case_size = 100
#         self.setFixedSize(8 * self.case_size, 8 * self.case_size)
#         self.board = echequier
#         self.dict_case = {}
#         self.from_logic_to_board()
#         self.pieceToMove = None
#
#     def paintEvent(self, event):
#         """
#         :param event:
#         :return:
#         """
#         self.painter = QPainter(self)
#         self.draw(self.painter)
#
#         # self.essaidep()
#
#         self.draw_images_pieces(self.painter)
#
#     def draw(self, painter: QPainter):
#         '''
#         This Function draws the chessboard
#         :param painter:
#         :return:
#         '''
#         x, y, colored = 0, 0, False
#
#         for _ in range(8):
#             for _ in range(8):
#                 if not colored:
#                     # paint lines with lightGray color
#                     painter.setPen(QPen(Qt.lightGray))
#                     painter.setBrush(Qt.lightGray)
#                 else:
#                     # paint lines with lightGray color
#                     painter.setPen(QPen(Qt.lightGray))
#                     painter.setBrush(Qt.darkGray)
#                 colored = not colored
#                 rect = QRect(x, y, self.case_size, self.case_size)
#
#                 # paint chessboard's squares
#                 painter.drawRect(rect)
#                 x += self.case_size
#
#             x = 0
#             y += self.case_size
#             colored = not colored
#
#     def from_logic_to_board(self):
#         """
#
#         :return:
#         """
#         # reshapes the variable *cases* as array 8x8
#         a = np.reshape(np.asarray(self.board.cases), (-1, 8))
#         for i in range(8):
#             for j in range(8):
#                 x = i * self.case_size
#                 y = j * self.case_size
#                 # warning::
#                 self.dict_case[x, y] = a[j][i]
#
#     def draw_images_pieces(self, painter: QPainter):
#         """
#         This Function draws the pieces in the chessboard
#         :param painter:
#         :return:
#         """
#         for key in self.dict_case:
#             value = self.dict_case[key]
#             if value is not None:
#                 #  create the image from the files *images*
#                 pixmap = QPixmap(value.image)
#
#                 # paint every Pieces in chessboard from its position in *cases*
#                 painter.drawPixmap(QPoint(key[0] + self.case_size / 5, key[1] + self.case_size // 10), pixmap)
#
#     def mousePressEvent(self, event: QMouseEvent):
#         point: QPoint = event.pos()
#         x = (point.x() // self.case_size) * self.case_size
#         y = (point.y() // self.case_size) * self.case_size
#         x1 = x // self.case_size
#         y1 = y // self.case_size
#
#         value = self.dict_case[x, y]
#         l = []
#
#         pent: QPen = self.painter.pen()
#         if pent.color() == QColor(120, 255, 255, 150):
#             # deplacement
#             self.board.deplacer(self.pieceToMove, Echequier.coord[self.conversion(x1, y1)])
#             self.pieceToMove = None
#             self.update()
#
#         else:  # first click
#
#             self.pieceToMove = value
#             if value is not None:
#                 l = value.moves(self.conversion(x1, y1), self.board)
#
#             l1 = []
#             for pos in l:
#
#                 l1.append(self.conversion2(pos))
#                 pen = QPen(Qt.red)
#                 pen.setWidth(5)
#                 self.painter.setPen(pen)
#                 self.painter.setBrush(QColor(120, 255, 255, 150))
#                 self.painter.drawRect(QRect(x, y, self.case_size, self.case_size))
#
#                 pen = QPen(Qt.lightGray)
#                 pen.setWidth(1)
#                 self.painter.setPen(pen)
#
#                 for key in l1:
#                     self.painter.drawRect(QRect(key[0], key[1], self.case_size, self.case_size))
#
#             self.update()
#             # QtWidgets.QMainWindow.mousePressEvent(self, event)
#
#     def conversion(self, x, y):
#         if x == 0:
#             return y
#         if x == 1:
#             return y + 8
#         if x == 2:
#             return y + 16
#         if x == 3:
#             return y + 24
#         if x == 4:
#             return y + 32
#         if x == 5:
#             return y + 40
#         if x == 6:
#             return y + 48
#         if x == 7:
#             return y + 56
#
#     def conversion2(self, pos):
#         return pos // 8, pos % 8

# window.setCentralWidget(QtBoard(E))
# window.show()
# app.exec_()
