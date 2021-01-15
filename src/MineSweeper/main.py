import pygame
import sys
import random
import gamestate

WIDTH = HEIGHT = 800
MAX_FPS = 30

# barvy
BLACK = pygame.Color("white")
WHITE = pygame.Color("black")
RED = pygame.Color("red")

pygame.init()
pygame.mixer.init()

# nacteni grafiky, hudby, zvuku



# definice spritu
my_sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pycheckers")
clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.draw.rect(screen, pygame.Color("black"), (50, 50, 100, 50), 2)

while True:
    # kontrola FPS
    clock.tick(MAX_FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # update

    # render
    pygame.display.flip()



