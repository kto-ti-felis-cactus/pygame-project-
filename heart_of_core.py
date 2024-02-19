import pygame
import math
import random
import bullets_code
import animation
import ai
import NPCWork
import player as player_file_code


def rotate_player():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x = mouse_x - (15 * cells.cell_size + cells.left)
    rel_y = mouse_y - (4 * cells.cell_size + cells.top)
    angle = math.degrees(-math.atan2(rel_y, rel_x))
    return angle


def rotate_object(target, self_object):
    if target == 'player':
        result_x = (15 * cells.cell_size + cells.left) - ((map_pos[0] * cells.cell_size +
                                                           cells.left * self_object.position[0]))
        result_y = (4 * cells.cell_size + cells.top) - ((map_pos[1] * cells.cell_size +
                                                         cells.left * (self_object.position[1] + 4)))
    else:
        target_object = f'ai.{target}'
        x, y = eval(target_object).position
        result_x = (map_pos[0] * cells.cell_size + cells.left * x) - (map_pos[0] * cells.cell_size +
                                                                      cells.left * self_object.position[0])
        result_y = (map_pos[1] * cells.cell_size + cells.left * y) - (map_pos[1] * cells.cell_size +
                                                                      cells.left * (self_object.position[1] + 4))
    self_angle = math.degrees(-math.atan2(result_y, result_x))
    return self_angle


def create_player_data(player_name):
    file = open(fr'player_stats\players_data.txt', 'r')
    file_data = file.readlines()
    file.close()
    if player_name not in file_data:
        file = open(fr'player_stats\{player_name}.txt', 'w')
        file.write(f'''name--{player_name}
weapon_in_inventory--5
health--10
location--1
complexity_tick--25
complexity--1
very_important_number--{random.randint(1, 5)}
stats--0''')
        file.close()

        file_data.append(player_name)
        file = open(fr'player_stats\players_data.txt', 'w')
        file.write('\n'.join(file_data))
        file.close()
        return 1
    else:
        return 0


def read_player_data():
    file = open(fr'player_stats\players_data.txt', 'r', encoding='utf-8')
    file_data = file.read().split('\n')
    file.close()
    return file_data


def load_map(map_name):
    file = open(f'{map_name}.txt', 'r', encoding='utf-8')
    data = file.read().split('-</>-\n')
    data[1] = data[1].split('\n')
    for i in range(len(data[1])):
        data[1][i] = data[1][i].split(',')
    file.close()
    return data


def edit_map_entities(map_entities):
    return_map = []
    for i in map_entities:
        i = i.split()
        i[0] = i[0].split('(')
        if i[0][0] != 'player':
            i[0] = f'ai.{i[0][0]} = ai.{i[0][1]}('
        else:
            i[0] = i[0][0]
        i = ', '.join(i)
        i = i.replace('(, ', '(')
        return_map.append(i)
    return return_map


def get_form_size():
    width, height = pygame.display.get_surface().get_size()
    return [width, height]


