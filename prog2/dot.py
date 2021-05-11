from random import randint
import math
import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, start, radius, target, status = [False, False]):
        super().__init__()
        self.image = pygame.Surface([16, 16], pygame.SRCALPHA)
        self.image.set_colorkey(WHITE)
        self.status = status                                                                                            #self.status is regulations followed.  status[0] is SD6 and status[1] is SIP
        pygame.draw.circle(self.image, color, [8, 8], 5)
        if self.status[0] == True:
            pygame.draw.circle(self.image, BLACK, [8, 8], 8, 1)
        self.rect = self.image.get_rect()
        self.radius = 8
        self.color = color
        self.go = True
        self.start = start
        self.rect.x = start[0]
        self.rect.y = start[1]
        self.gps = start
        self.time = 0
        self.target = target
        self.pos = start

    # Sets the Status of the Person (Sick, Infected, Immune, etc.)
    def set_status(self, color, time):
        temp = self.gps
        tempX = self.rect.x
        tempY = self.rect.y
        self.__init__(color, self.start, 5, self.target, self.status)
        self.time = time
        self.gps = temp
        self.rect.x = tempX
        self.rect.y = tempY

    # Returns keywords depending on the status of the Person
    def get_status(self):
        if self.color == RED:
            return "s"
        if self.color == BLUE:
            return "u"
        if self.color == ORANGE:
            return "in"
        if self.color == BLACK:
            return "d"
        if self.color == GREEN:
            return "i"

    # Moves the people towards thier Dest at a constant speed
    def move(self):
        if self.get_status() == "s" or self.get_status() == "d":
            return
        if self.status[1]:
            return
        if not(self.go):
            return

        distX = abs(self.target[0] - self.start[0])
        distY = abs(self.target[1] - self.start[1])

        if self.gps[0] > self.target[0]:
            distX = -distX
        if self.gps[0] == self.target[0]:
            distX = 0

        if self.gps[1] > self.target[1]:
            distY = -distY
        elif self.gps[1] == self.target[1]:
            distY = 0

        dx = distX
        nx = self.gps[0] + (.01 * dx)
        dy = distY
        ny = self.gps[1] + (.01 * dy)
        self.pos = [int(round(nx)), int(round(ny))]
        self.gps = [nx, ny]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        temp_1 = self.pos[0] - self.target[0]
        temp_2 = self.pos[1] - self.target[1]

        if math.hypot(temp_1, temp_2) <= 5:
            self.gps = self.target
            self.pos = self.target
            self.rect.x = self.target[0]
            self.rect.y = self.target[1]
            temp = self.start
            self.start = self.target
            self.target = temp

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 500:
            self.rect.y = 500
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 500:
            self.rect.x = 500

    # Checks where the next move will put the ball
    def next_step(self):
        dx = self.target[0] - self.start[0]
        nx = round(self.gps[0] + .01 * dx)
        dy = self.target[1] - self.start[1]
        ny = round(self.gps[1] + .01 * dy)
        return [int(nx), int(ny)]