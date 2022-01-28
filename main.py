import pygame
import os
import sys
import random
# Нужно сделать презентацию
# Нужно написать документацию
WIDTH = 600  # Ширина окна
HEIGHT = 500  # Высота окна
FPS = 30  # Количество кадров в секунду
WHITE = (255, 255, 255)  # Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
frame_changing_map = {'right': [0, 1, 2, -1], 'left': [-2, -1, 0, 1],
                      'up': [1, 2, -1, 0], 'down': [-1, 0, 1, 2]}  # Смена кадров
bullet_moving_map = {0: (1, 0), 1: (0.9, 0.1), 2: (0.8, 0.2), 3: (0.7, 0.3), 4: (0.55, 0.45),
                     5: (0.45, 0.55), 6: (0.4, 0.6), 7: (0.3, 0.7), 8: (0.2, 0.8), 9: (0, 1)}  # Движение пули по
# осям в зависимости от направления
bullet_pos = {0: (1, 0.5), 1: (0.9, 0.55), 2: (0.85, 0.6), 3: (0.8, 0.65), 4: (0.75, 0.7), 5: (0.7, 0.75),
              6: (0.65, 0.8), 7: (0.6, 0.9), 8: (0.5, 1), 9: (0.4, 0.9), 10: (0.35, 0.8), 11: (0.3, 0.75),
              12: (0.25, 0.7), 13: (0.2, 0.65), 14: (0.15, 0.6), 15: (0.1, 0.55), 16: (0.05, 0.6), 17: (0.1, 0.5),
              18: (1, 0.5), 19: (0.9, 0.55), 20: (0.85, 0.6), 21: (0.8, 0.65), 22: (0.75, 0.7), 23: (0.7, 0.75),
              24: (0.65, 0.8), 25: (0.6, 0.9), 26: (0.5, 1), 27: (0.5, 1), 28: (0.55, 0.9), 29: (0.6, 0.85),
              30: (0.65, 0.8), 31: (0.7, 0.75), 32: (0.75, 0.7), 33: (0.8, 0.6), 34: (0.85, 0.55), 35: (0.5, 1)}
pygame.init()  # Инициализация
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна
pygame.display.set_caption("Шутер")  # Установить название окна
clock = pygame.time.Clock()  # Инициализация таймера
all_sprites = pygame.sprite.Group()  # Группы спрайтов
enemy_sprites = pygame.sprite.Group()
player_bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()


def create_blood(pos, rect):  # функция создания крови
    for i in range(20):  # создать обьекты крови
        Blood(pos, random.choice(range(-5, 6)), random.choice(range(-5, 6)), rect)


def load_image(*name, colorkey=None):  # Функция загрузки изображения из файла
    for i in name:  # чтение аргументов
        if type(i) != str:  # если один из аргументов является colorkey-ем то удалить его из списка и
            # присвоить его значение
            name = list(name)
            colorkey = name.pop(name.index(i))
    fullname = os.path.join('data', 'images', *name)  # добавить аргументы в путь к файлу
    if not os.path.isfile(fullname):  # если такого файла не существует, закрыть программу
        print("Изображение не найдено")
        sys.exit()
    image = pygame.image.load(fullname)  # загрузить изображение
    if colorkey is not None or 'bullet-1.png' in name or 'player-image-1.png' in name:  # если цветовой ключ не пустой
        # или искомое изображение - изображение пули или игрока, то сделать прозрачным заданный цвет изображения
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        if 'bullet-1.png' in name or 'player-image-1.png' in name:
            colorkey = pygame.color.Color('white')
        image.set_colorkey(colorkey)
    else:  # иначе конвертировать прозрачность
        image = image.convert_alpha()
    return image


def find_moving_k(points):  # Функция, находящая направления движения по заданным точкам
    a = {0: [], 1: [], 2: [], 3: []}  # Пустой словарь
    for i, j in enumerate(points):
        if points[i][0] == points[(i + 1) % 4][0]:  # Если оси х совпадают
            if points[i][1] > points[(i + 1) % 4][1]:  # Движение вверх
                a[i] = (0, -1)
            else:  # Или вниз
                a[i] = (0, 1)
        if points[i][1] == points[(i + 1) % 4][1]:  # Если оси у совпадают
            if points[i][0] > points[(i + 1) % 4][0]:  # Движение влево
                a[i] = (-1, 0)
            else:  # Или в вправо
                a[i] = (1, 0)
    return a  # Возвращение результата


