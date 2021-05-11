import pygame
pygame.init()
from Dot_test import Ball
pygame.mixer.init()


RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

all_sprites = pygame.sprite.Group()
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Quiz 10")

ball_2 = (Ball(BLUE, [0, 0], 10, [390, 390]))
ball_1 = (Ball(BLACK, [440, 0], 10, [0, 440]))
all_sprites.add(ball_1)
all_sprites.add(ball_2)


carryOn = True

clock = pygame.time.Clock()

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    if pygame.sprite.collide_circle(ball_1, ball_2):
        sound = pygame.mixer.Sound("Cartoon Funny Bonk - Sound Effect [HD].wav")
        sound.play()
    for ball in all_sprites:
        ball.move()


    clock.tick(60)
    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

