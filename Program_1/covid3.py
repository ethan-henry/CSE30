import pygame
pygame.init()
import math
from dot import Ball
import random

store_hist = []

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

people = people = int(input("Enter Number of people (Not Recommended to go over 500): "))
all_sprites = pygame.sprite.Group()
size = (1500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Scenario 3")
screen.fill(WHITE)

x = 501
draw = True
max_s = 0
max_in = 0

time = 0
ball = []
start = []
end = []
num = 0
num_2 = 0


while num < people:
    num_2 = 0
    startY = random.choice(range(0, 490, 5))
    startX = random.choice(range(0, 490, 5))
    destX = random.choice(range(0, 490, 5))
    destY = random.choice(range(0, 490, 5))

    while num_2 < num:
        start_coordX = startX - start[num_2][0]
        start_coordY = startY - start[num_2][1]
        coord = math.hypot(start_coordX, start_coordY)
        if coord <= 15:
            startY = int(random.choice(range(0, 490, 5)))
            startX = int(random.choice(range(0, 490, 5)))
            num_2 = 0
            continue
        num_2 += 1
    start.append([startX, startY])
    num_2 = 0
    while num_2 < num:
        end_coordX = destX - end[num_2][0]
        end_coordY = destY - end[num_2][1]
        coord = math.hypot(end_coordX, end_coordY)
        if coord <= 15:
            destY = int(random.choice(range(0, 490, 5)))
            destX = int(random.choice(range(0, 490, 5)))
            num_2 = 0
            continue
        num_2 += 1
    end.append([destX, destY])
    if num == 94:
        ball.append(Ball(RED, [startX, startY], 5, [destX, destY]))
    elif num < 75:
        ball.append(Ball(BLUE, [startX, startY], 5, [destX, destY], [True, True]))
    else:
        if num < 97:
            ball.append(Ball(BLUE, [startX, startY], 5, [destX, destY], [True, False]))
        else:
            ball.append(Ball(BLUE, [startX, startY], 5, [destX, destY], [False, False]))
    all_sprites.add(ball[num])
    num += 1

num = 0
available = list(range(0, people, 1))

while num < 5:
    rand = random.choice(available)
    if not (ball[rand].get_status() == "s"):
        available.remove(rand)
        ball[rand].set_status(GREEN, 0)
    num += 1

carryOn = True
clock = pygame.time.Clock()

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    for ball in all_sprites:
        for other in all_sprites:
            if not(other == ball):

                rand_dead = random.choice(range(1, 101, 1))
                if ball.get_status() == "s" and (time - ball.time >= 10):
                    if rand_dead <= 2:
                        temp = list(ball.rect.center)
                        ball.set_status(BLACK, time)
                        ball.rect.center = temp
                    else:
                        ball.set_status(GREEN, time)
                if ball.get_status() == "in":
                    if time - ball.time >= 5:
                        rand_sick = random.choice([1, 2])
                        if rand_sick == 1:
                            temp = ball.rect.center
                            ball.set_status(RED, time)
                            ball.rect.center = temp

                    if time - ball.time >= 15:
                        rand_sick = random.choice([1, 2])
                        if rand_sick == 2:
                            ball.set_status(GREEN, time)

                move1 = ball.next_step()[0] - other.next_step()[0]
                move2 = ball.next_step()[1] - other.next_step()[1]

                dist = math.hypot(move1, move2)
                if ((ball.status[0] or other.status[0]) and dist < 16):                                                 # Collision Avoidance
                    rand = random.choice([1, 2])
                    if not (ball.get_status() == "d") and not (other.get_status() == "d") and (
                            not (ball.get_status() == "s") or not (other.get_status() == "s")):
                        if ball.get_status() == "s":
                            rand = 1
                        elif other.get_status() == "s":
                            rand = 2
                        if ball.rect.x >= 490 or ball.rect.x <= 10 or ball.rect.y >= 490 or ball.rect.y <= 10:
                            rand = 1
                        elif other.rect.y >= 490 or other.rect.y <= 10 or other.rect.x <= 10 or other.rect.x >= 490:
                            rand = 2
                        if ball.status[1]:
                            rand = 1
                        elif other.status[1]:
                            rand = 2

                        if rand == 1:
                            ball.go = False
                            if ball.next_step()[0] > other.next_step()[0]:
                                other.rect.x -= 1
                            elif ball.next_step()[0] < other.next_step()[0]:
                                other.rect.x += 1
                            if other.next_step()[1] < ball.next_step()[1]:
                                other.rect.y -= 1
                            elif other.next_step()[1] > ball.next_step()[1]:
                                other.rect.y += 1
                            other.gps[0] = other.rect.x
                            other.gps[1] = other.rect.y
                            other.pos[0] = other.rect.x
                            other.pos[1] = other.rect.y

                        if rand == 2:
                            other.go = False
                            if ball.next_step()[0] > other.next_step()[0]:
                                ball.rect.x += 1
                            elif ball.next_step()[0] < other.next_step()[0]:
                                ball.rect.x -= 1
                            if ball.next_step()[1] > other.next_step()[1]:
                                ball.rect.y += 1
                            elif ball.next_step()[1] < other.next_step()[1]:
                                ball.rect.y -= 1
                            ball.gps[0] = ball.rect.x
                            ball.gps[1] = ball.rect.y
                            ball.pos[0] = ball.rect.x
                            ball.pos[1] = ball.rect.y

                if pygame.sprite.collide_circle(ball, other):                                                           # Testing if dot gets infected
                    if (ball.get_status() == "in"  or ball.get_status() == "s") and not(other.get_status() == "in" or other.get_status() == "d" or other.get_status() == "i" or other.get_status() == "s") :
                        rand = random.choice(range(1, 11, 1))

                        if rand > 2:
                            temp = other.rect.center
                            temp_2 = ball.rect.center
                            other.set_status(ORANGE, time)
                            other.rect.center = temp
                            ball.rect.center = temp_2
                    elif (other.get_status() == "in" or other.get_status() == "s") and not(ball.get_status() == "in" or ball.get_status() == "d" or ball.get_status() == "i" or ball.get_status() == "s"):
                        rand = random.choice(range(1, 10, 1))
                        if rand > 2:
                            temp = ball.rect.center
                            temp_2 = other.rect.center
                            ball.set_status(ORANGE, time)
                            ball.rect.center = temp
                            other.rect.center = temp_2
        ball.move()
        ball.go = True
        other.go = True
    clock.tick(20)
    all_sprites.update()
    pygame.draw.rect(screen, WHITE, [0, 0, 500, 500])
    all_sprites.draw(screen)
    pygame.display.flip()
    time += .05

    dead = 0
    infected = 0
    sick = 0
    immune = 0
    healthy = 0

    for peeps in all_sprites:                                                                                           # Helps generate Histogram
        temp = peeps.get_status()
        if temp == "d":
            dead += 1
        elif temp == "in":
            infected += 1
        elif temp == "s":
            sick += 1
        elif temp == "i":
            immune += 1
        elif temp == "u":
            healthy += 1

    if sick > max_s:
        max_s = sick
    if infected > max_in:
        max_in = infected

    if (sick + infected == 0) and draw:
        draw = False
        print("SIMULATION FINISHED")
        print("MAX NUMBER OF SICK PEOPLE AT ONE TIME: {}\nMAX NUMBER OF INFECTED PEOPLE AT ONE TIME: {}".format(max_s, max_in))
        print("TIME OF SIMULATION: {}".format(x))

    if draw:                                                                                                            #drawing Histogram
        pygame.draw.line(screen, ORANGE, [int(x), 500], [int(x), 500 - ((infected))], 1)
        pygame.draw.line(screen, RED, [int(x), 500 - infected], [int(x), 500 - (sick + infected)])
        temp_1 = (sick + infected)
        pygame.draw.line(screen, BLUE, [int(x), 500 - temp_1], [int(x), (500 - (temp_1 + healthy))], 1)
        temp_2 = sick + infected + healthy
        pygame.draw.line(screen, BLACK, [int(x), 500 - temp_2], [int(x), (500 - (temp_2 + dead))], 1)
        temp_3 = sick + infected + healthy + dead
        pygame.draw.line(screen, GREEN, [int(x), 500 - (temp_3)], [int(x), 500 - (temp_3 + immune)], 1)
    x += 1
    pygame.draw.line(screen, BLACK, [500, 0], [500, 500], 1)
    pygame.display.flip()





