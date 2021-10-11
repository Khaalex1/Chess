import time

from board import *
from random import choice
import copy
from dict import *
import random


class AIEngine:

    def __init__(self):
        self.zobTable = [[random.randint(1, 2 ** 64 - 1) for _ in range(12)] for _ in range(64)]  #liste qui contient 8x8 listes de 12 elemetns
        self.transposition = {}
        self.open_tree_AI = OpenBookTree("book.txt")

    def negamax(self, board, depth, alpha, beta, color):
        hashcode = self.compute_hash(
            board)  # codification du tableau a chaque situation ( ensemble des pions dans une positions)
        if self.transposition and self.transposition.__contains__(hashcode):
            position = self.transposition.get(hashcode)
            if position.lowerbound >= beta:
                return position.best_move, position.lowerbound
            if position.upperbound <= alpha:
                return position.best_move, position.upperbound
            alpha = max(alpha, position.lowerbound)
            beta = min(beta, position.upperbound)

        moves = board.get_move()
        if depth == 0 or board.check_echec_matt() or not moves:
            score = self.evaluate(board, color)
            return None, score

        best_move = choice(moves)
        evaluation = -10000
        for move in moves:
            piece = board.cases[Echiquier.coord.index(move[0])]
            board.deplacer(piece, move[1])
            current_eval = - self.negamax(board, depth - 1, -beta, -alpha, self.switch_color(color))[1]
            board.back_last_move(piece.couleur)
            if current_eval > evaluation:
                evaluation = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break

        tosavepos = Position()  # instance de classe
        tosavepos.best_move = best_move
        if evaluation <= alpha:
            tosavepos.upperbound = evaluation
            self.transposition[hashcode] = tosavepos
        elif alpha < evaluation < beta:
            tosavepos.lowerbound = evaluation
            tosavepos.upperbound = evaluation
            self.transposition[hashcode] = tosavepos
        elif beta <= evaluation:
            tosavepos.lowerbound = evaluation
            self.transposition[hashcode] = tosavepos

        return best_move, evaluation

    def minimax(self, board, depth, alpha, beta, maximizing_player, maximizing_color):
        hashcode = self.compute_hash(board)
        if self.transposition and self.transposition.__contains__(hashcode):
            position = self.transposition.get(hashcode)
            if position.lowerbound >= beta:
                return position.best_move, position.lowerbound
            if position.upperbound <= alpha:
                return position.best_move, position.upperbound
            alpha = max(alpha, position.lowerbound)
            beta = min(beta, position.upperbound)

        moves = board.get_move()
        if depth == 0 or board.check_echec_matt() or not moves:
            score = self.evaluate(board, maximizing_color)
            return None, score

        best_move = choice(moves)
        # evaluation = None
        if maximizing_player:
            evaluation = -10000
            for move in moves:
                piece = board.cases[Echiquier.coord.index(move[0])]
                board.deplacer(piece, move[1])
                current_eval = self.minimax(board, depth - 1, alpha, beta, False, maximizing_color)[1]
                board.back_last_move(piece.couleur)
                if current_eval > evaluation:
                    evaluation = current_eval
                    best_move = move
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
        else:
            evaluation = 10000
            for move in moves:
                piece = board.cases[Echiquier.coord.index(move[0])]
                board.deplacer(piece, move[1])
                current_eval = self.minimax(board, depth - 1, alpha, beta, True, maximizing_color)[1]
                board.back_last_move(piece.couleur)
                if current_eval < evaluation:
                    evaluation = current_eval
                    best_move = move
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break

        tosavepos = Position()
        tosavepos.best_move = best_move
        if evaluation <= alpha:
            tosavepos.upperbound = evaluation
            self.transposition[hashcode] = tosavepos
        elif alpha < evaluation < beta:
            tosavepos.lowerbound = evaluation
            tosavepos.upperbound = evaluation
            self.transposition[hashcode] = tosavepos
        elif beta <= evaluation:
            tosavepos.lowerbound = evaluation
            self.transposition[hashcode] = tosavepos

        return best_move, evaluation

    def basic_AI(self, board):
        time.sleep(2)
        piece_dep = ""
        to_position = ""
        hasTake = None
        oldPos = None
        liste_pieces = [piece for piece in board.cases if isinstance(piece, Piece) and piece.couleur == "noir"]
        i = 0
        random.shuffle(liste_pieces)
        if len(liste_pieces) < 16:
            ai_move = self.negamax(board, 2, -10000, 10000, board.current_player_color)[0]
            return ai_move[0], ai_move[1]
        if len(liste_pieces) < 8:
            ai_move = self.negamax(board, 3, -10000, 10000, board.current_player_color)[0]
            return ai_move[0], ai_move[1]

        if board.check_echec("noir"):
            j = 0
            for piece in liste_pieces:
                li = board.pos_piece_pouvant_etre_manger("blanc")
                move = piece.moves(board.cases.index(piece), board)
                liste_inter = inter(li, board.num(move))
                if liste_inter:
                    j = 1
                    to_position = board.choice_best_piece(liste_inter)
                    piece_dep = piece
                    hasTake = True
                    oldPos = board.cases.index(piece_dep)
                    # self.deplacer(piece_dep, to_position)
                    return Echiquier.coord[oldPos], to_position
                else:
                    pass
            if j == 0:
                for piece in liste_pieces:
                    move = piece.moves(board.cases.index(piece), board)
                    if move:
                        to_position = choice(move)
                        piece_dep = piece
                        if board.cases[to_position] is not None:
                            hasTake = True
                        oldPos = board.cases.index(piece_dep)
                        # self.deplacer(piece_dep, Echequier.coord[to_position])
                        return Echiquier.coord[oldPos], Echiquier.coord[to_position]

        for piece in liste_pieces:
            if piece.moves(board.cases.index(piece), board):
                li = board.pos_piece_pouvant_etre_manger("blanc")
                if board.pos_piece_pouvant_etre_manger("blanc"):
                    liste_inter = inter(board.num(piece.moves(board.cases.index(piece), board)), li)
                    if liste_inter:
                        to_position = board.choice_best_piece(liste_inter)
                        piece_dep = piece
                        if isinstance(piece_dep, Roi):
                            oldPos = board.cases.index(piece_dep)
                            # board.deplacer(piece_dep, to_position)
                            return Echiquier.coord[oldPos], to_position
                        echequier_copy = copy.deepcopy(board)
                        echequier_copy.cases[echequier_copy.coord.index(to_position)] = None
                        li = echequier_copy.check_menace("noir")
                        if li.__contains__(Echiquier.coord.index(to_position)):
                            liste_pos = board.pos_piece_pouvant_etre_manger("blanc")
                            for pieces in board.piece_pouvant_etre_mange(liste_pos):
                                if not li.__contains__(board.cases.index(pieces)):
                                    hasTake = True
                                    oldPos = board.cases.index(piece_dep)
                                    # self.deplacer(piece_dep, Echequier.coord[self.cases.index(pieces)])
                                    return Echiquier.coord[oldPos], to_position

                                else:
                                    if piece_dep.evaluer(pieces) >= 0:
                                        hasTake = True
                                        oldPos = board.cases.index(piece_dep)
                                        # self.deplacer(piece_dep, Echequier.coord[self.cases.index(pieces)])
                                        return Echiquier.coord[oldPos], to_position
                                    else:
                                        i = 0
                        else:
                            hasTake = True
                            oldPos = board.cases.index(piece_dep)
                            # self.deplacer(piece_dep, to_position)
                            return Echiquier.coord[oldPos], to_position

        if i == 0:
            random.shuffle(liste_pieces)
            for piece in liste_pieces:
                move = piece.moves(board.cases.index(piece), board)
                if move:
                    menace = board.check_menace("noir")
                    for i in menace:
                        if move.__contains__(i):
                            move.remove(i)
                    if move:
                        to_position = choice(move)
                        piece_dep = piece
                        if board.cases[to_position] is not None:
                            hasTake = True
                        oldPos = board.cases.index(piece_dep)
                        # self.deplacer(piece_dep, Echequier.coord[to_position])
                        return Echiquier.coord[oldPos], Echiquier.coord[to_position]
            if to_position == "":
                random.shuffle(liste_pieces)
                for piece in liste_pieces:
                    move = piece.moves(board.cases.index(piece), board)
                    if move:
                        to_position = choice(move)
                        piece_dep = piece
                        if board.cases[to_position] is not None:
                            hasTake = True
                        oldPos = board.cases.index(piece_dep)
                        # self.deplacer(piece_dep, Echequier.coord[to_position])
                        return Echiquier.coord[oldPos], Echiquier.coord[to_position]
        return oldPos, to_position

    def compute_hash(self, board):
        h = 0
        for i in range(len(board.cases)):
            piece = board.cases[i]
            if piece is not None:
                h ^= self.zobTable[i][piece.code]
        return h

    def switch_color(self, color):
        if color == "blanc":
            return "noir"
        else:
            return "blanc"

    def evaluate(self, board, maximizing_color):
        """
        :param board: echequier
        :param maximizing_color: couleur a maximiser
        :return: le score de la couleur a maximiser
        """
        evalachevalier_blanc = [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                                - 4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0,
                                - 3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0,
                                - 3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0,
                                - 3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0,
                                - 3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0,
                                - 4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0,
                                - 5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]

        evalachevalier_noir = evalachevalier_blanc[::-1]

        evalfou_blanc = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                         - 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0,
                         - 1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0,
                         - 1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0,
                         - 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0,
                         - 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
                         - 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0,
                         - 2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]

        evalfou_noir = evalfou_blanc[::-1]

        evaltour_blanc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5,
                          -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                          -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                          -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                          -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                          -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                          0.0, 0.0, 0.0, 1.5, 0.5, 1.5, 0.0, 0.0]

        evaltour_noir = evaltour_blanc[::-1]

        evalreine_blanche = [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                             -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0,
                             -1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0,
                             -0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5,
                             0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5,
                             -1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0,
                             -1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0,
                             -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]

        evalreine_noir = evalreine_blanche[::-1]

        evalroi_blanc = [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                         -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                         -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                         -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                         -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                         -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                         2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0,
                         2.0, 3.0, 5.0, -1.0, 0.0, -1.0, 5.0, 2.0]

        evalroi_noir = evalroi_blanc[::-1]

        evalpion_blanc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                          1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0,
                          0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5,
                          0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0,
                          0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5,
                          0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        evalpion_noir = evalpion_blanc[::-1]

        bonus_or_malus_pion = 0
        bonus_or_malus_pion_noir = 0
        bonus_or_malus_fou = 0
        bonus_or_malus_fou_noir = 0
        bonus_or_malus_reine = 0
        bonus_or_malus_reine_noir = 0
        bonus_or_malus_roi = 0
        bonus_or_malus_roi_noir = 0
        bonus_or_malus_tour = 0
        bonus_or_malus_tour_noir = 0
        bonus_or_malus_caval = 0
        bonus_or_malus_caval_noir = 0

        for i in board.pos_piece("blanc", Pion):
            bonus_or_malus_pion = bonus_or_malus_pion + evalpion_blanc[i]
        for i in board.pos_piece("blanc", Fou):
            bonus_or_malus_fou = bonus_or_malus_fou + evalfou_blanc[i]
        for i in board.pos_piece("blanc", Roi):
            bonus_or_malus_roi = bonus_or_malus_roi + evalroi_blanc[i]
        for i in board.pos_piece("blanc", Reine):
            bonus_or_malus_reine = bonus_or_malus_reine + evalreine_blanche[i]
        for i in board.pos_piece("blanc", Tour):
            bonus_or_malus_tour = bonus_or_malus_tour + evaltour_blanc[i]
        for i in board.pos_piece("blanc", Cavalier):
            bonus_or_malus_caval = bonus_or_malus_caval + evalachevalier_blanc[i]
        bonus_or_malus_blanc = bonus_or_malus_reine + bonus_or_malus_tour + bonus_or_malus_roi + bonus_or_malus_roi + bonus_or_malus_pion + bonus_or_malus_caval

        for i in board.pos_piece("noir", Pion):
            bonus_or_malus_pion_noir = bonus_or_malus_pion_noir + evalpion_noir[i]
        for i in board.pos_piece("noir", Fou):
            bonus_or_malus_fou_noir = bonus_or_malus_fou_noir + evalfou_noir[i]
        for i in board.pos_piece("noir", Roi):
            bonus_or_malus_roi_noir = bonus_or_malus_roi_noir + evalroi_noir[i]
        for i in board.pos_piece("noir", Reine):
            bonus_or_malus_reine_noir = bonus_or_malus_reine_noir + evalreine_noir[i]
        for i in board.pos_piece("noir", Tour):
            bonus_or_malus_tour_noir = bonus_or_malus_tour_noir + evaltour_noir[i]
        for i in board.pos_piece("noir", Cavalier):
            bonus_or_malus_caval_noir = bonus_or_malus_caval_noir + evalachevalier_noir[i]
        bonus_or_malus_noir = bonus_or_malus_reine + bonus_or_malus_tour + bonus_or_malus_roi + bonus_or_malus_roi + bonus_or_malus_pion + bonus_or_malus_caval_noir

        if maximizing_color == "blanc":

            return board.score_blanc() - board.score_noir() + bonus_or_malus_blanc - bonus_or_malus_noir
        else:

            return board.score_noir() - board.score_blanc() + bonus_or_malus_noir - bonus_or_malus_blanc


class Position:
    def __init__(self):
        self.lowerbound = -10000
        self.upperbound = 10000
        self.best_move = None
