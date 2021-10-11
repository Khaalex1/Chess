from pieces import *


def inter(l1, l2):
    """
    permet juste de faire l'intersection entre deux listes
    :param l1:
    :param l2:
    :return:
    """
    t = []
    for i in l1:
        for j in l2:
            if i == j:
                t.append(i)
    return t


class Echiquier():
    coord = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
             'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
             'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
             'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
             'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
             'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
             'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
             'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

    def __init__(self):
        self.cases = [Tour('noir'), Cavalier('noir'), Fou('noir'), Reine('noir'), Roi('noir'), Fou('noir'),
                      Cavalier('noir'), Tour('noir'),
                      Pion('noir'), Pion('noir'), Pion('noir'), Pion('noir'), Pion('noir'), Pion('noir'), Pion('noir'),
                      Pion('noir'),
                      None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None,
                      Pion('blanc'), Pion('blanc'), Pion('blanc'), Pion('blanc'), Pion('blanc'), Pion('blanc'),
                      Pion('blanc'), Pion('blanc'),
                      Tour('blanc'), Cavalier('blanc'), Fou('blanc'), Reine('blanc'), Roi('blanc'), Fou('blanc'),
                      Cavalier('blanc'), Tour('blanc')]
        self.is_echec_blanc = False
        self.is_echec_noir = False
        self.current_player = None
        self.current_player_color = "blanc"
        self.is_echec_matt = False
        self.last_moves_white = []
        self.last_moves_black = []

    def switch_current_player_color(self):
        if self.current_player_color == 'blanc':
            self.current_player_color = "noir"
            return self.current_player_color
        else:
            self.current_player_color = "blanc"
            return self.current_player_color

    def check_echec(self, couleur):
        if couleur == 'blanc':
            return self.is_echec_blanc
        elif couleur == 'noir':
            return self.is_echec_noir

    def get_dest_pos(self, pos: str):
        """
        :param pos: postion dans la variable #coord#   exp:#a1
        :return: la postion dans la variable #cases#
        """
        return Echiquier.coord.index(pos)

    def deplacer(self, piece, pos2):
        """
        deplacer , enregistrer les info du mouvement executer et changer la couleur du joueur
        :param piece: piece a deplacer
        :param pos2: position finale
        :return: None
        """
        move_to_save, is_echec_info = self.deplacer_simple(piece, pos2)
        self.save_last_move(piece.couleur, move_to_save)
        # changer la couleur du joueur apres deplaement
        self.switch_current_player_color()
        return is_echec_info

    def deplacer_simple(self, piece, pos2):
        """
        deplacement effectif d'une piece, dependant des situations
        :param piece: piece a deplacer
        :param pos2: position finale
        :return: information du mouvement executer sous forme de liste
        """
        pos1 = Echiquier.coord[self.cases.index(piece)]
        move = [pos1, pos2, piece, self.cases[self.get_dest_pos(pos2)]]
        if isinstance(piece, Roi) and piece.couleur == "blanc" and pos1 == "e1" and pos2 == "c1":
            # rendre effectif le grand_roque
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            self.cases[self.get_dest_pos("d1")] = self.cases[self.get_dest_pos('a1')]
            self.cases[self.get_dest_pos("a1")] = None
            piece.has_do_first_move_r = True
            self.cases[self.get_dest_pos("d1")].has_do_first_move_t = True
            move.append("a1")
            move.append("d1")
            move.append(self.cases[self.get_dest_pos("d1")])
            move.append(self.cases[self.get_dest_pos("a1")])
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Roi) and piece.couleur == "blanc" and pos1 == "e1" and pos2 == "g1":
            # rendre effectif le petit_roque
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            self.cases[self.get_dest_pos("f1")] = self.cases[self.get_dest_pos('h1')]
            self.cases[self.get_dest_pos("h1")] = None
            piece.has_do_first_move_r = True
            move.append("h1")
            move.append("f1")
            move.append(self.cases[self.get_dest_pos("f1")])
            move.append(self.cases[self.get_dest_pos("h1")])
            self.is_echec(piece.couleur)
            self.cases[self.get_dest_pos("f1")].has_do_first_move_t = True
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Roi) and piece.couleur == "noir" and pos1 == "e8" and pos2 == "g8":
            # rendre effectif le grand_roque
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            self.cases[self.get_dest_pos("f8")] = self.cases[self.get_dest_pos('h8')]
            self.cases[self.get_dest_pos("h8")] = None
            piece.has_do_first_move_r = True
            self.cases[self.get_dest_pos("f8")].has_made_first_t = True
            move.append("h8")
            move.append("f8")
            move.append(self.cases[self.get_dest_pos("f8")])
            move.append(self.cases[self.get_dest_pos("h8")])
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Roi) and piece.couleur == "noir" and pos1 == "e8" and pos2 == "c8":
            # rendre effectif le petit_roque
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            self.cases[self.get_dest_pos("d8")] = self.cases[self.get_dest_pos('a8')]
            self.cases[self.get_dest_pos("a8")] = None
            piece.has_do_first_move_r = True
            self.cases[self.get_dest_pos("d8")].has_do_first_move_r = True
            move.append("a8")
            move.append("d8")
            move.append(self.cases[self.get_dest_pos("d8")])
            move.append(self.cases[self.get_dest_pos("a8")])
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Tour):
            # deplacement de la tour
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            piece.has_do_first_move_t = True
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Roi):
            # deplacement du roi
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            piece.has_do_first_move_r = True
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "noir" and ((pos1 == "a7" and pos2 == "a5")
                                                                    or (pos1 == "b7" and pos2 == "b5") or (
                                                                            pos1 == "c7" and pos2 == "c5") or (
                                                                            pos1 == "d7" and pos2 == "d5")
                                                                    or (pos1 == "e7" and pos2 == "e5") or (
                                                                            pos1 == "f7" and pos2 == "f5") or (
                                                                            pos1 == "g7" and pos2 == "g5")
                                                                    or (pos1 == "h7" and pos2 == "h5")):
            # rendre effectif le deplacement de deux cases du pion noir
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            self.is_echec(piece.couleur)
            piece.test_deplace_p = True
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "blanc" and ((pos1 == "a2" and pos2 == "a4")
                                                                     or (pos1 == "b2" and pos2 == "b4") or (
                                                                             pos1 == "c2" and pos2 == "c4") or (
                                                                             pos1 == "d2" and pos2 == "d4")
                                                                     or (pos1 == "e2" and pos2 == "e4") or (
                                                                             pos1 == "f2" and pos2 == "f4") or (
                                                                             pos1 == "g2" and pos2 == "g4")
                                                                     or (pos1 == "h2" and pos2 == "h4")):
            # rendre effectif le deplacement de deux cases du pion blanc
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            piece.test_deplace_p = True
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "blanc" and ((pos1 == "b5" and (pos2 == "a6" or pos2 == "c6"))
                                                                     or (pos1 == "a5" and pos2 == "b6") or (
                                                                             pos1 == "c5" and (
                                                                             pos2 == "b6" or pos2 == "d6")) or (
                                                                             pos1 == "d5" and (
                                                                             pos2 == "c6" or pos2 == "e6"))
                                                                     or (pos1 == "e5" and (
                        pos2 == "d6" or pos2 == "f6")) or (

                                                                             pos1 == "f5" and (
                                                                             pos2 == "e6" or pos2 == "g6")) or (
                                                                             pos1 == "g5" and (
                                                                             pos2 == "f6" or pos2 == "h6"))
                                                                     or (pos1 == "h5" and pos2 == "g6")):
            if (isinstance(self.cases[self.get_dest_pos(pos1) + 1], Pion) and self.cases[
                self.get_dest_pos(pos1) + 1].couleur == "noir"):
                # rendre effectif la prise en passant
                # ici faut enregister l index et la reference du pion qui es manger
                pos = Echiquier.coord[self.get_dest_pos(pos2) + 8]
                move.append(pos)
                move.append(pos)
                move.append(self.cases[self.get_dest_pos(pos2) + 8])
                move.append(None)
                self.cases[self.get_dest_pos(pos1)] = None
                self.cases[self.get_dest_pos(pos2)] = piece
                self.cases[self.get_dest_pos(pos2) + 8] = None
                self.is_echec(piece.couleur)
                self.is_echec(piece.opponent_color())
                return move, self.is_echec(piece.opponent_color())
            if (isinstance(self.cases[self.get_dest_pos(pos1) - 1], Pion) and self.cases[
                self.get_dest_pos(pos1) - 1].couleur == "noir"):
                pos = Echiquier.coord[self.get_dest_pos(pos2) + 8]
                move.append(pos)
                move.append(pos)
                move.append(self.cases[self.get_dest_pos(pos2) + 8])
                move.append(None)
                self.cases[self.get_dest_pos(pos1)] = None
                self.cases[self.get_dest_pos(pos2)] = piece
                self.cases[self.get_dest_pos(pos2) + 8] = None
                self.is_echec(piece.couleur)
                return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "noir" and ((pos1 == "b4" and (pos2 == "a3" or pos2 == "c3"))
                                                                    or (pos1 == "a4" and pos2 == "b3") or (
                                                                            pos1 == "c4" and (
                                                                            pos2 == "b3" or pos2 == "d3")) or (
                                                                            pos1 == "d4" and (
                                                                            pos2 == "c3" or pos2 == "e3"))
                                                                    or (pos1 == "e4" and (
                        pos2 == "d3" or pos2 == "f3")) or (
                                                                            pos1 == "f4" and (
                                                                            pos2 == "e3" or pos2 == "g3")) or (
                                                                            pos1 == "g4" and (
                                                                            pos2 == "f3" or pos2 == "h3"))
                                                                    or (pos1 == "h4" and pos2 == "g3")):
            if (isinstance(self.cases[self.get_dest_pos(pos1) + 1], Pion) and self.cases[
                self.get_dest_pos(pos1) + 1].couleur == "blanc"):
                # rendre effectif la prise en passant
                pos = Echiquier.coord[self.get_dest_pos(pos2) - 8]
                move.append(pos)
                move.append(pos)
                move.append(self.cases[self.get_dest_pos(pos2) - 8])
                move.append(None)
                self.cases[self.get_dest_pos(pos1)] = None
                self.cases[self.get_dest_pos(pos2)] = piece
                self.cases[self.get_dest_pos(pos2) - 8] = None
                self.is_echec(piece.couleur)
                return move, self.is_echec(piece.opponent_color())
            if (isinstance(self.cases[self.get_dest_pos(pos1) - 1], Pion) and self.cases[
                self.get_dest_pos(pos1) - 1].couleur == "blanc"):
                pos = Echiquier.coord[self.get_dest_pos(pos1) - 1]
                move.append(pos)
                move.append(pos)
                move.append(self.cases[self.get_dest_pos(pos2) - 8])
                move.append(None)
                self.cases[self.get_dest_pos(pos1)] = None
                self.cases[self.get_dest_pos(pos2)] = piece
                self.cases[self.get_dest_pos(pos2) - 8] = None
                self.is_echec(piece.couleur)
                self.is_echec(piece.opponent_color())
                return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "noir" and ["a1", "b1", "c1", "d1", "e1", "f1", "g1",
                                                                                                        "h1"].__contains__(
            pos2):
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            piece.promotion(self, pos2)
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())

        if isinstance(piece, Pion) and piece.couleur == "blanc" and ["a8", "b8", "c8", "d8", "e8", "f8", "g8",
                                                                                                         "h8"].__contains__(
            pos2):
            self.cases[self.get_dest_pos(pos1)] = None
            self.cases[self.get_dest_pos(pos2)] = piece
            piece.promotion(self, pos2)
            self.is_echec(piece.couleur)
            return move, self.is_echec(piece.opponent_color())
        # rendre effectif un deplacement quelconque , autres que les precedents
        self.cases[self.get_dest_pos(pos1)] = None
        self.cases[self.get_dest_pos(pos2)] = piece
        self.is_echec(piece.couleur)
        piece.test_deplace_p = False
        return move, self.is_echec(piece.opponent_color())

    def num(self, l: list):
        """
        :param l: liste des positions #12
        :return: liste des positions en aphanumerique #a4#
        """
        l3 = []
        for ele in l:
            position_al = self.coord[ele]
            l3.append(position_al)
        return l3

    def save_last_move(self, color, move):
        """

        :param color: couleur du joueur
         :param move: deplacement sous forme de couple (pos_initiale, pos_finale,
        reference du pion a la position pos_initial, reference du pion a la position pos_finale)
        :return:
        """
        if color == "blanc":
            self.last_moves_white.append(move)
        else:
            self.last_moves_black.append(move)

    def back_last_move(self, color):
        """
        Annule le dernier deplacement effectuer par le joueur de couleur color
        :param color: couleur du joueur
        :return:
        """
        if color == "blanc":
            last_moves = self.last_moves_white
        else:
            last_moves = self.last_moves_black

        move = last_moves.pop()

        if move.__len__() == 4:
            piece1 = move[2]  # piece initial
            piece2 = move[3]  # piece finale
            if isinstance(piece1, Roi):
                r_first_move = False
                for mov in last_moves:
                    if isinstance(mov[3], Roi):
                        # si le roi est dans le last_move apres qu'on ait efface le dernier mouvement de last_move
                        # c'est qu'il s'etait deplace
                        r_first_move = True
                        break
                piece1.has_do_first_move_r = r_first_move
            elif isinstance(piece1, Tour):
                t_first_move = False
                for mov in last_moves:
                    if isinstance(mov[3], Tour):
                        t_first_move = True
                        break
                piece1.has_do_first_move_t = t_first_move
            self.cases[self.get_dest_pos(move[0])] = piece1  # remettre les pieces a leur positions
            self.cases[self.get_dest_pos(move[1])] = piece2
        elif move.__len__() == 8:  # mouvement special
            piece1 = move[2]  # piece initial
            piece2 = move[3]  # piece finale

            piece3 = move[6]  # piece initial
            piece4 = move[7]  # piece finale
            if isinstance(piece1, Roi) and isinstance(piece3, Tour):  # reset le premier mouvement du roi ou de la Tour
                piece1.has_do_first_move_r = False
                piece3.has_do_first_move_t = False
            self.cases[self.get_dest_pos(move[0])] = piece1
            self.cases[self.get_dest_pos(move[1])] = piece2
            if move[4] is not move[5]:  # grand roque ou petit roque
                self.cases[self.get_dest_pos(move[4])] = piece3
                self.cases[self.get_dest_pos(move[5])] = piece4
            else:  # prise en passant
                self.cases[self.get_dest_pos(move[4])] = piece3
        self.switch_current_player_color()

    def pos_piece(self, color, type_piece):
        l = []
        for index, piece in enumerate(self.cases):
            if isinstance(piece, type_piece) and piece.couleur == color:
                l.append(index)
        return l

    def choice_best_piece(self, l: list):
        """
        :param l: liste des positions des pions pouvant etre mangé
        :return: retourne la position du  pion ayant la plus grande valeur
        """
        l1 = []
        l2 = []
        for ele in l:
            x1 = self.cases[Echiquier.coord.index(ele)]
            l1.append(x1)
        for piece in l1:
            if not isinstance(piece, Roi):
                evalu = piece.evaluation
                l2.append(evalu)
        maxi = max(l2)
        choix = l2.index(maxi)
        return l[choix]

    def pos_piece_pouvant_etre_manger(self, color):
        """
        :param liste: liste des positions possibles
        :return: renvoi la  liste des postions des pions pouvant etre mangé
        """
        l = []
        menace = self.check_menace(color)
        l1 = [piece for piece in self.cases if piece is not None and piece.couleur == color]
        for piece in l1:
            pos = self.cases.index(piece)
            if menace.__contains__(pos):
                l.append(pos)
        return self.num(l)

    def piece_pouvant_etre_mange(self, liste: list):
        """
              :param liste: liste des positions des pieces pouvant etre mange
              :return: renvoi la  liste des pions pouvant etre mangé
              """
        l = []
        for pos in liste:
            piece = self.cases[Echiquier.coord.index(pos)]
            l.append(piece)
        return l

    def is_echec(self, color):
        """
        :param color: couleur dont on veut  verifier s#il est en echec
        :return: booleen True si le roi est en echec
        """
        pos = 0
        idx_echec = None
        for index, piece in enumerate(self.cases):
            if isinstance(piece, Roi) and piece.couleur == color:
                pos = Echiquier.coord[index]
                idx_echec = index
        if self.num(self.check_menace(color)).__contains__(pos):
            self.cases[Echiquier.coord.index(pos)].echec = True
            if color == 'blanc':
                self.is_echec_blanc = True
            else:
                self.is_echec_noir = True

            return True, idx_echec
        else:
            if color == 'blanc':
                self.is_echec_blanc = False
            else:
                self.is_echec_noir = False
            return False, None



    def check_menace(self, color):
        """
        :param color:
        :return: renvoi la  liste des positions menacées par l'adversaire de la coleur #color#
        """
        l = []
        lpion = []
        if color == "noir":
            for index, piece in enumerate(self.cases):
                if isinstance(piece, Piece) and not isinstance(piece, Pion):
                    if piece.couleur == "blanc":
                        l.extend(piece.simple_moves(self.get_dest_pos(Echiquier.coord[index]), self))
                elif isinstance(piece, Pion) and piece.couleur == "blanc":
                    if tab120[tab64[index] - 9] != -1:
                        lpion.extend([tab120[tab64[index] - 9]])
                    if tab120[tab64[index] - 11] != -1:
                        lpion.extend([tab120[tab64[index] - 11]])
        else:
            for index, piece in enumerate(self.cases):
                if isinstance(piece, Piece) and not isinstance(piece, Pion):
                    if piece.couleur == "noir":
                        l.extend(piece.simple_moves(self.get_dest_pos(Echiquier.coord[index]), self))
                elif isinstance(piece, Pion) and piece.couleur == "noir":
                    if tab120[tab64[index] + 9] != -1:
                        lpion.extend([tab120[tab64[index] + 9]])
                    if tab120[tab64[index] + 11] != -1:
                        lpion.extend([tab120[tab64[index] + 11]])

        return list(dict.fromkeys(l + lpion))

    def play_ai_move(self, ai_move):
        """
        :param ai_move: deplacement du AI
        :return: (si le AI a mangé, son ancienne position, nouvelle position)
        """
        if ai_move[0] is not None and ai_move[1] is not None:
            oldPos = Echiquier.coord.index(ai_move[0])
            newPos = Echiquier.coord.index(ai_move[1])
            hasTake = False
            if self.cases[newPos] is not None:
                hasTake = True
            is_echec_info = self.deplacer(self.cases[oldPos], ai_move[1])
            return hasTake, oldPos, newPos, is_echec_info
        else:
            return False, None, None

    def check_echec_matt(self):
        l = []
        for index, piece in enumerate(self.cases):
            if piece is not None and piece.couleur == self.current_player_color:
                l.extend(piece.moves(self.get_dest_pos(Echiquier.coord[index]), self))
        if not l and self.is_echec(self.current_player_color)[0]:
            return True
        else:
            return False

    def check_pat(self):
        l = []
        for index, piece in enumerate(self.cases):
            if piece is not None and piece.couleur == self.current_player_color:
                l.extend(piece.moves(self.get_dest_pos(Echiquier.coord[index]), self))
        if not l and not self.is_echec(self.current_player_color)[0]:
            return True
        else:
            return False

    def score_noir(self):
        return self.get_score_by_color("noir")

    def score_blanc(self):
        return self.get_score_by_color("blanc")

    def get_score_by_color(self, color):
        score = 0
        l = [piece for piece in self.cases if isinstance(piece, Piece) and piece.couleur == color]
        for piece in l:
            score = piece.evaluation + score

        return score

    def get_move(self):
        move = []
        pieces = [piece for piece in self.cases if
                  isinstance(piece, Piece) and piece.couleur == self.current_player_color]
        for piece in pieces:
            src = Echiquier.coord[self.cases.index(piece)]
            destList = self.num(piece.moves(self.cases.index(piece), self))
            for dest in destList:
                move.append((src, dest))
        return move
