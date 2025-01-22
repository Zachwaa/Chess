class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5,
                   "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToColumns = {"a": 0, "b": 1, "c": 2,
                      "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {v: k for k, v in filesToColumns.items()}

    def __init__(self, startPos, endPos, board, func="", coMove=""):
        self.startRow = startPos[0]
        self.startColumn = startPos[1]
        self.endRow = endPos[0]
        self.endColumn = endPos[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        self.ID = self.startRow * 1000 + self.startColumn * \
            100 + self.endRow * 10 + self.endColumn
        self.function = func

        self.coMove = coMove

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.ID == other.ID
        else:
            return False

    def getRankFile(self, r, c):
        return self.columnsToFiles[c] + self.rowsToRanks[r]

    def coordToNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)
