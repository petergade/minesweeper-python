import pygame
from common import SpecialSquareValues


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images[SpecialSquareValues.FOG]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = SpecialSquareValues.FOG

    def update(self) -> None:
        center = self.rect.center
        self.image = self.images[self.value]
        self.rect = self.image.get_rect()
        self.rect.center = center


# TODO: sprite animace