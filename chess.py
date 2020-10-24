import math
from typing import List, Tuple
import copy

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

def chstocr(coord : str or List[str]) -> (int,int):
    if type(coord) is str:
        if len(coord) > 2:
            raise Exception("Chess coords are 2 chars long")
        return( ord(coord[0]) - 65 , int(coord[1]) - int('1'))
    elif type(coord) is list:
        l = []
        for c in coord:
            l.append(chstocr(c))
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

    def move_piece(self, _from:(int,int), _to:(int,int)):
        t = self.data[_from[0]][_from[1]].type
        if _to not in self.get_moves(_from):
            raise Exception('Invalid move for this piece')
        else:
            self.remove_piece(_from)
            self.place_piece(t,_to)


    #TODO: Gets pieces that are on board
    #Gets all pieces on board if king is set to ""
    #Gets all pieces of given king if set to k or K
    def get_pieces(self, king: str = "") -> list:
        if king != "k" and king != "K" and king != "":
            king = ""

        l = []
        d = {
            "K" : lambda x: x.isupper(),
            "k" : lambda x: x.islower(),
            "" : lambda x: True 
        }

        for i in range(self.W):
            for j in range(self.H):
                if type(self.data[i][j]) is Piece and d[king](self.data[i][j].type):
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
        
        #remove king from board
        king = self.data[x][y]
        self.remove_piece(coords)
        #produce all contested squares
        csqs = self.__produce_csqs(king.type)
        #place king on it's square back again
        self.place_piece(king.type, coords) 

        # king can move 1 square in every direction, but cannot move on fields that will result in check
        for d in dirs.values():
            nc = (d[0] + x, d[1] + y) #new coords
            if nc not in csqs: 
                if nc[0] > self.W-1 or nc[0] < 0 or nc[1] > self.H-1 or nc[1] < 0: #bound check
                    continue
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
    def __produce_csqs(self, king: str) -> bool:
        # get all pieces
        pieces = self.get_pieces(king.swapcase()) #we want to get all possible moves, of the opposite side
        csqs = []
        for p in pieces:
            # get all contested squares
            if(p.type.lower() == "k"):
                for d in dirs.values():
                    x = d[0] + p.coords[0]
                    y = d[1] + p.coords[1]
                    csqs.append((x, y))
            else:
                csqs.extend(self.get_moves(p.coords))
        return csqs

    def check_check(self, coords: (int,int), king:str):
        csqs = self.__produce_csqs(king)
        for csq in csqs:
            if coords == csq:  # if chosen coord is contested
                return True
        return False

    def check_mate(self, coords: (int, int), king: str) -> bool:
        print(coords,king)
        if not self.get_moves(coords) and b.check_check(coords, king):
            return True
        return False

    def __str__(self) -> str:
        s = ""
        for j in range(self.H-1, -1, -1):
            s += "\n"
            s += str(j+1) + "|"
            for i in range(self.W):
                s += str( self.data[i][j] ) + " "

        s += "\n  - - - - - - - -\n  "
        for i in range(self.W):
            s += str(chr(i + 65)) + " "
        return s


    def get_mating_moves(self, coords: (int, int), king_coords: (int,int)):
        moves = self.get_moves(coords)
        print("moves: ",moves)
        king=self.data[king_coords[0]][king_coords[1]].type
        if king is not "k" and king is not "K":
            raise Exception('provided king is not a king')

        mating = []
        for move in moves:
            sub = copy.deepcopy(self)
            sub.move_piece(coords,move)
            print(sub, sub.check_mate(king_coords,king), move, king_coords, king)
            if sub.check_mate(king_coords,king):
                mating.add(move)

        return mating

b = Board()
b.place_piece("q", (4, 3))
b.place_piece("K", (6, 7))
b.place_piece("k", (7, 5))




print(crtochs(b.get_mating_moves((4,3),(6,7))))



#print(b)

#print(b.check_mate((6, 7), "K"))
