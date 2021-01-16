import pygame
from startscreen import StartScreen
from endscreen import EndScreen
from mainscreen import MainScreen

pygame.init()


class Game:

    def start(self):
        start_screen = StartScreen()
        difficulty = start_screen.show()
        main_screen = MainScreen(difficulty)
        game_result = main_screen.show()
        end_screen = EndScreen(game_result)
        end_screen.show()


if __name__ == "__main__":
    game = Game()
    game.start()
