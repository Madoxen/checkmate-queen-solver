import math

PIECE_REPR = [None, "p", "n", "b", "r", "q", "k", "P", "N", "B", "R", "Q", "K"]




#create discrete ray
def ray() -> list:




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

    # place piece of given piece ID on x,y position
    # both x and y must be: > 0 and < 8
    def place_piece(self, piece_id: int, x: int, y: int) -> None:
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        if self.data[x][y] != 0:
            raise Exception('Piece already exists at this position')

        p = Piece(piece_id)
        self.data[x][y] = p

    def remove_piece(self, x: int, y: int):
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        self.data[x][y] = 0

    def get_pieces(self) -> list:
        l = []
        for i in range(self.W):
            for j in range(self.H):
                if self.data[i][j] is Piece:
                    l.append(self.data[i][j])
        return l

    # gets list of possible moves for piece on x,y position
    def get_moves(self, x: int, y: int) -> list:
        if x > 7 or x < 0 or y > 7 or y < 0:
            raise Exception('Piece position out of bounds')
        if self.data[x][y] == 0:
            return None
        
        

    def __str__(self) -> str:
        s = ""
        for i in range(self.H):            
                s += str(self.data[j][i])
        return s

    # move definitions
    def __move_queen(self, x: int, y: int) -> list:
        #queen moves diagonally, forward, backwards, left, right in rays 



            

            
    
    def __move_king(self, x: int, y: int) -> list:
        








b = Board()
b.place_piece(1, 1, 1)
b.remove_piece(1, 1)
b.place_piece(5, 1, 1)

print(b)

print(b.get_pieces())
