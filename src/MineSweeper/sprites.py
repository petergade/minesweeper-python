import pygame
import common


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

# TODO: sprite animace