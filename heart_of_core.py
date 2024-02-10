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
        image = pygame.image.load(fullname)
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
        self.game_screen = pygame.Rect(form_size[0] - (form_size[0] / 30 * 22),
                                       form_size[1] - (form_size[1] / 37 * 37),
                                       form_size[0] - (form_size[0] / 30 * 13),
                                       form_size[1] - (form_size[1] / 37 * 14))
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
        '''for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white',
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)'''
        if mode == 0:
            '''file = open('1.txt', 'r', encoding='utf-8')
            self.data = file.read().split('\n')
            for i in range(len(self.data)):
                self.data[i] = self.data[i].split(',')'''

            for y in range(len(self.map)):
                for x in range(len(self.map[y])):
                    if self.map[y][x] == '0':
                        '''pygame.draw.rect(surface, 'green',
                                         (x * self.cell_size + self.left * map_position[0],
                                          y * self.cell_size + self.top * map_position[1],
                                          self.cell_size, self.cell_size), 0)'''
                        if self.game_screen.collidepoint((x * self.cell_size + self.left * map_position[0],
                                                          y * self.cell_size + self.left * map_position[1])):
                            surface.blit(load_image('hell_path_0.png'),
                                         (x * self.cell_size + self.left * map_position[0],
                                          y * self.cell_size + self.left * map_position[1]))
                    elif self.map[y][x] == '1':
                        if self.game_screen.collidepoint((x * self.cell_size + self.left * map_position[0],
                                                          y * self.cell_size + self.left * map_position[1])):
                            surface.blit(self.list_cells_image_id[y][x],
                                         (x * self.cell_size + self.left * map_position[0],
                                          y * self.cell_size + self.left * map_position[1]))
                    elif self.map[y][x] == '2':
                        pygame.draw.rect(surface, 'black',
                                         (x * self.cell_size + self.left * map_position[0],
                                          y * self.cell_size + self.top * map_position[1],
                                          self.cell_size, self.cell_size), 0)
                '''>>>>>>>>>>>>>>>>>>>>>>>>>>>for i in self.board:
                    pygame.draw.rect(surface, 'red',
                                     ((i[0] + 11) * self.cell_size + self.left * map_position[0],
                                      (i[1] + 4) * self.cell_size + self.top * map_position[1],
                                      self.cell_size, self.cell_size), 0)>>>>>>>>>>>>>>>>>>>>>>>>>>>'''


            '''---------------------pygame.draw.rect(screen, 'red',
                             (15 * self.cell_size + self.left + 1,
                              4 * self.cell_size + self.top + 1,
                              self.cell_size - 2, self.cell_size - 2), 0)---------------------'''


            '''            elif self.data_map[y][x] == 'p':
                        pygame.draw.rect(screen, 'red',
                                         (15 * x * self.cell_size + self.left + 1,  # 8   15       112         11
                                          y * self.cell_size + self.top + 1,  # 5    4     270          3
                                          self.cell_size - 2, self.cell_size - 2), 0)
                        if self.data_map[y][x] == 'p':
                            situation = 1

            file.close()'''

        elif mode == 1:
            '''----------------------pygame.draw.rect(screen, 'red',
                             ((form_values[0] // 100 - 1) * self.cell_size + self.left + 1,  # 8   15       112
                              (form_values[1] // 270 + 1) * self.cell_size + self.top + 1,  # 5    4     270
                              self.cell_size - 2, self.cell_size - 2), 0)----------------------'''
            '''pygame.draw.rect(screen, 'red',
                             (15 * self.cell_size + self.left + 1,  # 8   15       112         11
                              4 * self.cell_size + self.top + 1,  # 5    4     270          3
                              self.cell_size - 2, self.cell_size - 2), 0)'''
            for i in entities:
                if i != 'player':
                    if self.game_screen.collidepoint((map_position[0] * self.cell_size + self.left * i.position[0] -
                                                      11) - 20, (map_position[1] * self.cell_size + self.top *
                                                                 (i.position[1] + 4 - 4)) - 10):
                        surface.blit(i.image, ((map_position[0] * self.cell_size + self.left * i.position[0] - 11) - 20,
                                               (map_position[1] * self.cell_size + self.top *
                                                (i.position[1] + 4 - 4)) - 10))  # 4

            surface.blit(image, (15 * self.cell_size + self.left - 10, 4 * self.cell_size + self.top - 10))

        '''for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(surface, 'white',
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)'''

        if mode == 3:
            form_size = get_form_size()
            pygame.draw.rect(surface, 'grey',
                             (form_size[0] - (form_size[0] / 30 * 5),
                              form_size[1] - (form_size[1] / 37 * 7),
                              form_size[0] - (form_size[0] / 30 * 25),
                              form_size[1] - (form_size[1] / 37 * 30)), 0)

            pygame.draw.rect(surface, 'orange',
                             (form_size[0] - (form_size[0] / 30 * 5),
                              form_size[1] - (form_size[1] / 37 * 28),
                              form_size[0] - (form_size[0] / 30 * 27.5),
                              form_size[1] - (form_size[1] / 37 * 16)), 0)

            pygame.draw.rect(surface, 'red',
                             (form_size[0] - (form_size[0] / 30 * 2.5),
                              form_size[1] - (form_size[1] / 37 * 28),
                              form_size[0] - (form_size[0] / 30 * 27.5),
                              form_size[1] - (form_size[1] / 37 * 16)), 0)

            pygame.draw.rect(surface, 'white',
                             (form_size[0] - (form_size[0] / 30 * 5),
                              form_size[1] - (form_size[1] / 37 * 37),
                              form_size[0] - (form_size[0] / 30 * 25),
                              form_size[1] - (form_size[1] / 37 * 28)), 0)

            '''--------------------pygame.draw.rect(surface, (150, 2, 0),
                             (form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 37),
                              form_size[0] - (form_size[0] / 30 * 13),
                              form_size[1] - (form_size[1] / 37 * 14)), 0)--------------------'''


            '''pygame.draw.rect(surface, (150, 2, 0),
                             (form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 37),
                              form_size[0] - (form_size[0] / 30 * 13),
                              form_size[1] - (form_size[1] / 37 * 1)), 0)'''


            pygame.draw.rect(surface, 'purple',
                             (form_size[0] - (form_size[0] / 30 * 30),
                              form_size[1] - (form_size[1] / 37 * 37),
                              form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 23)), 0)

            pygame.draw.rect(surface, 'cyan',
                             (form_size[0] - (form_size[0] / 30 * 30),
                              form_size[1] - (form_size[1] / 37 * 14),
                              form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 23)), 0)

            pygame.draw.rect(surface, 'cyan',
                             (form_size[0] - (form_size[0] / 30 * 30),
                              form_size[1] - (form_size[1] / 37 * 23),
                              form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 23)), 0)

            pygame.draw.rect(surface, 'green',
                             (form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 14),
                              form_size[0] - (form_size[0] / 30 * 13),
                              form_size[1] - (form_size[1] / 37 * 30)), 0)

            pygame.draw.rect(surface, 'blue',
                             (form_size[0] - (form_size[0] / 30 * 22),
                              form_size[1] - (form_size[1] / 37 * 7),
                              form_size[0] - (form_size[0] / 30 * 13),
                              form_size[1] - (form_size[1] / 37 * 30)), 0)


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


