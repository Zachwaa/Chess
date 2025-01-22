from move import Move
import random
from cmath import inf


class chessEngine():

    def __init__(self):

        # Pawn = p
        # King = k
        # Queen = q
        # Bishop = b
        # Horse = h
        # Rook = r

        self.checkMate = False
        self.staleMate = False

        self.validMoves = []
        self.pCactive = False
        self.storedPiece = []

        self.whiteToMove = True
        self.moveFunctions = {"p": self.pawnMove, "r": self.rookMove, "b": self.bishopMove,
                              "q": self.queenMove, "k": self.kingMove, "h": self.horseMove}
        self.moveLog = []
        self.board = [["br", "bh", "bb", "bq", "bk", "bb", "bh", "br"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wr", "wh", "wb", "wq", "wk", "wb", "wh", "wr"]
                      ]
        self.whiteKingPos = [7, 4]
        self.blackKingPos = [0, 4]

        self.validMoves = self._getValidMoves()

    def _makeMove(self, move):

        if move.function != "":
            move.function(move)
        else:
            self.board[move.endRow][move.endColumn] = move.pieceMoved

        self.board[move.startRow][move.startColumn] = "--"
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wk":
            self.whiteKingPos = [move.endRow, move.endColumn]
        if move.pieceMoved == "bk":
            self.blackKingPos = [move.endRow, move.endColumn]

        self.moveLog.append(move)

    def _printBoard(self):
        for i in self.board:
            print(i)

    def _undoMove(self):
        if len(self.moveLog):
            lastMove = self.moveLog[len(self.moveLog)-1]

            self.board[lastMove.startRow][lastMove.startColumn] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endColumn] = lastMove.pieceCaptured

            self.whiteToMove = not self.whiteToMove
            if lastMove.pieceMoved == "wk":
                self.whiteKingPos = [lastMove.startRow, lastMove.startColumn]
            if lastMove.pieceMoved == "bk":
                self.blackKingPos = [lastMove.startRow, lastMove.startColumn]

            self.moveLog.pop()
            if lastMove.coMove != "":
                self._undoMove()
                self.whiteToMove = not self.whiteToMove

    def _getValidMoves(self):
        moves = self.getAllMoves()

        self.whiteToMove = not self.whiteToMove
        checkMoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove

        if self._inCheck(checkMoves):
            for i in moves:
                if i.function == self.castle:
                    moves.remove(i)

        for i in range(len(moves)-1, -1, -1):
            self._makeMove(moves[i])
            oppMoves = self.getAllMoves()
            self.whiteToMove = not self.whiteToMove
            if self._inCheck(oppMoves):
                moves.remove(moves[i])
            self._undoMove()
            self.whiteToMove = not self.whiteToMove

        return moves

    def _inCheck(self, moves):
        if self.whiteToMove:
            for move in moves:
                if move.endRow == self.whiteKingPos[0] and move.endColumn == self.whiteKingPos[1]:
                    return True
        else:
            for move in moves:
                if move.endRow == self.blackKingPos[0] and move.endColumn == self.blackKingPos[1]:
                    return True
        return False

    def getAllMoves(self):
        moves = []
        color = "w" if self.whiteToMove else "b"
        for r in range(0, 8):
            for c in range(0, 8):
                piece = self.board[r][c]
                if piece[1] != "-" and color == piece[0]:
                    self.moveFunctions[piece[1]](r, c, moves)
        return moves

    def Z_keyPress(self):

        self._undoMove()
        self.validMoves = []
        self.validMoves = self._getValidMoves()
        self.pCactive = False  # Reset values for next move
        self.storedPiece = []

    def _processClick(self, coords, gui):
        if self.pCactive:  # Confirmation Click

            if coords != self.storedPiece:  # UnHighlight piece if click is in orignial square

                move = Move(self.storedPiece, coords, self.board)
                for moveToDo in self.validMoves:
                    if move == moveToDo:
                        self._makeMove(moveToDo)
                        self._checkGameStatus()
                        self.validMoves = []

                        self._makeMove(self.minimax(3, False, "b")[0])
                        gui._refreshBoard(self.board)

                        self.validMoves = self._getValidMoves()
                        self._printBoard()

            self.pCactive = False  # Reset values for next move
            self.storedPiece = []

        else:  # Highlight piece to move
            if ((self.board[coords[0]][coords[1]][0] == "w" and self.whiteToMove)):  # or
                #  (self.board[coords[0]][coords[1]][0] == "b" and not self.whiteToMove)):
                self.storedPiece = coords  # Store Piece selected
                self.pCactive = True  # Change to confirmation click

    def _checkGameStatus(self):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove

        if len(self.validMoves) == 0:
            if self._inCheck(oppMoves):
                self.checkMate = True
                print(
                    f"Checkmate   {'Black' if self.whiteToMove else 'White'} Has Won")
            else:
                self.staleMate = True
                print(f"StaleMate")

    def PromoteToQueen(self, move):

        color = move.pieceMoved[0]
        self.board[move.endRow][move.endColumn] = f"{color}q"

    def enPassant(self, move):
        self._makeMove(move.coMove)
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove

    def castle(self, move):

        self._makeMove(move.coMove)
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove

    def File(self, r, c, moves, direction):
        straight = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        diagnol = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.board[r][c][0]
        oppColor = "b" if color == "w" else "w"
        tempmoves = []
        if direction == "diagnol":
            tempmoves = diagnol
        else:
            tempmoves = straight

        for dir in tempmoves:
            i = dir[0]
            p = dir[1]
            while (0 <= r+i < 8) and (0 <= c+p < 8):
                if self.board[r+i][c+p][0] != color:
                    moves.append(Move([r, c], [r+i, c+p], self.board))
                    if self.board[r+i][c+p][0] == oppColor:
                        break
                else:
                    break
                i += dir[0]
                p += dir[1]

    def pawnMove(self, r, c, moves):
        color = self.board[r][c][0]
        oppColor = "b" if color == "w" else "w"
        if self.board[r][c][0] == "w":
            if r == 6 and self.board[r-2][c] == "--":
                moves.append(Move([r, c], [r-2, c], self.board))
            if r == 3:
                if c-1 >= 0:
                    if self.board[r][c-1][0] == oppColor:
                        moves.append(Move([r, c], [r-1, c-1], self.board,
                                          self.enPassant, Move([r, c-1], [r, c-1], self.board)))
                if c+1 < 8:
                    if self.board[r][c+1][0] == oppColor:
                        moves.append(Move([r, c], [r-1, c+1], self.board,
                                          self.enPassant, Move([r, c+1], [r, c+1], self.board)))
            if r-1 >= 0:
                if self.board[r-1][c] == "--":
                    if r-1 > 0:
                        moves.append(Move([r, c], [r-1, c], self.board))
                    else:
                        moves.append(
                            Move([r, c], [r-1, c], self.board, self.PromoteToQueen))

                if c+1 < 8:
                    if self.board[r-1][c+1][0] == oppColor:
                        if r-1 > 0:
                            moves.append(Move([r, c], [r-1, c+1], self.board))
                        else:
                            moves.append(
                                Move([r, c], [r-1, c+1], self.board, self.PromoteToQueen))
                if c-1 >= 0:
                    if self.board[r-1][c-1][0] == oppColor:
                        if r-1 > 0:
                            moves.append(Move([r, c], [r-1, c-1], self.board))
                        else:
                            moves.append(
                                Move([r, c], [r-1, c-1], self.board, self.PromoteToQueen))

        else:
            if r == 1 and self.board[r+2][c] == "--":
                moves.append(Move([r, c], [r+2, c], self.board))
            if r == 4:
                if c-1 >= 0:
                    if self.board[r][c-1][0] == oppColor:
                        moves.append(Move([r, c], [r+1, c-1], self.board,
                                          self.enPassant, Move([r, c-1], [r, c-1], self.board)))
                if c+1 < 8:
                    if self.board[r][c+1][0] == oppColor:
                        moves.append(Move([r, c], [r+1, c+1], self.board,
                                          self.enPassant, Move([r, c+1], [r, c+1], self.board)))
            if r+1 < 8:
                if self.board[r+1][c] == "--":
                    if r+1 < 7:
                        moves.append(Move([r, c], [r+1, c], self.board))
                    else:
                        moves.append(
                            Move([r, c], [r+1, c], self.board, self.PromoteToQueen))
                if c+1 < 8:
                    if self.board[r+1][c+1][0] == oppColor:
                        if r+1 < 7:
                            moves.append(Move([r, c], [r+1, c+1], self.board))
                        else:
                            moves.append(
                                Move([r, c], [r+1, c+1], self.board, self.PromoteToQueen))
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == oppColor:
                        if r+1 < 7:
                            moves.append(Move([r, c], [r+1, c-1], self.board))
                        else:
                            moves.append(
                                Move([r, c], [r+1, c-1], self.board, self.PromoteToQueen))

    def horseMove(self, r, c, moves):
        tempmoves = [[r+2, c+1], [r-2, c+1], [r+2, c-1], [r-2, c-1],
                     [r+1, c+2], [r-1, c+2], [r+1, c-2], [r-1, c-2]]

        for i in tempmoves:
            if (0 <= i[0] < 8) and (0 <= i[1] < 8):
                if (self.board[i[0]][i[1]][0] != self.board[r][c][0]):
                    moves.append(Move([r, c], [i[0], i[1]], self.board))

    def rookMove(self, r, c, moves):
        self.File(r, c, moves, "straight")

    def queenMove(self, r, c, moves):
        self.File(r, c, moves, "straight")
        self.File(r, c, moves, "diagnol")

    def bishopMove(self, r, c, moves):
        self.File(r, c, moves, "diagnol")

    def kingMove(self, r, c, moves):

        tempmoves = [(r+1, c+1), (r, c+1), (r+1, c-1), (r+1, c),
                     (r-1, c+1), (r-1, c-1), (r-1, c), (r, c-1)]
        color = self.board[r][c][0]
        for i in tempmoves:
            if (0 <= i[0] < 8) and (0 <= i[1] < 8):
                if (self.board[i[0]][i[1]][0] != color):
                    moves.append(Move([r, c], [i[0], i[1]], self.board))

        leftRook = rightRook = king = False

        for m in self.moveLog:
            if m.pieceMoved == f"{color}k":
                king = True
            if color == "w":
                if m.pieceMoved[1] == "r":
                    if m.startRow == 7 and m.startColumn == 0:
                        leftRook = True
                    if m.startRow == 7 and m.startColumn == 7:
                        rightRook = True

            if color == "b":
                if m.pieceMoved[1] == "r":
                    if m.startRow == 0 and m.startColumn == 0:
                        leftRook = True
                    if m.startRow == 0 and m.startColumn == 7:
                        rightRook = True

        if color == "w":
            if r == 7 and c == 4:
                if not king:
                    if self.board[7][7] == "wr" and self.board[7][6] == "--" and self.board[7][5] == "--" and not rightRook:
                        moves.append(Move([r, c], [7, 6], self.board, self.castle, Move(
                            [7, 7], [7, 5], self.board)))
                    if self.board[7][0] == "wr" and self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--" and not leftRook:
                        moves.append(Move([r, c], [7, 2], self.board, self.castle, Move(
                            [7, 0], [7, 3], self.board)))
        else:
            if r == 0 and c == 4:
                if not king:
                    if self.board[0][7] == "br" and self.board[0][6] == "--" and self.board[0][5] == "--" and not rightRook:
                        moves.append(Move([r, c], [0, 6], self.board, self.castle, Move(
                            [0, 7], [0, 5], self.board)))
                    if self.board[0][0] == "br" and self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--" and not leftRook:
                        moves.append(Move([r, c], [0, 2], self.board, self.castle, Move(
                            [0, 0], [0, 3], self.board)))

    def getScore(self, color):
        score = 0
        for r in self.board:
            for c in r:
                if c[0] == color:
                    if c[1] == "p":
                        score += 100
                    elif c[1] == "r":
                        score += 500
                    elif c[1] == "h" or c[1] == "b":
                        score += 300
                    elif c[1] == "q":
                        score += 900

        return score

    def evaluate(self, maximising_color):
        whiteScore = self.getScore("w")
        blackScore = self.getScore("b")
        if maximising_color == "b":
            return blackScore - whiteScore
        else:
            return whiteScore - blackScore

    def minimax(self, depth, maximising_player, maximising_color):
        if depth == 0 or self.checkMate:
            return None, self.evaluate(maximising_color)

        moves = self._getValidMoves()

        best_move = random.choice(moves)

        if maximising_player:
            max_eval = -inf
            for move in moves:

                self._makeMove(move)
                self.checkMate = False

                current_eval = self.minimax(
                    depth-1, False, maximising_color)[1]
                self._undoMove()

                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
            return best_move, max_eval
        else:
            max_eval = inf
            for move in moves:

                self._makeMove(move)

                current_eval = self.minimax(
                    depth-1, True, maximising_color)[1]

                self._undoMove()
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
            return best_move, max_eval