def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Cells:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.list_cells_image_id = []
        self.left = 10
        self.top = 10
        self.cell_size = 30
        form_size = get_form_size()

        self.fullscreen_btn = pygame.Rect(form_size[0] - 150, form_size[1] - 150, 150, 150)
        self.game_screen = pygame.Rect(0, 0, form_size[0], form_size[1] / 5 * 4)
        self.create_map()

    def create_map(self):
        self.data_map = load_map(1)
        self.map = self.data_map[1]
        self.board = []
        for i in self.map:
            self.list_cells_image_id.append([])

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if list(self.map[y][x])[0] == '0':
                    self.list_cells_image_id[y].append('0')
                elif list(self.map[y][x])[0] == '1':
                    self.list_cells_image_id[y].append(load_image(f'hell_rock_{random.randint(0, 3)}.png'))
                elif list(self.map[y][x])[0] == '2':
                    self.board.append([x - 11, y - 4])
                    self.list_cells_image_id[y].append('2')
                elif list(self.map[y][x])[0] == '3':
                    self.list_cells_image_id[y].append('3')
                elif list(self.map[y][x])[0] == '_':
                    self.list_cells_image_id[y].append('_')
                self.create_map_entities()

    def create_map_entities(self):
        self.map_entities = self.data_map[0]
        self.map_entities = self.map_entities.replace('npc_objects:[', '')
        self.map_entities = self.map_entities.replace(']:', '')
        self.map_entities = self.map_entities.split(';\n             ')
        self.map_entities = edit_map_entities(self.map_entities)

    def render(self, surface, map_position, mode):
        if mode == 0:
            texture_surface = pygame.Surface((len(self.map[0]) * 50, len(self.map) * 50))

            for y in range(len(self.map)):
                for x in range(len(self.map[y])):
                    if self.map[y][x] == '0':
                        if self.game_screen.collidepoint((x * self.cell_size + self.left * map_position[0],
                                                          y * self.cell_size + self.left * map_position[1])):
                            texture_surface.blit(load_image('hell_path_0.png'),
                                                 (x * self.cell_size + self.left * map_position[0],
                                                  y * self.cell_size + self.left * map_position[1]))
                    elif self.map[y][x] == '1':
                        if self.game_screen.collidepoint((x * self.cell_size + self.left * map_position[0],
                                                          y * self.cell_size + self.left * map_position[1])):
                            texture_surface.blit(self.list_cells_image_id[y][x],
                                                 (x * self.cell_size + self.left * map_position[0],
                                                  y * self.cell_size + self.left * map_position[1]))
            surface.blit(texture_surface, (0, 0))

        elif mode == 1:
            for i in entities:
                if i != 'player':
                    if self.game_screen.collidepoint((map_position[0] * self.cell_size + self.left * i.position[0] -
                                                      11) - 20, (map_position[1] * self.cell_size + self.top *
                                                                 (i.position[1] + 4 - 4)) - 10):
                        surface.blit(i.image, ((map_position[0] * self.cell_size + self.left * i.position[0] - 11) - 20,
                                               (map_position[1] * self.cell_size + self.top *
                                                (i.position[1] + 4 - 4)) - 10))  # 4

            surface.blit(image, (15 * self.cell_size + self.left - 10, 4 * self.cell_size + self.top - 10))

        if mode == 2:
            form_size = get_form_size()

            pygame.draw.rect(surface, (20, 20, 20), (0, form_size[1] / 5 * 4, form_size[0], form_size[1] / 5 * 1), 0)

            image_interface = load_image("big_shotgun.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 3, form_size[1] / 5 * 1))
            surface.blit(image_interface, (form_size[0] / 10 * 2, form_size[1] / 5 * 4))

            image_interface = load_image("bag_bullets.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 3, form_size[1] / 5 * 1))
            surface.blit(image_interface, (form_size[0] / 10 * 5, form_size[1] / 5 * 4))

            for i in texts:
                text_x = ((form_size[0] / 10 * 1)) - text.get_width() // 2
                text_y = (form_size[1] / 5 * 4) + (((form_size[1]) - (form_size[1] / 5 * 4)) / 5) * (texts.index(i) + 1)
                screen.blit(i, (text_x, text_y))

            image_interface = load_image("I_dont_know_how_to_name_this.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 2, form_size[1] / 5 * 1))
            surface.blit(image_interface, (form_size[0] / 10 * 8, form_size[1] / 5 * 4))

            image_interface = load_image("I_dont_know_how_to_name_this.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 3, form_size[1] / 5 * 1))
            surface.blit(image_interface, (form_size[0] / 10 * 5, form_size[1] / 5 * 4))

            image_interface = load_image("I_dont_know_how_to_name_this.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 3, form_size[1] / 5 * 1))
            surface.blit(image_interface, (form_size[0] / 10 * 2, form_size[1] / 5 * 4))

            image_interface = load_image("I_dont_know_how_to_name_this.png")
            image_interface = pygame.transform.scale(image_interface, (form_size[0] / 10 * 2, form_size[1] / 5 * 1))
            surface.blit(image_interface, (0, form_size[1] / 5 * 4))

            '''pygame.draw.rect(surface, 'black', (form_size[0] / 10 * 8, form_size[1] / 5 * 4, form_size[0] / 10 * 2,
                                                form_size[1] / 5 * 1), 0)

            pygame.draw.rect(surface, 'gray', (form_size[0] / 10 * 5, form_size[1] / 5 * 4, form_size[0] / 10 * 3,
                                                form_size[1] / 5 * 1), 0)

            pygame.draw.rect(surface, 'orange', (form_size[0] / 10 * 2, form_size[1] / 5 * 4, form_size[0] / 10 * 3,
                                               form_size[1] / 5 * 1), 0)

            pygame.draw.rect(surface, 'red', (0, form_size[1] / 5 * 4, form_size[0] / 10 * 2,
                                                 form_size[1] / 5 * 1), 0)'''

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


clock = pygame.time.Clock()
pygame.init()

display_info = pygame.display.Info()
monitor_width = display_info.current_w
monitor_height = display_info.current_h
'''------------------form_values = [monitor_width, monitor_height - 50]------------------'''

screen = pygame.display.set_mode((monitor_width, monitor_height - 50), pygame.RESIZABLE)
pygame.display.set_caption('40 Degrees Of Hell')
del monitor_height, monitor_width, display_info



start_game = False
mode = 0
name = ''
tick = 27
form_size = get_form_size()

image = load_image(r'D:\саша\Л.А.Я. лицей академии яндекса\второй проект pygame\unuse\backround_main_menu.png')
image1 = load_image(r'D:\саша\Л.А.Я. лицей академии яндекса\второй проект pygame\unuse\game_name2_1.png')
image3 = pygame.transform.scale(image1, (form_size[0] / 4.2, form_size[1] / 2))  # 4.2  2
image2 = pygame.transform.smoothscale(image, (form_size[0], form_size[1]))

running = True

while running:
    if not start_game:
        if tick == 28:
            tick = 0

        if mode == 0:

            texts = []

            font = pygame.font.Font(None, (round((form_size[0] + form_size[1]) / 31.5)))

            text = font.render('новая игра', True, 'black')
            texts.append(text)
            text = font.render('загрузить игру', True, 'black')
            texts.append(text)
            text = font.render('выйти из игры', True, 'black')
            texts.append(text)

            new_game_button = pygame.Rect(7 * (form_size[0] // 12), 2 * (form_size[1] // 10), 4 * (form_size[0] // 12),
                                          form_size[1] // 10)
            load_game_button = pygame.Rect(7 * (form_size[0] // 12), 4 * (form_size[1] // 10), 4 * (form_size[0] // 12),
                                           form_size[1] // 10)
            exit_game_button = pygame.Rect(7 * (form_size[0] // 12), 6 * (form_size[1] // 10), 4 * (form_size[0] // 12),
                                           form_size[1] // 10)

            screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    image2 = pygame.transform.smoothscale(image, (event.w, event.h))
                    image3 = pygame.transform.scale(image1, (event.w / 4.2, event.h / 2))  # 4.2  2
                    form_size = get_form_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(pygame.mouse.get_pos()):
                        mode = 1
                        name = ''
                    if load_game_button.collidepoint(pygame.mouse.get_pos()):
                        mode = 2
                        list_position = 1
                    if exit_game_button.collidepoint(pygame.mouse.get_pos()):
                        running = False

            screen.blit(image2, (0, 0))
            screen.blit(image3, (screen.get_width() // 5 - image3.get_width() // 2, screen.get_height() // 3 -
                                 image3.get_height() // 2))


            pygame.draw.rect(screen, (71, 6, 6), (7 * (form_size[0] // 12), 2 * (form_size[1] // 10),
                                                  4 * (form_size[0] // 12), form_size[1] // 10), 0, 4)
            pygame.draw.rect(screen, (71, 6, 6), (7 * (form_size[0] // 12), 4 * (form_size[1] // 10),
                                                  4 * (form_size[0] // 12), form_size[1] // 10), 0, 4)
            pygame.draw.rect(screen, (71, 6, 6), (7 * (form_size[0] // 12), 6 * (form_size[1] // 10),
                                                  4 * (form_size[0] // 12), form_size[1] // 10), 0, 4)

            for i in texts:
                text_x = (9 * (form_size[0] // 12)) - text.get_width() // 2
                text_y = ((2 * (texts.index(i) + 1)) * (form_size[1] // 10))
                screen.blit(i, (text_x, text_y))

        elif mode == 1:

            texts = []

            font = pygame.font.Font(None, (round((form_size[0] + form_size[1]) / 31.5)))

            text = font.render('введите имя', True, 'black')
            text_name = font.render(name, True, 'white')

            screen.fill((71, 6, 6))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    image2 = pygame.transform.smoothscale(image, (event.w, event.h))
                    image3 = pygame.transform.scale(image1, (event.w / 4.2, event.h / 2))  # 4.2  2
                    form_size = get_form_size()
            if tick == 27:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    name += 'a'
                if keys[pygame.K_b]:
                    name += 'b'
                if keys[pygame.K_c]:
                    name += 'c'
                if keys[pygame.K_d]:
                    name += 'd'
                if keys[pygame.K_e]:
                    name += 'e'
                if keys[pygame.K_f]:
                    name += 'f'
                if keys[pygame.K_g]:
                    name += 'g'
                if keys[pygame.K_h]:
                    name += 'h'
                if keys[pygame.K_i]:
                    name += 'i'
                if keys[pygame.K_j]:
                    name += 'j'
                if keys[pygame.K_k]:
                    name += 'k'
                if keys[pygame.K_l]:
                    name += 'l'
                if keys[pygame.K_m]:
                    name += 'm'
                if keys[pygame.K_n]:
                    name += 'n'
                if keys[pygame.K_o]:
                    name += 'o'
                if keys[pygame.K_p]:
                    name += 'p'
                if keys[pygame.K_q]:
                    name += 'q'
                if keys[pygame.K_r]:
                    name += 'r'
                if keys[pygame.K_s]:
                    name += 's'
                if keys[pygame.K_t]:
                    name += 't'
                if keys[pygame.K_u]:
                    name += 'u'
                if keys[pygame.K_v]:
                    name += 'v'
                if keys[pygame.K_w]:
                    name += 'w'
                if keys[pygame.K_x]:
                    name += 'x'
                if keys[pygame.K_y]:
                    name += 'y'
                if keys[pygame.K_z]:
                    name += 'z'
                if keys[pygame.K_SPACE]:
                    name += ' '

                if keys[pygame.K_BACKSPACE]:
                    name = ''.join(list(name)[:-1])
                if keys[pygame.K_ESCAPE]:
                    mode = 0
                if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                    if name != '' or name != ' ':
                        answer = create_player_data(name)
                        if answer == 1:
                            start_game = True
                            running = False

            pygame.draw.rect(screen, 'black', (4 * (form_size[0] // 12), 4 * (form_size[1] // 10), 4 * (form_size[0] // 12),
                                               form_size[1] // 10), 0, 4)

            text_x = form_size[0] // 2 - text.get_width() // 2
            text_y = 3 * (form_size[1] // 10) - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

            text_x = form_size[0] // 2 - text_name.get_width() // 2
            text_y = 4.5 * (form_size[1] // 10) - text_name.get_height() // 2
            screen.blit(text_name, (text_x, text_y))

            tick += 1

        elif mode == 2:
            texts = read_player_data()
            buttons = []

            screen.fill((71, 6, 6))
            pygame.draw.rect(screen, 'black', (0.5 * (form_size[0] // 12), 0.5 * (form_size[1] // 10),
                                               11 * (form_size[0] // 12), 9 * form_size[1] // 10), 0, 4)

            font = pygame.font.Font(None, (round((form_size[0] + form_size[1]) / 31.5)))

            for i in texts:
                text = font.render(i, True, 'white')

                text_x = form_size[0] // 2 - text.get_width() // 2
                text_y = form_size[1] // 11 * (texts.index(i) + 1) + list_position - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()

                button = pygame.Rect(0.5 * (form_size[0] // 12), text_y - 10, 11 * (form_size[0] // 12), text_h + 20)
                buttons.append(button)
                pygame.draw.rect(screen, 'white', (0.5 * (form_size[0] // 12), text_y - 10, 11 * (form_size[0] // 12),
                                                   text_h + 20), 1)
                screen.blit(text, (text_x, text_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    form_size = get_form_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                            name = texts[buttons.index(button)]
                            start_game = True
                            running = False
                    if event.button == 4:
                        list_position -= 30
                    if event.button == 5:
                        list_position += 30

            if tick == 27:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    mode = 0

            pygame.draw.rect(screen, (71, 6, 6), (0, 0, form_size[0], 0.5 * (form_size[1] // 10)))
            pygame.draw.rect(screen, (71, 6, 6), (0, 9 * (form_size[1] // 10) + 0.5 * (form_size[1] // 10),
                                                  form_size[0], 0.5 * (form_size[1] // 10)))

            tick += 1

        pygame.display.flip()
    else:
        player = player_file_code.Player(name, [0, 0],
                                         animation.AnimatedSprite(load_image("player_test_2_1.png"), 4, 1, 0,
                                                                  0))
        player.read_player_stats()
        NPCWork.create_npc(player.player_data['location'], player.player_data['complexity'],
                           player.player_data['very_important_number'])
        player_angle = 0

        cells = Cells(11, 11)
        cells.set_view(50, 50, 50)
        '''----------------------------cells.set_view(50, 50, (monitor_height - 50) // 20)----------------------------'''
        '''----------------------------print(monitor_width // 33, (monitor_height - 50) // 20, (monitor_height - 50) // 20)
        print(monitor_width // 50, (monitor_height - 50) // 50, (monitor_height - 50) // 50)
        print(monitor_height // 50)
        print(monitor_width, monitor_height)----------------------------'''
        tick = 5
        weapons_ready = 1
        weapons_reload_tick = 0
        npc_weapon_tick = 0
        map_pos = [5, 1]
        begin = 1
        active = False
        bullets_counter = 8
        bullet_shotgun = load_image("shotgun_bullet.png")
        bullet_shotgun_rect = pygame.Rect(form_size[0] / 10 * 6, form_size[1] / 5 * 4.5, 73, 28)

        entities = []

        npc_image = animation.AnimatedSprite(load_image("npc_human_1.png"), 4, 1, 0, 0)

        for i in cells.map_entities:
            exec(i)

        for i in cells.map_entities:
            if i != 'player':
                entities.append(eval(i.split(' = ')[0]))
            else:
                entities.append('player')

        for i in entities:
            if i != 'player':
                i.update_danger()

        running = True
        while running:

            texts = []

            font = pygame.font.Font(None, (round((form_size[0] + form_size[1]) / 85)))

            text = font.render(f'здровье    {player.health}', True, 'green')
            texts.append(text)
            text = font.render(f'броня    {player.health}', True, 'green')
            texts.append(text)
            text = font.render(f'патроны в магазине    {bullets_counter}', True, 'green')
            texts.append(text)

            if tick == 6:
                tick = 0
            if weapons_reload_tick == 2:
                weapons_reload_tick = 0
            if npc_weapon_tick == 31:
                npc_weapon_tick = 0
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    '''------------------------cells.set_view(50, 50, event.h // 21)
                    form_values = [event.w, event.h]
                    print(event.w // 33, event.h // 20, event.h // 20)
                    print(event.w, event.h)------------------------'''
                    form_size = get_form_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pygame.Rect(form_size[0] / 10 * 5, form_size[1] / 5 * 4, form_size[0] / 10 * 3,
                                       form_size[1] / 5 * 1).collidepoint(event.pos):
                            active = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if pygame.Rect(form_size[0] / 10 * 2, form_size[1] / 5 * 4, form_size[0] / 10 * 3,
                                       form_size[1] / 5 * 1).collidepoint(event.pos):
                            bullet_shotgun_rect = pygame.Rect(form_size[0] / 10 * 6, form_size[1] / 5 * 4.5, 73, 28)
                            bullets_counter += 1
                        active = False

                if event.type == pygame.MOUSEMOTION:
                    if active:
                        bullet_shotgun_rect.move_ip(event.rel)

                if weapons_ready == 1:
                    if cells.game_screen.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bullets_counter != 0:
                                bullets_code.bullets.append(
                                    bullets_code.Bullet((15 * cells.cell_size + cells.left) + 14,
                                                        (4 * cells.cell_size + cells.top) + 14, 0,
                                                        '[NULL]', map_pos, cells.cell_size,
                                                        cells.left, cells.top, 'player'))
                                bullets_counter -= 1
                        weapons_ready = 0

                if begin == 0:
                    if cells.game_screen.collidepoint(pygame.mouse.get_pos()):
                        player_angle = rotate_player()
                        image = pygame.transform.rotate(player.image_class.image, int(player_angle))
                else:
                    player_angle = rotate_player()
                    image = pygame.transform.rotate(player.image_class.image, int(player_angle))

            keys = pygame.key.get_pressed()
            if tick == 5:
                if keys[pygame.K_LSHIFT]:
                    if keys[pygame.K_a]:
                        if [player.position[0] - 2, player.position[1]] not in cells.board and \
                                [player.position[0] - 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] + 2, map_pos[1]]
                            player.position = [player.position[0] - 2, player.position[1]]

                        elif [player.position[0] - 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] + 1, map_pos[1]]
                            player.position = [player.position[0] - 1, player.position[1]]

                    if keys[pygame.K_d]:
                        if [player.position[0] + 2, player.position[1]] not in cells.board and \
                                [player.position[0] + 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] - 2, map_pos[1]]
                            player.position = [player.position[0] + 2, player.position[1]]

                        elif [player.position[0] + 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] - 1, map_pos[1]]
                            player.position = [player.position[0] + 1, player.position[1]]

                    if keys[pygame.K_w]:
                        if [player.position[0], player.position[1] - 2] not in cells.board and \
                                [player.position[0], player.position[1] - 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] + 2]
                            player.position = [player.position[0], player.position[1] - 2]

                        elif [player.position[0], player.position[1] - 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] + 1]
                            player.position = [player.position[0], player.position[1] - 1]

                    if keys[pygame.K_s]:
                        if [player.position[0], player.position[1] + 2] not in cells.board and \
                                [player.position[0], player.position[1] + 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] - 2]
                            player.position = [player.position[0], player.position[1] + 2]

                        elif [player.position[0], player.position[1] + 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] - 1]
                            player.position = [player.position[0], player.position[1] + 1]
                else:
                    if keys[pygame.K_a]:
                        if [player.position[0] - 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] + 1, map_pos[1]]
                            player.position = [player.position[0] - 1, player.position[1]]

                    if keys[pygame.K_d]:
                        if [player.position[0] + 1, player.position[1]] not in cells.board:
                            map_pos = [map_pos[0] - 1, map_pos[1]]
                            player.position = [player.position[0] + 1, player.position[1]]

                    if keys[pygame.K_w]:
                        if [player.position[0], player.position[1] - 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] + 1]
                            player.position = [player.position[0], player.position[1] - 1]

                    if keys[pygame.K_s]:
                        if [player.position[0], player.position[1] + 1] not in cells.board:
                            map_pos = [map_pos[0], map_pos[1] - 1]
                            player.position = [player.position[0], player.position[1] + 1]
                image = pygame.transform.rotate(player.image_class.image, int(player_angle))

            if weapons_ready == 0:
                weapons_reload_tick += 1
            if weapons_reload_tick == 1:
                weapons_ready = 1

            for bullet in bullets_code.bullets:
                bullet.update(map_pos)
                if not screen.get_rect().collidepoint(bullet.bullets_parameters[0][0]):
                    bullets_code.bullets.remove(bullet)
                else:
                    for i in cells.board:
                        coliderect = pygame.Rect((i[0] + 11) * cells.cell_size + cells.left * map_pos[0],
                                                 (i[1] + 4) * cells.cell_size + cells.top * map_pos[1],
                                                 cells.cell_size, cells.cell_size)
                        if coliderect.collidepoint(bullet.bullets_parameters[0][0]):
                            bullets_code.bullets.remove(bullet)

            if tick == 5:
                for i in entities:
                    if i != 'player':
                        if i.is_dead is False:
                            i.perseverance(player.position)
                            i.angle = rotate_object(i.max_danger[0], i)
                            i.image = pygame.transform.rotate(i.image_class.image, int(i.angle))
                        else:
                            if i.type_of_entity == '[human]':
                                i.set_image(animation.AnimatedSprite(load_image("npc_human_corpse_1.png"), 1, 1, 0, 0))
                                i.image = pygame.transform.rotate(i.image_class.image, int(i.angle))
                            elif i.type_of_entity == '[cuscas]':
                                i.set_image(animation.AnimatedSprite(load_image("npc_cuscas_corpse_1.png"), 1, 1, 0, 0))
                                i.image = pygame.transform.rotate(i.image_class.image, int(i.angle))
                            elif i.type_of_entity == '[robot]':
                                i.set_image(animation.AnimatedSprite(load_image("npc_robot_corpse_1.png"), 1, 1, 0, 0))
                                i.image = pygame.transform.rotate(i.image_class.image, int(i.angle))

            for i in entities:
                if i != 'player':
                    if i.is_dead is False:
                        if npc_weapon_tick == 30:
                            if i.max_danger[0] == 'player':
                                bullets_code.bullets.append(bullets_code.Bullet((map_pos[0] * cells.cell_size +
                                                                                 cells.left * i.position[0] + 11),
                                                                                (map_pos[1] * cells.cell_size +
                                                                                 cells.top * i.position[1]), 1,
                                                                                eval(i.max_danger[0]), map_pos,
                                                                                cells.cell_size, cells.left, cells.top,
                                                                                i.name))
                            else:
                                bullets_code.bullets.append(bullets_code.Bullet((map_pos[0] * cells.cell_size +
                                                                                 cells.left * i.position[0]),
                                                                                (map_pos[1] * cells.cell_size +
                                                                                 cells.top * (i.position[1] - 11)), 1,
                                                                                eval(f'ai.{i.max_danger[0]}'), map_pos,
                                                                                cells.cell_size, cells.left, cells.top,
                                                                                i.name))

                        coliderect = pygame.Rect((map_pos[0] * cells.cell_size + cells.left * i.position[0] + 11),
                                                 (map_pos[1] * cells.cell_size + cells.top * i.position[1] + 20),
                                                 cells.cell_size, cells.cell_size)
                        for bullet in bullets_code.bullets:
                            if coliderect.collidepoint(bullet.bullets_parameters[0][0]):
                                if i.is_dead is False:
                                    if i.name != bullet.shooter:
                                        i.health -= 5
                                        if random.randint(0, 1) == 0:
                                            bullets_code.bullets.remove(bullet)
                else:
                    coliderect = pygame.Rect((15 * cells.cell_size + cells.left + 11),
                                             (4 * cells.cell_size + cells.top + 20),
                                             cells.cell_size, cells.cell_size)
                    for bullet in bullets_code.bullets:
                        if coliderect.collidepoint(bullet.bullets_parameters[0][0]):
                            if bullet.shooter != 'player':
                                player.health -= 1

                    if player.health == 0:
                        running = False

            screen.fill('black')
            cells.render(screen, map_pos, 0)

            cells.render(screen, map_pos, 1)
            animation.all_sprites.update()

            for bullet in bullets_code.bullets:
                bullet.draw(screen, map_pos)

            cells.render(screen, map_pos, 2)
            if active:
                screen.blit(bullet_shotgun, bullet_shotgun_rect[:2])
            pygame.display.flip()

            tick += 1
            npc_weapon_tick += 1
            begin = 0

            clock.tick(60)

pygame.quit()