player = player_file_code.Player('victor', [0, 0], animation.AnimatedSprite(load_image("player_test_2_1.png"), 4, 1, 0,
                                                                            0))
player.read_player_stats()
asd = NPCWork.create_npc(player.player_data['location'], player.player_data['complexity'],
                         player.player_data['very_important_number'])


cells = Cells(11, 11)
cells.set_view(50, 50, 50)
'''----------------------------cells.set_view(50, 50, (monitor_height - 50) // 20)----------------------------'''
'''----------------------------print(monitor_width // 33, (monitor_height - 50) // 20, (monitor_height - 50) // 20)
print(monitor_width // 50, (monitor_height - 50) // 50, (monitor_height - 50) // 50)
print(monitor_height // 50)
print(monitor_width, monitor_height)----------------------------'''
# player = player_file_code.Player('victor', [0, 0], animation.AnimatedSprite(load_image("player_test_2_1.png"), 4, 1, 0,
#                                                                             0))
tick = 5
weapons_ready = 1
weapons_reload_tick = 0
npc_weapon_tick = 0
map_pos = [5, 1]
begin = 1

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


'''-----------------player.read_player_stats()
asd = NPCWork.create_npc(player.player_data['location'], player.player_data['complexity'],
                         player.player_data['very_important_number'])-----------------'''


running = True
while running:
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
        if weapons_ready == 1:
            if cells.game_screen.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    '''bullets_code.bullets.append(bullets_code.Bullet((814,
                                                                    264), 0)'''
                    bullets_code.bullets.append(bullets_code.Bullet((15 * cells.cell_size + cells.left) + 14,
                                                                    (4 * cells.cell_size + cells.top) + 14, 0,
                                                                    '[NULL]', map_pos, cells.cell_size,
                                                                    cells.left, cells.top, 'player'))
                weapons_ready = 0

        if begin == 0:
            if cells.game_screen.collidepoint(pygame.mouse.get_pos()):
                player_angle = rotate_player()
                image = pygame.transform.rotate(player.image_class.image, int(player_angle))
        else:
            player_angle = rotate_player()
            image = pygame.transform.rotate(player.image_class.image, int(player_angle))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        print(2)
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
    # print(f'weapons_ready:{weapons_ready}')
    # print(f'weapons_reload_tick:{weapons_reload_tick}')

    for bullet in bullets_code.bullets[:]:
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
                                                                         cells.left * i.position[0] - 11),
                                                                        (map_pos[1] * cells.cell_size +
                                                                         cells.top * (i.position[1])), 1,
                                                                        eval(i.max_danger[0]), map_pos, cells.cell_size,
                                                                        cells.left, cells.top, i.name))
                    else:
                        bullets_code.bullets.append(bullets_code.Bullet((map_pos[0] * cells.cell_size +
                                                                         cells.left * i.position[0]),
                                                                        (map_pos[1] * cells.cell_size +
                                                                         cells.top * (i.position[1] - 11)), 1,
                                                                        eval(f'ai.{i.max_danger[0]}'), map_pos,
                                                                        cells.cell_size, cells.left, cells.top, i.name))

                coliderect = pygame.Rect((map_pos[0] * cells.cell_size + cells.left * i.position[0] - 11) - 20,
                                         (map_pos[1] * cells.cell_size + cells.top * (i.position[1])) - 10,
                                         cells.cell_size, cells.cell_size)
                for bullet in bullets_code.bullets:
                    if coliderect.collidepoint(bullet.bullets_parameters[0][0]):
                        if i.is_dead is False:
                            if i.name != bullet.shooter:
                                i.health -= 5
                                if random.randint(0, 1) == 0:
                                    bullets_code.bullets.remove(bullet)

    screen.fill('black')
    cells.render(screen, map_pos, 0)

    cells.render(screen, map_pos, 1)
    animation.all_sprites.update()

    for bullet in bullets_code.bullets:
        bullet.draw(screen, map_pos)

    cells.render(screen, map_pos, 2)
    pygame.display.flip()

    tick += 1
    npc_weapon_tick += 1
    begin = 0
    print()

    clock.tick(60)

pygame.quit()
