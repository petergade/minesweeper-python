import pygame
import sys
import common


class StartScreen:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    def show(self) -> common.Difficulty:
        self.screen = pygame.display.set_mode((300, 600))
        pygame.display.set_caption("Start of the game")

        # TODO: udelat nejaky uvodni label (uvitani do hry)
        # TODO: udelat tlacitko pro vybrani obriznosti
        # TODO: udelat prvky pro zadani sirky, vysky a poctu min (kdyz zbyde cas)

        while True:
            self.clock.tick(common.MAX_FPS)
            for e in pygame.event.get():
                # print(e)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    # TODO: najit vybrane tlacitko nebo custom rozmery a predat obtiznost jako vystup metody
                    return common.Beginner()
                    # return common.Difficulty(width, height, mines) # custom rozmery a pocet min
            self.screen.fill(common.WHITE)
            pygame.display.flip()
