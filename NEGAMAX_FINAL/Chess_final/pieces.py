tab120 = (
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, 0, 1, 2, 3, 4, 5, 6, 7, -1,
    -1, 8, 9, 10, 11, 12, 13, 14, 15, -1,
    -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
    -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
    -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
    -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
    -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
    -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
)
tab64 = (
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
)

class Piece:
    """
This class allows manages the creation and movement of
pieces
    """

    def opponent_color(self):
        if self.couleur == "blanc":
            return "noir"
        else:
            return "blanc"

    def move(self, north, sud, west, east, pos, echequier):
        """
        :param north: deplacement vers le haut dans tab64(#ROBERT HYATT's method#)
        :param sud: deplacement vers le bas dans tab64(#ROBERT HYATT's method#)
        :param west: deplacement vers la gauche dans tab64(#ROBERT HYATT's method#)
        :param east: deplacement vers la droite dans tab64(#ROBERT HYATT's method#)
        :param pos: postion initiale
        :param echequier: objet de la class Echequier
        :return:  liste des positions possibles # notons que cette fonction est pour les pieces ayant un deplacement
        continue#
        """
        index_t64 = tab64[pos]
        list_N = []
        list_S = []
        list_E = []
        list_O = []

        index_t64 = index_t64 + north
        while tab120[index_t64] != -1:
            posi = tab120[index_t64]
            list_N.append(posi)
            index_t64 = index_t64 + north
            if echequier.cases[posi] is not None:  # ne pas sauter de pieces
                break

        index_t64 = tab64[pos]
        index_t64 = index_t64 + sud
        while tab120[index_t64] != -1:
            posi = tab120[index_t64]
            list_S.append(posi)
            index_t64 = index_t64 + sud
            if echequier.cases[posi] is not None:  # ne pas sauter de pieces
                break

        index_t64 = tab64[pos]
        index_t64 = index_t64 + west
        while tab120[index_t64] != -1:
            posi = tab120[index_t64]
            list_O.append(posi)
            index_t64 = index_t64 + west

            if echequier.cases[posi] is not None:  # ne pas sauter de pieces
                break

        index_t64 = tab64[pos]
        index_t64 = index_t64 + east
        while tab120[index_t64] != -1:
            posi = tab120[index_t64]
            list_E.append(posi)
            index_t64 = index_t64 + east

            if echequier.cases[posi] is not None:  # ne pas sauter de pieces
                break

        liste = list_N + list_S + list_E + list_O
        return self.filter_from_color_pieces(liste, echequier)

    def another_type_move(self, possible_move, echequier, pos):
        """
        :param possible_move: liste des positions  occupe dans le tab64(#ROBERT HYATT's method#)
        :param echequier: objet de la class Echequier
        :param pos: position initial
        :return: liste des positions possibles # notons que contraire a la fonction #move#  cette fonction est pour
        les pieces  ayant un deplacement non-continue#
        """
        liste = []
        index_t64 = tab64[pos]
        for i in possible_move:
            index = index_t64 + i
            liste.append(index)
        p_moves = [tab120[i] for i in liste if tab120[i] != -1]
        return self.filter_from_color_pieces(p_moves, echequier)

    def filter_from_color_pieces(self, liste, echequier):
        """
        :param liste: liste des positions de deplacement ne tenant pas compte des couleurs
        :param echequier:
        :return: liste des positions de deplacement tenant compte des couleurs
        """
        temp = []
        for i in liste:
            if echequier.cases[i] is not None:
                if echequier.cases[i].couleur == self.couleur:
                    temp.append(i)

        for i in temp:
            liste.remove(i)

        return liste

    def __init__(self, nom='vide', couleur=''):
        self.nom = nom
        self.couleur = couleur
        self.image = './images/{} {}.png'.format(nom, couleur)
        self.code = -1

    def simple_moves(self, pre_position, echequier):
        """
        :param pre_position:
        :param echequier:
        :return:
        """

    def moves(self, pre_position, echequier):
        """
                :param pre_position: position initiale dans l'echequier #entre 0 et 63#
                :param echequier: objet de la class Echequier:
                :return: None
                """

    def simulation_move(self, board, pre_position):
        temp = []
        piece = board.cases[pre_position]
        liste = piece.simple_moves(pre_position, board)
        for pos in liste:
            piece = board.cases[pre_position]
            board.deplacer(piece, board.coord[pos])
            if board.check_echec(piece.couleur):
                temp.append(pos)
            board.back_last_move(piece.couleur)
        for i in temp:
            liste.remove(i)
        return liste


