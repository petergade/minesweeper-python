import pygame
import common
import sys
import time
import os
from os import path
from gamestate import GameState
from sprites import Brick

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
        self.images[common.SpecialSquareValues.MINE] = pygame.image.load(path.join(common.assets_folder, "mina2.png")).convert()
        self.images[common.SpecialSquareValues.FLAG] = pygame.image.load(path.join(common.assets_folder, "flag2.png")).convert()
        self.images[common.SpecialSquareValues.FOG] = pygame.image.load(path.join(common.assets_folder, "pole.png")).convert()
        self.images[0] = pygame.image.load(path.join(common.assets_folder, "pole-odkryte.png")).convert()
        for i in range(8):
            self.images[i + 1] = pygame.image.load(path.join(common.assets_folder, f"pole-{i + 1}.png")).convert()

    def scale_images(self):
        for key in self.images.keys():
            self.images[key] = pygame.transform.scale(self.images[key], (common.SQ_SIZE, common.SQ_SIZE))

    def show(self) -> common.GameResult:

        # Grafika
        self.load_images()
        self.scale_images()

        # Zvuky, hudba, animace
        explosion_sound = pygame.mixer.Sound(path.join(common.assets_folder, "vybuch.mp3"))

        screen = pygame.display.set_mode((self.width * common.SQ_SIZE, self.height * common.SQ_SIZE))
        pygame.display.set_caption("Minesweeper")
        common.set_game_icon()
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
                    for brick in self.bricks:
                        if brick.rect.collidepoint(e.pos):
                            row = brick.r
                            col = brick.c
                            if e.button == 1:  # leve tlacitko
                                if self.game_state.reveal(row, col):
                                    explosion_sound.play()
                            elif e.button == 3:  # prave tlacitko
                                self.game_state.add_flag(row, col)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        self.hide_board = not self.hide_board

            # update
            self.update_bricks()
            self.bricks.update()

            # render
            self.bricks.draw(screen)
            pygame.display.flip()

            if self.game_state.game_result_type == common.GameResultType.LOST or \
                    self.game_state.game_result_type == common.GameResultType.WIN:
                time.sleep(5)
                return common.GameResult(self.game_state.game_result_type, self.game_state.elapsed_seconds)

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