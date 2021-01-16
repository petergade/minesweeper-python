import pygame
import common
import sys
import time
from gamestate import GameState

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION


class MainScreen:
    def __init__(self):
        self.hide_board = True
        self.game_state = None

    def show(self) -> common.GameResult:

        screen = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("minesweeper")
        clock = pygame.time.Clock()
        self.game_state = GameState(8, 8, 10)
        running = True

        while running:
            # kontrola FPS
            clock.tick(common.MAX_FPS)

            for e in pygame.event.get():
                #print(e)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if e.button == 1:  # leve tlacitko
                        self.game_state.reveal(row, col)
                    elif e.button == 3:  # prave tlacitko
                        self.game_state.add_flag(row, col)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        self.hide_board = not self.hide_board

            # update
            screen.fill(common.WHITE)
            self.draw_game_state(screen)

            # render
            pygame.display.flip()

            if self.game_state.game_result == common.GameResult.LOST or self.game_state.game_result == common.GameResult.WIN:
                time.sleep(2)
                return self.game_state.game_result

    def draw_game_state(self, screen: pygame.Surface) -> None:
        print(self.game_state.game_result)
        if self.game_state.game_result == common.GameResult.LOST or self.game_state.game_result == common.GameResult.WIN:
            map_to_draw = self.game_state.game_map
        else:
            map_to_draw = self.game_state.player_map if self.hide_board else self.game_state.game_map
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                pygame.draw.rect(screen, common.GREY, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
        for r in range(self.game_state.height):
            for c in range(self.game_state.width):
                text = self.get_text_to_draw(map_to_draw[r][c])
                text_surface = common.FONT.render(text, True, common.BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (c * SQ_SIZE + 30, r * SQ_SIZE + 30)
                screen.blit(text_surface, text_rect)

    @staticmethod
    def get_text_to_draw(square_type: int) -> str:
        if square_type == common.SpecialSquareValues.FOG:
            return 'F'
        elif square_type == common.SpecialSquareValues.FLAG:
            return 'V'
        elif square_type == common.SpecialSquareValues.MINE:
            return 'X'
        else:
            return str(square_type)