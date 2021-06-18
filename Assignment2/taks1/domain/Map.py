import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255,127,80)


#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        destination = pygame.Surface((20, 20))
        roadGreedy = pygame.Surface((20, 20))
        roadAStar = pygame.Surface((20, 20))
        road = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        destination.fill(RED)
        roadGreedy.fill(GREEN)
        roadAStar.fill(GRAYBLUE)
        road.fill(ORANGE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                if (self.surface[i][j] == 2):
                    imagine.blit(destination, (j * 20, i * 20))
                if (self.surface[i][j] == 3):
                    imagine.blit(roadGreedy, (j * 20, i * 20))
                if (self.surface[i][j] == 4):
                    imagine.blit(roadAStar, (j * 20, i * 20))
                if (self.surface[i][j] == 5):
                    imagine.blit(road, (j * 20, i * 20))

        return imagine


    def get_neighbours(self, xi, yi):
        neighbours = [(xi+1, yi), (xi-1, yi), (xi, yi+1), (xi, yi-1)]
        removing_outlines = list(filter(lambda t: (0 <= t[0] <= 19 and 0 <= t[1] <= 19), neighbours))
        return list(filter(lambda t: (self.surface[t[0]][t[1]] == 0 or self.surface[t[0]][t[1]] >= 2) , removing_outlines))
