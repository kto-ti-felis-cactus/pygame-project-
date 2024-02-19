import pygame
import math


class Bullet:
    def __init__(self, x, y, mode, target, map_position, cell_size, left, top, shooter):
        self.mode = mode
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.x, self.y = x, y
        self.shooter = shooter
        if self.mode == 0:
            target_x, target_y = pygame.mouse.get_pos()
        elif self.mode == 1:
            if target != '[NULL]':
                if target.type_of_entity == '[player]':
                    target_x, target_y = ((15 * self.cell_size + self.left) + 14, (4 * self.cell_size + self.top) + 14)
                else:
                    target_x, target_y = ((map_position[0] * self.cell_size + self.left * target.position[0]) + 20,
                                          (map_position[1] * self.cell_size + self.top * (target.position[1] + 4)) + 10)

        self.bullets_parameters = [[(self.x, self.y), 0, 0, 0],
                                   [(self.x, self.y), 0, 0, 0],
                                   [(self.x, self.y), 0, 0, 0]]

        for i in self.bullets_parameters:
            if self.bullets_parameters.index(i) == 0:
                i[1] = (target_x - self.x, target_y - self.y)
            elif self.bullets_parameters.index(i) == 1:
                i[1] = (target_x - (self.x - 10), target_y - (self.y - 10))
            elif self.bullets_parameters.index(i) == 2:
                i[1] = (target_x - (self.x + 10), target_y - (self.y + 10))

        for i in self.bullets_parameters:
            if self.bullets_parameters.index(i) == 0:
                i[2] = math.hypot(*i[1])
            elif self.bullets_parameters.index(i) == 1:
                i[2] = math.hypot(*i[1])
            elif self.bullets_parameters.index(i) == 2:
                i[2] = math.hypot(*i[1])

        for i in self.bullets_parameters:
            if i[2] == 0.0:
                i[1] = (0, -1)
            else:
                i[1] = (i[1][0] / i[2], i[1][1] / i[2])

        for i in self.bullets_parameters:
            i[2] = math.degrees(math.atan2(-i[1][1], i[1][0]))

        for i in self.bullets_parameters:
            i[3] = pygame.Surface((7, 2)).convert_alpha()
            i[3].fill((255, 255, 255))
            i[3] = pygame.transform.rotate(i[3], i[2])
        self.speed = 45

    def update(self, map_position):
        for i in self.bullets_parameters:
            if self.shooter == 'player':
                i[0] = (i[0][0] + i[1][0] * self.speed, i[0][1] + i[1][1] * self.speed)
            else:
                i[0] = ((map_position[0] * self.cell_size + self.left) + (i[0][0] + i[1][0] * self.speed),
                        (map_position[1] * self.cell_size + self.left) + (i[0][1] + i[1][1] * self.speed))

    def draw(self, surf, map_position):
        for i in self.bullets_parameters:
            bullet_rect = i[3].get_rect(center=i[0])
            surf.blit(i[3], bullet_rect)
            if self.shooter != 'player':
                i[0] = (i[0][0] - (map_position[0] * self.cell_size + self.left),
                        i[0][1] - (map_position[1] * self.cell_size + self.left))


bullets = []
