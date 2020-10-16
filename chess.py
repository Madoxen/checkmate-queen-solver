import math

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

    for i in range(limit):
        results.append((origin[0] + dirs[dir][0] * i,
                        origin[1] + dirs[dir][1] * i))
    return results


def normalize(vector: (float, float)) -> (float, float):
    # calc norm
    norm = math.sqrt(vector[0]**2 + vector[1]**2)
    return (vector[0] / norm, vector[1]/norm)
    # represents piece on chess board


class Piece:
    def __init__(self, piece_id: int):
        self.type = piece_id

    def __str__(self) -> str:
        return PIECE_REPR[self.type]


# represents chess board 8x8
class Board:
    W, H = 8, 8

    def __init__(self):
        self.data = [[0 for x in range(self.W)] for y in range(self.H)]
        self.move_methods = {
            "q":  self.__move_queen,
            "k": self.__move_king,
        }

    # place piece of given piece ID on x,y position
    # both x and y must be: > 0 and < 8
    # TODO: change position arugments to tuples

    def place_piece(self, piece_id: int, coords: (int, int)) -> None:
        x = coords[0]
        y = coords[1]
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        if self.data[x][y] != 0:
            raise Exception('Piece already exists at this position')

        p = Piece(piece_id)
        self.data[x][y] = p

    # TODO: change position arugments to tuples
    def remove_piece(self, coords: (int, int)):
        x = coords[0]
        y = coords[1]
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        self.data[x][y] = 0

    # TODO: change position arugments to tuples

    def get_pieces(self) -> list:
        l = []
        for i in range(self.W):
            for j in range(self.H):
                if self.data[i][j] is Piece:
                    l.append(self.data[i][j])
        return l

    # gets list of possible moves for piece on x,y position
    def get_moves(self, coords: (int, int)) -> list:
        x = coords[0]
        y = coords[1]
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        p = self.data[x][y]
        if p != 0:
            return self.move_methods[PIECE_REPR[p.type].lower()](coords)
        return None

    # move definitions

    def __move_queen(self, coords: (int, int)) -> list:
        # queen moves diagonally, forward, backwards, left, right in rays
        x = coords[0]
        y = coords[1]
        moves = []
        if self.data[x][y] == 0:
            raise Exception("There is no queen on given position")

        for i in range(8):
           moves.extend(self.__raycast_move(self.data[x][y], ray(coords, i, 9)))

    def __move_king(self, coords: (int, int)) -> list:
        return None

    # this method accepts RAY list (so only one avenue of move, not WHOLE array of every move) and then checks it against the board, to determine cutoff points
    def __raycast_move(self, piece: Piece, ray: list) -> list:
        result = []
        for i in range(len(ray)):
            x = ray[i][0]
            y = ray[i][1]
            if x > 7 or x < 0 or y > 7 or y < 0:
                result = ray[:i]
                break  # if out of bounds, cut now including current square
            if self.data[x][y] is str:
                if self.data[x][y].isupper() == PIECE_REPR[piece.type].isupper() or self.data[x][y].islower() == PIECE_REPR[piece.type].islower():
                    result = ray[:i]
                    break  # if encountered our piece, cut now including current square
                else:
                    # if encountered enemy, return everything including that enemy square
                    result = ray[:i+1]
                    break
        return result

    def __str__(self) -> str:
        s = ""
        for j in range(self.W):
            s += "\n"
            for i in range(self.H):
                s += str(self.data[j][i])
        return s


b = Board()
b.place_piece(1, (1, 1))
b.remove_piece((1, 1))
b.place_piece(5, (1, 1))
print(b.get_moves((1, 1)))

print(b)

print(b.get_pieces())
