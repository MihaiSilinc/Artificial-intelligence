# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np

from console.console import Console
from controller.controller import Service
from domain.Drone import *
from domain.Map import *
from controller import *

# define a main function
from domain.Drone import Drone

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


# define a main function
def main():
    # we create the map
    # define a variable to control the main loop
    service = Service()
    console = Console(service)
    console.run()
    # path = dummysearch()
    # screen.blit(displayWithPath(m.image(), path),(0,0))

    pygame.display.flip()
    time.sleep(1)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()