def load_level(level):  # Функция, загружающая уровень
    clear_sprites()  # Очистка всех спрайтов
    if level == 1:  # Загрузка первого уровня
        name = 'map-1.png'  # название изображения
        lev = open('data\\level1.txt', encoding='utf-8')  # открытие файла
    elif level == 2:  # Загрузка второго уровня
        name = 'map-2.png'  # название изображения
        lev = open('data\\level2.txt', encoding='utf-8')  # открытие файла
    else:  # Загрузка третьего уровня
        name = 'map-3.png'  # название изображения
        lev = open('data\\level3.txt', encoding='utf-8')  # открытие файла
    lev_info = lev.read().split('\n')  # чтение файла
    walls = [[int(j) for j in i.split()] for i in lev_info[0].split('|')]  # координаты стен
    player_pos = [int(i) for i in lev_info[1].split()]  # позиция игрока
    enemy_pos = [[j for j in i.split('|')] for i in lev_info[2:]]  # позиция врагов
    for i in walls:
        Walls(i, wall_sprites, all_sprites)  # создание стен
    image = pygame.transform.scale(load_image(name), (WIDTH, HEIGHT))  # загрузка изображения уровня
    game(image, player_pos, level, enemy_pos)  # загрузка игр


def clear_sprites():  # Очистка спрайтов
    all_sprites.empty()
    enemy_sprites.empty()
    player_bullet_sprites.empty()
    enemy_bullet_sprites.empty()
    player_sprites.empty()
    wall_sprites.empty()


def levels():  # окно выбора уровней
    opened_levels = open('data\\opened_levels.txt', mode='r', encoding='utf-8').read().split()[0]  # Загрузка прогресса
    global current_window
    screen.fill(BLUE)
    screen.blit(pygame.transform.scale(load_image('фон.png'), (WIDTH, 336)), (0, 0))  # Установить фон
    levels_sprites = pygame.sprite.Group()  # Группа спрайтов
    btn_1 = Button('levels_btn1', levels_sprites, (172, 200))  # Кнопки
    btn_2 = Button('levels_btn2', levels_sprites, (256, 200))
    btn_3 = Button('levels_btn3', levels_sprites, (352, 200))
    back_btn = Button('levels_back', levels_sprites, (10, 400))
    levels_running = True
    while levels_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выход из программы
                sys.exit()
            if event.type == pygame.KEYDOWN:  # При нажатии кнопки
                if event.key == pygame.K_ESCAPE:  # Выйти в главное меню
                    current_window = 'main_menu'
                    return
        if btn_1.clicked:  # Загрузка уровней
            load_level(1)
            return
        if btn_2.clicked:
            if int(opened_levels) >= 2:  # Если игрок прошел первый уровень
                load_level(2)
                return
            else:
                return
        if btn_3.clicked:
            if int(opened_levels) >= 3:  # Если игрок прошел предыдущие уровни
                load_level(3)
                return
            else:
                return
        if back_btn.clicked:  # Выход в главное меню
            current_window = 'main_menu'
            return
        levels_sprites.update()  # Обновление спрайтов
        levels_sprites.draw(screen)  # Рисовка спрайтов
        pygame.display.flip()  # Обновление окна


def game(image, pos, level, enemy_pos):  # Игра
    enemy_count = len(enemy_pos)  # количество врагов
    for i in enemy_pos:  # Разместить персонажи
        Enemy(i, level, all_sprites, enemy_sprites)
    player = Player(pos, all_sprites)  # Разместить спрайт игрока
    game_running = True
    while game_running:
        screen.fill(BLUE)
        screen.blit(image, (0, 0))  # изображение карты
        clock.tick(FPS)  # смена кадров в секунду
        player.pos[0] += player.frame_changing  # смена положения игрока
        player.pos[0] %= 36  # чтобы не вышло за предел списка
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из системы
                sys.exit()
            if event.type == pygame.KEYDOWN:  # При нажатии клавиатуры
                player.key_press_event(event)  # Передать событие в спрайт игрока
                if event.key == pygame.K_ESCAPE:  # Открыть паузу
                    if pause():  # Если в меню паузы игрок вышел в главное меню, завершить игру
                        return
            if event.type == pygame.KEYUP:  # При отпускании клавиатуры
                player.key_press_event(event)  # Передать событие в спрайт игрока
            if event.type == pygame.MOUSEBUTTONDOWN:  # При нажатии кнопки мыши
                player.shoot()  # Выстрел игрока
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEWHEEL:
                pass
        all_sprites.update()  # Обновление спрайт
        all_sprites.draw(screen)  # Нарисовать спрайты
        pygame.display.flip()  # Обновить окно
        score = enemy_count - len(enemy_sprites)  # Подсчет очков
        if player.kill_value and player.player_die_time > 10:  # Если игрок умер, и прошло определнное время
            game_over(score)  # Завершить игру
            return
        if len(enemy_sprites) == 0:  # Если все враги уничтожены, завершить игру
            you_win(score, level)
            return


