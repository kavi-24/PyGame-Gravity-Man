# Project: Gravity Man

import random
import time
import math

import pygame
from pygame import mixer

pygame.init()
pygame.font.init()
mixer.init()

WIDTH = 800
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAVITY MAN")
font = pygame.font.SysFont("comicsans", 67)


class Man:
    global imgIdx

    def __init__(self, img, y, rotated) -> None:
        self.x = 25
        self.y = y
        self.img = img
        self.rotated = rotated
        self.imgIdx = imgIdx
        self.speed = 1.2

    def draw(self) -> None:
        if not self.rotated:
            screen.blit(self.img, (self.x, self.y))
        else:
            screen.blit(pygame.transform.rotate(pygame.transform.flip(
                self.img, True, False), 180), (self.x, self.y))

    def move(self) -> None:
        if not self.rotated:
            if self.y + self.img.get_height() >= HEIGHT-platformImg.get_height():
                self.y = HEIGHT - self.img.get_height() - platformImg.get_height()
            else:
                self.y += self.speed
        else:
            if self.y <= platformImg.get_height():
                self.y = platformImg.get_height()
            else:
                self.y -= self.speed

        self.draw()

    def change_img(self) -> None:
        self.imgIdx += 1
        self.img = gManImg[self.imgIdx % len(gManImg)]

    def update(self) -> None:
        self.move()


class Platform:

    def __init__(self, x, img) -> None:
        self.x = x
        self.img = img
        self.speed = 1

    def move(self) -> None:
        self.x -= self.speed
        if self.x + self.img.get_width() <= 0:
            self.x = WIDTH

    def draw(self):
        screen.blit(self.img, (self.x, 0))
        screen.blit(self.img, (self.x, HEIGHT - self.img.get_height()))

    def update(self):
        self.move()
        self.draw()


class BG:

    def __init__(self, x, img) -> None:
        self.x = x
        self.img = img
        self.speed = 1

    # def move(self) -> None:
    #     self.x -= self.speed
    #     if self.x + self.img.get_width() < 0:
    #         self.x = WIDTH

    def draw(self):
        # screen.blit(self.img, (self.x, 0))
        screen.blit(self.img, (0, 0))

    def update(self):
        # self.move()
        self.draw()


class Obstacle:

    def __init__(self) -> None:
        self.x = WIDTH
        self.width = 10
        self.speed = 1

        gap = gManImg[imgIdx].get_height() + 175

        self.height1 = random.randrange(
            platformImg.get_height(), HEIGHT - platformImg.get_height() - gap - 30)
        self.height2 = HEIGHT - gap - self.height1 - platformImg.get_height()

        self.y1 = platformImg.get_height()
        self.y2 = self.y1 + self.height1 + gap - platformImg.get_height()

        self.color = (0, 0, 0)

    def draw(self):
        self.x -= self.speed

        self.rectTop = pygame.Rect(self.x, self.y1, self.width, self.height1)
        if self.height2 < 0:
            self.rectBotton = pygame.Rect(self.x, self.y2, self.width, 0)
        else:
            self.rectBotton = pygame.Rect(
                self.x, self.y2, self.width, self.height2)

        pygame.draw.rect(screen, self.color, self.rectTop)
        pygame.draw.rect(screen, self.color, self.rectBotton)


def collide(a: Man, b: Obstacle):

    collide_x = a.x < b.x < a.x + a.img.get_width()
    collide_y = not(a.y > b.y1 + b.height1 and (a.y + a.img.get_height()
                    < 0 if b.height2 < 0 else a.y + a.img.get_height() < b.y2))

    if collide_x:
        if collide_y:
            return True
    return False


def paused():
    text = font.render("PAUSED", 1, (255, 0, 0))
    screen.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))


def pause_text():
    text = pygame.font.SysFont("comicsans", 20).render("PRESS P TO PAUSE", 1, (0, 0, 0))
    screen.blit(text, (WIDTH - text.get_width() - 10, 30))


def game_over():
    song = mixer.Sound("./hit.mp3")
    song.set_volume(0.4)
    song.play()

    text = font.render("GAME OVER", 1, (255, 0, 0))
    screen.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))


clock = pygame.time.Clock()


def main():

    global imgIdx, platformImg, gManImg, run, man, obstacles, obstacle, OBSTACLE, RUN, platforms, bgImg, bg

    try:
        gManImg = [pygame.image.load("./GMan1.png"), pygame.image.load(
            "./GMan2.png"), pygame.image.load("./GMan3.png"), pygame.image.load("./GMan4.png")]
    except:
        import os
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        gManImg = [pygame.image.load("./GMan1.png"), pygame.image.load(
            "./GMan2.png"), pygame.image.load("./GMan3.png"), pygame.image.load("./GMan4.png")]

    imgIdx = 0

    platformImg = pygame.image.load("./platform.png")
    bgImg = pygame.image.load("./bg.png")

    RUN = pygame.USEREVENT
    pygame.time.set_timer(RUN, 100)

    OBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(OBSTACLE, 1500)

    man = Man(gManImg[imgIdx], HEIGHT -
              platformImg.get_height() - gManImg[imgIdx].get_height(), False)
    platforms = [Platform(0, platformImg), Platform(WIDTH, platformImg)]
    bg = BG(0, bgImg)
    obstacles = []
    while True:
        screen.fill((255, 255, 255))
        text = font.render("PRESS SPACE TO START", False, (200, 200, 200))
        screen.blit(text, (0, 300 + (math.sin(time.time() * 10) * 5)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                obstacles.clear()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mainloop()
                    return
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.update()


def mainloop():

    # Get FPS
    # fps = clock.get_fps()

    run = True
    pause = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                obstacles.clear()
                run = False

            if event.type == RUN:
                man.change_img()

            if event.type == OBSTACLE and not pause:
                obstacles.append(Obstacle())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    song = mixer.Sound("./jump.mp3")
                    song.set_volume(0.4)
                    song.play()
                    man.rotated = not man.rotated
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_ESCAPE:
                    obstacles.clear()
                    run = False

        if not pause:

            screen.fill((255, 255, 255))

            bg.update()
            man.update()
            pause_text()

            for platform in platforms:
                platform.update()

            for obstacle in obstacles:

                if collide(man, obstacle):
                    game_over()
                    run = False
                    main()

                if obstacle.x <= 0:
                    obstacles.remove(obstacle)
                obstacle.draw()

        else:
            paused()

        pygame.display.update()


main()
