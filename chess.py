import math
from typing import List, Tuple


# TODO: simplify ID system
# white -> lower case ; black -> upper case
PIECE_REPR = [None, "p", "n", "b", "r", "q", "k", "P", "N", "B", "R", "Q", "K"]

dirs = {
    0: (1, 0),  # N
    1: (1, 1),  # NE
    2: (0, 1),  # E
    3: (-1, 1),  # SE
    4: (-1, 0),  # S
    5: (-1, -1),  # SW
    6: (0, -1),  # W
    7: (1, -1),  # NW
}

# dir 1 N, 2 NE, 3 E and so on
# discerete ray function (8 directional)


def ray(origin: (int, int), dir: int, limit: int) -> list:
    results = []  # list of intersected squares, tuples

    for i in range(1, limit):
        results.append((origin[0] + dirs[dir][0] * i,
                        origin[1] + dirs[dir][1] * i))
    return results


def crtochs(coords: (int, int) or List[Tuple[int, int]]) -> str or List[str]:
    if type(coords) is tuple:
        return chr(65 + coords[0]) + str(coords[1]+1)
    elif type(coords) is list:
        l = []
        for i in range(len(coords)):
            l.append(crtochs(coords[i]))
        return l


class Piece:
    def __init__(self, piece_id: str, coords: (int, int)):
        self.type = piece_id
        self.coords = coords

    def __str__(self) -> str:
        return self.type


# represents chess board 8x8
class Board:
    W, H = 8, 8

    def __init__(self):
        self.data = [[0 for x in range(self.W)] for y in range(self.H)]
        self.move_methods = {  # move method bindings for given pieces
            "q":  self.__moves_queen,
            "k": self.__moves_king,
        }

    # place piece of given piece ID on x,y position
    # both x and y must be: > 0 and < 8
    def place_piece(self, piece_id: str, coords: (int, int)) -> None:
        x = coords[0]
        y = coords[1]
        if x > self.W-1 or x < 0 or y > self.H-1 or y < 0:
            raise Exception('Piece position out of bounds')
        if self.data[x][y] != 0:
            raise Exception('Piece already exists at this position')

        p = Piece(piece_id, (x, y))
        self.data[x][y] = p

    def remove_piece(self, coords: (int, int)):
        x = coords[0]
        y = coords[1]
        if x > self.W-1 or x < 0 or y > self.H-1 or y < 0:
            raise Exception('Piece position out of bounds')
        self.data[x][y].coords = (-1, -1)
        self.data[x][y] = 0

    def get_pieces(self) -> list:
        l = []
        for i in range(self.W):
            for j in range(self.H):
                if type(self.data[i][j]) is Piece:
                    l.append(self.data[i][j])
        return l

    # gets list of possible moves for piece on x,y position
    def get_moves(self, coords: (int, int)) -> list:
        x = coords[0]
        y = coords[1]
        if x > self.W-1 or x < 0 or y > self.H-1 or y < 0:
            raise Exception('Piece position out of bounds')
        p = self.data[x][y]
        if p != 0:
            return self.move_methods[p.type.lower()](coords)
        return None

    # move definitions
    def __moves_queen(self, coords: (int, int)) -> list:
        # queen moves diagonally, forward, backwards, left, right in rays
        x = coords[0]
        y = coords[1]
        moves = []
        if self.data[x][y] == 0:
            raise Exception("There is no queen on given position")

        for i in range(8):
            moves.extend(self.__raycast_move(
                self.data[x][y], ray(coords, i, 9)))
        return moves

    def __moves_king(self, coords: (int, int)) -> list:
        moves = []
        x = coords[0]
        y = coords[1]
        # king can move 1 square in every direction, but cannot move on fields that will result in check
        for d in dirs.values():
            nc = (d[0] + x, d[1] + y)
            if self.check_check(nc, self.data[x][y].type) == False:
                moves.append(nc)
        return moves

    # this method accepts RAY list (so only one avenue of move, not WHOLE array of every move) and then checks it against the board, to determine cutoff points

    def __raycast_move(self, piece: Piece, ray: list) -> list:
        result = []
        for i in range(len(ray)):
            x = ray[i][0]
            y = ray[i][1]
            if x > self.W-1 or x < 0 or y > self.H-1 or y < 0:
                result = ray[:i]
                break  # if out of bounds, cut now including current square
            if type(self.data[x][y]) is Piece:
                # we check colour by checking case of piece
                if self.data[x][y].type.isupper() == piece.type.isupper() or self.data[x][y].type.islower() == piece.type.islower():
                    result = ray[:i]
                    break  # if encountered our piece, cut now including current square
                else:
                    # if encountered enemy, return everything including that enemy square
                    result = ray[:i+1]
                    break
        return result

    # checks if check can occur with current game state on given position
    def check_check(self, coords: (int, int), king: str) -> bool:
        # get all pieces
        pieces = self.get_pieces()
        for p in pieces:
            if p.type == king: #we need to eliminate checked King from piece pool to avoid infinite recursive loop
                pieces.remove(p)
                continue

            csqs = []
            # get all contested squares
            if(p.type.lower() == "k"):
                for d in dirs.values():
                    csqs.append((d[0] + p.coords[0], d[1] + p.coords[1]))
            else:
                csqs = self.get_moves(p.coords)


            for csq in csqs:
                if coords == csq:  # if chosen coord is contested
                    return True
        return False

    def __str__(self) -> str:
        s = ""
        for j in range(self.H-1, -1, -1):
            s += "\n"
            s += str(j+1) + "|"
            for i in range(self.W):
                s += str(self.data[i][j])

        s += "\n  --------\n  "
        for i in range(self.W):
            s += chr(i + 65)
        return s


b = Board()
b.place_piece("q", (1, 1))
b.remove_piece((1, 1))
b.place_piece("q", (1, 1))
b.place_piece("K", (3, 3))
b.place_piece("k", (1, 3))

print(crtochs(b.get_moves((1, 1))))
print(crtochs(b.get_moves((3, 3))))
print(b)
print(b.get_pieces())
print(b.check_check((3, 3), "K"))