def you_win(score, level):  # Победа игрока
    global current_window
    with open('data\\opened_levels.txt', mode='w', encoding='utf-8') as z:  # Открыть файл уровней
        print(str(level + 1), end='', file=z)
    if level < 3:  # При прохождении не последних уровней вывести окно you win
        image = pygame.transform.scale(load_image('you_win.png'), (WIDTH, HEIGHT))
    else:  # а при прохождении последнего вывести окно "вы прошли игру"
        image = pygame.transform.scale(load_image('конец.png'), (WIDTH, HEIGHT))
    screen.fill(BLUE)
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 35)
    text_score = font.render('SCORE:', True, (255, 0, 0))  # Вывести результаты игрока
    text_score_int = font.render(str(score), True, (255, 0, 0))
    you_win_running = True
    while you_win_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выйти из программы
                sys.exit()
            if event.type == pygame.KEYDOWN:  # При нажатии клавиатуры
                if event.key == pygame.K_SPACE:  # при нажатии клавишы ПРОБЕЛ закрыть вкладку
                    return
                if event.key == pygame.K_ESCAPE:  # при нажатии клавишы ESC закрыть окно и откырть главное меню
                    current_window = 'main_menu'
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:  # при нажатии мыши закрыть окно
                return
        screen.blit(text_score, (420, 30))  # Вывести количество очков
        screen.blit(text_score_int, (520, 30))
        pygame.display.flip()  # Обновить окно


def game_over(score):  # Поражение игрока
    global current_window
    screen.fill(BLUE)
    screen.blit(pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT)), (0, 0))  # загрузка изображения
    game_over_sprites = pygame.sprite.Group()  # группа спрайтов
    font = pygame.font.Font(None, 35)  # Текст результатов и сообщения
    text_score = font.render('SCORE:', True, (255, 0, 0))
    text_score_int = font.render(str(score), True, (255, 0, 0))
    text_restart = font.render('PRESS SPACE TO RESTART', True, (255, 0, 0))
    text_menu = font.render('PRESS ESC TO GO TO THE MAIN MENU', True, (255, 0, 0))
    game_over_running = True
    while game_over_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выйти из программы
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # При нажатии мыши закрыть вкладку
                return
            if event.type == pygame.KEYDOWN:  # При нажатии клавиатуры
                if event.key == pygame.K_ESCAPE:  # При нажатии клавишы ESC выйти в главное меню
                    current_window = 'main_menu'
                    return
                if event.key == pygame.K_SPACE:  # При нажатии клавишы ПРОБЕЛ закрыть окно
                    return
        game_over_sprites.draw(screen)  # нарисовать спрайты
        screen.blit(text_score, (125, 370))  # нарисовать результаты и сообщение
        screen.blit(text_score_int, (250, 370))
        screen.blit(text_restart, (120, 400))
        screen.blit(text_menu, (75, 430))
        pygame.display.flip()  # обновить окно


