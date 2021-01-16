import pygame
import common
import sys
import time
from os import path
from gamestate import GameState
from sprites import Brick

assets_folder = path.join(path.dirname(__file__), "assets")


class MainScreen:
    def __init__(self, difficulty: common.Difficulty):
        self.hide_board = True  # parametr pro testovani, zda se ma zobrazovat zakryta nebo odkryta hraci plocha
        self.game_state = None
        self.width: int = difficulty.width
        self.height: int = difficulty.height
        self.mines: int = difficulty.mines
        self.images = {}
        self.bricks = pygame.sprite.Group()

    def load_images(self):
        self.images[common.SpecialSquareValues.MINE] = pygame.image.load(path.join(assets_folder, "mina.png")).convert()
        self.images[common.SpecialSquareValues.FLAG] = pygame.image.load(path.join(assets_folder, "flag.png")).convert()
        self.images[common.SpecialSquareValues.FOG] = pygame.image.load(path.join(assets_folder, "pole.png")).convert()
        self.images[0] = pygame.image.load(path.join(assets_folder, "pole-odkryte.png")).convert()
        for i in range(8):
            self.images[i + 1] = pygame.image.load(path.join(assets_folder, f"pole-{i + 1}.png")).convert()

    def scale_images(self):
        for key in self.images.keys():
            self.images[key] = pygame.transform.scale(self.images[key], (common.SQ_SIZE, common.SQ_SIZE))


    def show(self) -> common.GameResult:
        # TODO: podle width a height urcit rozmery obrazovky a kosticky
        # TODO: nacteni grafiky, zvuků, hudby, animací

        # Grafika
        self.load_images()
        self.scale_images()

        # Zvuky, hudba, animace
        explosion_sound = pygame.mixer.Sound(path.join(assets_folder, "vybuch.mp3"))
        background_music = pygame.mixer.Sound(path.join(assets_folder, "relax-mix.mp3"))

        screen = pygame.display.set_mode((self.width * 32, self.height * 32))
        pygame.display.set_caption("minesweeper")
        clock = pygame.time.Clock()
        self.game_state = GameState(self.width, self.height, self.mines)
        self.initialize_sprites()
        running = True

        while running:
            # kontrola FPS
            clock.tick(common.MAX_FPS)

            for e in pygame.event.get():
                #print(e)
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    # TODO: udelat detekci kolize se spritem jak rikal Safr
                    location = pygame.mouse.get_pos()
                    for brick in self.bricks:
                        if brick.collide_rect(brick, pygame.Rect(location[0], location[1], 1, 1)):
                            row = brick.r
                            col = brick.c
                            if e.button == 1:  # leve tlacitko
                                self.game_state.reveal(row, col)
                            elif e.button == 3:  # prave tlacitko
                                self.game_state.add_flag(row, col)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        self.hide_board = not self.hide_board

            # update
            self.update_bricks()
            self.bricks.update()

            # render
            #screen.fill(common.WHITE)
            self.bricks.draw(screen)
            pygame.display.flip()

            if self.game_state.game_result_type == common.GameResultType.LOST or \
                    self.game_state.game_result_type == common.GameResultType.WIN:
                time.sleep(2)
                # TODO: nahradit skutecny casem
                return common.GameResult(self.game_state.game_result_type, 0)

    def initialize_sprites(self):
        for r in range(self.height):
            for c in range(self.width):
                brick = Brick(r, c, self.images)
                self.bricks.add(brick)

    def update_bricks(self) -> None:
        if self.game_state.game_result_type == common.GameResultType.LOST or self.game_state.game_result_type == common.GameResultType.WIN:
            map_to_draw = self.game_state.game_map
        else:
            map_to_draw = self.game_state.player_map if self.hide_board else self.game_state.game_map
        for brick in self.bricks:
            brick.value = map_to_draw[brick.r][brick.c]


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