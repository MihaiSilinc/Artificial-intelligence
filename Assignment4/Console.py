import copy
import time
from random import randint
from typing import List

import numpy as np
import pygame

from domain.Ant import Ant
from utilities import *

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 255, 0)


class Console:
    def __init__(self, service):
        self.service = service

    def epoca(self, noAnts, alpha, beta, q0, ovidiu, adjacency_matrix: List, current_pheromone: List,
              sensor_nr: int, energy: int):

        antSet = []
        for id in np.random.choice([i for i in range(sensor_nr)], noAnts, False):
            antSet.append(Ant(adjacency_matrix, current_pheromone, id, sensor_nr, energy))

        for i in range(sensor_nr):
            # degradare
            minim = 1
            should_increase = False
            for i in range(sensor_nr):
                for j in range(sensor_nr):
                    current_pheromone[i][j] *= ovidiu
                    if current_pheromone[i][j] < minim and current_pheromone[i][j] != 0:
                        minim = current_pheromone[i][j]

            for i in range(sensor_nr):
                for j in range(sensor_nr):
                    current_pheromone[i][j] /= minim

            for x in antSet:
                x.addMove(q0, alpha, beta)
                current_position = x.current_sensor_id
                last_position = x.path[-1]
                current_pheromone[last_position][current_position] += (1 - ovidiu) * (
                        1 / adjacency_matrix[last_position][current_position])

        # return best ant path
        f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
        f = min(f)
        return antSet[f[1]].path, f[0]

    def main(self, adjacency_matrix, current_pheromone, sensor_nr, energy, noEpoch=100, noAnts=3, alpha=1.9, beta=0.9,
             rho=0.05, q0=0.5):
        sol = []
        bestSol = []
        best_fitness = 99999
        print("Programul ruleaza! Dureaza ceva timp pana va termina!")
        for i in range(noEpoch):
            print("Suntem la epoca", i)
            sol, fitness = self.epoca(noAnts, alpha, beta, q0, rho, adjacency_matrix, current_pheromone, sensor_nr,
                                      energy)
            if fitness < best_fitness:
                bestSol = copy.deepcopy(sol)
                best_fitness = fitness
                print("best changed:", bestSol, best_fitness)

        print("Drumul detectat este:", bestSol)

        return bestSol

    def image(self, currentMap, colour=BLUE, background=WHITE, sensor_colour=GREEN):
        # creates the image of a map

        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        sensor.fill(sensor_colour)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if currentMap.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                if currentMap.surface[i][j] == 2:
                    imagine.blit(sensor, (j * 20, i * 20))
        return imagine

    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with AE")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        return screen

    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()

    def movingDrone(self, currentMap, path, iteration=-1, speed=.4):
        # animation of a drone on a path
        screen = self.initPyGame((currentMap.n * 20, currentMap.m * 20))
        if iteration >= 0:
            pygame.display.set_caption(str('iteration: ' + str(iteration)))
        drona = pygame.image.load("drona.png")
        mark = pygame.Surface((20, 20))
        mark.fill(RED)
        for i in range(len(path)):
            screen.blit(self.image(currentMap), (0, 0))
            screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
            pygame.display.flip()
            time.sleep(0.5 * speed)
        for move in path:
            if currentMap.surface[move[0]][move[1]] != 2:
                screen.blit(mark, (move[1] * 20, move[0] * 20))
        pygame.display.flip()

        self.closePyGame()

    def run(self):

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        # main loop
        # while running:
        #     # event handling, gets all event from the event queue
        #     for event in pygame.event.get():
        #         # only do something if the event is of type QUIT
        #         if event.type == pygame.QUIT:
        #             # change the value to False, to exit the main loop
        #             running = False
        #
        #         if event.type == KEYDOWN:
        #             d.move(m) #this call will be erased
        #
        #
        # screen.blit(self.service.repo.drone.mapWithDrone(self.service.repo.mapM.image()), (0, 0))
        # pygame.display.flip()

        start_x = randint(0, 19)
        start_y = randint(0, 19)
        while self.service.repo.mapM.surface[start_x][start_y] == 1:
            start_x = randint(0, 19)
            start_y = randint(0, 19)

        nr_sensors = 20

        ok = 0
        while ok == 0:
            for i in range(self.service.repo.mapM.n):
                for j in range(self.service.repo.mapM.m):
                    if self.service.repo.mapM.surface[i][j] == 2:
                        self.service.repo.mapM.surface[i][j] = 0

            ok = 1
            all_paths = []
            sensors = []

            adjacency_matrix = []

            for i in range(nr_sensors):
                init_list = []
                for j in range(nr_sensors):
                    init_list.append(float("inf"))
                adjacency_matrix.append(init_list)

            for id in range(nr_sensors):
                x = randint(0, 19)
                y = randint(0, 19)
                while self.service.repo.mapM.surface[x][y] == 1 or self.service.repo.mapM.surface[x][y] == 2:
                    x = randint(0, 19)
                    y = randint(0, 19)
                self.service.repo.mapM.surface[x][y] = 2
                sensors.append([x, y])

            for i in range(nr_sensors):
                for j in range(i + 1, nr_sensors):
                    start_sensor = sensors[i]
                    end_sensor = sensors[j]
                    path = self.service.aStarSearch(start_sensor[0], start_sensor[1], end_sensor[0], end_sensor[1])
                    if path is None:
                        ok = 0
                    else:
                        adjacency_matrix[i][j] = len(path) - 1
                        adjacency_matrix[j][i] = len(path) - 1

                        all_paths.append([i, j, path])

        current_pheromone = []

        for i in range(nr_sensors):
            init_list = []
            for j in range(nr_sensors):
                init_list.append(1 / adjacency_matrix[i][j])
            current_pheromone.append(init_list)

        total_pheromone = []

        for i in range(nr_sensors):
            init_list = []
            for j in range(nr_sensors):
                init_list.append(0)
            total_pheromone.append(init_list)

        for x in adjacency_matrix:
            print(x)
        for x in current_pheromone:
            print([float("{:.2f}".format(a)) for a in x])

        for x in total_pheromone:
            print(x)

        for path in all_paths:
            print(path)

        energy = 10000

        running = True
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            screen.blit(self.service.repo.drone.mapWithDrone(self.service.repo.mapM.image()), (0, 0))
            screen.blit(self.image(self.service.repo.mapM), (0, 0))
            pygame.display.flip()

        # def main(self, adjacency_matrix, current_pheromone, sensor_nr, energy, noEpoch=100, noAnts=3, alpha=1.9, beta=0.9,

        best_sol = self.main(adjacency_matrix, current_pheromone, nr_sensors, energy)

        full_path = []
        for index in range(nr_sensors - 1):
            for path in all_paths:
                if [path[0], path[1]] == [best_sol[index], best_sol[index + 1]]:
                    full_path += copy.deepcopy(path[2])
                    continue
                elif [path[1], path[0]] == [best_sol[index], best_sol[index + 1]]:
                    p = copy.deepcopy(path[2])
                    p.reverse()
                    full_path += p
                    continue
        print(full_path)
        self.movingDrone(self.service.repo.mapM, full_path)
