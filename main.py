import pygame
import os
import sys

WIDTH = 360
HEIGHT = 480
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hotline Uralsk")
clock = pygame.time.Clock()


gg_surf = load_image('гг спец 2 тест.png')
gg_rect = gg_surf.gg_rect(bottomright=(WIDTH, HEIGHT))
screen.blit(gg_surf, gg_rect)

pygame.display.update()


running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GREEN)
    pygame.display.flip()

pygame.quit()
