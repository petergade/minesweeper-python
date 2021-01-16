import pygame

class SpecialSquareValues:
    FOG = -1
    FLAG = -2
    MINE = -3


class GameResult:
    UNKNOWN = 0
    WIN = 1
    LOST = 2


class Difficulty:
    def __init__(self, w, h, m):
        self.width = w
        self.height = h
        self.mines = m


class Beginner(Difficulty):
    def __init__(self):
        Difficulty.__init__(self, 9, 9, 10)


class Intermediate(Difficulty):
    def __init__(self):
        Difficulty.__init__(self, 16, 16, 40)


class Expert(Difficulty):
    def __init__(self):
        Difficulty.__init__(self, 30, 16, 99)


MAX_FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GREY = pygame.Color("grey")

pygame.font.init()
FONT = pygame.font.Font("freesansbold.ttf", 32)