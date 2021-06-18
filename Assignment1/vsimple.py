

# import the pygame module, so you can use it
import pickle,pygame,sys
import time

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

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Environment():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill :
                    self.__surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string
                
    def readUDMSensors(self, x,y):
        readings=[0,0,0,0]
        # UP 
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__n) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__m) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1
     
        return readings
    
    def saveEnvironment(self, numFile):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine

    def get_rows(self):
        return self.__n

    def get_columns(self):
        return self.__m
        
        
class DMap():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1
        
        
    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the wals that you detect
        wals = e.readUDMSensors(x, y)
        i = x - 1
        if wals[UP] > 0:
            while ((i>=0) and (i >= x - wals[UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i>=0):
            self.surface[i][y] = 1
            
        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self.__n) and (i <= x + wals[DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1
            
        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self.__m) and (j <= y + wals[LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1
        
        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1
        
        return None
        
    def image(self, x, y):
        
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        empty = pygame.Surface((20,20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)
        
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                elif (self.surface[i][j] == 0):
                    imagine.blit(empty, ( j * 20, i * 20))
                
        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y *20, x*20))
        return imagine
        
        
class Drone():
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.visited = {}
        self.environment = environment
        self.stack = []
        # we need to be able to go back if the drone gets stuck, so we create a traceback
        self.prev_visited = []

        self.dfs_started = False
        self.going_back = False
        self.next = None

        # we initialize the visited dict with False on all positions
        for i in range(self.environment.get_rows()):
            for j in range(self.environment.get_columns()):
                self.visited[(i, j)] = False

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
              if pressed_keys[K_LEFT]and detectedMap.surface[self.x][self.y-1]==0:
                  self.y = self.y - 1
        if self.y < 19:        
              if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                  self.y = self.y + 1

# we check if the next move is available or if we need to perform traceback

    def check_move(self, x, y):
        # if (self.x + self.y) - (x + y) != 1 and (self.x + self.y) - (x + y) != -1:
        #     return False
        # else:
        #     return True
        if abs(self.x - x) + abs(self.y - y) < 2:
            return True
        else:
            return False

    def moveDSF(self, detectedMap):
        if not self.dfs_started:
            self.visited[(self.x, self.y)] = True
            self.prev_visited.append((self.x, self.y))
            available_squares = self.environment.readUDMSensors(self.x, self.y)

            if available_squares[UP] != 0:
                if not self.visited[(self.x - 1, self.y)]:
                    self.stack.append((self.x - 1, self.y))
            if available_squares[DOWN] != 0:
                if not self.visited[(self.x + 1, self.y)]:
                    self.stack.append((self.x + 1, self.y))
            if available_squares[LEFT] != 0:
                if not self.visited[(self.x, self.y + 1)]:
                    self.stack.append((self.x, self.y + 1))
            if available_squares[RIGHT] != 0:
                if not self.visited[(self.x, self.y - 1)]:
                    self.stack.append((self.x, self.y - 1))
            self.dfs_started = True

        # we check if the stack is empty
        if len(self.stack) == 0:
            return True

        # we move the drone
        if not self.going_back:
            self.next = self.stack.pop()

        if self.check_move(self.next[0], self.next[1]):
            self.going_back = False
            self.prev_visited.append((self.x, self.y)) # we add a tuple of the previous visited point
            self.x = self.next[0]
            self.y = self.next[1]
        else:
            self.x, self.y = self.prev_visited.pop()
            self.going_back = True
            return

        self.visited[self.next] = True
        detectedMap.markDetectedWalls(self.environment, self.x, self.y)
        available_squares = self.environment.readUDMSensors(self.x, self.y)
        if available_squares[UP] != 0:
            if not self.visited[(self.x - 1, self.y)]:
                self.stack.append((self.x - 1, self.y))
        if available_squares[DOWN] != 0:
            if not self.visited[(self.x + 1, self.y)]:
                self.stack.append((self.x + 1, self.y))
        if available_squares[LEFT] != 0:
            if not self.visited[(self.x, self.y + 1)]:
                self.stack.append((self.x, self.y + 1))
        if available_squares[RIGHT] != 0:
            if not self.visited[(self.x, self.y - 1)]:
                self.stack.append((self.x, self.y - 1))

                  
# define a main function
def main():
    #we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    #print(str(e))
    
    # we create the map
    m = DMap() 
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")
        
    
    
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #cream drona
    d = Drone(x, y, e)
    
    
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800,400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0,0))
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == KEYDOWN:
                # use this function instead of move
                while True:
                    time.sleep(0.1)
                    dfs = d.moveDSF(m)
                    if dfs:
                        break
                    m.markDetectedWalls(e, d.x, d.y)
                    screen.blit(m.image(d.x,d.y),(400,0))
                    pygame.display.flip()
       
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()