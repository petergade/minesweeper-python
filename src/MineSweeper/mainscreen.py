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
        self.sprites = pygame.sprite.Group()

    def load_images(self):
        self.images[common.SpecialSquareValues.MINE] = pygame.image.load(path.join(assets_folder, "mina.png"))
        self.images[common.SpecialSquareValues.FLAG] = pygame.image.load(path.join(assets_folder, "flag.png"))
        self.images[common.SpecialSquareValues.FOG] = pygame.image.load(path.join(assets_folder, "pole.png"))
        self.images[0] = pygame.image.load(path.join(assets_folder, "pole-odkryte.png"))
        for i in range(8):
            self.images[i + 1] = pygame.image.load(path.join(assets_folder, f"pole-{i + 1}.png"))

    def show(self) -> common.GameResult:
        # TODO: podle width a height urcit rozmery obrazovky a kosticky
        # TODO: nacteni grafiky, zvuků, hudby, animací

        #player = Spritesheet(path.join(folder, ""))
        #folder = path.dirname(_file_)

        # Grafika
        self.load_images()

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
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # TODO: udelat detekci kolize se spritem jak rikal Safr
                    location = pygame.mouse.get_pos()
                    col = location[0] // common.SQ_SIZE
                    row = location[1] // common.SQ_SIZE
                    if e.button == 1:  # leve tlacitko
                        self.game_state.reveal(row, col)
                    elif e.button == 3:  # prave tlacitko
                        self.game_state.add_flag(row, col)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        self.hide_board = not self.hide_board

            # update
            self.sprites.update()

            # render
            screen.fill(common.WHITE)
            self.sprites.draw(screen)
            pygame.display.flip()

            if self.game_state.game_result_type == common.GameResultType.LOST or \
                    self.game_state.game_result_type == common.GameResultType.WIN:
                time.sleep(2)
                # TODO: nahradit skutecny casem
                return common.GameResult(self.game_state.game_result_type, 0)

    def initialize_sprites(self):
        for r in range(self.height):
            for c in range(self.width):
                brick = Brick(r * common.SQ_SIZE, c * common.SQ_SIZE, self.images)
                self.sprites.add(brick)

    def draw_game_state(self, screen: pygame.Surface) -> None:
        if self.game_state.game_result_type == common.GameResultType.LOST or self.game_state.game_result_type == common.GameResultType.WIN:
            map_to_draw = self.game_state.game_map
        else:
            map_to_draw = self.game_state.player_map if self.hide_board else self.game_state.game_map
        for r in range(self.height):
            for c in range(self.width):
                text = self.get_text_to_draw(map_to_draw[r][c])
                brick = Brick(self.images[common.SpecialSquareValues.FOG])


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