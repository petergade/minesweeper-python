import pygame
import common
import sys
import time
from gamestate import GameState

# TODO: toto by melo zmizet jakmile vykreslime obrazovku pomoci predanych parametru z difficulty
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION


class MainScreen:
    def __init__(self, difficulty: common.Difficulty):
        self.hide_board = True  # parametr pro testovani, zda se ma zobrazovat zakryta nebo odkryta hraci plocha
        self.game_state = None
        self.width: int = difficulty.width
        self.height: int = difficulty.height
        self.mines: int = difficulty.mines

    def show(self) -> common.GameResult:
        # TODO: podle width a height urcit rozmery obrazovky a kosticky
        # TODO: nacteni grafiky, zvuků, hudby, animací
        block_main = pygame.image.load(path.join(folder, "pole.png"))
        block_plain = pygame.image.load(path.join(folder, "pole-odkryte.png"))
        explosion = pygame.mixer.Sound(path.join(folder, "vybuch.mp3"))
        block1 = pygame.image.load(path.join(folder, "pole.png"))
        block2 = pygame.image.load(path.join(folder, "pole.png"))
        block3 = pygame.image.load(path.join(folder, "pole.png"))
        block4 = pygame.image.load(path.join(folder, "pole.png"))
        block5 = pygame.image.load(path.join(folder, "pole.png"))
        block6 = pygame.image.load(path.join(folder, "pole.png"))
        block7 = pygame.image.load(path.join(folder, "pole.png"))
        block8 = pygame.image.load(path.join(folder, "pole.png"))
        flag = pygame.image.load(path.join(folder, "flag.png"))



        screen = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("minesweeper")
        clock = pygame.time.Clock()
        self.game_state = GameState(self.width, self.height, self.mines)
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
                    # TODO: udelat detekci kolize se spritem jak rikal Safr
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

            if self.game_state.game_result_type == common.GameResultType.LOST or \
                    self.game_state.game_result_type == common.GameResultType.WIN:
                time.sleep(2)
                # TODO: nahradit skutecny casem
                return common.GameResult(self.game_state.game_result_type, 0)

    def draw_game_state(self, screen: pygame.Surface) -> None:
        print(self.game_state.game_result_type)
        if self.game_state.game_result_type == common.GameResultType.LOST or self.game_state.game_result_type == common.GameResultType.WIN:
            map_to_draw = self.game_state.game_map
        else:
            map_to_draw = self.game_state.player_map if self.hide_board else self.game_state.game_map
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                pygame.draw.rect(screen, common.GREY, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
        for r in range(self.height):
            for c in range(self.width):
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