def main_menu():  # Главное меню
    global current_window
    screen.fill(BLUE)
    main_menu_sprites = pygame.sprite.Group()  # группа спрайтов
    screen.blit(pygame.transform.scale(load_image('preview-image-1.png'), (WIDTH, HEIGHT)), (0, 0))  # Загрузка
    # изображения
    start_btn = Button('main_menu_start', main_menu_sprites, (367, 200))  # Кнопки
    settings_btn = Button('main_menu_settings', main_menu_sprites, (367, 300))
    quit_btn = Button('main_menu_quit', main_menu_sprites, (367, 400))
    start_screen_running = True
    while start_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выйти из программы
                sys.exit()
        main_menu_sprites.update()  # обновление спрайтов
        if start_btn.clicked:  # При нажатии кнопки СТАРТ открыть вкладку уровней
            current_window = 'levels'
            return
        if settings_btn.clicked:  # При нажатии кнопки НАСТРОЙКИ открыть вкладку настройке
            settings()
            return
        if quit_btn.clicked:  # При нажатии кнопки ВЫХОД выйти из программы
            sys.exit()
        main_menu_sprites.draw(screen)  # Нарисовать спрайты
        main_menu_sprites.update()  # обновить спрайты
        pygame.display.flip()  # обновить окно


def settings():
    screen.fill(BLUE)
    settings_sprites = pygame.sprite.Group()  # группа спрайтов
    screen.blit(pygame.transform.scale(load_image('фон2.png'), (WIDTH, 338)), (0, 80))  # загрузить изображение
    settings_running = True
    delete_btn = Button('delete_progress', settings_sprites, (100, HEIGHT / 2))  # Кнопки
    back_btn = Button('levels_back', settings_sprites, (10, 400))
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выйти из программы
                sys.exit()
            if event.type == pygame.KEYDOWN:  # При нажатии клавиатуры
                if event.key == pygame.K_ESCAPE:  # При нажатии кнопки ESC закрыть вкладку
                    return
        if delete_btn.clicked:  # Если нажата кнопка удаления прогресса
            text = open('data\\opened_levels.txt', mode='w', encoding='utf-8')  # удалить прогресс
            print('1', end='', file=text)  # очистить файл
            text.close()  # закрыть файл
        if back_btn.clicked:  # если нажата кнопка НАЗАД, закрыть вкладку
            return
        settings_sprites.update()  # обновить спрайты
        settings_sprites.draw(screen)  # нарисовать спрайты
        pygame.display.flip()  # обновить окно


def pause():  # пауза
    global current_window
    screen.fill(BLUE)
    pause_sprites = pygame.sprite.Group()  # группа спрайтов
    screen.blit(pygame.transform.scale(load_image('фон3.png'), (WIDTH, HEIGHT)), (0, 0))  # загрузка изображения
    pause_running = True
    resume_btn = Button('pause_resume', pause_sprites, (367, 0))  # Кнопки
    settings_btn = Button('pause_settings', pause_sprites, (367, 110))
    menu_btn = Button('pause_main_menu', pause_sprites, (367, 210))
    quit_btn = Button('pause_quit', pause_sprites, (367, 310))
    while pause_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выйти из программы
                sys.exit()
            if event.type == pygame.KEYDOWN:  # При нажатии клавиатуры
                if event.key == pygame.K_ESCAPE:  # При нажатии кнопки ESC закрыть вкладку
                    return
        pause_sprites.update()  # обновить спрайты
        pause_sprites.draw(screen)  # нарисовать спрайты
        pygame.display.flip()  # обновить окно
        if resume_btn.clicked:  # если нажата кнопка ВОЗОБНОВИТЬ, закрыть вкладку
            return
        if settings_btn.clicked:  # при нажатии кнопки НАСТРОЙКИ, открыть вкладку настроек
            settings()
            settings_btn.clicked = False  # Снять флажок
            screen.fill(BLUE)  # залить все элементы предыдущей вкладки
            screen.blit(pygame.transform.scale(load_image('фон3.png'), (WIDTH, HEIGHT)), (0, 0))
            # загрузить изображение
        if menu_btn.clicked:  # при нажатии кнопки МЕНЮ открыть главное меню
            current_window = 'main_menu'
            return True  # возвращает Тrue
        if quit_btn.clicked:  # Выйти из программы
            sys.exit()


class Walls(pygame.sprite.Sprite):  # класс стены
    def __init__(self, rect, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('blood-1.png', -1), (rect[2], rect[3]))  # загрузка невидимого
        # изображения
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0], rect[1]  # размещение по переданным аргументам


