from .constants import COLS
from .piece import Rock, Knight, Bishop, Queen, King, Pawn


class Board():
    def __init__(self, whiteBottom):
        """_summary_

        Args:
            bool (_type_): _description_
        """
        self.selectedPosition = None
        self.moveLog = []
        self.whiteBottom = whiteBottom
        self.createBoard()

    def createBoard(self):
        wP_line = []
        bP_line = []
        clean_line = [None]*COLS
        for i in range(COLS):
            wP_line.append(Pawn("wP"))
            bP_line.append(Pawn("bP"))
        if self.whiteBottom:
            B_line = [Rock("bR"),
                      Knight("bN"),
                      Bishop("bB"),
                      Queen("bQ"),
                      King("bK"),
                      Bishop("bB"),
                      Knight("bN"),
                      Rock("bR")]
            W_line = [Rock("wR"),
                      Knight("wN"),
                      Bishop("wB"),
                      King("wK"),
                      Queen("wQ"),
                      Bishop("wB"),
                      Knight("wN"),
                      Rock("wR")]
            for i in range(COLS):
                wP_line.append(Pawn("wP"))
                bP_line.append(Pawn("bP"))
            self.arrayBoard = [
                B_line,
                bP_line,
                clean_line*1,
                clean_line*1,
                clean_line*1,
                clean_line*1,
                wP_line,
                W_line,
            ]
        else:
            B_line = [Rock("bR"),
                      Knight("bN"),
                      Bishop("bB"),
                      King("bK"),
                      Queen("bQ"),
                      Bishop("bB"),
                      Knight("bN"),
                      Rock("bR")]
            W_line = [Rock("wR"),
                      Knight("wN"),
                      Bishop("wB"),
                      Queen("wQ"),
                      King("wK"),
                      Bishop("wB"),
                      Knight("wN"),
                      Rock("wR")]
            self.arrayBoard = [
                W_line,
                wP_line,
                clean_line*1,
                clean_line*1,
                clean_line*1,
                clean_line*1,
                bP_line,
                B_line,
            ]
        # self.init_available_moves()

    def getAvailableMove(self, position, filterCheck=True):
        self.arrayBoard[position[0]][position[1]
                                     ].getAvailableMove(position, self)
        # prise en passant:
        if isinstance(self.arrayBoard[position[0]][position[1]], Pawn):
            # blanc en bas et pièce blanche ou noir et pièce noir en bas
            if self.arrayBoard[position[0]][position[1]].isWhite() == self.whiteBottom:
                if position[0] == 3:
                    # si pas sur dernière colonne => vérification à droite
                    if position[1] < 7:
                        if isinstance(self.arrayBoard[position[0]][position[1]+1], Pawn):
                            # Dernier move est un pion et à la bonne place
                            if self.moveLog[-1][1][0][1] == "P" and self.moveLog[-1][3] == (position[0], position[1]+1):
                                # était le premier move
                                if self.moveLog[-1][1][2] == True:
                                    self.arrayBoard[position[0]][position[1]].availableMove.append(
                                        (position[0]-1, position[1]+1))
                    # si pas sur première colonne => vérification à gauche
                    if position[1] > 0:
                        if isinstance(self.arrayBoard[position[0]][position[1]-1], Pawn):
                            # Dernier move est un pion
                            if self.moveLog[-1][1][0][1] == "P" and self.moveLog[-1][3] == (position[0], position[1]-1):
                                # était le premier move
                                if self.moveLog[-1][1][2] == True:
                                    self.arrayBoard[position[0]][position[1]].availableMove.append(
                                        (position[0]-1, position[1]-1))
            else:
                if position[0] == 4:
                    # si pas sur dernière colonne => vérification à droite
                    if position[1] < 7:
                        if isinstance(self.arrayBoard[position[0]][position[1]+1], Pawn):
                            # Dernier move est un pion et à la bonne place
                            if self.moveLog[-1][1][0][1] == "P" and self.moveLog[-1][3] == (position[0], position[1]+1):
                                # était le premier move
                                if self.moveLog[-1][1][2] == True:
                                    self.arrayBoard[position[0]][position[1]].availableMove.append(
                                        (position[0]+1, position[1]+1))
                    # si pas sur première colonne => vérification à gauche
                    if position[1] > 0:
                        if isinstance(self.arrayBoard[position[0]][position[1]-1], Pawn):
                            # Dernier move est un pion
                            if self.moveLog[-1][1][0][1] == "P" and self.moveLog[-1][3] == (position[0], position[1]-1):
                                # était le premier move
                                if self.moveLog[-1][1][2] == True:
                                    self.arrayBoard[position[0]][position[1]].availableMove.append(
                                        (position[0]+1, position[1]-1))
        # roque
        # si roi qui n'a jamais bougé
        if isinstance(self.arrayBoard[position[0]][position[1]], King) and self.arrayBoard[position[0]][position[1]].firstMove == True:
            availableMoveLoop = False
            leftRockPossible, rightRockPossible = True, True
            kingColorIsWhite = self.arrayBoard[position[0]][position[1]].isWhite(
            )
            # si même ligne tout à Droite est une tour et first move aussi
            if isinstance(self.arrayBoard[position[0]][7], Rock) and self.arrayBoard[position[0]][7].firstMove == True:
                # si pas de pièces entre King et tout à Droite
                found = False
                for i in range(position[1]+1, 7):
                    if not found and self.arrayBoard[position[0]][i] != None:
                        found = True
                if not found:
                    availableMoveLoop = True
                    # on vérifie qu'aucune pièce de couleure opposée ne pointe vers entre King et tout à Droite(extrémité comprises)
                    for row in range(8):
                        for col in range(8):
                            if self.arrayBoard[row][col] != None and self.arrayBoard[row][col].isWhite() != kingColorIsWhite:
                                self.getAvailableMove((row, col), False)
                                for move in self.arrayBoard[row][col].availableMove:
                                    if move[0] == position[0]:
                                        if col >= position[1]:
                                            rightRockPossible = False
                                        if col <= position[1]:
                                            leftRockPossible = False
                else:
                    rightRockPossible = False
            else:
                rightRockPossible = False
            # ou si même ligne tout à Gauche est une tour et first move aussi
            if isinstance(self.arrayBoard[position[0]][0], Rock) and self.arrayBoard[position[0]][0].firstMove == True and leftRockPossible:
                # si pas de pièces entre King et tout à Droite:
                found = False
                for i in range(1, position[1]):
                    if not found and self.arrayBoard[position[0]][i] != None:
                        found = True
                if not found:
                    if not availableMoveLoop:
                        for row in range(8):
                            for col in range(8):
                                if self.arrayBoard[row][col] != None and self.arrayBoard[row][col].isWhite() != kingColorIsWhite:
                                    self.getAvailableMove((row, col), False)
                                    for move in self.arrayBoard[row][col].availableMove:
                                        if move[0] == position[0]:
                                            if col <= position[1]:
                                                leftRockPossible = False
                else:
                    leftRockPossible = False
            else:
                leftRockPossible = False

            if leftRockPossible:
                self.arrayBoard[position[0]][position[1]].availableMove.append(
                    (position[0], 0))
            if rightRockPossible:
                self.arrayBoard[position[0]][position[1]].availableMove.append(
                    (position[0], 7))

        if filterCheck:
            self.filterCheck(position)

    def filterCheck(self, position):
        pieceColor = self.arrayBoard[position[0]][position[1]].isWhite()
        toDel = []
        # pour chaque move
        for move in self.arrayBoard[position[0]][position[1]].availableMove:
            if self.arrayBoard[move[0]][move[1]] == None:
                self.moveTo(position, move)
            else:
                self.eatTo(position, move)
            # vérifier si les pièce de la couleur opposés mettent en échec
            for row in range(8):
                for col in range(8):
                    if self.arrayBoard[row][col] != None and self.arrayBoard[row][col].isWhite() != pieceColor:
                        self.getAvailableMove((row, col), filterCheck=False)
                        for move2 in self.arrayBoard[row][col].availableMove:
                            if self.arrayBoard[move2[0]][move2[1]] != None and isinstance(self.arrayBoard[move2[0]][move2[1]], King) and self.arrayBoard[move2[0]][move2[1]].isWhite() == pieceColor:
                                toDel.append(move)
            self.undoLog()
        newAvailableMove = []
        for move in self.arrayBoard[position[0]][position[1]].availableMove:
            if move not in toDel:
                newAvailableMove.append(move)
        self.arrayBoard[position[0]][position[1]
                                     ].availableMove = newAvailableMove

    def moveTo(self, pastPosition, futurePosition):
        self.moveLog.append(
            ("move", self.arrayBoard[pastPosition[0]][pastPosition[1]].getState(), pastPosition, futurePosition))
        self.arrayBoard[futurePosition[0]][futurePosition[1]
                                           ] = self.arrayBoard[pastPosition[0]][pastPosition[1]]
        self.arrayBoard[pastPosition[0]][pastPosition[1]] = None
        # modification particulière de certaines pièces
        self.arrayBoard[futurePosition[0]][futurePosition[1]].moveTo()
        if self.arrayBoard[futurePosition[0]][futurePosition[1]].isWhite() == self.whiteBottom:
            if futurePosition[0] == 0 and isinstance(self.arrayBoard[futurePosition[0]][futurePosition[1]], Pawn):
                return "Promotion"
        else:
            if futurePosition[0] == 7 and isinstance(self.arrayBoard[futurePosition[0]][futurePosition[1]], Pawn):
                return "Promotion"

    def eatTo(self, pastPosition, toEatPosition):
        self.moveLog.append(
            ("eat", self.arrayBoard[pastPosition[0]][pastPosition[1]].getState(), self.arrayBoard[toEatPosition[0]][toEatPosition[1]].getState(), pastPosition, toEatPosition))
        self.arrayBoard[toEatPosition[0]][toEatPosition[1]
                                          ] = self.arrayBoard[pastPosition[0]][pastPosition[1]]
        self.arrayBoard[pastPosition[0]][pastPosition[1]] = None
        # modification particulière de certaines pièces
        self.arrayBoard[toEatPosition[0]][toEatPosition[1]].eatTo()
        # blanc en bas et pièce blanche ou noir et pièce noir en bas
        if self.arrayBoard[toEatPosition[0]][toEatPosition[1]].isWhite() == self.whiteBottom:
            if toEatPosition[0] == 0 and isinstance(self.arrayBoard[toEatPosition[0]][toEatPosition[1]], Pawn):
                return "Promotion"
        else:
            if toEatPosition[0] == 7 and isinstance(self.arrayBoard[toEatPosition[0]][toEatPosition[1]], Pawn):
                return "Promotion"

    def enPassant(self, pastPosition, toEatPosition, futurePosition):
        self.moveLog.append(
            ("enPassant", self.arrayBoard[pastPosition[0]][pastPosition[1]].getState(), self.arrayBoard[toEatPosition[0]][toEatPosition[1]].getState(), pastPosition, toEatPosition, futurePosition))
        self.arrayBoard[futurePosition[0]][futurePosition[1]
                                           ] = self.arrayBoard[pastPosition[0]][pastPosition[1]]
        self.arrayBoard[pastPosition[0]][pastPosition[1]] = None
        self.arrayBoard[toEatPosition[0]][toEatPosition[1]] = None
        self.arrayBoard[futurePosition[0]][futurePosition[1]].enPassant()

    def roque(self, rockPosition):
        kingPosition = self.selectedPosition[0], self.selectedPosition[1]
        # si roque vers la droite
        if kingPosition[1] < rockPosition[1]:
            self.moveLog.append(("roque", kingPosition, (kingPosition[0], kingPosition[1] + 2), self.arrayBoard[kingPosition[0]][kingPosition[1]].getState(
            ), rockPosition, (kingPosition[0], kingPosition[1] + 1), self.arrayBoard[rockPosition[0]][rockPosition[1]].getState()))
            self.arrayBoard[kingPosition[0]][kingPosition[1] +
                                             2] = self.arrayBoard[kingPosition[0]][kingPosition[1]]
            self.arrayBoard[kingPosition[0]][kingPosition[1] +
                                             1] = self.arrayBoard[rockPosition[0]][rockPosition[1]]
            self.arrayBoard[kingPosition[0]][kingPosition[1]] = None
            self.arrayBoard[rockPosition[0]][rockPosition[1]] = None
            self.arrayBoard[kingPosition[0]][kingPosition[1] +
                                             2].roque()
            self.arrayBoard[kingPosition[0]][kingPosition[1] +
                                             1].roque()
        # roque gauche
        else:
            self.moveLog.append(("roque", kingPosition, (kingPosition[0], kingPosition[1] - 2), self.arrayBoard[kingPosition[0]][kingPosition[1]].getState(
            ), rockPosition, (kingPosition[0], kingPosition[1] - 1), self.arrayBoard[rockPosition[0]][rockPosition[1]].getState()))
            self.arrayBoard[kingPosition[0]][kingPosition[1] -
                                             2] = self.arrayBoard[kingPosition[0]][kingPosition[1]]
            self.arrayBoard[kingPosition[0]][kingPosition[1] -
                                             1] = self.arrayBoard[rockPosition[0]][rockPosition[1]]
            self.arrayBoard[kingPosition[0]][kingPosition[1]] = None
            self.arrayBoard[rockPosition[0]][rockPosition[1]] = None
            self.arrayBoard[kingPosition[0]][kingPosition[1] -
                                             2].roque()
            self.arrayBoard[kingPosition[0]][kingPosition[1] -
                                             1].roque()

    def undoRoque(self, kingPastPosition, kingFuturePosition, kingState, rockPastPosition, rockFuturePosition, rockState):
        self.arrayBoard[kingPastPosition[0]][kingPastPosition[1]
                                             ] = self.arrayBoard[kingFuturePosition[0]][kingFuturePosition[1]]
        self.arrayBoard[kingFuturePosition[0]][kingFuturePosition[1]] = None
        self.arrayBoard[kingPastPosition[0]
                        ][kingPastPosition[1]].undoRoque(kingState)
        self.arrayBoard[rockPastPosition[0]][rockPastPosition[1]
                                             ] = self.arrayBoard[rockFuturePosition[0]][rockFuturePosition[1]]
        self.arrayBoard[rockFuturePosition[0]][rockFuturePosition[1]] = None
        self.arrayBoard[rockPastPosition[0]
                        ][rockPastPosition[1]].undoRoque(rockState)

    def undoLog(self):
        move = self.moveLog[-1]
        del self.moveLog[-1]
        if move[0] == "move":
            self.undoMove(move[1], move[2], move[3])
        if move[0] == "eat":
            self.undoEat(move[1], move[2], move[3], move[4])
        if move[0] == "enPassant":
            self.undoEnPassant(move[1], move[2], move[3], move[4], move[5])
        if move[0] == "roque":
            self.undoRoque(move[1], move[2], move[3],
                           move[4], move[5], move[6])

    def undoMove(self, pieceState, futurePosition, pastPosition):
        self.arrayBoard[futurePosition[0]][futurePosition[1]
                                           ] = self.arrayBoard[pastPosition[0]][pastPosition[1]]
        self.arrayBoard[pastPosition[0]][pastPosition[1]] = None
        # remise en place de l'état de la pièce
        self.arrayBoard[futurePosition[0]
                        ][futurePosition[1]].undoMove(pieceState)

    def undoEat(self, pieceState, pieceAteState, futurePosition, pastPosition):
        self.arrayBoard[futurePosition[0]][futurePosition[1]
                                           ] = self.arrayBoard[pastPosition[0]][pastPosition[1]]
        self.arrayBoard[pastPosition[0]][pastPosition[1]
                                         ] = createPieceByType(pieceAteState[0])
        # remise en place des états de pièces
        self.arrayBoard[futurePosition[0]
                        ][futurePosition[1]].undoEat(pieceState)
        self.arrayBoard[pastPosition[0]
                        ][pastPosition[1]].undoEat(pieceAteState)

    def undoEnPassant(self, pieceState, pieceAteState, pastPosition, pastAtePosition, futurePosition):
        self.arrayBoard[pastPosition[0]][pastPosition[1]
                                         ] = self.arrayBoard[futurePosition[0]][futurePosition[1]]
        self.arrayBoard[pastAtePosition[0]][pastAtePosition[1]
                                            ] = createPieceByType(pieceAteState[0])
        self.arrayBoard[futurePosition[0]][futurePosition[1]
                                           ] = None
        # remise en place des états de pièces
        self.arrayBoard[pastPosition[0]
                        ][pastPosition[1]].undoEnPassantMoved(pieceState)
        self.arrayBoard[pastAtePosition[0]
                        ][pastAtePosition[1]].undoEnPassantAte(pieceAteState)


def createPieceByType(type):
    switcher = {
        "wP": Pawn("wP"),
        "bP": Pawn("bP"),
        "bR": Rock("bR"),
        "wR": Rock("wR"),
        "bN": Knight("bN"),
        "wN": Knight("wN"),
        "bB": Bishop("bB"),
        "wB": Bishop("wB"),
        "bQ": Queen("bQ"),
        "wQ": Queen("wQ"),
        "bK": King("bK"),
        "wK": King("wK"),
    }
    return switcher.get(type, "nothing")
