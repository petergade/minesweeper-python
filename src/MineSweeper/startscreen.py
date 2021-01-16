import pygame
import sys
import common


class StartScreen:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    @staticmethod
    def text_objects(text, font, colour=common.BLACK):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()

    def button(self, text, x, y, w, h, click, inactive_colour=common.BLACK, active_colour=common.RED,
               text_colour=common.WHITE):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h))
            if click and pygame.time.get_ticks() > 100:
                return_value = True
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h))

        text_surf, text_rect = self.text_objects(text, common.FONT, colour=text_colour)
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def show(self) -> common.Difficulty:
        self.screen = pygame.display.set_mode((370, 600))
        pygame.display.set_caption("minesweeper")
        common.set_game_icon()

        # TODO: udelat nejaky uvodni label (uvitani do hry)
        # TODO: udelat tlacitko pro vybrani obriznosti
        # TODO: udelat prvky pro zadani sirky, vysky a poctu min (kdyz zbyde cas)
        self.screen.fill(common.GREY2)

        while True:
            click = False
            self.clock.tick(common.MAX_FPS)
            for e in pygame.event.get():
                # print(e)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    click = True
            if self.button('B E G I N N E R', 50, 150, 270, 50, click):
                return common.Beginner()
            if self.button('I N T E R M E D I A T E', 50, 250, 270, 50, click):
                return common.Intermediate()
            if self.button('E X P E R T', 50, 350, 270, 50, click):
                return common.Expert()
            if self.button('Q U I T   G A M E', 50, 450, 270, 50, click):
                pygame.quit()
                sys.exit()
            pygame.display.flip()
