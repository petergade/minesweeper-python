import pygame
import common
import sys
from os import path
from gamestate import GameState
from sprites import Brick, Emoji, Explosion, SpriteSheet



class MainScreen:
    def __init__(self, difficulty: common.Difficulty):
        self.hide_board = True  # parametr pro testovani, zda se ma zobrazovat zakryta nebo odkryta hraci plocha
        self.game_state = None
        self.screen = None
        self.clock = None
        self.width: int = difficulty.width
        self.height: int = difficulty.height
        self.mines: int = difficulty.mines
        self.images = {}
        self.bricks = pygame.sprite.Group()
        self.emojis = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.game_over = False

    def load_images(self):
        self.images[common.SpecialSquareValues.MINE] = pygame.image.load(path.join(common.assets_folder, "mina2.png")).convert()
        self.images[common.SpecialSquareValues.FLAG] = pygame.image.load(path.join(common.assets_folder, "flag2.png")).convert()
        self.images[common.SpecialSquareValues.FOG] = pygame.image.load(path.join(common.assets_folder, "pole.png")).convert()
        self.images[0] = pygame.image.load(path.join(common.assets_folder, "pole-odkryte.png")).convert()
        self.images["emoji-happy"] = pygame.image.load(path.join(common.assets_folder, "emoji-smiley.jpg")).convert()
        self.images["emoji-sad"] = pygame.image.load(path.join(common.assets_folder, "emoji-exploding.jpg")).convert()
        for i in range(8):
            self.images[i + 1] = pygame.image.load(path.join(common.assets_folder, f"pole-{i + 1}.png")).convert()
        self.images["explosion"] = pygame.image.load(path.join(common.assets_folder, "animation.png")).convert()

    def scale_images(self):
        for key in self.images.keys():
            if key == "explosion":
                continue
            self.images[key] = pygame.transform.scale(self.images[key], (common.SQ_SIZE, common.SQ_SIZE))
        self.images["emoji-happy"] = pygame.transform.scale(self.images["emoji-happy"], (common.STATUS_BAR_HEIGHT, common.STATUS_BAR_HEIGHT))
        self.images["emoji-sad"] = pygame.transform.scale(self.images["emoji-sad"], (common.STATUS_BAR_HEIGHT, common.STATUS_BAR_HEIGHT))

    def show(self) -> bool:

        # Grafika
        self.load_images()
        self.scale_images()

        # Zvuky, hudba, animace
        explosion_sound = pygame.mixer.Sound(path.join(common.assets_folder, "vybuch.mp3"))

        self.screen = pygame.display.set_mode((self.width * common.SQ_SIZE, self.height * common.SQ_SIZE +
                                          common.LOGO_HEIGHT + common.STATUS_BAR_HEIGHT + common.STATUS_BAR_PADDINGTOP))
        pygame.display.set_caption("Minesweeper")
        common.set_game_icon()
        self.screen.fill(common.GREY2)
        common.set_game_logo((self.width * common.SQ_SIZE)/2-common.LOGO_WIDTH/2, 10, self.screen)
        self.clock = pygame.time.Clock()
        self.game_state = GameState(self.width, self.height, self.mines)
        self.initialize_bricks()
        self.initialize_emojis()
        self.draw_text("Time: ", common.FONT, (self.width * common.SQ_SIZE) - 130, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)
        self.draw_text("Mines: ", common.FONT, 30, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)
        running = True

        while running:
            if self.game_over and len(self.explosions) == 0:
                if self.show_game_over_screen():
                    return True

            # kontrola FPS
            self.clock.tick(common.MAX_FPS)

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
                                    self.play_explosion_animation(brick.rect.center)
                            elif e.button == 3:  # prave tlacitko
                                self.game_state.add_flag(row, col)
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_q:
                        self.hide_board = not self.hide_board

            # update
            self.update_bricks()
            self.update_emojis()
            self.bricks.update()
            self.emojis.update()
            self.explosions.update()
            print(len(self.explosions))

            # render
            self.screen.fill(common.GREY2)
            common.set_game_logo((self.width * common.SQ_SIZE)/2-common.LOGO_WIDTH/2, 10, self.screen)
            self.draw_text("Mines: ", common.FONT, 10, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)
            self.draw_remaining_mines()
            self.draw_text("Time: ", common.FONT, (self.width * common.SQ_SIZE) - 130, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)
            self.draw_elapsed_time()
            self.bricks.draw(self.screen)
            self.emojis.draw(self.screen)
            self.explosions.draw(self.screen)
            pygame.display.flip()

            if self.game_state.game_result_type == common.GameResultType.LOST or \
                    self.game_state.game_result_type == common.GameResultType.WIN:
                self.game_over = True

    def initialize_bricks(self):
        for r in range(self.height):
            for c in range(self.width):
                brick = Brick(r, c, self.images)
                self.bricks.add(brick)

    def initialize_emojis(self):
        emoji = Emoji((self.width * common.SQ_SIZE // 2) - 20, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP - 10, self.images)
        self.emojis.add(emoji)

    def play_explosion_animation(self, center):
        explosion = Explosion(center, SpriteSheet(self.images["explosion"]))
        self.explosions.add(explosion)

    def update_bricks(self) -> None:
        if self.game_state.game_result_type == common.GameResultType.LOST or self.game_state.game_result_type == common.GameResultType.WIN:
            map_to_draw = self.game_state.game_map
        else:
            map_to_draw = self.game_state.player_map if self.hide_board else self.game_state.game_map
        for brick in self.bricks:
            brick.value = map_to_draw[brick.r][brick.c]

    def update_emojis(self):
        for emoji in self.emojis:
            emoji.is_happy = False if self.game_state.game_result_type == common.GameResultType.LOST else True

    def draw_text(self, text, font, x, y, alliasing=False, colour=common.BLACK):
        text_surface = font.render(text, alliasing, colour)
        self.screen.blit(text_surface, (x, y))

    def draw_centered_text(self, text, font, y, alliasing=False, colour=common.BLACK):
        text_surface = font.render(text, alliasing, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = self.screen.get_rect().center
        text_rect.y = y
        self.screen.blit(text_surface, text_rect.topleft)

    def draw_elapsed_time(self):
        if self.game_over:
            elapsed_time = self.game_state.game_duration_in_seconds
        else:
            elapsed_time = self.game_state.get_elapsed_time()
        if elapsed_time is None:
            return
        elapsed_time_str = "%.1fs" % elapsed_time
        self.draw_text(elapsed_time_str, common.FONT, (self.width * common.SQ_SIZE) - 65, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)

    def draw_remaining_mines(self):
        self.draw_text(str(self.game_state.mines_not_selected), common.FONT, 85, common.LOGO_HEIGHT + common.STATUS_BAR_PADDINGTOP)

    def show_game_over_screen(self):
        self.draw_centered_text("G A M E  O V E R", common.BIG_FONT, 260, alliasing=True, colour=common.RED)
        self.draw_centered_text("Press space to return to main menu", common.SMALL_FONT, 400, alliasing=True, colour=common.RED)

        if self.game_state.game_result_type == common.GameResultType.WIN:
            self.draw_centered_text("W I N", common.BIG_FONT, 200, alliasing=True, colour=common.RED)

        if self.game_state.game_result_type == common.GameResultType.LOST:
            self.draw_centered_text("L O S T", common.BIG_FONT, 200, alliasing=True, colour=common.RED)

        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(common.MAX_FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE:
                        return True
