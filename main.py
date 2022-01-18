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
frame_changing_map = {'right': [0, 1, 2, -1], 'left': [-2, -1, 0, 1],
                      'up': [1, 2, -1, 0], 'down': [-1, 0, 1, 2]}
bullet_moving_map = {0: (1, 0), 1: (0.9, 0.1), 2: (0.8, 0.2), 3: (0.7, 0.3), 4: (0.6, 0.4),
                     5: (0.5, 0.5), 6: (0.4, 0.6), 7: (0.3, 0.7), 8: (0.2, 0.8), 9: (0.1, 0.9),
                     10: (0, 1)}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        if 'bullet' in name:
            colorkey = pygame.color.Color('white')
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, x, y, *group):
        super().__init__(group)
        self.image = Bullet.images[(pos - 30) % 40]
        if pos == 30:
            self.image = Bullet.images[39]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.moving_kx, self.moving_ky = bullet_moving_map[pos % 10]
        if pos % 10 == 0 and pos // 10 % 2 != 0:
            self.moving_kx, self.moving_ky = bullet_moving_map[10]
        if 20 < pos < 40:
            self.moving_ky = -self.moving_ky
        if 10 < pos < 30:
            self.moving_kx = -self.moving_kx

    def update(self):
        self.rect = self.rect.move(self.moving_kx * 10, self.moving_ky * 10)


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.moving_kx, self.moving_ky = 0, 0
        self.pos = [0, 0]
        self.frame_changing = 0
        self.lastPressedKey = 'right'

    def update(self):
        self.image = Player.images[self.pos[0]]
        self.rect = self.rect.move(self.moving_kx * 5, self.moving_ky * 5)

    def key_press_event(self, event=None):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_kx = -1
                self.pos = [self.pos[0], 20]
                self.frame_changing = frame_changing_map[self.lastPressedKey][2]
                self.lastPressedKey = 'left'
            if event.key == pygame.K_RIGHT:
                self.moving_kx = 1
                self.pos = [self.pos[0], 0]
                self.frame_changing = frame_changing_map[self.lastPressedKey][0]
                self.lastPressedKey = 'right'
            if event.key == pygame.K_DOWN:
                self.moving_ky = 1
                self.pos = [self.pos[0], 10]
                self.frame_changing = frame_changing_map[self.lastPressedKey][1]
                self.lastPressedKey = 'down'
            if event.key == pygame.K_UP:
                self.moving_ky = -1
                self.pos = [self.pos[0], 30]
                self.frame_changing = frame_changing_map[self.lastPressedKey][3]
                self.lastPressedKey = 'up'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_kx = 0
            if event.key == pygame.K_RIGHT:
                self.moving_kx = 0
            if event.key == pygame.K_DOWN:
                self.moving_ky = 0
            if event.key == pygame.K_UP:
                self.moving_ky = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Шутер")
    clock = pygame.time.Clock()
    Player.images = [load_image('player-image-1.png'), load_image('player-image-2.png'),
                     load_image('player-image-3.png'), load_image('player-image-4.png'),
                     load_image('player-image-5.png'), load_image('player-image-6.png'),
                     load_image('player-image-7.png'), load_image('player-image-8.png'),
                     load_image('player-image-9.png'), load_image('player-image-10.png')]
    Player.images += [pygame.transform.flip(Player.images[9], True, False),
                      pygame.transform.flip(Player.images[8], True, False),
                      pygame.transform.flip(Player.images[7], True, False),
                      pygame.transform.flip(Player.images[6], True, False),
                      pygame.transform.flip(Player.images[5], True, False),
                      pygame.transform.flip(Player.images[4], True, False),
                      pygame.transform.flip(Player.images[3], True, False),
                      pygame.transform.flip(Player.images[2], True, False),
                      pygame.transform.flip(Player.images[1], True, False),
                      pygame.transform.flip(Player.images[0], True, False),
                      pygame.transform.flip(Player.images[0], True, True),
                      pygame.transform.flip(Player.images[1], True, True),
                      pygame.transform.flip(Player.images[2], True, True),
                      pygame.transform.flip(Player.images[3], True, True),
                      pygame.transform.flip(Player.images[4], True, True),
                      pygame.transform.flip(Player.images[5], True, True),
                      pygame.transform.flip(Player.images[6], True, True),
                      pygame.transform.flip(Player.images[7], True, True),
                      pygame.transform.flip(Player.images[8], True, True),
                      pygame.transform.flip(Player.images[9], True, True),
                      pygame.transform.flip(Player.images[9], False, True),
                      pygame.transform.flip(Player.images[8], False, True),
                      pygame.transform.flip(Player.images[7], False, True),
                      pygame.transform.flip(Player.images[6], False, True),
                      pygame.transform.flip(Player.images[5], False, True),
                      pygame.transform.flip(Player.images[4], False, True),
                      pygame.transform.flip(Player.images[3], False, True),
                      pygame.transform.flip(Player.images[2], False, True),
                      pygame.transform.flip(Player.images[1], False, True),
                      pygame.transform.flip(Player.images[0], False, True)]
    Bullet.images = [load_image('bullet-10.png', -1), load_image('bullet-9.png', -1),
                     load_image('bullet-8.png', -1), load_image('bullet-7.png', -1),
                     load_image('bullet-6.png', -1), load_image('bullet-5.png', -1),
                     load_image('bullet-4.png', -1), load_image('bullet-3.png', -1),
                     load_image('bullet-2.png', -1), load_image('bullet-1.png', -1)]
    Bullet.images += [pygame.transform.flip(Bullet.images[0], False, True),
                      pygame.transform.flip(Bullet.images[1], False, True),
                      pygame.transform.flip(Bullet.images[2], False, True),
                      pygame.transform.flip(Bullet.images[3], False, True),
                      pygame.transform.flip(Bullet.images[4], False, True),
                      pygame.transform.flip(Bullet.images[5], False, True),
                      pygame.transform.flip(Bullet.images[6], False, True),
                      pygame.transform.flip(Bullet.images[7], False, True),
                      pygame.transform.flip(Bullet.images[8], False, True),
                      pygame.transform.flip(Bullet.images[9], False, True),
                      pygame.transform.flip(Bullet.images[9], True, True),
                      pygame.transform.flip(Bullet.images[8], True, True),
                      pygame.transform.flip(Bullet.images[7], True, True),
                      pygame.transform.flip(Bullet.images[6], True, True),
                      pygame.transform.flip(Bullet.images[5], True, True),
                      pygame.transform.flip(Bullet.images[4], True, True),
                      pygame.transform.flip(Bullet.images[3], True, True),
                      pygame.transform.flip(Bullet.images[2], True, True),
                      pygame.transform.flip(Bullet.images[1], True, True),
                      pygame.transform.flip(Bullet.images[0], True, True),
                      pygame.transform.flip(Bullet.images[0], True, False),
                      pygame.transform.flip(Bullet.images[1], True, False),
                      pygame.transform.flip(Bullet.images[2], True, False),
                      pygame.transform.flip(Bullet.images[3], True, False),
                      pygame.transform.flip(Bullet.images[4], True, False),
                      pygame.transform.flip(Bullet.images[5], True, False),
                      pygame.transform.flip(Bullet.images[6], True, False),
                      pygame.transform.flip(Bullet.images[7], True, False),
                      pygame.transform.flip(Bullet.images[8], True, False),
                      pygame.transform.flip(Bullet.images[9], True, False)]
    Enemy.image = load_image('enemy-image-1.png')
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    player = Player(all_sprites)
    Bullet(5, 200, 200, all_sprites)
    enemy = Enemy(enemy_sprites, all_sprites)
    running = True
    while running:
        screen.fill(WHITE)
        clock.tick(FPS)
        if player.pos[0] != player.pos[1]:
            player.pos[0] += player.frame_changing
            player.pos[0] %= 40
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.key_press_event(event)
            if event.type == pygame.KEYUP:
                player.key_press_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(player.pos[0], player.rect.x, player.rect.y, all_sprites)
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEWHEEL:
                pass
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()