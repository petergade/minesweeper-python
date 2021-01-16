import pygame
import sys
import common


class StartScreen:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    def show(self):
        self.screen = pygame.display.set_mode((300, 600))
        pygame.display.set_caption("Start of the game")
        running = True

        while running:
            self.clock.tick(common.MAX_FPS)
            for e in pygame.event.get():
                # print(e)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            self.screen.fill(common.WHITE)
            pygame.display.flip()
