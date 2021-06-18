# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np

from controller.controller import Service
from domain.Drone import *
from domain.Map import *
from controller import *

# define a main function
from domain.Drone import Drone


class Console:
    def __init__(self, service):
        self.service = service


    def run(self):
        m = Map()
        # m.randomMap()
        # m.saveMap("test2.map")
        m.loadMap("test1.map")

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)

        # create drona
        d = Drone(x, y)

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)
        m.surface[2][4] = 2
        running = True
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        print('path for A*')
                        finished = self.service.searchAStar(m, d, d.x, d.y, 2, 4, self.service.heuristic)
                        if finished != False:
                            for pos in finished:
                                if m.surface[pos[0]][pos[1]] == 3 or m.surface[pos[0]][pos[1]] == 5:
                                    m.surface[pos[0]][pos[1]] = 5
                                else:
                                    m.surface[pos[0]][pos[1]] = 4

                    if event.key == pygame.K_DOWN:
                        print('path for greedy')
                        finished3 = self.service.searchGreedy(m, d, d.x, d.y, 2, 4, self.service.heuristic)
                        print(finished3)
                        if finished3 != False:
                            for pos in finished3:
                                if m.surface[pos[0]][pos[1]] == 4 or m.surface[pos[0]][pos[1]] == 5:
                                    m.surface[pos[0]][pos[1]] = 5
                                else:
                                    m.surface[pos[0]][pos[1]] = 3

            screen.blit(d.mapWithDrone(m.image()), (0, 0))
            pygame.display.flip()