class Button(pygame.sprite.Sprite):  # класс кнопок
    # все изображения
    images = {'main_menu_start': [load_image('start-1.png'),
                                  load_image('start-2.png')],
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
              'delete_progress': [pygame.transform.scale(load_image('delete1.png', -1), (400, 70)),
                                  pygame.transform.scale(load_image('delete2.png', -1), (400, 70))]
              }

    def __init__(self, name, group, pos):
        super().__init__(group)
        self.image_list = Button.images[name]  # выбор изображений по переданному названию
        self.image = self.image_list[0]  # установить изображения
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos  # разместить по переданным аргументам
        self.clicked = False  # флажок, нажата ли клавиша
        self.clicked_time = 0  # время пройденное после нажатия

    def update(self):
        if self.clicked_time > 0:  # если начался отсчет, продолжит его
            self.clicked_time += 1
        if self.clicked_time > 20:  # если прошло определенное количество времени, установить флажок, обнулить отсчет
            self.clicked = True
            self.clicked_time = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # если положение мыши находится на этой кнопке
            if any(pygame.mouse.get_pressed()):  # если мышь нажата, начать отсчет
                self.clicked_time = 1
            if len(self.image_list) != 1:  # если есть сменное изображение, сменить его
                self.image = self.image_list[1]
        else:  # иначе вернуть изображение
            self.image = self.image_list[0]


class Blood(pygame.sprite.Sprite):  # класс крови
    # загрузка изображений
    images = [pygame.transform.scale(load_image('blood-1.png'), (i, i)) for i in (1, 2, 3)]

    def __init__(self, pos, dx, dy, rect):
        super().__init__(all_sprites)
        self.image = random.choice(Blood.images)  # установка изображения
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]  # движение по осям по переданным аргументам
        self.rect.x, self.rect.y = pos  # координаты по переданным аргументам
        self.rectangle = rect  # прямоугольник(границы) за которые обьект не должен выходить
        self.gravity = 0.5  # гравитация

    def update(self):
        self.velocity[1] += self.gravity  # действие гравитации
        self.rect.x += self.velocity[0]  # движение по осям
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.rectangle):  # если за пределами границ, убрать спрайт
            self.kill()


class Bullet(pygame.sprite.Sprite):  # класс пули
    # загрузка изображении
    images = [pygame.transform.rotate(load_image('bullet-1.png'), i) for i in range(360, 0, -10)]

    def __init__(self, pos, x, y, *group):
        super().__init__(*group)
        self.image = Bullet.images[pos]  # выбор изображения по заданному положению
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 20, y + 15  # разместить по переданным аргументам
        self.moving_kx, self.moving_ky = bullet_moving_map[pos % 9]  # движение по заданному направлению
        if pos // 9 % 2 != 0:  # смена направления
            self.moving_ky, self.moving_kx = self.moving_kx, self.moving_ky
        if 18 <= pos <= 36:  # смена направления
            self.moving_ky = -self.moving_ky
        if 9 <= pos <= 27:  # смена направления
            self.moving_kx = -self.moving_kx
        self.kill_value = False  # флажок, попал ли обьект по цели, и следует ли его "убить"

    def update(self):
        if self.kill_value:  # если флажок активирован, убрать спрайт
            self.kill()
        self.rect = self.rect.move(self.moving_kx * 20, self.moving_ky * 20)  # движение
        self.check_status()  # проверка статуса

    def check_status(self):
        if (enemy_bullet_sprites in self.groups() and pygame.sprite.spritecollideany(self, player_sprites)) or \
                    (player_bullet_sprites in self.groups() and pygame.sprite.spritecollideany(self, enemy_sprites))\
                or (self.rect.x > screen.get_width() or self.rect.y > screen.get_height() or
                    self.rect.x < 0 or self.rect.y < 0):
            # Если пуля попала по цели или вышла за пределы окна, активировать флажок
            self.kill_value = True
        if pygame.sprite.spritecollideany(self, wall_sprites):  # Если пуля попала по стенке, убрать его
            self.kill()


