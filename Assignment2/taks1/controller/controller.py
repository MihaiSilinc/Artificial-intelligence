import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np
from domain import Drone
from domain import Map
from domain.PriorityQueue import PriorityQueue
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
# manhattan

class Service:
    def heuristic(self, start_x, start_y, final_x, final_y):
        return abs(start_x - final_x) + abs(start_y - final_y)

    def searchGreedy(self, map, drone, start_x, start_y, final_x, final_y, heuristic):

        visited = set()
        toVisit = PriorityQueue()
        toVisit.push((start_x, start_y), heuristic(start_x, start_y, final_x, final_y))
        drone.roadGreedy[(start_x, start_y)] = None
        found = False

        while((not toVisit.isEmpty()) and (not found)):
            if toVisit.isEmpty():
                return False

            node = toVisit.pop()[0]
            visited.add(node)
            if node == (final_x, final_y):
                found = True
            neighbours = map.get_neighbours(node[0], node[1])

            for neighbour in neighbours:
                if (not toVisit.contains(neighbour)) and (neighbour not in visited):
                    toVisit.push(neighbour, heuristic(neighbour[0], neighbour[1], final_x, final_y))
                    drone.roadGreedy[(neighbour[0], neighbour[1])] = (node[0], node[1])

        if found == True:
            path = []
            path.append((final_x, final_y))
            while(drone.roadGreedy[path[-1]] != None):
                path.append(drone.roadGreedy[path[-1]])

            return list(reversed(path))


    def searchAStar(self, mapM, droneD, initialX, initialY, finalX, finalY, h):
        visited = set()
        toVisit = PriorityQueue()
        toVisit.push((initialX, initialY), h(initialX, initialY, finalX, finalY))
        droneD.roadAStar[(initialX, initialY)] = None
        droneD.costs[(initialX, initialY)] = 0
        found = False

        while((not toVisit.isEmpty()) and (not found)):
            if toVisit.isEmpty():
                return False

            node = toVisit.pop()[0]
            visited.add(node)
            if node == (finalX, finalY):
                found = True
            neighbours = mapM.get_neighbours(node[0], node[1])
            for n in neighbours:
                if n not in visited:
                    if droneD.costs.get((n[0], n[1])) is None:
                        droneD.costs[(n[0], n[1])] = 1 + droneD.costs[(node[0], node[1])]
                        heuristic = droneD.costs[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                        toVisit.push(n, heuristic)
                        droneD.roadAStar[(n[0], n[1])] = (node[0], node[1])


                    else:
                        distance_to_neighbour = 1 + droneD.costs[(node[0], node[1])]
                        if distance_to_neighbour < droneD.costs[(n[0], n[1])]:
                            droneD.costs[(n[0], n[1])] = distance_to_neighbour
                            heuristic = droneD.costs[(n[0], n[1])] + h(n[0], n[1], finalX, finalY)
                            toVisit.update(n, heuristic)
                            droneD.roadAStar[(n[0], n[1])] = (node[0], node[1])

        if found == True:
            route = []
            route.append((finalX, finalY))
            while(droneD.roadAStar[route[-1]] != None):
                route.append(droneD.roadAStar[route[-1]])
            return list(reversed(route))

        return []



    def dummysearch(self):

        return [[5 ,7] ,[5 ,8] ,[5 ,9] ,[5 ,10] ,[5 ,11] ,[6 ,11] ,[7 ,11]]

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20 ,20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))

        return image