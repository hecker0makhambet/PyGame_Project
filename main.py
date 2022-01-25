import pygame
import os
import sys
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
bullet_pos = {0: (1, 0.5), 1: (0.9, 0.55), 2: (0.85, 0.6), 3: (0.8, 0.65), 4: (0.75, 0.7), 5: (0.7, 0.75),
              6: (0.65, 0.8), 7: (0.6, 0.9), 8: (0.5, 1), 9: (0.4, 0.9), 10: (0.35, 0.8), 11: (0.3, 0.75),
              12: (0.25, 0.7), 13: (0.2, 0.65), 14: (0.15, 0.6), 15: (0.1, 0.55), 16: (0.05, 0.6), 17: (0.1, 0.5),
              18: (1, 0.5), 19: (0.9, 0.55), 20: (0.85, 0.6), 21: (0.8, 0.65), 22: (0.75, 0.7), 23: (0.7, 0.75),
              24: (0.65, 0.8), 25: (0.6, 0.9), 26: (0.5, 1), 27: (0.5, 1), 28: (0.55, 0.9), 29: (0.6, 0.85),
              30: (0.65, 0.8), 31: (0.7, 0.75), 32: (0.75, 0.7), 33: (0.8, 0.6), 34: (0.85, 0.55), 35: (0.5, 1)}
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шутер")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()


def find_moving_k(points):
    a = {0: [], 1: [], 2: [], 3: []}
    for i, j in enumerate(points):
        if points[i][0] == points[(i + 1) % 4][0]:
            if points[i][1] > points[(i + 1) % 4][1]:
                a[i] = (0, -1)
            else:
                a[i] = (0, 1)
        if points[i][1] == points[(i + 1) % 4][1]:
            if points[i][0] > points[(i + 1) % 4][0]:
                a[i] = (-1, 0)
            else:
                a[i] = (1, 0)
    return a


def load_level(level):
    clear_sprites()
    if level == 1:
        name = 'map-1.png'
        lev = open('data\\level1.txt', encoding='utf-8')
    elif level == 2:
        name = 'map-2.png'
        lev = open('data\\level2.txt', encoding='utf-8')
    else:
        name = 'map-3.png'
        lev = open('data\\level3.txt', encoding='utf-8')
    lev_info = lev.read().split('\n')
    walls = [[int(j) for j in i.split()] for i in lev_info[0].split('|')]
    player_pos = [int(i) for i in lev_info[1].split()]
    enemy_pos = [[j for j in i.split('|')] for i in lev_info[2:]]
    for i in walls:
        Walls(i, wall_sprites, all_sprites)
    image = pygame.transform.scale(load_image(name), (WIDTH, HEIGHT))
    generate_level(image, player_pos, level, enemy_pos)


def generate_level(image, pos, level, enemy_pos):
    screen.blit(image, (0, 0))
    game(image, pos, level, enemy_pos)


def clear_sprites():
    all_sprites.empty()
    enemy_sprites.empty()
    player_bullet_sprites.empty()
    enemy_bullet_sprites.empty()
    player_sprites.empty()
    wall_sprites.empty()


def levels():
    opened_levels = open('data\\opened_levels.txt', mode='r', encoding='utf-8').read().split()[0]
    global current_window
    screen.fill(BLUE)
    levels_sprites = pygame.sprite.Group()
    btn_1 = Button('levels_btn1', levels_sprites, (172, 200))
    btn_2 = Button('levels_btn2', levels_sprites, (256, 200))
    btn_3 = Button('levels_btn3', levels_sprites, (352, 200))
    back_btn = Button('levels_back', levels_sprites, (10, 400))
    levels_running = True
    while levels_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_window = 'main_menu'
                    return
        if btn_1.clicked:
            load_level(1)
            return
        if btn_2.clicked:
            if int(opened_levels) >= 2:
                load_level(2)
                return
            else:
                return
        if btn_3.clicked:
            if int(opened_levels) >= 3:
                load_level(3)
                return
            else:
                return
        if back_btn.clicked:
            current_window = 'main_menu'
            return
        levels_sprites.update()
        levels_sprites.draw(screen)
        pygame.display.flip()


def game(image, pos, level, enemy_pos):
    enemy_count = len(enemy_pos)
    for i in enemy_pos:
        Enemy(i, level, all_sprites, enemy_sprites)
    player = Player(pos, all_sprites)
    game_running = True
    while game_running:
        screen.fill(BLUE)
        screen.blit(image, (0, 0))
        clock.tick(FPS)
        player.pos[0] += player.frame_changing
        player.pos[0] %= 36
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player.key_press_event(event)
                if event.key == pygame.K_ESCAPE:
                    if pause():
                        return
            if event.type == pygame.KEYUP:
                player.key_press_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEWHEEL:
                pass
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        score = enemy_count - len(enemy_sprites)
        if player.kill_value and player.player_die_time > 10:
            game_over(score)
            return
        if len(enemy_sprites) == 0:
            you_win(score, level)
            return


