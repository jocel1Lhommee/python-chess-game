class Piece:
    def __init__(self, type):
        self.type = type
        self.availableMove = []

    def getType(self):
        return self.type

    def isWhite(self):
        if self.type[0] == 'w':
            return True
        else:
            return False

    def clearAvailableMove(self):
        if self.availableMove != []:
            self.availableMove = []

    def getState(self):
        return [self.type, self.availableMove]

    def moveTo(self):
        pass

    def roque():
        pass

    def eatTo(self):
        pass

    def undoMove(self, pieceState):
        self.type = pieceState[0]
        self.availableMove = pieceState[1]

    def undoEat(self, pieceState):
        self.type = pieceState[0]
        self.availableMove = pieceState[1]

    def undoEnPassantMoved(self, pieceState):
        self.type = pieceState[0]
        self.availableMove = pieceState[1]

    def undoEnPassantAte(self, pieceState):
        self.type = pieceState[0]
        self.availableMove = pieceState[1]

    def undoRoque(self, pieceState):
        self.type = pieceState[0]
        self.availableMove = pieceState[1]


class Pawn(Piece):
    def __init__(self, type):
        super().__init__(type)
        # peut avancer de deux cases au prmier move
        self.firstMove = True

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        # blanc en bas et pièce blanche ou noir et pièce noir en bas
        if self.isWhite() == board.whiteBottom:
            if position[0] > 0:
                if board.arrayBoard[position[0]-1][position[1]] == None:
                    self.availableMove.append((position[0]-1, position[1]))
                    if position[0] > 1 and board.arrayBoard[position[0]-2][position[1]] == None and self.firstMove:
                        self.availableMove.append((position[0]-2, position[1]))
                if position[1] < 7:
                    if board.arrayBoard[position[0]-1][position[1]+1] != None:
                        if board.arrayBoard[position[0]-1][position[1]+1].isWhite() != self.isWhite():
                            self.availableMove.append(
                                (position[0]-1, position[1]+1))
                if position[1] > 0:
                    if board.arrayBoard[position[0]-1][position[1]-1] != None:
                        if board.arrayBoard[position[0]-1][position[1]-1].isWhite() != self.isWhite():
                            self.availableMove.append(
                                (position[0]-1, position[1]-1))
        else:
            if position[0] < 7:
                if board.arrayBoard[position[0]+1][position[1]] == None:
                    self.availableMove.append((position[0]+1, position[1]))
                    if position[0] < 6 and board.arrayBoard[position[0]+2][position[1]] == None and self.firstMove:
                        self.availableMove.append((position[0]+2, position[1]))
                if position[1] < 7:
                    if board.arrayBoard[position[0]+1][position[1]+1] != None:
                        if board.arrayBoard[position[0]+1][position[1]+1].isWhite() != self.isWhite():
                            self.availableMove.append(
                                (position[0]+1, position[1]+1))
                if position[1] > 0:
                    if board.arrayBoard[position[0]+1][position[1]-1] != None:
                        if board.arrayBoard[position[0]+1][position[1]-1].isWhite() != self.isWhite():
                            self.availableMove.append(
                                (position[0]+1, position[1]-1))

    def moveTo(self):
        super().moveTo()
        self.firstMove = False

    def undoMove(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def eatTo(self):
        super().moveTo()
        self.firstMove = False

    def undoEat(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def getState(self):
        return super().getState()+[self.firstMove]

    def enPassant(self):
        pass

    def undoEnPassantMoved(self, pieceState):
        super().undoEnPassantMoved(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def undoEnPassantAte(self, pieceState):
        super().undoEnPassantAte(pieceState[:-1])
        self.firstMove = pieceState[-1]


class Bishop(Piece):
    def __init__(self, type):
        super().__init__(type)

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        orientation = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
        for coord in orientation:
            row, col = position[0]+coord[0], position[1]+coord[1]
            found = False
            while((row not in (-1, 8)) and (col not in (-1, 8)) and not found):
                self.availableMove.append((row, col))
                if (board.arrayBoard[row][col] != None):
                    found = True
                    if (board.arrayBoard[row][col].isWhite() == self.isWhite()):
                        del self.availableMove[-1]
                row += coord[0]
                col += coord[1]


class Rock(Piece):
    def __init__(self, type):
        super().__init__(type)
        # peut roquer si au prmier move
        self.firstMove = True

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        orientation = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for coord in orientation:
            row, col = position[0]+coord[0], position[1]+coord[1]
            found = False
            while((row not in (-1, 8)) and (col not in (-1, 8)) and not found):
                self.availableMove.append((row, col))
                if (board.arrayBoard[row][col] != None):
                    found = True
                    if (board.arrayBoard[row][col].isWhite() == self.isWhite()):
                        del self.availableMove[-1]
                row += coord[0]
                col += coord[1]

    def getState(self):
        return super().getState()+[self.firstMove]

    def moveTo(self):
        super().moveTo()
        self.firstMove = False

    def undoRoque(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def undoMove(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def eatTo(self):
        super().moveTo()
        self.firstMove = False

    def undoEat(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def roque(self):
        super().moveTo()
        self.firstMove = False

    def getState(self):
        return super().getState()+[self.firstMove]


class Queen(Piece):
    def __init__(self, type):
        super().__init__(type)

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        orientation = [(1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, -1), (1, 1), (-1, 1), (-1, -1)]
        for coord in orientation:
            row, col = position[0]+coord[0], position[1]+coord[1]
            found = False
            while((row not in (-1, 8)) and (col not in (-1, 8)) and not found):
                self.availableMove.append((row, col))
                if (board.arrayBoard[row][col] != None):
                    found = True
                    if (board.arrayBoard[row][col].isWhite() == self.isWhite()):
                        del self.availableMove[-1]
                row += coord[0]
                col += coord[1]


class Knight(Piece):
    def __init__(self, type):
        super().__init__(type)

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        coordList = [(2, 1), (-2, 1), (2, -1), (-2, -1),
                     (1, 2), (-1, 2), (1, -2), (-1, -2)]
        for coord in coordList:
            row, col = position[0]+coord[0], position[1]+coord[1]
            if(row > -1 and row < 8 and col > -1 and col < 8):
                if(board.arrayBoard[row][col] == None or board.arrayBoard[row][col].isWhite() != self.isWhite()):
                    self.availableMove.append((row, col))


class King(Piece):
    def __init__(self, type):
        super().__init__(type)
        # peut roquer si au prmier move
        self.firstMove = True

    def getAvailableMove(self, position, board):
        self.clearAvailableMove()
        coordList = [(1, 1), (1, 0), (1, -1), (0, 1),
                     (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        for coord in coordList:
            row, col = position[0]+coord[0], position[1]+coord[1]
            if(row > -1 and row < 8 and col > -1 and col < 8):
                if(board.arrayBoard[row][col] == None or board.arrayBoard[row][col].isWhite() != self.isWhite()):
                    self.availableMove.append((row, col))

    def moveTo(self):
        super().moveTo()
        self.firstMove = False

    def undoMove(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def undoRoque(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def eatTo(self):
        super().moveTo()
        self.firstMove = False

    def roque(self):
        super().moveTo()
        self.firstMove = False

    def undoEat(self, pieceState):
        super().undoMove(pieceState[:-1])
        self.firstMove = pieceState[-1]

    def getState(self):
        return super().getState()+[self.firstMove]