class Pion(Piece):
    def __init__(self, couleur):
        super().__init__('pion', couleur)
        self.evaluation = 10
        self.test_deplace_p = False
        if couleur == "noir":
            self.code = 0
        else:
            self.code = 6

    def simple_moves(self, pre_position, echequier):
        """
        simple deplacement # il ne tient pas compte de l'echec au Roi
        :param pre_position:
        :param echequier:
        :return:
        """
        if self.couleur == "blanc":
            liste = [81, 82, 83, 84, 85, 86, 87, 88]  # postion initial des pions blanc(pouvant se deplacer) au debut
            l = []
            if liste.__contains__(tab64[pre_position]):  # si un pion est dans la liste #liste# il peut se deplacer de
                # deux ou une case
                for i in [-9, -11]:
                    index = tab64[pre_position] + i
                    index_2 = tab120[index]
                    # possibilite de manger en diagonale
                    if index_2 != -1 and echequier.cases[index_2] is not None:
                        if echequier.cases[index_2].couleur != self.couleur:
                            l.append(index_2)
                dep = [-10, -20]
                for i in dep:
                    index = tab64[pre_position] + i
                    if echequier.cases[tab120[index]] is not None:
                        break
                    l.append(tab120[index])
            else:
                posi = tab120[tab64[pre_position] - 10]
                if echequier.cases[posi] is None:  # ne pas sauter de pieces

                    l.append(posi)  # a defaut se deplacer d'une  case
                dep = [-9, -11]
                for i in dep:
                    index = tab64[pre_position] + i
                    index_2 = tab120[index]
                    # possibilite de manger en diagonale
                    if index_2 != -1 and echequier.cases[index_2] is not None:
                        if echequier.cases[index_2].couleur != self.couleur:
                            l.append(index_2)
        else:
            liste = [31, 32, 33, 34, 35, 36, 37, 38]  # postion initial des pions blanc(pouvant se deplacer) au debut
            l = []
            if liste.__contains__(tab64[pre_position]):  # si un pion est dans la liste #liste# il peut se deplacer de
                # deux ou une case
                for i in [9, 11]:
                    index = tab64[pre_position] + i
                    index_2 = tab120[index]
                    # possibilite de manger en diagonale
                    if index_2 != -1 and echequier.cases[index_2] is not None:
                        if echequier.cases[index_2].couleur != self.couleur:
                            l.append(index_2)
                dep = [10, 20]
                for i in dep:
                    index = tab64[pre_position] + i
                    if echequier.cases[tab120[index]] is not None:
                        break
                    l.append(tab120[index])
            else:
                posi = tab120[tab64[pre_position] + 10]
                if echequier.cases[posi] is None:  # ne pas sauter de pieces

                    l.append(posi)

                dep = [9, 11]
                for i in dep:
                    index = tab64[pre_position] + i
                    index_2 = tab120[index]
                    # possibilite de manger en diagonale
                    if index_2 != -1 and echequier.cases[index_2] is not None:
                        if echequier.cases[index_2].couleur != self.couleur:
                            l.append(index_2)
        if self.couleur == "blanc":
            if ["a5", "b5", "c5", "d5", "e5", "f5", "h5"].__contains__(echequier.coord[pre_position]):
                return l + self.prise_en_passant_g(echequier) + self.prise_en_passant_d(echequier)

        if self.couleur == "noir":
            if ["a4", "b4", "c4", "d4", "e4", "f4", "h4"].__contains__(echequier.coord[pre_position]):
                return l + self.prise_en_passant_g(echequier) + self.prise_en_passant_d(echequier)
        return l


    def moves(self, pre_position, echequier):
        """
                :param pre_position: position initiale dans l'echequier #entre 0 et 63#
                :param echequier: objet de la class Echequier:
                :return: liste des position  possibles #entre 0 et 63#
                """

        return self.simulation_move(echequier, pre_position)



    def prise_en_passant_g(self, echequier):
        """
        :param echequier: objet de la classe Echequier
        :return: liste des possibilite de la prise en passant case gauche, dependant de la couleur
        """
        l1 = []
        if self.couleur == "blanc":
            a4, b4, c4, d4, e4, f4, g4, h4 = echequier.cases[echequier.coord.index("a4")], \
                                             echequier.cases[echequier.coord.index("b4")], \
                                             echequier.cases[echequier.coord.index("c4")], \
                                             echequier.cases[echequier.coord.index("d4")], \
                                             echequier.cases[echequier.coord.index("e4")], \
                                             echequier.cases[echequier.coord.index("f4")], \
                                             echequier.cases[echequier.coord.index("g4")], \
                                             echequier.cases[echequier.coord.index("h4")]
            a5, b5, c5, d5, e5, f5, g5, h5 = echequier.cases[echequier.coord.index("a5")], \
                                             echequier.cases[echequier.coord.index("b5")], \
                                             echequier.cases[echequier.coord.index("c5")], \
                                             echequier.cases[echequier.coord.index("d5")], \
                                             echequier.cases[echequier.coord.index("e5")], \
                                             echequier.cases[echequier.coord.index("f5")], \
                                             echequier.cases[echequier.coord.index("g5")], \
                                             echequier.cases[echequier.coord.index("h5")]
            for pion in [a4, b4, c4, d4, e4, f4, g4, h4]:
                if isinstance(pion, Pion) and pion.couleur == "blanc":
                    pos = echequier.cases.index(pion)

                    i = -11
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos - 1], Pion) and echequier.cases[
                        pos - 1].test_deplace_p:
                        if echequier.cases[pos - 1].couleur == "noir":
                            echequier.cases[pos - 1].test_deplace_p = False

            for pion in [a5, b5, c5, d5, e5, f5, g5, h5]:
                if isinstance(pion, Pion) and pion.couleur == "blanc":
                    pos = echequier.cases.index(pion)

                    i = -11
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos - 1], Pion) and echequier.cases[
                        pos - 1].test_deplace_p:

                        if echequier.cases[pos - 1].couleur == "noir":
                            l1.append(index_2)
        else:
            a5, b5, c5, d5, e5, f5, g5, h5 = echequier.cases[echequier.coord.index("a5")], \
                                             echequier.cases[echequier.coord.index("b5")], \
                                             echequier.cases[echequier.coord.index("c5")], \
                                             echequier.cases[echequier.coord.index("d5")], \
                                             echequier.cases[echequier.coord.index("e5")], \
                                             echequier.cases[echequier.coord.index("f5")], \
                                             echequier.cases[echequier.coord.index("g5")], \
                                             echequier.cases[echequier.coord.index("h5")]
            a4, b4, c4, d4, e4, f4, g4, h4 = echequier.cases[echequier.coord.index("a4")], \
                                             echequier.cases[echequier.coord.index("b4")], \
                                             echequier.cases[echequier.coord.index("c4")], \
                                             echequier.cases[echequier.coord.index("d4")], \
                                             echequier.cases[echequier.coord.index("e4")], \
                                             echequier.cases[echequier.coord.index("f4")], \
                                             echequier.cases[echequier.coord.index("g4")], \
                                             echequier.cases[echequier.coord.index("h4")]
            for pion in [a5, b5, c5, d5, e5, f5, g5, h5]:
                if isinstance(pion, Pion) and pion.couleur == "noir":
                    pos = echequier.cases.index(pion)
                    i = 9
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos - 1], Pion) and echequier.cases[
                        pos - 1].test_deplace_p:
                        if echequier.cases[pos - 1].couleur == "blanc":
                            echequier.cases[pos - 1].test_deplace_p = False
            for pion in [a4, b4, c4, d4, e4, f4, g4, h4]:
                if isinstance(pion, Pion) and pion.couleur == "noir":
                    pos = echequier.cases.index(pion)

                    i = 9
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos - 1], Pion) and echequier.cases[
                        pos - 1].test_deplace_p:

                        if echequier.cases[pos - 1].couleur == "blanc":
                            l1.append(index_2)

        return l1

    def prise_en_passant_d(self, echequier):
        """
                :param echequier: objet de la classe Echequier
                :return: liste des possibilite de la prise en passant case droite, dependant de la couleur
                """
        l1 = []
        if self.couleur == "blanc":
            a4, b4, c4, d4, e4, f4, g4, h4 = echequier.cases[echequier.coord.index("a4")], \
                                             echequier.cases[echequier.coord.index("b4")], \
                                             echequier.cases[echequier.coord.index("c4")], \
                                             echequier.cases[echequier.coord.index("d4")], \
                                             echequier.cases[echequier.coord.index("e4")], \
                                             echequier.cases[echequier.coord.index("f4")], \
                                             echequier.cases[echequier.coord.index("g4")], \
                                             echequier.cases[echequier.coord.index("h4")]
            a5, b5, c5, d5, e5, f5, g5, h5 = echequier.cases[echequier.coord.index("a5")], \
                                             echequier.cases[echequier.coord.index("b5")], \
                                             echequier.cases[echequier.coord.index("c5")], \
                                             echequier.cases[echequier.coord.index("d5")], \
                                             echequier.cases[echequier.coord.index("e5")], \
                                             echequier.cases[echequier.coord.index("f5")], \
                                             echequier.cases[echequier.coord.index("g5")], \
                                             echequier.cases[echequier.coord.index("h5")]
            for pion in [a4, b4, c4, d4, e4, f4, g4, h4]:
                if isinstance(pion, Pion) and pion.couleur == "blanc":
                    pos = echequier.cases.index(pion)

                    i = -9
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos + 1], Pion) and echequier.cases[
                        pos + 1].test_deplace_p:
                        if echequier.cases[pos + 1].couleur == "noir":
                            echequier.cases[pos + 1].test_deplace_p = False

            for pion in [a5, b5, c5, d5, e5, f5, g5, h5]:
                if isinstance(pion, Pion) and pion.couleur == "blanc":
                    pos = echequier.cases.index(pion)

                    i = -9
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos + 1], Pion) and echequier.cases[
                        pos + 1].test_deplace_p:

                        if echequier.cases[pos + 1].couleur == "noir":
                            l1.append(index_2)
        else:
            a5, b5, c5, d5, e5, f5, g5, h5 = echequier.cases[echequier.coord.index("a5")], \
                                             echequier.cases[echequier.coord.index("b5")], \
                                             echequier.cases[echequier.coord.index("c5")], \
                                             echequier.cases[echequier.coord.index("d5")], \
                                             echequier.cases[echequier.coord.index("e5")], \
                                             echequier.cases[echequier.coord.index("f5")], \
                                             echequier.cases[echequier.coord.index("g5")], \
                                             echequier.cases[echequier.coord.index("h5")]
            a4, b4, c4, d4, e4, f4, g4, h4 = echequier.cases[echequier.coord.index("a4")], \
                                             echequier.cases[echequier.coord.index("b4")], \
                                             echequier.cases[echequier.coord.index("c4")], \
                                             echequier.cases[echequier.coord.index("d4")], \
                                             echequier.cases[echequier.coord.index("e4")], \
                                             echequier.cases[echequier.coord.index("f4")], \
                                             echequier.cases[echequier.coord.index("g4")], \
                                             echequier.cases[echequier.coord.index("h4")]
            for pion in [a5, b5, c5, d5, e5, f5, g5, h5]:
                if isinstance(pion, Pion) and pion.couleur == "noir":
                    pos = echequier.cases.index(pion)

                    i = 11
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos + 1], Pion) and echequier.cases[
                        pos + 1].test_deplace_p:

                        if echequier.cases[pos + 1].couleur == "blanc":
                            echequier.cases[pos + 1].test_deplace_p = False

            for pion in [a4, b4, c4, d4, e4, f4, g4, h4]:
                if isinstance(pion, Pion) and pion.couleur == "noir":
                    pos = echequier.cases.index(pion)

                    i = 11
                    index = tab64[pos] + i
                    index_2 = tab120[index]
                    if index_2 != -1 and isinstance(echequier.cases[pos + 1], Pion) and echequier.cases[
                        pos + 1].test_deplace_p:

                        if echequier.cases[pos + 1].couleur == "blanc":
                            l1.append(index_2)

        return l1

    def promotion(self, echequier, pos):
        """
        Promotion d'une piece de type Pion
        :param echequier: objet de classe Echequier
        :return: None
        """
        if self.couleur == "blanc":
            echequier.cases[echequier.coord.index(pos)] = Reine("blanc")

        else:
            echequier.cases[echequier.coord.index(pos)] = Reine("noir")

    def evaluer(self, piece):
        return piece.evaluation - self.evaluation