def you_win(score, level):
    global current_window
    with open('data\\opened_levels.txt', mode='w', encoding='utf-8') as z:
        print(str(level + 1), end='', file=z)
    image = pygame.transform.scale(load_image('you_win.png'), (WIDTH, HEIGHT))
    screen.fill(BLUE)
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 35)
    text_score = font.render('SCORE:', True, (255, 0, 0))
    text_score_int = font.render(str(score), True, (255, 0, 0))
    you_win_running = True
    while you_win_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    current_window = 'main_menu'
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.blit(text_score, (420, 30))
        screen.blit(text_score_int, (520, 30))
        pygame.display.flip()


def game_over(score):
    global current_window
    screen.fill(BLUE)
    screen.blit(pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT)), (0, 0))
    game_over_sprites = pygame.sprite.Group()
    font = pygame.font.Font(None, 35)
    text_score = font.render('SCORE:', True, (255, 0, 0))
    text_score_int = font.render(str(score), True, (255, 0, 0))
    text_restart = font.render('PRESS SPACE TO RESTART', True, (255, 0, 0))
    text_menu = font.render('PRESS ESC TO GO TO THE MAIN MENU', True, (255, 0, 0))
    game_over_running = True
    while game_over_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_window = 'main_menu'
                    return
                if event.key == pygame.K_SPACE:
                    return
        game_over_sprites.draw(screen)
        screen.blit(text_score, (125, 370))
        screen.blit(text_score_int, (250, 370))
        screen.blit(text_restart, (120, 400))
        screen.blit(text_menu, (75, 430))
        pygame.display.flip()


def main_menu():
    global current_window
    screen.fill(BLUE)
    main_menu_sprites = pygame.sprite.Group()
    screen.blit(load_image('preview-image-1.png'), (0, 0))
    start_btn = Button('main_menu_start', main_menu_sprites, (200, 100))
    settings_btn = Button('main_menu_settings', main_menu_sprites, (200, 200))
    quit_btn = Button('main_menu_quit', main_menu_sprites, (200, 300))
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
        if start_btn.clicked:
            current_window = 'levels'
            return
        if settings_btn.clicked:
            settings()
            return
        if quit_btn.clicked:
            sys.exit()
        main_menu_sprites.draw(screen)
        pygame.display.flip()


def settings():
    screen.fill(BLUE)
    settings_sprites = pygame.sprite.Group()
    settings_running = True
    delete_btn = Button('delete_progress', settings_sprites, (100, HEIGHT / 2))
    back_btn = Button('levels_back', settings_sprites, (10, 400))
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        if delete_btn.clicked:
            text = open('data\\opened_levels.txt', mode='w', encoding='utf-8')
            print('1', end='', file=text)
            text.close()
        if back_btn.clicked:
            return
        settings_sprites.update()
        settings_sprites.draw(screen)
        pygame.display.flip()


def pause():
    global current_window
    screen.fill(BLUE)
    pause_sprites = pygame.sprite.Group()
    pause_running = True
    resume_btn = Button('pause_resume', pause_sprites, (200, 0))
    settings_btn = Button('pause_settings', pause_sprites, (200, 110))
    menu_btn = Button('pause_main_menu', pause_sprites, (200, 210))
    quit_btn = Button('pause_quit', pause_sprites, (200, 310))
    while pause_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_running = False
        pause_sprites.update()
        pause_sprites.draw(screen)
        pygame.display.flip()
        if resume_btn.clicked:
            return
        if settings_btn.clicked:
            settings()
        if menu_btn.clicked:
            current_window = 'main_menu'
            return True
        if quit_btn.clicked:
            sys.exit()


def load_image(*name, colorkey=None):
    for i in name:
        if type(i) != str:
            name = list(name)
            colorkey = name.pop(name.index(i))
    fullname = os.path.join('data', 'images', *name)
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


class Walls(pygame.sprite.Sprite):
    def __init__(self, rect, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('blood-1.png', -1), (rect[2], rect[3]))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0], rect[1]


