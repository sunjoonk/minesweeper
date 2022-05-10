class Piece:
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False
    
    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked
    
    def getFlagged(self):
        return self.flagged

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
    
    def getNeighbors(self):
        return self.neighbors
    
    def setAround(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.getHasBomb():
                num += 1
            self.around = num
    
    def getAround(self):
        return self.around

    def toggleFlag(self):
        self.flagged = not self.flagged

    def handleClick(self):
        self.clicked = True