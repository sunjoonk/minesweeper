import os
import sys
import time
import pygame
from board import Board
from timer import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.size = 25
        self.count = 100
        self.rows, self.cols = 20, 30
        self.board = Board(self.rows, self.cols, self.count)
        self.loadSource()
        self.timer = None
        self.record = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mine Sweeper")
        pygame.display.set_icon(self.buttons["icon"])
        self.resetRect = pygame.Rect(self.size * 15, self.size / 2, self.size * 2, self.size * 2)

    def loadSource(self):
        self.images = {}
        self.buttons = {}
        for dirName, _, fileNames in os.walk("source"):
            for fileName in fileNames:
                if "image" in dirName:
                    img = pygame.image.load(os.path.join(dirName, fileName))
                    img = pygame.transform.scale(img, (self.size, self.size))
                    self.images[fileName.split('.')[0]] = img
                elif "button" in dirName:
                    button = pygame.image.load(os.path.join(dirName, fileName))
                    button = pygame.transform.scale(button, (self.size * 2, self.size * 2))
                    self.buttons[fileName.split('.')[0]] = button
                elif "font" in dirName:
                    self.font = pygame.font.Font(os.path.join(dirName, fileName), 50)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.resetRect.collidepoint(event.pos):
                    self.record = 0
                    self.timer = None
                    self.board = Board(self.rows, self.cols, self.count)
                elif event.type == pygame.MOUSEBUTTONUP and not (self.board.getWon() or self.board.getLost()):
                    if self.timer == None:
                        self.timer = Timer()
                    rightClick = (event.button == 3)
                    self.handleClick(event.pos, rightClick, True)
            if not self.timer == None and not (self.board.getWon() or self.board.getLost()):
                self.timer.setTime()
                self.record = self.timer.getTime()
            self.draw()
            pygame.display.update()
    
    def draw(self):
        self.screen.fill((192, 192, 192))
        button = self.buttons[self.getButton()]
        self.screen.blit(button, (self.size * 15, self.size / 2))
        pygame.draw.rect(self.screen, "black", (self.size, self.size / 2, self.size * 4, self.size * 2))
        pygame.draw.rect(self.screen, "black", (self.size * 27, self.size / 2, self.size * 4, self.size * 2))
        scoreScreen = self.font.render("{:1d}".format(self.board.getLastBomb()), True, "red")
        self.screen.blit(scoreScreen, (self.size + 12.5, self.size / 2))
        timerScreen = self.font.render("{:03d}".format(self.record), True, "red")
        self.screen.blit(timerScreen, (self.size * 27 + 12.5, self.size / 2))
        topLeft = (25, 75)
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board.getPiece((row, col))
                string = self.getString(piece)
                img = self.images[string]
                self.screen.blit(img, topLeft)
                topLeft = (topLeft[0] + self.size, topLeft[1])
            topLeft = (25, topLeft[1] + self.size)
    
    def getString(self, piece):
        if piece.getClicked():
            return str(piece.getAround()) if not piece.getHasBomb() else "bomb_clicked"
        if self.board.getLost():
            if piece.getHasBomb():
                return "bomb"
        return "unclicked" if not piece.getFlagged() else "flagged"

    def getButton(self):
        if self.board.getWon():
            return "won"
        if self.board.getLost():
            return "lost"
        return "play"

    def handleClick(self, position, rightClick, byUser):
        index = (int((position[1] - self.size * 2) / self.size) - 1, int((position[0]) / self.size) - 1)
        if index[0] < 0 or index[0] >= self.rows or index[1] < 0 or index[1] >= self.cols:
            return
        self.board.handleClick(self.board.getPiece(index), rightClick, byUser)