class Button(pygame.sprite.Sprite):
    images = {'main_menu_start': [load_image('start-1.png'),
                                  load_image('start-2.png'),
                                  load_image('start-3.png')],
              'main_menu_settings': [pygame.transform.scale(load_image('settings-1.png'), (233, 100)),
                                     pygame.transform.scale(load_image('settings-2.png', -1), (233, 100))],
              'main_menu_quit': [pygame.transform.scale(load_image('quit-1.png', -1), (233, 100)),
                                 pygame.transform.scale(load_image('quit-2.png', -1), (233, 100))],
              'pause_resume': [pygame.transform.scale(load_image('resume-1.png', -1), (233, 100)),
                               pygame.transform.scale(load_image('resume-2.png', -1), (233, 100))],
              'pause_settings': [pygame.transform.scale(load_image('settings-1.png'), (233, 100)),
                                 pygame.transform.scale(load_image('settings-2.png', -1), (233, 100))],
              'pause_main_menu': [pygame.transform.scale(load_image('menu-1.png', -1), (233, 100)),
                                  pygame.transform.scale(load_image('menu-2.png', -1), (233, 100))],
              'pause_quit': [pygame.transform.scale(load_image('quit-1.png', -1), (233, 100)),
                             pygame.transform.scale(load_image('quit-2.png', -1), (233, 100))],
              'levels_btn1': [pygame.transform.scale(load_image('btn-1-1.png', -1), (64, 64)),
                              pygame.transform.scale(load_image('btn-1-2.png', -1), (64, 64))],
              'levels_btn2': [pygame.transform.scale(load_image('btn-2-1.png', -1), (64, 64)),
                              pygame.transform.scale(load_image('btn-2-2.png', -1), (64, 64))],
              'levels_btn3': [pygame.transform.scale(load_image('btn-3-1.png', -1), (64, 64)),
                              pygame.transform.scale(load_image('btn-3-2.png', -1), (64, 64))],
              'levels_back': [pygame.transform.scale(load_image('back-1.png', -1), (128, 64)),
                              pygame.transform.scale(load_image('back-2.png', -1), (128, 64))],
              'delete_progress': [pygame.transform.scale(load_image('delete-progress.png', -1), (400, 70))]
              }

    def __init__(self, name, group, pos):
        super().__init__(group)
        self.image_list = Button.images[name]
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.clicked = False
        self.clicked_time = 0

    def update(self):
        if self.clicked_time > 0:
            self.clicked_time += 1
        if self.clicked_time > 20:
            self.clicked = True
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if any(pygame.mouse.get_pressed()):
                self.clicked_time = 1
            if len(self.image_list) != 1:
                self.image = self.image_list[1]
        else:
            self.image = self.image_list[0]


class Blood(pygame.sprite.Sprite):
    images = [pygame.transform.scale(load_image('blood-1.png'), (i, i)) for i in (1, 2, 3)]

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
    images = [pygame.transform.rotate(load_image('bullet-1.png'), i) for i in range(360, 0, -10)]

    def __init__(self, pos, x, y, *group):
        super().__init__(*group)
        self.image = Bullet.images[pos]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 20, y + 15
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
        if enemy_bullet_sprites in self.groups() and pygame.sprite.spritecollideany(self, player_sprites):
            self.kill_value = True
        if player_bullet_sprites in self.groups() and pygame.sprite.spritecollideany(self, enemy_sprites):
            self.kill_value = True
        if pygame.sprite.spritecollideany(self, wall_sprites):
            self.kill()
        if self.rect.x > screen.get_width() or self.rect.y > screen.get_height()\
                or self.rect.x < 0 or self.rect.y < 0:
            self.kill_value = True


class Player(pygame.sprite.Sprite):
    images = [pygame.transform.rotate(load_image('player-image-1.png'), i) for i in range(360, 0, -10)]
    die_images = [load_image('player-die-1.png', -1), load_image('player-die-2.png', -1),
                  load_image('player-die-3.png')]

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Player.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.moving_kx, self.moving_ky = 0, 0
        self.pos = [0, 0]
        self.frame_changing = 0
        self.lastPressedKey = 'right'
        self.kill_value = False
        self.player_die_time = 0
        self.score = 0

    def update(self):
        if self.kill_value:
            self.die()
        else:
            self.image = Player.images[self.pos[0]]
            self.rect = self.rect.move(self.moving_kx * 5, self.moving_ky * 5)
            if pygame.sprite.spritecollideany(self, wall_sprites):
                self.rect = self.rect.move(-self.moving_kx * 5, -self.moving_ky * 5)
        self.check_status()

    def shoot(self):
        if not self.kill_value:
            Bullet(self.pos[0], self.rect.x, self.rect.y, all_sprites, player_bullet_sprites)

    def die(self):
        self.player_die_time += 0.05
        if self.image != self.die_images[int(self.player_die_time) % 3] and \
                (self.player_die_time < 5 or int(self.player_die_time) % 3 == 0):
            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            create_blood((self.rect.x + 32, self.rect.y + 32), self.rect)
        self.image = self.die_images[int(self.player_die_time) % 3]
        if self.player_die_time > 2:
            self.image = self.die_images[-1]
        if self.player_die_time >= 20:
            self.kill()
        player_sprites.remove(self)

    def check_status(self):
        if pygame.sprite.spritecollideany(self, enemy_bullet_sprites):
            self.kill_value = True

    def key_press_event(self, event=None):
        if event.type == pygame.KEYDOWN:
            if not self.kill_value:
                if event.key == pygame.K_a:
                    self.moving_kx = -1
                if event.key == pygame.K_d:
                    self.moving_kx = 1
                if event.key == pygame.K_s:
                    self.moving_ky = 1
                if event.key == pygame.K_w:
                    self.moving_ky = -1
                if event.key == pygame.K_LEFT:
                    self.frame_changing = -1
                    self.lastPressedKey = 'left'
                if event.key == pygame.K_RIGHT:
                    self.frame_changing = 1
                    self.lastPressedKey = 'right'
                if event.key == pygame.K_SPACE:
                    self.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.moving_kx = 0
            if event.key == pygame.K_d:
                self.moving_kx = 0
            if event.key == pygame.K_s:
                self.moving_ky = 0
            if event.key == pygame.K_w:
                self.moving_ky = 0
            if event.key in (pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT):
                self.frame_changing = 0


