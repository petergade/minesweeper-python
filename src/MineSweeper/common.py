import pygame
from os import path


class SpecialSquareValues:
    FOG = -1
    FLAG = -2
    MINE = -3


class GameResultType:
    UNKNOWN = 0
    WIN = 1
    LOST = 2


class GameResult:
    def __init__(self, game_result_type: GameResultType, elapsed_time: int):
        self.game_result_type = game_result_type
        self.elapsed_time = elapsed_time # pocet sekund


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
SQ_SIZE = 36
LOGO_HEIGHT = 80
LOGO_WIDTH = 320
STATUS_BAR_HEIGHT = 36
STATUS_BAR_PADDINGTOP = 24
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GREY = pygame.Color("grey")
BLUE = pygame.Color(33, 150, 243)
LIGHT_BLUE = pygame.Color(0, 191, 255)
GREY2 = pygame.Color(224, 224, 224)
RED = pygame.Color(204, 0, 0)

pygame.font.init()
SMALL_FONT = pygame.font.Font("freesansbold.ttf", 18)
FONT = pygame.font.Font("freesansbold.ttf", 20)
BIG_FONT = pygame.font.Font("freesansbold.ttf", 36)

assets_folder = path.join(path.dirname(__file__), "assets")


def set_game_icon():
    icon = pygame.image.load(path.join(assets_folder, "mina.png")).convert()
    icon.set_colorkey(BLACK)
    pygame.display.set_icon(icon)


def set_game_logo(x, y, surface):
    logo = pygame.image.load(path.join(assets_folder, "logo2.jpg"))
    logo = pygame.transform.scale(logo, (LOGO_WIDTH, LOGO_HEIGHT))
    logo = logo.convert()
    #logo.set_colorkey(BLACK)
    surface.blit(logo, pygame.Rect(x, y, LOGO_WIDTH, LOGO_HEIGHT))