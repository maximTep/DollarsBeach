import requests
from bs4 import BeautifulSoup
import re
import time
import pygame
import math
import random
import numpy
from multiprocessing import Process




start_time = time.time()
website_url = requests.get('https://ratestats.com/dollar/').text
soup = BeautifulSoup(website_url, 'lxml')
#print(soup.prettify())


# BNeawe iBp4i AP7Wnd
finds = soup.find_all('span', {'class': 'b-current-rate__value'})
#print(finds)
rez = finds[0].get('content')
#print(rez)

data = float(rez)

curDollar = data


website_url = requests.get('http://bhom.ru/currencies/usd/?startdate=month').text
soup = BeautifulSoup(website_url, 'lxml')
#print(soup.prettify())

finds = soup.find_all('div', {'class': 'stat-value stat-value-0'})
finds = finds[0]
print(finds)

rez = finds.text
print(rez)
rez = float(rez)

averageDollar = rez




running = True



pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 25)
lobster = pygame.font.SysFont('Lobster Regular 400', 20)
screenWidth = 900
screenHeight = 650
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("Simon")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
CYAN_INVIS = (0, 255, 255, 1)
YELLOW = (255, 255, 0)
ORANGE = (255, 91, 0)
HZ = (100, 100, 100)


grid = [[False for y in range(screenHeight)] for x in range(screenWidth)]


class WaterDrop:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.physics()
        self.default_speed = 3
        self.float_speed = self.default_speed
        self.speed = int(self.float_speed)

    def physics(self):
        x = self.pos[0]
        y = self.pos[1]
        #level = max(groundLevel, waterLevel)
        if y == 0:
            pass
        elif not grid[x][y+1]:
            grid[x][y] = False
            self.pos = [x, y+1]
            grid[x][y + 1] = True
        else:
            r = random.choice([-1, 1])
            if not grid[x+r][y]:
                grid[x][y] = False
                self.pos = [x + r, y]
                grid[x + r][y] = True
            elif not grid[x-r][y]:
                grid[x][y] = False
                self.pos = [x - r, y]
                grid[x - r][y] = True

        pygame.draw.line(screen, CYAN, self.pos, self.pos)


    def new_physics(self):
        x = self.pos[0]
        y = self.pos[1]
        level = max(groundLevel, waterLevel)
        if y >= screenHeight - level:
            return
        try:
            if not grid[x][y + self.speed]:
                grid[x][y] = False
                self.pos = [x, y + self.speed]
                grid[x][y + self.speed] = True
            else:
                r = random.choice([-self.speed, self.speed])
                if not grid[x + r][y]:
                    grid[x][y] = False
                    self.pos = [x + r, y]
                    grid[x + r][y] = True
                elif not grid[x - r][y]:
                    grid[x][y] = False
                    self.pos = [x - r, y]
                    grid[x - r][y] = True

        except:
            pass



        pygame.draw.line(screen, CYAN, self.pos, self.pos)


class Water:
    def __init__(self):
        self.drops = []

    def add_drop(self, x, y):
        if grid[x][y]:
            return
        self.drops.append(WaterDrop(x, y))
        grid[x][y] = True

    def add_big_drop(self, x, y, radius):
        if grid[x][y]:
            return
        self.drops.append(WaterDrop(x, y))
        grid[x][y] = True
        for i in numpy.arange(0, 2 * math.pi, 0.5):
            for j in range(1, radius):
                new_x = int(x + i * math.cos(j))
                new_y = int(y + i * math.sin(j))
                self.drops.append(WaterDrop(new_x, new_y))
                grid[new_x][new_y] = True
        #print(len(self.drops))



    def physics_flow(self):
        for drop in self.drops:
            drop.new_physics()




waterLevel = (averageDollar / 140) * screenHeight
groundLevel = (curDollar / 140) * screenHeight






if __name__ == '__main__':
    running = True
    water = Water()
    while running:
        screen.fill(WHITE)
        isPressed = pygame.mouse.get_pressed(3)[0]

        pygame.time.delay(33)
        pygame.draw.rect(screen, YELLOW, [0, screenHeight - groundLevel, screenWidth, groundLevel])
        #pygame.draw.rect(screen, CYAN_INVIS, [0, screenHeight - waterLevel, screenWidth, waterLevel])

        s = pygame.Surface((screenWidth, waterLevel))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill(CYAN)  # this fills the entire surface
        screen.blit(s, (0, screenHeight - waterLevel))

        textCurDollar = myFont.render('CurDollar ' + str(curDollar), False, (0, 0, 0))
        screen.blit(textCurDollar, (screenWidth - 250, screenHeight - groundLevel))
        textAverageDollar = myFont.render('AverageDollar ' + str(averageDollar), False, (0, 0, 0))
        screen.blit(textAverageDollar, (20, screenHeight - waterLevel))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mx, my = pygame.mouse.get_pos()

        water.physics_flow()
        if isPressed:
            water.add_big_drop(mx, my, 20)



        pygame.display.update()

    pygame.quit()