class Enemy(pygame.sprite.Sprite):
    images = [pygame.transform.rotate(load_image('enemy-image-1.png'), i) for i in range(360, 0, -10)]
    die_images = [load_image('enemy-die-1.png'), load_image('enemy-die-2.png'),
                  load_image('enemy-die-3.png'), load_image('enemy-die-4.png')]

    def __init__(self, pos, hurt_count, *group):
        super().__init__(*group)
        pos = [[int(j) for j in i.split()] for i in pos]
        self.positions = pos
        self.positions_num = 0
        self.moving_k = find_moving_k(pos)
        self.moving_kx, self.moving_ky = self.moving_k[self.positions_num]
        self.image = Enemy.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0][0], pos[0][1]
        self.kill_value = False
        self.enemy_die_time = 0
        self.shoot_time = 0
        self.pos = [pos[0][2], pos[0][2]]
        self.frame_changing_k = 0
        self.hurt_count = 0
        self.hurt = False
        self.die_hurt_count = hurt_count

    def update(self):
        if self.kill_value:
            self.die()
        else:
            if abs(self.pos[0] - self.pos[1]) < 36 - abs(self.pos[0] - self.pos[1]):
                if self.pos[0] > self.pos[1]:
                    self.frame_changing_k = -1
                else:
                    self.frame_changing_k = 1
            elif abs(self.pos[0] - self.pos[1]) > 36 - abs(self.pos[0] - self.pos[1]):
                if self.pos[0] > self.pos[1]:
                    self.frame_changing_k = 1
                else:
                    self.frame_changing_k = -1
            else:
                self.frame_changing_k = 0
            self.image = self.images[int(self.pos[0])]
            self.rect = self.rect.move(self.moving_kx * 3, self.moving_ky * 3)
            if abs(self.rect.x - self.positions[(self.positions_num + 1) % 4][0]) < 3 and\
                    abs(self.rect.y - self.positions[(self.positions_num + 1) % 4][1]) < 3:
                self.moving_kx, self.moving_ky = self.moving_k[(self.positions_num + 1) % 4]
                self.positions_num += 1
                self.positions_num %= 4
                self.pos = [self.pos[1], self.positions[self.positions_num][2]]
            if self.pos[0] != self.pos[1]:
                self.pos[0] += self.frame_changing_k
                if self.pos[0] < 0:
                    self.pos[0] += 36
                self.pos[0] %= 36
            self.shoot()
            self.check_status()

    def shoot(self):
        self.shoot_time += 0.4
        if int(self.shoot_time) % 10 == 0:
            self.shoot_time += 1
            Bullet(int(self.pos[0]), self.rect.x, self.rect.y, all_sprites, enemy_bullet_sprites)

    def die(self):
        self.enemy_die_time += 0.1
        enemy_sprites.remove(self)
        if self.image != Enemy.die_images[int(self.enemy_die_time) % 4] and \
                (self.enemy_die_time < 5 or int(self.enemy_die_time % 3) == 0):
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
        self.image = Enemy.die_images[int(self.enemy_die_time) % 4]
        if self.enemy_die_time > 3:
            self.image = Enemy.die_images[-1]
        if self.enemy_die_time >= 20:
            self.kill()

    def check_status(self):
        if pygame.sprite.spritecollideany(self, player_bullet_sprites) and not self.hurt:
            self.hurt_count += 1
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
            self.hurt = True
        elif self.hurt_count == self.die_hurt_count:
            self.kill_value = True
        else:
            self.hurt = False


if __name__ == '__main__':
    clear_sprites()
    running = True
    current_window = 'main_menu'
    while running:
        if current_window == 'main_menu':
            main_menu()
        if current_window == 'levels':
            levels()
