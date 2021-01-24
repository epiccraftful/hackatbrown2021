# -----------------------------------------------------------------------------
#
# Two Ball
# version: 1.0
# Language - Python
# Modules - pygame, sys, random, math
#
# Controls - click to place ball, drag to aim, release to throw, have fun :)
#
# By - Malachi Hornbuckle, James Lu
# Brown University '22
#
# Adapted from - Jatin Kumar Mandav's 8 Ball Pool
# https://jatinmandav.wordpress.com
#
# -----------------------------------------------------------------------------

import pygame
import sys
from math import *
import random

pygame.init()
width = 660
height = 360
outerHeight = 400
margin = 30
display = pygame.display.set_mode((width, outerHeight))
pygame.display.set_caption("2 balls, 1 friends")
clock = pygame.time.Clock()

background = (2, 84, 20)
white = (236, 240, 241)

gray = (123, 125, 125)
black = (0,0,0)
orange = (245, 128, 37)
brown = (78, 54, 41)

colors = [orange,brown]

balls = []
noBalls = 2
radius = 10
friction = 0.01 # make bigger?

# Ball Class
class Ball:
    def __init__(self, x, y, speed, color, angle, ballNum):
        self.x = x + radius
        self.y = y + radius
        self.color = color
        self.angle = angle
        self.speed = speed
        self.ballNum = ballNum
        self.font = pygame.font.SysFont("Agency FB", 10)

    # Draws Balls on Display Window
    def draw(self, x, y):
        pygame.draw.ellipse(display, self.color, (x - radius, y - radius, radius*2, radius*2))


    # Moves the Ball around the Screen
    def move(self):
        self.speed -= friction
        if self.speed <= 0:
            self.speed = 0
        self.x = self.x + self.speed*cos(self.angle) #add time resolution?
        self.y = self.y + self.speed*sin(self.angle)

        if not (self.x < width - radius - margin):
            self.x = width - radius - margin
            self.angle = pi - self.angle
        if not(radius + margin < self.x):
            self.x = radius + margin
            self.angle = pi - self.angle
        if not (self.y < height - radius - margin):
            self.y = height - radius - margin
            self.angle = 2*pi - self.angle
        if not(radius + margin < self.y):
            self.y = radius + margin
            self.angle = 2*pi - self.angle

# Pocket Class
class Pockets:
    def __init__(self, x, y, color):
        self.r = margin/2
        self.x = x + self.r + 10
        self.y = y + self.r + 10
        self.color = color

    # Draws the Pockets on Pygame Window
    def draw(self):
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))

    # Checks if ball has entered the Hole
    def checkPut(self): # less complicated for 2 balls
        global balls
        orange_dist = ((self.x - balls[0].x)**2 + (self.y - balls[0].y)**2)**0.5
        if orange_dist < self.r + radius:
            gameOver()
        if len(balls) > 1:
            brown_dist = ((self.x - balls[1].x)**2 + (self.y - balls[1].y)**2)**0.5
            if brown_dist < self.r + radius:
                balls = [balls[0]] # remove red ball from balls

class Hits:
    def __init__(self, num):
        self.num = num


