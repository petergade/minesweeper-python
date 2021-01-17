import pygame

from startscreen import StartScreen
from mainscreen import MainScreen
import os

assets_folder = os.path.join(os.path.dirname(__file__), "assets")

pygame.init()


def start_background_music():
    background_music = pygame.mixer.Sound(os.path.join(assets_folder, "relax-mix.mp3"))
    pygame.mixer.init()
    background_music.play(loops=-1)


class Game:

    def start(self):
        start_background_music()
        repeat = True

        while repeat:
            start_screen = StartScreen()
            difficulty = start_screen.show()
            main_screen = MainScreen(difficulty)
            repeat = main_screen.show()


if __name__ == "__main__":
    game = Game()
    game.start()
