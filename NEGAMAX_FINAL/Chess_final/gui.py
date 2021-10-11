import sys
from functools import partial
from random import choice

from PyQt5 import *
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from qtconsole.qt import QtCore
from PyQt5 import QtWidgets
import threading
import numpy as np
from playsound import playsound
import os
import time
import ctypes

import copy

from AIEngine import AIEngine
from board import *


def conversion2(pos):
    """

    :param pos: position dans l'echequier
    :return: (abscisse , ordonnee) dans le tableau
    """
    return pos % 8, pos // 8


def conversion(x, y):
    """
    :param x: abscisse
    :param y: ordonnee
    :return: position dans l'echhequier (0 a 63)
    """
    if y == 0:
        return x
    if y == 1:
        return x + 8
    if y == 2:
        return x + 16
    if y == 3:
        return x + 24
    if y == 4:
        return x + 32
    if y == 5:
        return x + 40
    if y == 6:
        return x + 48
    if y == 7:
        return x + 56


MODE_PLAYER_PLAYER = "player vs player"
MODE_PLAYER_AI = "player vs ai"
MODE_AI_AI = "ai vs ai"


class QtBoard(QWidget):
    """
    This class allows to create the board
    """

    def __init__(self, mode, echequier):
        super().__init__()
        # self.window = None
        self.parent = None
        self.case_size = 85
        self.setFixedSize(8 * self.case_size, 8 * self.case_size)
        self.setWindowTitle("CHESS-GAME Developed by ---------------------------------------------------------JOEL-KHA")
        self.board = echequier
        self.dict_case = {}
        self.pieceToMove = ''
        self.paint_cell_positions = False
        self.paint_cell_after_move = False
        self.paint_cell_echec = False
        self.selected_pos = None
        self.move_cell_info = []
        self.echec_cell_info = None
        self.click = False
        self.pos = []
        self.mode = mode
        self.ai_move = None
        self.control_ai_thread = False
        self.mutex = False

        if mode == MODE_PLAYER_PLAYER:
            self.player_1 = HMPlayer("blanc")
            self.player_2 = HMPlayer("noir")
            self.ai_engine = None
            echequier.current_player_color = self.player_1.color
            return
        elif mode == MODE_PLAYER_AI:
            ai_color = choice(["blanc", "noir"])
            if ai_color == "blanc":
                self.player_1 = AIPlayer("blanc")
                self.player_2 = HMPlayer("noir")
                self.player_2.has_play = True
            else:
                self.player_1 = HMPlayer("blanc")
                self.player_2 = AIPlayer("noir")
            self.ai_engine = AIEngine()
            echequier.current_player_color = self.player_1.color
            if self.player_1.is_ai:
                self.ai_muss_play(self.player_1)
            return
        elif mode == MODE_AI_AI:
            self.player_1 = AIPlayer("blanc")
            self.player_2 = AIPlayer("noir")
            self.ai_engine = AIEngine()
            echequier.current_player_color = self.player_1.color
        print("joueur " + echequier.current_player_color + " commence.")
        print("player 1 is AI= " + str(self.player_1.is_ai))
        print("player 2 is AI= " + str(self.player_2.is_ai))

    def paintEvent(self, event):
        """
        :param event:
        :return:
        """
        painter = QPainter(self)
        self.draw(painter)

        self.from_logic_to_board()

        self.draw_images_pieces(painter)

        if self.paint_cell_positions:
            self.paint_possible_moves(painter)
        if self.paint_cell_after_move:
            self.paint_cell_info(painter)
        if self.paint_cell_echec:
            self.paint_cell_echec_info(painter)

    def draw(self, painter: QPainter):
        '''
        cette fonction permet de dessiner le tableau
        :param painter:
        :return:
        '''
        x, y, colored = 0, 0, False

        for _ in range(8):
            for _ in range(8):
                if not colored:
                    # peint les lignes avec la couleur  lightGray
                    painter.setPen(QPen(Qt.lightGray))
                    painter.setBrush(Qt.lightGray)
                else:
                    # peint les lignes avec la couleur  lightGray
                    painter.setPen(QPen(Qt.lightGray))
                    painter.setBrush(Qt.darkGray)
                colored = not colored
                rect = QRect(x, y, self.case_size, self.case_size)

                # dessin de carreau du tableau
                painter.drawRect(rect)
                x += self.case_size

            x = 0
            y += self.case_size
            colored = not colored

    def from_logic_to_board(self):
        """

        :return:
        """
        # reshapes the variable *cases* as array 8x8
        a = np.reshape(np.asarray(self.board.cases), (-1, 8))
        for i in range(8):
            for j in range(8):
                x = i * self.case_size
                y = j * self.case_size
                # warning::
                self.dict_case[x, y] = a[j][i]

    def draw_images_pieces(self, painter: QPainter):
        """
        This Function draws the pieces in the chessboard
        :param painter:
        :return:
        """
        for key in self.dict_case:
            value = self.dict_case[key]
            if value is not None:
                #  create the image from the files *images*
                pixmap = QPixmap(value.image)

                # paint every Pieces in chessboard from its position in *cases*
                painter.drawPixmap(QPoint(key[0] + self.case_size / 5, key[1] + self.case_size // 10), pixmap)

    def closeEvent(self, QCloseEvent):
        """
        permet de fermer une fenetre
        :param QCloseEvent:
        :return:
        """
        self.parent.show()
        self.window().close()

    def mousePressEvent(self, event: QMouseEvent):

        if self.mode == MODE_AI_AI:
            return

        if self.mode == MODE_PLAYER_AI:
            if (not self.player_1.is_ai and self.player_1.has_play and self.player_2.is_ai and \
                not self.player_2.has_play) or \
                    (not self.player_2.is_ai and self.player_2.has_play and self.player_1.is_ai and \
                     not self.player_1.has_play):
                # permet de bloquer les mouvements du Humanplayer lorsqu'il a deja joue et que l'AI n'a pas joue
                return

        point: QPoint = event.pos()
        x = (point.x() // self.case_size) * self.case_size
        y = (point.y() // self.case_size) * self.case_size
        # position du clik de la souris

        x1 = x // self.case_size
        y1 = y // self.case_size
        # permet de determiner la case du tableau ou l'on a clique
        position = conversion(x1, y1)
        pos_string = Echiquier.coord[position]
        value = self.board.cases[self.board.get_dest_pos(pos_string)]  # piece sur laquelle on a clique

        if not self.player_1.is_ai and not self.player_1.has_play and self.player_1.is_first_click \
                and value is not None and value.couleur == self.player_1.color:  # 1. click du player_1
            self.execute_first_click(x, y, position, value, self.player_1)
            return

        elif not self.player_1.is_ai and not self.player_1.has_play and not self.player_1.is_first_click:  # 2. click du player_1
            self.execute_second_click(x, y, position, pos_string, self.player_1)
            return

        elif not self.player_2.is_ai and not self.player_2.has_play and self.player_2.is_first_click \
                and value is not None and value.couleur == self.player_2.color:  # 1. click du player_2
            self.execute_first_click(x, y, position, value, self.player_2)
            return

        elif not self.player_2.is_ai and not self.player_2.has_play and not self.player_2.is_first_click:
            self.execute_second_click(x, y, position, pos_string, self.player_2)  # 2. click du player_1
            return

    def execute_first_click(self, x, y, position, value, player):
        """

        :param x: abscisse
        :param y: ordonnee
        :param position: position dans l'echequier
        :param value: piece sur laquelle on a clique
        :param player: l'instance du player qui a clique
        :return:
        """
        self.selected_pos = (x, y)
        self.pieceToMove = value
        l = []
        if value is not None:
            l = value.moves(position, self.board)
            self.paint_cell_positions = True
        self.pos.clear()
        for pos in l:
            key = conversion2(pos)
            self.pos.append(
                (key[0] * self.case_size, key[1] * self.case_size))  # cette liste contient les positions a peindre
        player.is_first_click = False
        self.paint_cell_after_move = False
        self.update()

    def execute_second_click(self, x, y, position, pos_string, player):
        """
        verifie si le second clik n'etait sur la meme case
        :param x:
        :param y:
        :param position:
        :param pos_string:
        :param player:
        """
        player.is_first_click = True
        if (x != self.selected_pos[0] or y != self.selected_pos[1]) and self.pieceToMove is not None:
            p = conversion(self.selected_pos[0] // self.case_size, self.selected_pos[1] // self.case_size)
            if self.pieceToMove.moves(p, self.board).__contains__(position):
                # si le second clik n'etait sur la meme case
                if self.board.cases[position] is not None:
                    sound_clik()
                self.move_cell_info.clear()  # vider avant deplacement
                key = conversion2(self.board.cases.index(self.pieceToMove))  # position ou etait la piece
                # la liste move_cell_info recupere la position d'une piece avant et apres mvt pour la peindre
                self.move_cell_info.append((key[0] * self.case_size, key[1] * self.case_size))
                is_echec_info = self.board.deplacer(self.pieceToMove, pos_string)
                if is_echec_info[0] and is_echec_info[1] is not None:
                    self.paint_cell_echec = True
                    key = conversion2(is_echec_info[1])
                    self.echec_cell_info = (key[0] * self.case_size, key[1] * self.case_size)
                    sound_echec()
                else:
                    self.paint_cell_echec = False
                player.has_play = True
                opponent = self.get_opponent(player)
                opponent.has_play = False  # le joueur oppose doit jouer
                if not opponent.is_ai:
                    opponent.is_first_click = True  #
                self.paint_cell_after_move = True  # donne l'autorisation de peindre a la fonction PaintEvent
                key = conversion2(position)
                self.move_cell_info.append(
                    (key[0] * self.case_size, key[1] * self.case_size))  # position ou sera la piece apres move
                sound_move()
                # self.player_deplaced = True
                if self.board.check_pat():
                    self.alert_pat()
                if self.board.check_echec_matt():
                    self.alert_echec_matt(self.board.current_player_color)
                if opponent.is_ai and not opponent.has_play:
                    self.ai_muss_play(opponent)
                self.pieceToMove = None
        # self.second_click = False
        self.paint_cell_positions = False
        self.update()

    def get_opponent(self, player):
        if player == self.player_1:
            return self.player_2
        else:
            return self.player_1

    def ai_game_ai(self):
        if not self.mutex and self.player_1.is_ai and self.player_2.is_ai:  # lors du challenge ai vs ai la variable
            # mutex permet de simuler que le joueur 2 a deja jouer pour que le premier joueur commence a jouer
            self.player_2.has_play = True
            self.mutex = True  # to avoid deadlock
        if self.player_1.is_ai and not self.player_1.has_play and self.player_2.is_ai and self.player_2.has_play \
                and not self.control_ai_thread:
            self.control_ai_thread = True
            #time.sleep(2)
            self.ai_1_muss_play()
            # threading.Thread(target=self.ai_1_muss_play, daemon=False).start()
        elif self.player_2.is_ai and not self.player_2.has_play and self.player_1.is_ai and self.player_1.has_play \
                and not self.control_ai_thread:
            self.control_ai_thread = True
            #time.sleep(2)
            self.ai_2_muss_play()
            # threading.Thread(target=self.ai_2_muss_play, daemon=False).start()

    def ai_muss_play(self, player):
        """
        execute la fonction play de l'AI dependant du player
        :param player:
        :return:
        """
        if self.player_1 == player:
            self.ai_1_muss_play()
        else:
            self.ai_2_muss_play()

    def ai_1_muss_play(self):
        if self.player_1.mode == 'AI':
            self.start_ai_compute(self.player_1, MinimaxWorker(), 2)
             #self.start_ai_compute(self.player_2, NegamaxWorker(), 2)
        else:
            self.start_ai_compute(self.player_1, OpeningAIWorker(), 0)

    def ai_2_muss_play(self):
        if self.player_2.mode == 'AI':
            self.start_ai_compute(self.player_2, MinimaxWorker(), 2)
            #self.start_ai_compute(self.player_2, NegamaxWorker(), 2)
            # self.start_ai_compute(self.player_2, BasicAIWorker(), 0)
        else:
            self.start_ai_compute(self.player_2, OpeningAIWorker(), 0)

    def start_ai_compute(self, player, strategy, depth):
        # quand le process est lancé on ne peut plus avoir acces a celui ci
        thread = QThread()  # creation d'un process
        worker = strategy  # tache du process
        worker.moveToThread(thread)  # donner la tache au process
        thread.started.connect(
            partial(worker.looper, player, self.mode, self.ai_engine, self.board, depth))  # connecte la methode start du
        # process a la methode looper de la tache en passant les parametre definie.
        worker.move.connect(self.can_play_ai_move)
        worker.change_mode.connect(self.ai_muss_play) # la tache a change le mode du player en mode AI et demande au
        # joeur de rejouer car aucun autre mouvement na ete trouver dans le mode opening.
        worker.finished.connect(thread.quit)  # si la tache est fini se deconnecter du process
        worker.finished.connect(worker.deleteLater)  # si la tache est fini detruire  la tache
        thread.finished.connect(thread.deleteLater)  # detruire le process
        thread.start()
        return thread

    def can_play_ai_move(self, player, ai_move):
        """
        apres avoir determiner par "la strategy" de l'AI quel move jouer cette methode execute donc le deplacement du pion sur l'echequier
        :param player:
        :param ai_move:
        :return:
        """
        (hasTake, oldPos, newPos, is_echec_info) = self.board.play_ai_move(ai_move)
        if oldPos is not None and newPos is not None:
            if hasTake:
                sound_clik()
            self.move_cell_info.clear()
            key = conversion2(oldPos)
            self.move_cell_info.append((key[0] * self.case_size, key[1] * self.case_size))
            key = conversion2(newPos)
            self.move_cell_info.append((key[0] * self.case_size, key[1] * self.case_size))
            self.paint_cell_after_move = True
            if is_echec_info[0] and is_echec_info[1] is not None:
                sound_echec()
                self.paint_cell_echec = True
                key = conversion2(is_echec_info[1])
                self.echec_cell_info = (key[0] * self.case_size, key[1] * self.case_size)

            else:
                self.paint_cell_echec = False
            # self.player_deplaced = False
            sound_move()
            if player == self.player_2:
                self.player_2.has_play = True
                self.player_1.has_play = False
                if self.mode == MODE_PLAYER_AI:
                    self.player_1.is_first_click = True
            else:
                self.player_1.has_play = True
                self.player_2.has_play = False
            self.update()

        if self.board.check_echec_matt():
            self.alert_echec_matt(self.board.current_player_color)

        self.control_ai_thread = False
        time.sleep(1.5)  # attendre 1.5s avant que le prochain joeur AI joue
        self.ai_game_ai()  # le prochain ai doit jouer

    def alert_echec_matt(self, player_color):
        sound_echec_mat()
        buttonReply = QMessageBox.information(self, 'Echec et Matt', "Joueur de couleur " + player_color + " a perdu!",
                                              QMessageBox.Ok, QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            self.close()

    def alert_pat(self):
        buttonReply = QMessageBox.information(self, 'PAT', "Egalité entre les deux joueurs",
                                              QMessageBox.Ok, QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            self.close()

    def alert_start_ai_duel(self):
        buttonReply = QMessageBox.question(self, 'AI vs AI', "Commencer le Duel AI vs AI ?",
                                           QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            self.ai_game_ai()
        if buttonReply == QMessageBox.No:
            self.hide()
            self.parent.show()

    def paint_possible_moves(self, painter: QPainter):
        pen = QPen(Qt.darkGray)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0, 40))
        painter.drawRect(QRect(self.selected_pos[0], self.selected_pos[1], self.case_size, self.case_size))

        pen = QPen(Qt.lightGray)
        pen.setWidth(1)
        painter.setPen(pen)

        for key in self.pos:
            painter.drawRect(QRect(key[0], key[1], self.case_size, self.case_size))

    def paint_cell_info(self, painter: QPainter):

        pen = QPen(Qt.darkGray)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 255, 0, 40))

        pen = QPen(Qt.lightGray)
        pen.setWidth(1)
        painter.setPen(pen)
        for key in self.move_cell_info:
            # cellInfo contient la position avant et apres deplacement
            painter.drawRect(QRect(key[0], key[1], self.case_size, self.case_size))

    def paint_cell_echec_info(self, painter: QPainter):

        pen = QPen(Qt.darkGray)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(207, 0, 15, 125))

        pen = QPen(Qt.lightGray)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(QRect(self.echec_cell_info[0], self.echec_cell_info[1], self.case_size, self.case_size))


class NegamaxWorker(QObject):
    finished = pyqtSignal()
    move = pyqtSignal(object, tuple)

    @pyqtSlot()
    def looper(self, player, mode, engine, board, depth):
        ai_move = engine.negamax(copy.deepcopy(board), depth, -10000, 10000, board.current_player_color)[0]
        self.move.emit(player, ai_move)  # apres avoir exexuter negamax envoi le signal au process
        self.finished.emit()  # envoi le signal que la tache est finie


class OpeningAIWorker(QObject):
    finished = pyqtSignal()
    change_mode = pyqtSignal(object)
    move = pyqtSignal(object, tuple)

    @pyqtSlot()
    def looper(self, player, mode,  engine, board, depth,):

        if player.color == "blanc":
            moves = board.last_moves_black
            next_move = None
            move = None
            if moves:
                move_tupel = moves[- 1]
                move = move_tupel[0] + move_tupel[1]
            if mode == MODE_AI_AI:
                next_move = engine.open_tree_AI.get_next_move_AI_AI()
            elif mode == MODE_PLAYER_AI:
                next_move = engine.open_tree_AI.get_next_move_single_AI(player.color, move)
        else:
            moves = board.last_moves_white
            next_move = None
            if moves:
                move_tupel = moves[- 1]
                move = move_tupel[0] + move_tupel[1]
                if mode == MODE_AI_AI:
                    next_move = engine.open_tree_AI.get_next_move_AI_AI()
                elif mode == MODE_PLAYER_AI:
                    next_move = engine.open_tree_AI.get_next_move_single_AI(player.color, move)

        if next_move is not None: # jouer next_move si il a trouver qqch
            self.move.emit(player, next_move)
        else: # dans le cas contraire change le mode du player en AI et demander lui de rejouer
            player.mode = 'AI'
            self.change_mode.emit(player)  # change_mode signale a la methode ai_muss_play enn lui passant l instance
            # du player qui doit rejouer en mode AI
        self.finished.emit()


class BasicAIWorker(QObject):
    change_mode = pyqtSignal()
    finished = pyqtSignal()
    move = pyqtSignal(object, tuple)

    @pyqtSlot()
    def looper(self, player, mode, engine, board, depth):
        ai_move = engine.basic_AI(board)
        self.move.emit(player, ai_move)  # apres avoir exexuter minimax envoi le signal au process
        self.finished.emit()  # envoi le signal que la tache est finie


class MinimaxWorker(QObject):
    change_mode = pyqtSignal()
    finished = pyqtSignal()
    move = pyqtSignal(object, tuple)

    @pyqtSlot()
    def looper(self, player, mode, engine, board, depth):
        ai_move = engine.minimax(copy.deepcopy(board), depth, -10000, 10000, True, board.current_player_color)[0]
        self.move.emit(player, ai_move)  # apres avoir exexuter BasicAi envoi le signal au process
        self.finished.emit()  # envoi le signal que la tache est finie


class Player:
    def __init__(self):
        self.color = ""
        self.has_play = False
        self.is_ai = False
        self.is_first_click = True  # variable de controle du premier et du second clique pour un humanPlayer. si la
        # variable est True le clique du player est considere comme le premier clique sinon comme le 2eme clique
        self.mode = ''


class HMPlayer(Player):

    def __init__(self, color):
        super().__init__()
        self.color = color


class AIPlayer(Player):

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.is_ai = True
        self.mode = 'open'


class MyWidget(QWidget):
    def closeEvent(self, event):
        sys.exit()


class Game:
    def __init__(self):
        self.wind2 = None
        self.window = None
        self.window = MyWidget()
        self.window.setWindowTitle(
            "CHESS-GAME Developed by ---------------------------------------------------------------------JOEL-KHA")
        self.window.setFixedWidth(900)
        # place window in (x,y) coordinates
        self.window.move(560, 0)
        self.window.setStyleSheet("background: #161219;")
        grid = QGridLayout()
        image = QPixmap("ima1.jpg")
        logo1 = QLabel()
        logo1.setPixmap(image)
        logo1.setAlignment(QtCore.Qt.AlignHCenter)
        logo1.setStyleSheet("margin-top: 100px;")
        image1 = QPixmap("imagg.png")
        logo2 = QLabel()
        logo2.setPixmap(image1)
        logo2.setAlignment(QtCore.Qt.AlignHCenter)
        logo2.setStyleSheet("margin-top: 50px;")

        button1 = QPushButton("PLAYER VS PLAYER")
        button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button1.setStyleSheet("*{border: 2px solid '#BC006C';" + "border-raduis: 20px;" + "font-size: 20px;"
                              + "color: white;" + "padding: 25px 0;" + "margin: 10px 20px;}" + "*:hover{background: "
                                                                                               "'#BC006C';}")
        button2 = QPushButton("PLAYER VS AI")
        button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button2.setStyleSheet("*{border: 2px solid '#BC006C';" + "border-raduis: 20px;" + "font-size: 20px;"
                              + "color: white;" + "padding: 25px 0;" + "margin: 10px 20px;}" + "*:hover{background: "
                                                                                               "'#BC006C';}")

        button3 = QPushButton("AI VS AI")
        button3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button3.setStyleSheet("*{border: 2px solid '#BC006C';" + "border-raduis: 20px;" + "font-size: 20px;"
                              + "color: white;" + "padding: 25px 0;" + "margin: 5px 20px;}" + "*:hover{background: "
                                                                                              "'#BC006C';}")
        button1.clicked.connect(self.start_mode_player_player)
        button2.clicked.connect(self.start_mode_player_ai)
        button3.clicked.connect(self.start_mode_ai_ai)
        grid.addWidget(logo2)
        grid.addWidget(logo1)
        grid.addWidget(button1)
        grid.addWidget(button2)
        grid.addWidget(button3)
        self.window.setLayout(grid)
        self.window.show()

    def start_mode_player_player(self):
        self.start_mode(MODE_PLAYER_PLAYER)

    def start_mode_player_ai(self):
        self.start_mode(MODE_PLAYER_AI)

    def start_mode_ai_ai(self):
        self.start_mode(MODE_AI_AI)
        self.wind2.alert_start_ai_duel()

    def start_mode(self, mode):
        sound_clik()
        E = Echiquier()

        # E.deplacer(E.cases[E.coord.index("a2")], "g7")
        # E.deplacer(E.cases[E.coord.index("c7")], "h2")
        # E.deplacer(E.cases[E.coord.index("d7")], "a6")
        # E.deplacer(E.cases[E.coord.index("a8")], "a5")
        # E.deplacer(E.cases[E.coord.index("b7")], "e3")
        # E.deplacer(E.cases[E.coord.index("b1")], "b7")
        # E.deplacer(E.cases[E.coord.index("g1")], "a4")
        # E.deplacer(E.cases[E.coord.index("c2")], "b3")
        # E.deplacer(E.cases[E.coord.index("c1")], "a2")
        # E.deplacer(E.cases[E.coord.index("f1")], "b2")
        # E.deplacer(E.cases[E.coord.index("d1")], "h7")
        # E.deplacer(E.cases[E.coord.index("f8")], "d1")
        # E.deplacer(E.cases[E.coord.index("a1")], "c1")
        # E.deplacer(E.cases[E.coord.index("b8")], "d4")
        #
        # E.deplacer(E.cases[E.coord.index("e8")], "d5")
        # E.deplacer(E.cases[E.coord.index("h1")], "e7")
        # E.deplacer(E.cases[E.coord.index("f7")], "a7")
        #
        # E.deplacer(E.cases[E.coord.index("h8")], "h5")
        # E.deplacer(E.cases[E.coord.index("d8")], "h1")
        # E.deplacer(E.cases[E.coord.index("e1")], "g8")
        # E.deplacer(E.cases[E.coord.index("c8")], "g1")
        #
        # E.cases[E.coord.index("a1")] = None
        # E.cases[E.coord.index("b1")] = None
        # E.cases[E.coord.index("c2")] = None
        # E.cases[E.coord.index("d2")] = None
        # E.cases[E.coord.index("e2")] = None
        # E.cases[E.coord.index("f2")] = None
        # E.cases[E.coord.index("g2")] = None
        # E.cases[E.coord.index("e1")] = None
        # E.cases[E.coord.index("f1")] = None
        # E.cases[E.coord.index("a8")] = None
        # E.cases[E.coord.index("b8")] = None
        # E.cases[E.coord.index("c8")] = None
        # E.cases[E.coord.index("d8")] = None
        # E.cases[E.coord.index("f8")] = None
        # E.cases[E.coord.index("h8")] = None
        # E.cases[E.coord.index("c7")] = None
        # E.cases[E.coord.index("f7")] = None
        # #test pat
        # E.cases[E.coord.index("b1")] = None
        # E.cases[E.coord.index("c1")] = None
        # E.cases[E.coord.index("d1")] = None
        # E.cases[E.coord.index("f1")] = None
        # E.cases[E.coord.index("g1")] = None
        # E.cases[E.coord.index("h1")] = None
        # E.cases[E.coord.index("a2")] = None
        # E.cases[E.coord.index("b2")] = None
        # E.cases[E.coord.index("c2")] = None
        # E.cases[E.coord.index("d2")] = None
        # E.cases[E.coord.index("e2")] = None
        # E.cases[E.coord.index("f2")] = None
        # E.cases[E.coord.index("h2")] = None
        # E.cases[E.coord.index("a8")] = None
        # E.cases[E.coord.index("b8")] = None
        # E.cases[E.coord.index("c8")] = None
        # E.cases[E.coord.index("d8")] = None
        # E.cases[E.coord.index("e7")] = None
        # E.cases[E.coord.index("f8")] = None
        # E.cases[E.coord.index("g8")] = None
        # E.cases[E.coord.index("h8")] = None
        # E.cases[E.coord.index("a7")] = None
        # E.cases[E.coord.index("b7")] = None
        # E.cases[E.coord.index("c7")] = None
        # E.cases[E.coord.index("d7")] = None
        # E.cases[E.coord.index("e7")] = None
        # E.cases[E.coord.index("f7")] = None
        # E.cases[E.coord.index("g7")] = None
        # E.cases[E.coord.index("h7")] = None
        # E.deplacer(E.cases[E.coord.index("g2")], "c6")
        # E.deplacer(E.cases[E.coord.index("a1")], "b1")
        # E.deplacer(E.cases[E.coord.index("e8")], "a8")

        self.wind2 = QtBoard(mode, E)
        self.wind2.parent = self.window
        self.wind2.show()
        self.window.hide()


def sound_move():
    threading.Thread(target=playsound, args=('soundmove.wav',), daemon=False).start()


def sound_clik():
    threading.Thread(target=playsound, args=('clique.wav',), daemon=False).start()


def sound_echec():
    threading.Thread(target=playsound, args=('echec_au_roi.wav',), daemon=False).start()


def sound_echec_mat():
    threading.Thread(target=playsound, args=('echec_et_mat.wav',), daemon=False).start()
