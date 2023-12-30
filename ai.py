import pygame


class Entity:
    def __init__(self, level, level_of_danger, level_of_peace):
        self.level = level
        self.level_of_danger = level_of_danger
        self.level_of_peace = level_of_peace


class Human(Entity):
    def __init__(self, level, level_of_danger, level_of_peace):
        super().__init__(level, level_of_danger, level_of_peace)
        print(self.level)


entity = Entity(1, 2, 3)
h = Human(2, 7, 0)
