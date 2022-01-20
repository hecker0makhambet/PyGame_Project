import pygame
import os
import sys
import math
import random
WIDTH = 600
HEIGHT = 500
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
frame_changing_map = {'right': [0, 1, 2, -1], 'left': [-2, -1, 0, 1],
                      'up': [1, 2, -1, 0], 'down': [-1, 0, 1, 2]}
bullet_moving_map = {0: (1, 0), 1: (0.9, 0.1), 2: (0.8, 0.2), 3: (0.7, 0.3), 4: (0.55, 0.45),
                     5: (0.45, 0.55), 6: (0.4, 0.6), 7: (0.3, 0.7), 8: (0.2, 0.8), 9: (0, 1)}


def main_menu():
    main_menu_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(load_image('preview-image-1.png'), (0, 0))
    start = Button('main_menu_start_images', main_menu_sprites, (200, 200))
    setting = Button('main_menu_settings_images', main_menu_sprites, (200, 300))
    start_screen_running = True
    while start_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        main_menu_sprites.update()
        if start.clicked:
            return
        if setting.clicked:
            return
        main_menu_sprites.draw(screen)
        pygame.display.flip()


def settings():
    pass


def load_image(*name, colorkey=None):
    for i in name:
        if type(i) != str:
            name = list(name)
            colorkey = name.pop(name.index(i))
    fullname = os.path.join('data', *name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None or 'bullet-1.png' in name or 'player-image-1.png' in name:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        if 'bullet-1.png' in name or 'player-image-1.png' in name:
            colorkey = pygame.color.Color('white')
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def create_blood(pos, rect):
    for i in range(20):
        Blood(pos, random.choice(range(-5, 6)), random.choice(range(-5, 6)), rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, name, group, pos):
        super().__init__(group)
        self.image_list = Button.images[name]
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.clicked = False

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if any(pygame.mouse.get_pressed()):
                self.image = self.image_list[2]
                self.clicked = True
            else:
                self.image = self.image_list[1]
        else:
            self.image = self.image_list[0]


class Blood(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, rect):
        super().__init__(all_sprites)
        self.image = random.choice(Blood.images)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.rectangle = rect
        self.gravity = 0.5

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.rectangle):
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, x, y, *group):
        super().__init__(*group)
        self.image = Bullet.images[pos]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.moving_kx, self.moving_ky = bullet_moving_map[pos % 9]
        if pos // 9 % 2 != 0:
            self.moving_ky, self.moving_kx = self.moving_kx, self.moving_ky
        if 18 <= pos <= 36:
            self.moving_ky = -self.moving_ky
        if 9 <= pos <= 27:
            self.moving_kx = -self.moving_kx
        self.kill_value = False

    def update(self):
        if self.kill_value:
            self.kill()
        self.check_status()
        self.rect = self.rect.move(self.moving_kx * 20, self.moving_ky * 20)

    def check_status(self):
        if pygame.sprite.spritecollideany(self, enemy_sprites):
            self.kill_value = True
        if self.rect.x > screen.get_width() or self.rect.y > screen.get_height()\
                or self.rect.x < 0 or self.rect.y < 0:
            self.kill_value = True


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
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_kx = -1
                self.pos = [self.pos[0], 18]
                self.frame_changing = frame_changing_map[self.lastPressedKey][2]
                self.lastPressedKey = 'left'
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_kx = 1
                self.pos = [self.pos[0], 0]
                self.frame_changing = frame_changing_map[self.lastPressedKey][0]
                self.lastPressedKey = 'right'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moving_ky = 1
                self.pos = [self.pos[0], 9]
                self.frame_changing = frame_changing_map[self.lastPressedKey][1]
                self.lastPressedKey = 'down'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moving_ky = -1
                self.pos = [self.pos[0], 27]
                self.frame_changing = frame_changing_map[self.lastPressedKey][3]
                self.lastPressedKey = 'up'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_kx = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_kx = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moving_ky = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moving_ky = 0

    def moving_event(self, angle):
        self.pos[0] = round(angle / 10) % 36
        self.pos[1] = self.pos[0]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.kill_value = False

    def update(self):
        global enemy_die_time
        if self.kill_value:
            enemy_die_time += clock.tick()
            if self.image != Enemy.die_images[enemy_die_time % 4] and\
                    (enemy_die_time < 5 or enemy_die_time % 3 == 0):
                create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
            self.image = Enemy.die_images[enemy_die_time % 4]
            if enemy_die_time > 3:
                self.image = Enemy.die_images[-1]
            if enemy_die_time >= 20:
                self.kill()
            enemy_sprites.remove(self)
        self.check_status()

    def check_status(self):
        if pygame.sprite.spritecollideany(self, player_bullet_sprites):
            self.kill_value = True


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Шутер")
    clock = pygame.time.Clock()
    Button.images = images = {'main_menu_start_images': [load_image('start-1.png'),
                                                         load_image('start-2.png'),
                                                         load_image('start-3.png')],
                              'main_menu_settings_images': [pygame.transform.scale(load_image('settings-1.png'),
                                                                                   (233, 100))],
                              'main_menu_quit_images': [],
                              'settings_resume_images': [],
                              'settings_settings_images': [],
                              'settings_main_menu_images': [],
                              'settings_quit_images': []}
    main_menu()
    image = load_image('blood-1.png')
    Blood.images = [pygame.transform.scale(image, (i, i)) for i in (1, 2, 3)]
    image = load_image('player-image-1.png')
    Player.images = [pygame.transform.rotate(image, i) for i in range(360, 0, -10)]
    Player.die_images = [load_image('player-die-1.png', -1), load_image('player-die-2.png', -1),
                         load_image('player-die-3.png')]
    image = load_image('bullet-1.png')
    Bullet.images = [pygame.transform.rotate(image, i) for i in range(360, 0, -10)]
    Enemy.image = load_image('enemy-image-1.png')
    Enemy.die_images = [load_image('enemy-die-1.png'), load_image('enemy-die-2.png'),
                        load_image('enemy-die-3.png'), load_image('enemy-die-4.png')]
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    player_bullet_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()
    enemy = Enemy(all_sprites, enemy_sprites)
    player = Player(all_sprites)
    Bullet(5, 200, 200, all_sprites)
    running = True
    enemy_die_time = 0
    while running:
        screen.fill(BLUE)
        clock.tick(FPS)
        if player.pos[0] != player.pos[1]:
            player.pos[0] += player.frame_changing
            player.pos[0] %= 36
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.key_press_event(event)
            if event.type == pygame.KEYUP:
                player.key_press_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(player.pos[0], player.rect.x, player.rect.y, all_sprites, player_bullet_sprites)
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEWHEEL:
                pass
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()