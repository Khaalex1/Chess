from random import choice
from textwrap import wrap


class OpenBookTree(object):
    "Generic tree node."

    class Node:
        def __init__(self, data):
            self.data = data
            self.children = []

        def add_child(self, data):
            # assert isinstance(node, Tree)
            for i in range(len(self.children)):
                if self.children[i].data == data:
                    return self.children[i]
            node = OpenBookTree.Node(data)
            self.children.append(node)
            return node

    def __init__(self, filename):

        self.root = self.create_tree(filename)
        self.pointer = self.root
        self.current_depth = 0

    def create_tree(self, nom_fichier):
        root = OpenBookTree.Node('root')

        with open(nom_fichier, "r") as file:
            lignes = file.readlines()
            for ligne in lignes:
                split = ligne.split()
                node = root
                for data in split:
                    node = node.add_child(data)
        return root

    def get_first_move(self):
        self.pointer = choice(self.pointer.children)
        return tuple(wrap(self.pointer.data, 2))

    def get_next_move_AI_AI(self):
        if self.pointer.children:
            self.pointer = choice(self.pointer.children)
            return tuple(wrap(self.pointer.data, 2))
        else:
            return None

    def get_next_move_single_AI(self, color, move_oppenent):
        if color == "blanc":
            if self.pointer.data == "root":
                self.pointer = choice(self.pointer.children)
                return tuple(wrap(self.pointer.data, 2))

            if self.pointer.children:
                for node in self.pointer.children:
                    if node.data == move_oppenent and node.children:
                        self.pointer = choice(node.children)
                        return tuple(wrap(self.pointer.data, 2))
        else:
            if self.pointer.data == "root":
                for node in self.pointer.children:
                    if node.data == move_oppenent and node.children:
                        self.pointer = choice(node.children)
                        return tuple(wrap(self.pointer.data, 2))
            elif self.pointer.children:
                for node in self.pointer.children:
                    if node.data == move_oppenent and node.children:
                        self.pointer = choice(node.children)
                        return tuple(wrap(self.pointer.data, 2))
        return None





        # if node.data == move and node.children:
        #
        # if self.pointer.children:
        #     shuffle(self.pointer.children)
        #     for node in self.pointer.children:
        #         if node.children:
        #             self.pointer = node
        #             return tuple(wrap(self.pointer.data, 2))
        # return None

        # for node in self.pointer.children:
        #     if node.data == move and node.children:
        #         self.pointer = choice(node.children)
        #         return wrap(self.pointer.data, 2)
        # return None

