import pygame
pygame.init()
import math

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, start, radius, target, status = [False, False]):
        super().__init__()
        self.image = pygame.Surface([radius * 8, radius * 8], pygame.SRCALPHA)
        self.image.set_colorkey(WHITE)
        self.start = start
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, [radius * 4, radius * 4], int(radius))
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        self.target = target
        self.radius = radius
        self.gps = start

    def move(self):
        dx = self.target[0] - self.start[0]
        nx = round(self.gps[0] + .01 * dx)
        dy = self.target[1] - self.start[1]
        ny = round(self.gps[1] + .01 * dy)
        self.gps = [int(nx), int(ny)]
        self.rect.x = self.gps[0]
        self.rect.y = self.gps[1]
        temp_1 = self.gps[0] - self.target[0]
        temp_2 = self.gps[1] - self.target[1]
        temp = math.hypot(temp_1, temp_2)
        if self.gps == self.target:
            self.gps = self.target
            temp = self.target
            self.target = self.start
            self.start = temp
