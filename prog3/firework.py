# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:07:14 2020
CSE 30 Spring 2020 Program 3 starter code
@author: Fahim
"""
import math
import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
pygame.mixer.init()
sound = pygame.mixer.Sound("Sound Folder/explode.wav")
cheer3 = pygame.mixer.Sound("Sound Folder/cheer3.wav")
cheer4 = pygame.mixer.Sound("Sound Folder/cheer4.wav")
cheer5 = pygame.mixer.Sound("Sound Folder/cheer5.wav")
whistle = pygame.mixer.Sound("Sound Folder/whistle.wav")
BGM = pygame.mixer.Channel(1)
bgm = pygame.mixer.Sound("Sound Folder/BGM.wav")
bgm.set_volume(.25)
BGM.queue(bgm)
whistle.set_volume(.25)
cheer3.set_volume(.25)
cheer4.set_volume(.25)
cheer5.set_volume(.25)
sound.set_volume(.25)


class Firework:
    def __init__(self, nump, type, startTime, endTime, startPOS, length, level = 0, split = False, color = 0):
        self.nump = nump
        self.plist = []
        self.color = color
        self.length = length
        self.startTime = startTime
        self.splitf = split
        self.type = type
        self.endTime = endTime
        self.startPOS = startPOS
        self.level = level
        self.first = True
        for i in range(nump):
          if color == 0:
              self.color = [random.random(), random.random(), random.random(), 1]
          self.plist.append(Particle(self.length, self.type, (self.endTime - self.startTime), self.endTime, self.startPOS[0], self.startPOS[1], self.startPOS[2], self.color, self.splitf, self.level, self.nump))
    def render(self, simtime, level = 0):
        if simtime > self.endTime and self.level < 1 and self.splitf:
            for i in range(len(self.plist)):
                self.plist[i].firework.render(simtime)
        if (simtime > self.endTime + 1 or simtime < self.startTime) or self.level > 1:
            return
        glEnable(GL_POINT_SMOOTH)
        glPointSize(3)
        glBegin(GL_POINTS)
        total = []
        new = []
        if self.plist[0].length <= len(self.plist[0].tail):
            for i in range(len(self.plist)):
                for p in range(0, self.plist[i].length):
                    self.plist.append(self.plist[i].tail[p])
                    total.append(self.plist[i].tail[p])

        for p in range(len(self.plist)):
            if self.plist[p].y >= 0:
                glColor4fv([self.plist[p].color[0], self.plist[p].color[1], self.plist[p].color[2], 2 / (self.length - (p % self.length))])
                glVertex3fv((self.plist[p].x, self.plist[p].y, self.plist[p].z))
                self.plist[p].update(self.type)
        for i in range(len(self.plist)):
            if not(self.plist[i] in total):
                new.append(self.plist[i])
        self.plist = new
        glEnd()

class Particle:
    def __init__(self, length, type, span, endTime,  x=0, y=0, z=0, color=(0, 0, 0, 1), split = False, level = 1, nump = 1):
        self.x = x
        self.y = y
        self.z = z
        self.nump = nump
        self.type = type
        self.endTime = endTime
        self.span = span
        self.split = split
        self.length = length
        self.tail = []
        self.simtime = 0
        self.color = color
        self.exploded = False
        self.first = True
        self.level = level + 1
        self.whistle = True
        self.velocity = [random.uniform(-.01, .01), random.uniform(-.01, .01), random.uniform(-.01, .01)]

    def update(self, type):
        new = Particle(self.length, self.type, self.span, self.endTime, self.x, self.y, self.z, (self.color[0], self.color[1], self.color[2], 1), False, self.level - 1, self.nump)
        new.velocity[1] = self.velocity[1]
        new.velocity[0] = self.velocity[0]
        new.velocity[2] = self.velocity[2]
        new.simtime = self.simtime
        self.tail.append(new)
        if (self.level <= 1 and self.simtime >= 75 and self.y >= 10) or (self.level > 1):
            self.exploded = True
            if self.first:
                self.first = False
                whistle.stop()
                sound.play()                                                                                            # plays sound
                print(cheer3.get_num_channels(), cheer4.get_num_channels(), cheer5.get_num_channels())
                cheer = random.choice([3, 4, 5])
                if cheer == 3:
                    cheer3.play()
                elif cheer == 4:
                    cheer4.play()
                elif cheer == 5:
                    cheer5.play()

        if self.exploded:
            self.x += self.velocity[0]
            self.y += self.velocity[1] - (.00004 * self.simtime)
            self.z += self.velocity[2]
        else:
            if self.whistle and not(self.exploded):
                whistle.play()
                self.whistle = False
            if type == "normal":
                self.start()
            elif type == "spin":
                self.start_spin()
        self.simtime += 1
        if self.split and self.level <= 1:
            if self.split:
                self.firework = Firework(self.nump, self.type, self.endTime, self.span + self.endTime, [self.x, self.y, self.z], self.length, self.level, True, self.color)
    def start(self):
        self.y += .1
    def start_spin(self):
        self.y += 0.05
        self.x = math.cos(self.simtime / 4)
        self.z = math.sin(self.simtime / 4)


def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((10, 0, 10))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-10, 0, 10))  # If you want to be fancy, you can replace this method
    glVertex3fv((-10, 0, -10))  # to draw the terrain from your prog1 instead.
    glVertex3fv((10, 0, -10))
    glEnd()

def main():
    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, -5, -25)

    play = True
    sim_time = 0

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()
    firework = Firework(5, "spin", 50, 500, [5, 5, 5], 50, 0, True)
    firework2 = Firework(5, "normal", 450, 950, [0, 0, 0], 50, 0, True, (.5, .5, 1, 1))

    while play:
        BGM.queue(bgm)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10, 0, 1, 0)

                if event.key == pygame.K_UP:
                    glRotatef(-10, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glRotatef(0.10, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain()

        firework.render(sim_time)
        firework2.render(sim_time)
        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()