class Player(pygame.sprite.Sprite):  # Класс игрока
    # Загрузка изображений
    images = [pygame.transform.rotate(load_image('player-image-1.png'), i) for i in range(360, 0, -10)]
    die_images = [load_image('player-die-1.png', -1), load_image('player-die-2.png', -1),
                  load_image('player-die-3.png')]

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Player.images[0]  # Установка изображения
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos  # Разместить по заданным координатам
        self.moving_kx, self.moving_ky = 0, 0  # движение по осям
        self.pos = [0, 0]  # индекс изображения игрока в списке
        self.frame_changing = 0  # смена индекса изображения
        self.kill_value = False  # флажок, умер ли игрок
        self.player_die_time = 0  # время после смерти

    def update(self):  # обновление
        if self.kill_value:  # если флажок активирован, вызвать функцию смерти
            self.die()
        else:  # Инача смена кадров и движение
            self.image = Player.images[self.pos[0]]  # смена изображения
            self.rect = self.rect.move(self.moving_kx * 5, self.moving_ky * 5)  # движение
            if pygame.sprite.spritecollideany(self, wall_sprites):  # если столкнулся со стенкой, то вернуть в
                # исходное положение
                self.rect = self.rect.move(-self.moving_kx * 5, -self.moving_ky * 5)
        self.check_status()  # проверка статуса

    def shoot(self):  # Функция выстрела
        if not self.kill_value:  # если игрок не умер, выстрелить
            Bullet(self.pos[0], self.rect.x, self.rect.y, all_sprites, player_bullet_sprites)

    def die(self):  # Функция смерти
        self.player_die_time += 0.05  # Время после смерти
        if self.image != self.die_images[int(self.player_die_time) % 3] and \
                (self.player_die_time < 5 or int(self.player_die_time) % 3 == 0):  # если прошло определенное время
            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()  # смена прямоугольника изображения и его координат
            self.rect.x, self.rect.y = x, y  # вернуть координаты в исходное значение
            create_blood((self.rect.x + 32, self.rect.y + 32), self.rect)  # создать кровь
        self.image = self.die_images[int(self.player_die_time) % 3]  # сменить изображения
        if self.player_die_time > 2:  # если прошло определенное время установить последнее изображение
            self.image = self.die_images[-1]
        if self.player_die_time >= 20:  # если прошло достаточное время, убрать спрайт
            self.kill()
        player_sprites.remove(self)  # убрать спрайт из группы спрайтов

    def check_status(self):  # проверка статуса
        if pygame.sprite.spritecollideany(self, enemy_bullet_sprites):  # если пуля попала по обьекту
            self.kill_value = True  # активировать флажок

    def key_press_event(self, event=None):  # функция обработки нажатий клавиатуры
        if event.type == pygame.KEYDOWN:  # если нажата клавиатура
            if not self.kill_value:  # если игрок не мертв
                if event.key == pygame.K_a:  # смена направления движения
                    self.moving_kx = -1
                if event.key == pygame.K_d:
                    self.moving_kx = 1
                if event.key == pygame.K_s:
                    self.moving_ky = 1
                if event.key == pygame.K_w:
                    self.moving_ky = -1
                if event.key == pygame.K_LEFT:  # смена направления поворота
                    self.frame_changing = -1
                if event.key == pygame.K_RIGHT:
                    self.frame_changing = 1
                if event.key == pygame.K_SPACE:  # выстрел
                    self.shoot()
        if event.type == pygame.KEYUP:  # если отпущена клавиатура
            if event.key == pygame.K_a:  # обнулить направление движения
                self.moving_kx = 0
            if event.key == pygame.K_d:
                self.moving_kx = 0
            if event.key == pygame.K_s:
                self.moving_ky = 0
            if event.key == pygame.K_w:
                self.moving_ky = 0
            if event.key in (pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT):  # обнулить направление
                # поворота
                self.frame_changing = 0


