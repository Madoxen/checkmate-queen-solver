from chess import *

q = "C5"

k = "A7"

K = "A8"

b = Board()
b.place_piece("q", q)
b.place_piece("K", K)
b.place_piece("k", k)

print(b)

print(b.get_mating_moves(q, K))
