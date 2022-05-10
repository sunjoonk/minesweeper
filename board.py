import random
from piece import Piece

class Board:
    def __init__(self, rows, cols, count):
        self.rows = rows
        self.cols = cols
        self.count = count
        self.won = False
        self.lost = False
        self.setBoard()

    def setBoard(self):
        self.board = []
        bombs = []
        while len(bombs) < self.count:
            bomb = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if bomb in bombs:
                continue
            bombs.append(bomb)
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                hasBomb = False
                if (row, col) in bombs:
                    hasBomb = True
                piece = Piece(hasBomb)
                line.append(piece)
            self.board.append(line)
        self.setNeighbors()
        self.setAround()

    def getBoard(self):
        return self.board

    def setNeighbors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                neighbors = self.getNeighborList(row, col)
                piece.setNeighbors(neighbors)

    def getNeighborList(self, row, col):
        neighbors = []
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                    continue
                neighbors.append(self.board[r][c])
        return neighbors
    
    def setAround(self):
        for row in self.board:
            for piece in row:
                piece.setAround()
    
    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def getWon(self):
        return self.won
    
    def getLost(self):
        return self.lost

    def checkWon(self):
        for row in self.board:
            for piece in row:
                if (piece.getHasBomb() and not piece.getFlagged()):
                    return False
                if (not piece.getHasBomb() and not piece.getClicked()):
                    return False
        return True

    def handleClick(self, piece, rightClick, byUser):
        if (piece.getFlagged() and not rightClick):
            return
        if not piece.getClicked() and rightClick:
            piece.toggleFlag()
            return
        if piece.getClicked():
            if byUser:
                self.openUnflagged(piece)
            return
        if not piece.getClicked() and not rightClick:
            piece.handleClick()
            if piece.getHasBomb():
                self.lost = True
                return
            elif piece.getAround() == 0:
                for neighbor in piece.getNeighbors():
                    self.handleClick(neighbor, False, False)
        if self.checkWon():
            self.won = True
            return
        else:
            return

    def openUnflagged(self, piece):
        around = piece.getAround()
        unknown = 0
        flagged = 0
        neighbors = piece.getNeighbors()
        for neighbor in neighbors:
            if not neighbor.getClicked():
                unknown += 1
            if neighbor.getFlagged():
                flagged += 1
        if around == flagged:
            for neighbor in neighbors:
                if not piece.getFlagged():
                    self.handleClick(neighbor, False, False)

    def getLastBomb(self):
        flagged = 0
        for rows in self.board:
            for piece in rows:
                if piece.getFlagged():
                    flagged += 1
        return self.count - flagged