class Enemy(pygame.sprite.Sprite):  # класс врага
    # загрузка изображений
    images = [pygame.transform.rotate(load_image('enemy-image-1.png'), i) for i in range(360, 0, -10)]
    die_images = [load_image('enemy-die-1.png'), load_image('enemy-die-2.png'),
                  load_image('enemy-die-3.png'), load_image('enemy-die-4.png')]

    def __init__(self, pos, hurt_count, *group):
        super().__init__(*group)
        pos = [[int(j) for j in i.split()] for i in pos]  # позиции по которым обьект должен перемещаться
        self.positions = pos
        self.positions_num = 0  # нынешняя позиция
        self.moving_k = find_moving_k(pos)  # направление движения
        self.moving_kx, self.moving_ky = self.moving_k[self.positions_num]
        self.image = Enemy.images[0]  # установить изображение
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0][0], pos[0][1]  # разместить по заданным аргументам
        self.kill_value = False  # флажок, умер ли обьект
        self.enemy_die_time = 0  # время после смерти
        self.shoot_time = 0  # время после выстрела
        self.pos = [pos[0][2], pos[0][2]]  # нынешняя позиция поворота и точка назначения поворота
        self.frame_changing_k = 0  # направление поворота
        self.hurt_count = 0  # количество попаданий в обьекта
        self.hurt = False  # флажок, ранен ли обьект
        self.die_hurt_count = hurt_count  # сколько нужно ранить, чтобы убить

    def update(self):
        if self.kill_value:  # если флажок активирован вызвать функцию смерти
            self.die()
        else:  # Иначе движение и поворот
            if abs(self.pos[0] - self.pos[1]) < 36 - abs(self.pos[0] - self.pos[1]):
                if self.pos[0] > self.pos[1]:  # поворот против часовой
                    self.frame_changing_k = -1
                else:
                    self.frame_changing_k = 1  # или по часовой
            elif abs(self.pos[0] - self.pos[1]) > 36 - abs(self.pos[0] - self.pos[1]):
                if self.pos[0] > self.pos[1]:  # поворот по часовой
                    self.frame_changing_k = 1
                else:  # или против часовой
                    self.frame_changing_k = -1
            else:  # без поворота
                self.frame_changing_k = 0
            self.image = self.images[int(self.pos[0])]  # смена изображения
            self.rect = self.rect.move(self.moving_kx * 3, self.moving_ky * 3)  # движение обьекта
            if abs(self.rect.x - self.positions[(self.positions_num + 1) % 4][0]) < 3 and\
                    abs(self.rect.y - self.positions[(self.positions_num + 1) % 4][1]) < 3:  # если достиг определенной
                # точки, то сменить направление движения
                self.moving_kx, self.moving_ky = self.moving_k[(self.positions_num + 1) % 4]  # смена направления
                self.positions_num += 1  # смена позиции
                self.positions_num %= 4
                self.pos = [self.pos[1], self.positions[self.positions_num][2]]
            if self.pos[0] != self.pos[1]:  # поворот
                self.pos[0] += self.frame_changing_k
                if self.pos[0] < 0:
                    self.pos[0] += 36
                self.pos[0] %= 36
            self.shoot()  # выстрел
            self.check_status()  # проверка статуса

    def shoot(self):  # функция выстрела
        self.shoot_time += 0.4  # отсчет временни после выстрела
        if int(self.shoot_time) % 10 == 0:  # прошло определенное время, выстрелить
            self.shoot_time += 1
            Bullet(int(self.pos[0]), self.rect.x, self.rect.y, all_sprites, enemy_bullet_sprites)

    def die(self):  # функция смерти
        self.enemy_die_time += 0.1  # отсчет времени после смерти
        enemy_sprites.remove(self)  # удалить спрайт из группа
        if self.image != Enemy.die_images[int(self.enemy_die_time) % 4] and \
                (self.enemy_die_time < 5 or int(self.enemy_die_time % 3) == 0):  # если прошло определенное время
            # создать кровь
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
        self.image = Enemy.die_images[int(self.enemy_die_time) % 4]  # смена изображения
        if self.enemy_die_time > 3:  # если прошло какое-то время установить последнее изображение
            self.image = Enemy.die_images[-1]
        if self.enemy_die_time >= 20:  # если прошло достаточно времени, убрать спрайт
            self.kill()

    def check_status(self):  # проверка статуса
        if pygame.sprite.spritecollideany(self, player_bullet_sprites) and not self.hurt:  # если пуля попала по цели,
            # и это не та же пуля что в предыдущий раз, увеличить ранения и создать кровь
            self.hurt_count += 1
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
            create_blood((self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.rect)
            self.hurt = True  # активировать флажок ранения
        elif self.hurt_count == self.die_hurt_count:  # Если получено достаточно ранений, активировать флажок смерти
            self.kill_value = True
        else:  # снять флажок ранения
            self.hurt = False


if __name__ == '__main__':
    clear_sprites()  # очистить все спрайты
    running = True
    current_window = 'main_menu'  # текущая вкладка
    while running:
        if current_window == 'main_menu':  # если текущая вкладка - главное меню, открыть главное меню
            main_menu()
        if current_window == 'levels':  # иначе если текущая вкладка - уровни, открыть уровни
            levels()