class Tour(Piece):

    def __init__(self, couleur):
        super().__init__('tour', couleur)
        self.evaluation = 60
        self.has_do_first_move_t = False
        if couleur == "noir":
            self.code = 3
        else:
            self.code = 9

    def simple_moves(self, pre_position, echequier):
        """
        simple deplacement # il ne tient pas compte de l'echec au Roi
        :param pre_position:
        :param echequier:
        :return:
        """
        return self.move(-10, 10, -1, 1, pre_position, echequier)

    def moves(self, pre_position, echequier):
        """
                :param pre_position: position initiale dans l'echequier #entre 0 et 63#
                :param echequier: objet de la class Echequier:
                :return: liste des position  possibles #entre 0 et 63#
                """

        return self.simulation_move(echequier, pre_position)

    def evaluer(self, piece):
        return piece.evaluation - self.evaluation


class Fou(Piece):
    def __init__(self, couleur):
        super().__init__('fou', couleur)
        self.evaluation = 30
        if couleur == "noir":
            self.code = 2
        else:
            self.code = 8

    def simple_moves(self, pre_position, echequier):
        """
               simple deplacement # il ne tient pas compte de l'echec au Roi
               :param pre_position:
               :param echequier:
               :return:
               """
        return self.move(- 9, 11, 9, -11, pre_position, echequier)

    def moves(self, pre_position, echequier):
        """
                :param pre_position: position initiale dans l'echequier #entre 0 et 63#
                :param echequier: objet de la class Echequier:
                :return: liste des position  possibles #entre 0 et 63#
                """

        return self.simulation_move(echequier, pre_position)

    def evaluer(self, piece):
        return piece.evaluation - self.evaluation


