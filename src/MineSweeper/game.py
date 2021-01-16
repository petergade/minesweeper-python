import pygame
import common
from startscreen import StartScreen
from endscreen import EndScreen
from mainscreen import MainScreen
from os import path

assets_folder = path.join(path.dirname(__file__), "assets")

pygame.init()


def start_background_music():
    background_music = pygame.mixer.Sound(path.join(assets_folder, "relax-mix.mp3"))
    pygame.mixer.init()
    background_music.play()


class Game:

    def start(self):
        start_background_music()
        start_screen = StartScreen()
        difficulty = start_screen.show()
        main_screen = MainScreen(common.Intermediate())
        game_result = main_screen.show()
        end_screen = EndScreen(game_result)
        end_screen.show()


if __name__ == "__main__":
    game = Game()
    game.start()
