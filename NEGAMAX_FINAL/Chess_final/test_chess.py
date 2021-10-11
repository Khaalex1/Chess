import unittest
from board import *
from random import choice


class TestChess(unittest.TestCase):

    def test_Pieces(self):
        """
        test l'instance des pieces
        :return:
        """
        E = Echiquier()
        pion = E.cases[Echiquier.coord.index("a7")]
        self.assertIsInstance(pion, Piece)

        cavalier = E.cases[Echiquier.coord.index("g1")]
        self.assertIsInstance(cavalier, Piece)

        fou = E.cases[Echiquier.coord.index("c1")]
        self.assertIsInstance(fou, Piece)

        reine = E.cases[Echiquier.coord.index("d8")]
        self.assertIsInstance(reine, Piece)

        roi = E.cases[Echiquier.coord.index("e1")]
        self.assertIsInstance(roi, Piece)

        tour = E.cases[Echiquier.coord.index("h1")]
        self.assertIsInstance(tour, Piece)

    def test_deplacement(self):
        """
        test l'effectivité du deplacement
        :return:
        """
        E = Echiquier()
        pion = E.cases[Echiquier.coord.index("a7")]
        E.deplacer(pion, "a5")
        self.assertEqual(Echiquier.coord[E.cases.index(pion)], "a5")  # effectivité du pion en 'a5'

        cavalier = E.cases[Echiquier.coord.index("g1")]
        E.deplacer(cavalier, "f3")
        self.assertEqual(Echiquier.coord[E.cases.index(cavalier)], "f3")  # effectivité du cavalier en 'f3'

        fou = E.cases[Echiquier.coord.index("c1")]
        E.deplacer(fou, "f4")
        self.assertEqual(Echiquier.coord[E.cases.index(fou)], "f4")  # effectivité du fou en 'f4'

        reine = E.cases[Echiquier.coord.index("d8")]
        E.deplacer(reine, "h4")
        self.assertEqual(Echiquier.coord[E.cases.index(reine)], "h4")  # effectivité de la reine en 'h4'

        roi = E.cases[Echiquier.coord.index("e1")]
        E.deplacer(roi, "f1")
        self.assertEqual(Echiquier.coord[E.cases.index(roi)], "f1")  # effectivité du roi en 'f1'

    def test_prise_en_passant(self):
        """
        test l'effectivité de la prise en passant
        :return:
        """
        E = Echiquier()
        pion = E.cases[Echiquier.coord.index("d2")]
        E.deplacer(pion, "d5")
        pion_test = E.cases[Echiquier.coord.index("c7")]
        E.deplacer(pion_test, "c5")
        E.deplacer(pion, "c6")
        self.assertIsNone(E.cases[Echiquier.coord.index("c5")])  # le pion_test est mangé

    def test_roque(self):
        """
        test l'effectivité du grand roque et du petit roque
        :return:
        """
        E = Echiquier()
        # ce rassurer qu'il n'y a aucune piece entre le roi et la tour
        E.cases[Echiquier.coord.index("b1")] = None
        E.cases[Echiquier.coord.index("c1")] = None
        E.cases[Echiquier.coord.index("d1")] = None
        E.cases[Echiquier.coord.index("f1")] = None
        E.cases[Echiquier.coord.index("g1")] = None
        # positionnement du roi et de la tour et test du roque
        roi = E.cases[Echiquier.coord.index("e1")]
        tour = E.cases[Echiquier.coord.index("a1")]
        E.deplacer(roi, "c1")
        self.assertEqual(Echiquier.coord[E.cases.index(tour)], "d1")
        E.back_last_move(roi.couleur)
        tour2 = E.cases[Echiquier.coord.index("h1")]
        E.deplacer(roi, "g1")
        self.assertEqual(Echiquier.coord[E.cases.index(tour2)], "f1")

    def test_back_move(self):
        """
         test l'annulation d'un mouvement incluant la prise en passant et les roques
        :return:
        """
        # annulation d'un mouvement quelconque
        E = Echiquier()
        pion = E.cases[Echiquier.coord.index("a7")]
        E.deplacer(pion, "a5")
        E.back_last_move(pion.couleur)
        self.assertEqual(Echiquier.coord[E.cases.index(pion)], "a7")
        # annulation de la prise en passant
        pion2 = E.cases[Echiquier.coord.index("b2")]
        E.deplacer(pion2, "b5")
        pion_test = E.cases[Echiquier.coord.index("c7")]
        E.deplacer(pion_test, "c5")
        E.deplacer(pion2, "c6")
        self.assertIsNone(E.cases[Echiquier.coord.index("c5")])
        E.back_last_move(pion2.couleur)
        self.assertEqual(Echiquier.coord[E.cases.index(pion2)], "b5")
        self.assertIsNotNone(E.cases[Echiquier.coord.index("c5")])
        # annulation du roque
        E.cases[Echiquier.coord.index("b1")] = None
        E.cases[Echiquier.coord.index("c1")] = None
        E.cases[Echiquier.coord.index("d1")] = None
        E.cases[Echiquier.coord.index("f1")] = None
        E.cases[Echiquier.coord.index("g1")] = None
        roi = E.cases[Echiquier.coord.index("e1")]
        tour = E.cases[Echiquier.coord.index("a1")]
        self.assertIsInstance(tour, Tour)  # verifier si la tour est a sa position
        E.deplacer(roi, "c1")
        self.assertIsNone(E.cases[Echiquier.coord.index("a1")])  # tour n'est plus a sa place
        E.back_last_move(roi.couleur)
        self.assertEqual(Echiquier.coord[E.cases.index(roi)], "e1")
        self.assertEqual(Echiquier.coord[E.cases.index(tour)], "a1")
        self.assertIsInstance(E.cases[Echiquier.coord.index("a1")], Tour)  # tour revenu a sa place

    def test_promotion_pion(self):
        """
        test la promotion d'un pion
        :return:
        """
        E = Echiquier()
        pion1 = E.cases[Echiquier.coord.index("a2")]  # pion de couleur blanc
        liste1 = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]
        choix1 = choice(liste1)
        E.deplacer(pion1, choix1)
        self.assertIsInstance(E.cases[Echiquier.coord.index(choix1)], Reine)  # le pion deplacé a la position 'choix'
        # est devenu reine
        self.assertEqual(E.cases[Echiquier.coord.index(choix1)].couleur, "blanc")  # reine blanche
        pion2 = E.cases[Echiquier.coord.index("a7")]  # pion de couleur noir
        liste2 = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
        choix2 = choice(liste2)
        E.deplacer(pion2, choix2)
        self.assertIsInstance(E.cases[Echiquier.coord.index(choix2)], Reine)  # pion deplacer a la position 'choix2'
        # est devenu reine
        self.assertEqual(E.cases[Echiquier.coord.index(choix2)].couleur, "noir")  # reine noire

    def test_si_deplacement_piece(self):
        """
        test si deplacement est fait
        :return:
        """
        E = Echiquier()
        roi = E.cases[Echiquier.coord.index("e1")]
        self.assertFalse(roi.has_do_first_move_r)
        E.deplacer(roi, "f1")
        self.assertTrue(roi.has_do_first_move_r)
        pion = E.cases[Echiquier.coord.index("a7")]
        E.deplacer(pion, "a5")
        self.assertTrue(pion.test_deplace_p)  # test si le pion c#est deplacer de deux cases (condition de la prise en
        # passant)
        tour = E.cases[Echiquier.coord.index("h1")]
        self.assertFalse(tour.has_do_first_move_t)
        E.deplacer(tour, "h3")
        self.assertTrue(tour.has_do_first_move_t)


if __name__ == '__main__':
    unittest.main()
