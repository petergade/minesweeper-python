import pygame
import sys
import common

BLUE = 33, 150, 243
LIGHT_BLUE = 0, 191, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0

class StartScreen:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    @staticmethod
    def text_objects(text, font, colour=BLACK):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()

    def button(self, text, x, y, w, h, inactive_colour=BLUE, active_colour=LIGHT_BLUE, text_colour=WHITE):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h))
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h))

        text_surf, text_rect = self.text_objects(text, common.FONT, colour=text_colour)
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def show(self) -> common.Difficulty:
        self.screen = pygame.display.set_mode((370, 600))
        pygame.display.set_caption("Start of the game")

        # TODO: udelat nejaky uvodni label (uvitani do hry)
        # TODO: udelat tlacitko pro vybrani obriznosti
        # TODO: udelat prvky pro zadani sirky, vysky a poctu min (kdyz zbyde cas)
        self.screen.fill(common.WHITE)


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
            self.button('B E G I N N E R', 50, 150, 270, 50)
            self.button('I N T E R M E D I A T E', 50, 250, 270, 50)
            self.button('E X P E R T', 50, 350, 270, 50)
            pygame.display.flip()
