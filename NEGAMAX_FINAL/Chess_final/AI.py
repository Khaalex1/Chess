from board import *
import math
from random import choice
import copy
from dict import *

zobTable = [[random.randint(1, 2 ** 64 - 1) for i in range(12)] for j in range(64)]
transposition = {}

open_tree_AI = OpenBookTree("book.txt")
#open_tree_AI_2 = OpenBookTree("book.txt")

class Position:
    def __init__(self):
        self.lowerbound = -10000
        self.upperbound = 10000
        self.best_move = None

def negamax(board, depth, alpha, beta, color):
    hashcode = computeHash(board)
    if transposition and transposition.__contains__(hashcode):
        position = transposition.get(hashcode)
        if position.lowerbound >= beta:
            return position.best_move, position.lowerbound
        if position.upperbound <= alpha:
            return position.best_move, position.upperbound
        alpha = max(alpha, position.lowerbound)
        beta = min(beta, position.upperbound)

    moves = board.get_move()
    if depth == 0 or board.check_echec_matt() or not moves:
        score = evaluate(board, color)
        return None, score

    best_move = choice(moves)
    evaluation = -10000
    for move in moves:
        piece = board.cases[Echequier.coord.index(move[0])]
        board.deplacer(piece, move[1])
        current_eval = - negamax(board, depth - 1, -beta, -alpha, switch_color(color))[1]
        board.back_last_move(piece.couleur)
        if current_eval > evaluation:
            evaluation = current_eval
            best_move = move
        alpha = max(alpha, current_eval)
        if beta <= alpha:
            break

    tosavepos = Position()
    tosavepos.best_move = best_move
    if evaluation <= alpha:
        tosavepos.upperbound = evaluation
        transposition[hashcode] = tosavepos
    elif alpha < evaluation < beta:
        tosavepos.lowerbound = evaluation
        tosavepos.upperbound = evaluation
        transposition[hashcode] = tosavepos
    elif beta <= evaluation:
        tosavepos.lowerbound = evaluation
        transposition[hashcode] = tosavepos

    return best_move, evaluation

def minimax(board, depth, alpha, beta, maximizing_player, maximizing_color):
    hashcode = computeHash(board)
    if transposition and transposition.__contains__(hashcode):
        position = transposition.get(hashcode)
        if position.lowerbound >= beta:
            return position.best_move, position.lowerbound
        if position.upperbound <= alpha:
            return position.best_move, position.upperbound
        alpha = max(alpha, position.lowerbound)
        beta = min(beta, position.upperbound)

    moves = board.get_move()
    if depth == 0 or board.check_echec_matt() or not moves:
        score = evaluate(board, maximizing_color)
        return None, score

    best_move = choice(moves)
    # evaluation = None
    if maximizing_player:
        evaluation = -10000
        for move in moves:
            piece = board.cases[Echequier.coord.index(move[0])]
            board.deplacer(piece, move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, False, maximizing_color)[1]
            board.back_last_move(piece.couleur)
            if current_eval > evaluation:
                evaluation = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        # return best_move, evaluation
    else:
        evaluation = 10000
        for move in moves:
            piece = board.cases[Echequier.coord.index(move[0])]
            board.deplacer(piece, move[1])
            current_eval = minimax(board, depth - 1, alpha, beta, True, maximizing_color)[1]
            board.back_last_move(piece.couleur)
            if current_eval < evaluation:
                evaluation = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        # return best_move, evaluation

    tosavepos = Position()
    tosavepos.best_move = best_move
    if evaluation <= alpha:
        tosavepos.upperbound = evaluation
        transposition[hashcode] = tosavepos
    elif alpha < evaluation < beta:
        tosavepos.lowerbound = evaluation
        tosavepos.upperbound = evaluation
        transposition[hashcode] = tosavepos
    elif beta <= evaluation:
        tosavepos.lowerbound = evaluation
        transposition[hashcode] = tosavepos

    return best_move, evaluation


def computeHash(board):
    h = 0
    for i in range(len(board.cases)):
        piece = board.cases[i]
        if piece is not None:
            h ^= zobTable[i][piece.code]
    return h

def switch_color(color):
    if color == "blanc":
        return "noir"
    else:
        return "blanc"

def evaluate(board, maximizing_color):
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
                      0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]

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
                     2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]

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

# def minimax(board, depth, alpha, beta, maximizing_player, maximizing_color):
#     moves = board.get_move()
#     if depth == 0 or board.check_echec_matt() or not moves:
#         return None, evaluate(board, maximizing_color)
#     best_move = choice(moves)
#     if maximizing_player:
#         maxEval = -10000
#         for move in moves:
#             piece = board.cases[Echequier.coord.index(move[0])]
#             board.deplacer(piece, move[1])
#             current_eval = minimax(copy.deepcopy(board), depth - 1, alpha, beta, False, maximizing_color)[1]
#             board.back_last_move(piece.couleur)
#             if current_eval > maxEval:
#                 maxEval = current_eval
#                 best_move = move
#             alpha = max(alpha, current_eval)
#             if beta <= alpha:
#                 break
#         return best_move, maxEval
#     else:
#         minEval = 10000
#         for move in moves:
#             piece = board.cases[Echequier.coord.index(move[0])]
#             board.deplacer(piece, move[1])
#             current_eval = minimax(copy.deepcopy(board), depth - 1, alpha, beta, True, maximizing_color)[1]
#             board.back_last_move(piece.couleur)
#             if current_eval < minEval:
#                 minEval = current_eval
#                 best_move = move
#             beta = min(beta, current_eval)
#             if beta <= alpha:
#                 break
#         return best_move, minEval