class Roi(Piece):
    def __init__(self, couleur):
        super().__init__('roi', couleur)
        self.echec = False
        self.has_do_first_move_r = False
        self.evaluation = 900
        if couleur == "noir":
            self.code = 5
        else:
            self.code = 11

    def simple_moves(self, pre_position, echequier):
        """
           simple deplacement # il ne tient pas compte de l'echec au Roi
           :param pre_position:
           :param echequier:
           :return:
           """
        p_moves = self.another_type_move([-10, 10, -9, 9, -1, 1, 11, -11], echequier, pre_position)
        return p_moves

    def moves(self, pre_position, echequier):
        """
        :param pre_position: position initiale dans l'echequier #entre 0 et 63#
        :param echequier: objet de la class Echequier:
        :return: liste des position  possibles #entre 0 et 63#
        """
        return self.simulation_move(echequier, pre_position) + self.grand_roque(echequier) + self.petit_roque(
            echequier)

    def grand_roque(self, echequier):
        l = []
        if self.couleur == "blanc":
            if not self.has_do_first_move_r:  # check si le roi a bougé
                possibilite = echequier.check_menace("blanc")  # liste de toutes les menaces de  l'adversaire

                if not (echequier.num(possibilite).__contains__("c1") or echequier.num(possibilite).__contains__("d1") or echequier.num(possibilite).__contains__("e1")):
                    # checker si la position du roi qu'il occupera est menacé
                    a1, e1, f1, g1 = echequier.cases[echequier.coord.index("a1")], echequier.cases[
                        echequier.coord.index("e1")] \
                        , echequier.cases[echequier.coord.index("f1")], echequier.cases[echequier.coord.index("g1")]
                    b1, c1, d1, h1 = echequier.cases[echequier.coord.index("b1")], echequier.cases[
                        echequier.coord.index("c1")], \
                                     echequier.cases[echequier.coord.index("d1")], echequier.cases[
                                         echequier.coord.index("h1")]
                    if isinstance(e1, Roi):
                        if e1.couleur == "blanc":
                            if b1 is None and c1 is None and d1 is None and isinstance(a1,
                                                                                       Tour) and a1.couleur == "blanc" and \
                                    not a1.has_do_first_move_t:
                                l.append(58)

        else:
            if not self.has_do_first_move_r:
                possibilite = echequier.check_menace("noir")
                if not (echequier.num(possibilite).__contains__("c8") or echequier.num(possibilite).__contains__("d8") or echequier.num(possibilite).__contains__("e8")):
                    a8, e8, f8, g8 = echequier.cases[echequier.coord.index("a8")], echequier.cases[
                        echequier.coord.index("e8")] \
                        , echequier.cases[echequier.coord.index("f8")], echequier.cases[echequier.coord.index("g8")],
                    b8, c8, d8, h8 = echequier.cases[echequier.coord.index("b8")], echequier.cases[
                        echequier.coord.index("c8")], \
                                     echequier.cases[echequier.coord.index("d8")], echequier.cases[
                                         echequier.coord.index("h8")]
                    if isinstance(e8, Roi):
                        if e8.couleur == "noir":
                            if b8 is None and c8 is None and d8 is None and isinstance(a8,
                                                                                       Tour) and a8.couleur == "noir" and not a8.has_do_first_move_t:
                                l.append(2)

        return l

    def petit_roque(self, echequier):
        """
        :param echequier: objet de la class Echequier
        :return: liste des positions
        """
        l = []
        if self.couleur == "blanc":  # check si le roi a bougé
            if not self.has_do_first_move_r:
                possibilite = echequier.check_menace("blanc")  # liste de toutes les menaces de  l'adversaire

                if not (echequier.num(possibilite).__contains__("f1") or echequier.num(possibilite).__contains__("g1") or echequier.num(possibilite).__contains__("e1")):
                    # checker si la position du roi qu'il occupera est menacé
                    a1, e1, f1, g1 = echequier.cases[echequier.coord.index("a1")], echequier.cases[
                        echequier.coord.index("e1")] \
                        , echequier.cases[echequier.coord.index("f1")], echequier.cases[echequier.coord.index("g1")]
                    b1, c1, d1, h1 = echequier.cases[echequier.coord.index("b1")], echequier.cases[
                        echequier.coord.index("c1")], \
                                     echequier.cases[echequier.coord.index("d1")], echequier.cases[
                                         echequier.coord.index("h1")]
                    if isinstance(e1, Roi):
                        if e1.couleur == "blanc":

                            if g1 is None and f1 is None and isinstance(h1,
                                                                        Tour) and h1.couleur == "blanc" and not h1.has_do_first_move_t:
                                l.append(62)
        else:
            if not self.has_do_first_move_r:
                possibilite = echequier.check_menace("noir")  # liste de toutes les menaces de  l'adversaire
                if not (echequier.num(possibilite).__contains__("f8") or echequier.num(possibilite).__contains__("g8") or echequier.num(possibilite).__contains__("e8")):
                    a8, e8, f8, g8 = echequier.cases[echequier.coord.index("a8")], echequier.cases[
                        echequier.coord.index("e8")] \
                        , echequier.cases[echequier.coord.index("f8")], echequier.cases[echequier.coord.index("g8")],
                    b8, c8, d8, h8 = echequier.cases[echequier.coord.index("b8")], echequier.cases[
                        echequier.coord.index("c8")], \
                                     echequier.cases[echequier.coord.index("d8")], echequier.cases[
                                         echequier.coord.index("h8")]
                    if isinstance(e8, Roi):
                        if e8.couleur == "noir":
                            if g8 is None and f8 is None and isinstance(h8,
                                                                        Tour) and h8.couleur == "noir" and not h8.has_do_first_move_t:
                                l.append(6)
        return l


