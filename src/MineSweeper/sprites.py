import pygame
from common import SpecialSquareValues, SQ_SIZE


class Brick(pygame.sprite.Sprite):
    def __init__(self, r, c, images):
        pygame.sprite.Sprite.__init__(self)
        self.r = r
        self.c = c
        self.images = images
        self.image = images[SpecialSquareValues.FOG]
        self.rect = self.image.get_rect()
        self.rect.x = r * SQ_SIZE
        self.rect.y = c * SQ_SIZE
        self.value = SpecialSquareValues.FOG

    def update(self) -> None:
        center = self.rect.center
        self.image = self.images[self.value]
        print(self.value)
        self.rect = self.image.get_rect()
        self.rect.center = center


# TODO: sprite animace