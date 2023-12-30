import pygame
import math


class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.ipos = (x, y)
        self.iipos = (x, y)
        mx, my = pygame.mouse.get_pos()

        self.dir = (mx - x, my - y)
        self.idir = (mx - (x - 10), my - (y - 10))
        self.iidir = (mx - (x + 10), my - (y + 10))

        length = math.hypot(*self.dir)
        ilength = math.hypot(*self.idir)
        iilength = math.hypot(*self.iidir)
        if length == 0.0:
            self.dir = (0, -1)
            self.idir = (0, -1)
            self.iidir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
            self.idir = (self.idir[0]/ilength, self.idir[1]/ilength)
            self.iidir = (self.iidir[0]/iilength, self.iidir[1]/iilength)

        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        iangle = math.degrees(math.atan2(-self.idir[1], self.idir[0]))
        iiangle = math.degrees(math.atan2(-self.iidir[1], self.iidir[0]))

        self.bullet = pygame.Surface((7, 2)).convert_alpha()
        self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)

        self.ibullet = pygame.Surface((7, 2)).convert_alpha()
        self.ibullet.fill((255, 255, 255))
        self.ibullet = pygame.transform.rotate(self.ibullet, iangle)

        self.iibullet = pygame.Surface((7, 2)).convert_alpha()
        self.iibullet.fill((255, 255, 255))
        self.iibullet = pygame.transform.rotate(self.iibullet, iiangle)
        self.speed = 45

    def update(self):
        self.pos = (self.pos[0]+self.dir[0] * self.speed,
                    self.pos[1]+self.dir[1] * self.speed)
        self.ipos = (self.ipos[0] + self.idir[0] * self.speed,
                    self.ipos[1] + self.idir[1] * self.speed)
        self.iipos = (self.iipos[0] + self.iidir[0] * self.speed,
                    self.iipos[1] + self.iidir[1] * self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)
        ibullet_rect = self.ibullet.get_rect(center=self.ipos)
        surf.blit(self.ibullet, ibullet_rect)
        iibullet_rect = self.iibullet.get_rect(center=self.iipos)
        surf.blit(self.iibullet, iibullet_rect)


bullets = []