# Checks Collision
def collision(ball1, ball2, hits):
    dist = ((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)**0.5
    if dist <= radius*2:
        hits.num = hits.num + 1

        u1 = ball1.speed
        u1x = u1 * cos(ball1.angle)
        u1y = u1 * sin(ball1.angle)
        u2 = ball2.speed
        u2x = u2 * cos(ball2.angle)
        u2y = u2 * sin(ball2.angle)

        n_x = cos(atan2(ball2.y - ball1.y, ball2.x - ball1.x)) # ball 1 hits ball 2
        n_y = sin(atan2(ball2.y - ball1.y, ball2.x - ball1.x))

        u_change = ((u1x - u2x) * n_x) + ((u1y - u2y) * n_y) # change in velocity in normal direction (mag)

        u1x = u1x - n_x * u_change
        u1y = u1y - n_y * u_change
        u2x = u2x + n_x * u_change
        u2y = u2y + n_y * u_change

        ball1.speed = (u1x**2 + u1y**2)**0.5
        ball2.speed = (u2x**2 + u2y**2)**0.5
        ball1.angle = atan2(u1y, u1x)
        ball2.angle = atan2(u2y, u2x)

        ball2.x = ball1.x + (n_x * 2 * radius)
        ball2.y = ball1.y + (n_y * 2 * radius)


def border():
    pygame.draw.rect(display, gray, (0, 0, width, 30))
    pygame.draw.rect(display, gray, (0, 0, 30, height))
    pygame.draw.rect(display, gray, (width - 30, 0, 30, height))
    pygame.draw.rect(display, gray, (0, height - 30, width, 30))

def score(hits): # get rid of or alter this
    font = pygame.font.SysFont("Agency FB", 30)

    pygame.draw.rect(display, (51, 51, 51), (0, height, width, outerHeight))

    text = font.render("Number of Hits: " + str(hits.num), True, white)
    display.blit(text, (width/2 + 50, height + radius/2))

def reset():
    global balls, noBalls
    noBalls = 2
    balls = []
    b1 = Ball(70, height/2, 0, colors[0], 0, 1) # orange ball
    b2 = Ball(width - 70, height/2, 0, colors[1], 0, 2) # brown ball

    balls.append(b1)
    balls.append(b2)



def gameOver(): # change to the resetting conditions
    font = pygame.font.SysFont("Agency FB", 75)
    text = font.render("Sent to the shadow realm", True, (133, 193, 233))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

                if event.key == pygame.K_r:
                    poolTable()
        display.blit(text, (50, height/2))

        pygame.display.update()
        clock.tick()

def close():
    pygame.quit()
    sys.exit()

# Main Function
def poolTable():
    loop = True
    hits = Hits(0) # start with no hits

    reset()

    noPockets = 6
    pockets = []

    p1 = Pockets(0, 0, black)
    p2 = Pockets(width/2 - p1.r*2, 0, black)
    p3 = Pockets(width - p1.r - margin - 5, 0, black)
    p4 = Pockets(0, height - margin - 5 - p1.r, black)
    p5 = Pockets(width/2 - p1.r*2, height - margin - 5 - p1.r, black)
    p6 = Pockets(width - p1.r - margin - 5, height - margin - 5 - p1.r, black)

    pockets.append(p1)
    pockets.append(p2)
    pockets.append(p3)
    pockets.append(p4)
    pockets.append(p5)
    pockets.append(p6)


    start = 0
    end = 0

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

                if event.key == pygame.K_r:
                    poolTable()

            if event.type == pygame.MOUSEBUTTONDOWN: # make this stuff happen in orange ball grabbable
                start_x, start_y = pygame.mouse.get_pos()
                start = (start_x, start_y)
                if len(balls) <= 1:
                    balls.append(Ball(start_x, start_y, 0, brown, 0, 2))
                else:
                    balls[1].x = start_x
                    balls[1].y = start_y
                    balls[1].speed = 0
                mouse_loop = True
                print("click")
                while mouse_loop:
                    if balls[0].speed == 0 and hits.num > 0:
                        gameOver()
                    display.fill(background)
                    for i in range(len(balls)):
                        balls[i].draw(balls[i].x, balls[i].y)
                        balls[i].move()
                    border()
                    for i in range(noPockets):
                        pockets[i].draw()
                    for i in range(noPockets):
                        pockets[i].checkPut()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            print("clack")
                            mouse_loop = False
                    score(hits)
                    pygame.display.update()
                    clock.tick(60)
                print("knack")
                end_x, end_y = pygame.mouse.get_pos()
                end = (end_x, end_y)
                dist = ((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5
                force = dist/10.0
                if force > 20:
                    force = 20
                angle = atan2(end[1] - start[1], end[0] - start[0])
                balls[1].speed = force
                balls[1].angle = angle


        display.fill(background)

        for i in range(len(balls)):
            balls[i].draw(balls[i].x, balls[i].y)

        for i in range(len(balls)):
           balls[i].move()

        if balls[0].speed == 0 and hits.num > 0:
            gameOver()

        if len(balls) > 1:
            collision(balls[0], balls[1], hits) # change orange/brown balls if colliding
        border()

        for i in range(noPockets):
            pockets[i].draw()

        for i in range(noPockets):
            pockets[i].checkPut() # ends game if orange ball in pocket

        score(hits)

        pygame.display.update()
        clock.tick(60)

poolTable()

