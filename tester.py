from chess import *


b = Board()

q = "C5"
k = "A7"
K = "A8"

b.place_piece("q", q)
b.place_piece("K", K)
b.place_piece("k", k)

print(b)
print(b.get_mating_moves(q, K))



