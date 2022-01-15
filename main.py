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


def load_image(name):
    fullname = os.path.join('sprait', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert()
    image.set_colorkey(image.get_at((0, 0)))
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hotline Uralsk")
    clock = pygame.time.Clock()
    image = load_image('player_image_1.png')
    Player.image = image
    all_sprites = pygame.sprite.Group()
    a = Player(all_sprites)
    running = True
    screen.fill(GREEN)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()