class Reine(Piece):
    def __init__(self, couleur):
        super().__init__('reine', couleur)
        self.evaluation = 90
        if couleur == "noir":
            self.code = 4
        else:
            self.code = 10

    def simple_moves(self, pre_position, echequier):
        """
               simple deplacement # il ne tient pas compte de l'echec au Roi
               :param pre_position:
               :param echequier:
               :return:
               """
        p_moves_1 = self.move(- 9, 11, 9, -11, pre_position, echequier)
        p_moves_2 = self.move(-10, 10, -1, 1, pre_position, echequier)
        return p_moves_1 + p_moves_2

    def moves(self, pre_position, echequier):
        """
                :param pre_position: position initiale dans l'echequier #entre 0 et 63#
                :param echequier: objet de la class Echequier:
                :return: liste des position  possibles #entre 0 et 63#
                """
        return self.simulation_move(echequier, pre_position)

    def evaluer(self, piece):
        return piece.evaluation - self.evaluation


class Cavalier(Piece):

    def __init__(self, couleur):
        super().__init__('cavalier', couleur)
        self.evaluation = 30
        if couleur == "noir":
            self.code = 1
        else:
            self.code = 7

    def simple_moves(self, pre_position, echequier):
        """
               simple deplacement # il ne tient pas compte de l'echec au Roi
               :param pre_position:
               :param echequier:
               :return:
               """
        dep = [-12, 12, -21, 21, -19, 19, -8, 8]
        moves = self.another_type_move(dep, echequier, pre_position)
        return moves

    def moves(self, pre_position, echequier):
        """
        :param pre_position: position initiale dans l'echequier #entre 0 et 63#
        :param echequier: objet de la class Echequier:
        :return: liste des position  possibles #entre 0 et 63#
        """
        return self.simulation_move(echequier, pre_position)

    def evaluer(self, piece):
        return piece.evaluation - self.evaluation
