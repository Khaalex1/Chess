from dict import *
arbre_1 = OpenBookTree("book.txt")
arbre_2 = OpenBookTree("book.txt")
first_move = arbre_1.get_first_move()
print(first_move)
second_move = arbre_2.get_next_move(first_move)
print(second_move)
third_move = arbre_1.get_next_move(second_move)
print(third_move)
four_move = arbre_2.get_next_move(third_move)
print(four_move)
