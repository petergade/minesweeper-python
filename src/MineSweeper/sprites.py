import pygame
import common


class SpriteSheet:
    def __init__(self, image):
        self.image = image

    def one_image(self, x, y, w, h):
        image = pygame.Surface((w, h))
        image.blit(self.image, (0, 0), pygame.Rect(x, y, w, h))
        return image


class Brick(pygame.sprite.Sprite):
    def __init__(self, r, c, images):
        pygame.sprite.Sprite.__init__(self)
        self.r = r
        self.c = c
        self.images = images
        self.image = images[common.SpecialSquareValues.FOG]
        self.rect = self.image.get_rect()
        self.rect.x = c * common.SQ_SIZE
        self.rect.y = common.LOGO_HEIGHT + common.STATUS_BAR_HEIGHT + r * common.SQ_SIZE + common.STATUS_BAR_PADDINGTOP
        self.value = common.SpecialSquareValues.FOG

    def update(self) -> None:
        center = self.rect.center
        self.image = self.images[self.value]
        # print(self.value)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Emoji(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["emoji-happy"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_happy = True

    def update(self) -> None:
        center = self.rect.center
        self.image = self.images["emoji-happy"] if self.is_happy else self.images["emoji-sad"]
        # print(self.value)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, sprite_sheet: SpriteSheet):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = sprite_sheet
        self.image = self.sprite_sheet.one_image(0, 0, 64, 64)
        self.image.set_colorkey(common.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.delay = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now
            self.frame += 1
            if self.frame == 16:
                self.kill()
            else:
                center = self.rect.center
                x = (self.frame % 4) * 64
                y = (self.frame // 4) * 64
                self.image = self.sprite_sheet.one_image(x, y, 64, 64)
                self.image.set_colorkey(common.WHITE)
                self.rect.center = center


