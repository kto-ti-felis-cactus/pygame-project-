import pygame
import math


def load_map():
    file = open('1.txt', 'r', encoding='utf-8')
    data = file.read().split('\n')
    for i in range(len(data)):
        data[i] = data[i].split(',')
    file.close()
    return data


def get_form_size():
    width, height = pygame.display.get_surface().get_size()
    return [width, height]


class Cells():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen, map_pos, mode):
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
            self.data_map = load_map()
            self.board = []

            for y in range(len(self.data_map)):
                for x in range(len(self.data_map[y])):
                    if self.data_map[y][x] == '1':
                        pygame.draw.rect(screen, 'blue',
                                         (x * self.cell_size + self.left * map_pos[0],
                                          y * self.cell_size + self.top * map_pos[1],
                                          self.cell_size, self.cell_size), 0)
                    elif self.data_map[y][x] == '0':
                        pygame.draw.rect(screen, 'green',
                                         (x * self.cell_size + self.left * map_pos[0],
                                          y * self.cell_size + self.top * map_pos[1],
                                          self.cell_size, self.cell_size), 0)
                    elif self.data_map[y][x] == '2':
                        pygame.draw.rect(screen, 'white',
                                         (x * self.cell_size + self.left * map_pos[0],
                                          y * self.cell_size + self.top * map_pos[1],
                                          self.cell_size, self.cell_size), 0)
                        self.board.append([x - 11, y - 4])

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
            screen.blit(image, (15 * self.cell_size + self.left, 4 * self.cell_size + self.top))

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white',
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

        if mode == 2:
            form_size = get_form_size()
            pygame.draw.rect(screen, 'grey',
                             (form_size[0] - (form_size[0] / 30 * 5),
                              form_size[1] - (form_size[1] / 37 * 7),
                              form_size[0] - (form_size[0] / 30 * 25),
                              form_size[1] - (form_size[1] / 37 * 30)), 0)
            self.fullscreen_btn = pygame.Rect(form_size[0] - 150, form_size[1] - 150, 150, 150)


    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        column = (mouse_pos[0] - self.left) // self.cell_size
        row = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= column < self.width and 0 <= row < self.height:
            return column, row
        else:
            return 1


clock = pygame.time.Clock()
pygame.init()

display_info = pygame.display.Info()
monitor_width = display_info.current_w
monitor_height = display_info.current_h
'''------------------form_values = [monitor_width, monitor_height - 50]------------------'''

screen = pygame.display.set_mode((monitor_width, monitor_height - 50), pygame.RESIZABLE)
pygame.display.set_caption('40 Degrees Of Hell')

cells = Cells(11, 11)
cells.set_view(50, 50, 50)
'''----------------------------cells.set_view(50, 50, (monitor_height - 50) // 20)----------------------------'''
'''----------------------------print(monitor_width // 33, (monitor_height - 50) // 20, (monitor_height - 50) // 20)
print(monitor_width // 50, (monitor_height - 50) // 50, (monitor_height - 50) // 50)
print(monitor_height // 50)
print(monitor_width, monitor_height)----------------------------'''
tick = 0
map_pos = [5, 1]
player_pos = [0, 0]

running = True
while running:
    if tick == 6:
        tick = 0
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if collidepoint(event.pos):
            print(cells.get_cell(event.pos))

        if event.type == pygame.MOUSEMOTION:
            original_image = pygame.image.load('player_test_1.png')
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x = mouse_x - (15 * cells.cell_size + cells.left + 0)
            rel_y = mouse_y - (4 * cells.cell_size + cells.top + 0)
            angle = math.degrees(-math.atan2(rel_y, rel_x))
            image = pygame.transform.rotate(original_image, int(angle))
            # rect = image.get_rect(center=(70, 70))
            # rect = image.get_rect(center=(25, 25))

    if tick == 5:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_a]:
                if [player_pos[0] - 2, player_pos[1]] not in cells.board and \
                   [player_pos[0] - 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] + 2, map_pos[1]]
                    player_pos = [player_pos[0] - 2, player_pos[1]]

                elif [player_pos[0] - 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] + 1, map_pos[1]]
                    player_pos = [player_pos[0] - 1, player_pos[1]]

            if keys[pygame.K_d]:
                if [player_pos[0] + 2, player_pos[1]] not in cells.board and \
                   [player_pos[0] + 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] - 2, map_pos[1]]
                    player_pos = [player_pos[0] + 2, player_pos[1]]

                elif [player_pos[0] + 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] - 1, map_pos[1]]
                    player_pos = [player_pos[0] + 1, player_pos[1]]

            if keys[pygame.K_w]:
                if [player_pos[0], player_pos[1] - 2] not in cells.board and \
                   [player_pos[0], player_pos[1] - 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] + 2]
                    player_pos = [player_pos[0], player_pos[1] - 2]

                elif [player_pos[0], player_pos[1] - 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] + 1]
                    player_pos = [player_pos[0], player_pos[1] - 1]

            if keys[pygame.K_s]:
                if [player_pos[0], player_pos[1] + 2] not in cells.board and \
                   [player_pos[0], player_pos[1] + 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] - 2]
                    player_pos = [player_pos[0], player_pos[1] + 2]

                elif [player_pos[0], player_pos[1] + 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] - 1]
                    player_pos = [player_pos[0], player_pos[1] + 1]
        else:
            if keys[pygame.K_a]:
                if [player_pos[0] - 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] + 1, map_pos[1]]
                    player_pos = [player_pos[0] - 1, player_pos[1]]

            if keys[pygame.K_d]:
                if [player_pos[0] + 1, player_pos[1]] not in cells.board:
                    map_pos = [map_pos[0] - 1, map_pos[1]]
                    player_pos = [player_pos[0] + 1, player_pos[1]]

            if keys[pygame.K_w]:
                if [player_pos[0], player_pos[1] - 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] + 1]
                    player_pos = [player_pos[0], player_pos[1] - 1]

            if keys[pygame.K_s]:
                if [player_pos[0], player_pos[1] + 1] not in cells.board:
                    map_pos = [map_pos[0], map_pos[1] - 1]
                    player_pos = [player_pos[0], player_pos[1] + 1]
    tick += 1

    screen.fill('black')
    cells.render(screen, map_pos, 0)
    cells.render(screen, map_pos, 1)
    cells.render(screen, map_pos, 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
