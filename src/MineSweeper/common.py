import pygame

class SpecialSquareValues:
    FOG = -1
    FLAG = -2
    MINE = -3


class GameResult:
    UNKNOWN = 0
    WIN = 1
    LOST = 2


MAX_FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GREY = pygame.Color("grey")

pygame.font.init()
FONT = pygame.font.Font("freesansbold.ttf", 32)