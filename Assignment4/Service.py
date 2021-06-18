from math import sqrt
from operator import add

import pygame

from domain.Node import Node

BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 255, 0)


class Service:

    def __init__(self, repo):
        self.repo = repo

    @staticmethod
    def ManhattanHeuristic(node, previousNode, start_node, goal_node):
        node.g = previousNode.g + 1
        node.h = abs(node.position[0] - goal_node.position[0]) + abs(
            node.position[1] - goal_node.position[1])
        node.f = node.g + node.h

    @staticmethod
    def EuclidHeuristic(node, previousNode, start_node, goal_node):
        node.g = previousNode.g + 1
        node.h = abs(node.position[0] - goal_node.position[0]) + abs(
            node.position[1] - goal_node.position[1])
        node.f = sqrt(node.h * node.h + node.g * node.g)

        # Check if a neighbor should be added to open list

    @staticmethod
    def add_to_open(open, neighbor):
        for node in open:
            if neighbor == node and neighbor.f >= node.f:
                return False
        return True

    def searchGreedy(self, initialX, initialY, finalX, finalY):

        toVisit = []
        visited = []
        start = [initialX, initialY]
        end = [finalX, finalY]
        start_node = Node(start, None)
        goal_node = Node(end, None)
        toVisit.append(start_node)

        while len(toVisit) > 0:

            toVisit.sort()
            current_node = toVisit.pop(0)
            visited.append(current_node)

            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                path.append(current_node.position)
                return path[::-1]

            (x, y) = current_node.position
            neighbors = [[-1, 0], [1, 0], [0, -1], [0, 1]]

            for any_move in neighbors:
                next = list(map(add, any_move, [x, y]))

                if not((0 <= next[0] <= 19) and (0 <= next[1] <= 19)):
                    continue
                    
                nextNode = self.repo.mapM.surface[next[0]][next[1]]
                if nextNode == 1:
                    continue
                neighbor = Node(next, current_node)
                if neighbor in visited:
                    continue
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.h

                if neighbor not in toVisit:
                    toVisit.append(neighbor)

        return None

    def aStarSearch(self, initialX, initialY, finalX, finalY):

        toVisit = []
        visited = []
        start = [initialX, initialY]
        end = [finalX, finalY]
        start_node = Node(start, None)
        goal_node = Node(end, None)
        toVisit.append(start_node)

        while len(toVisit) > 0:
            toVisit.sort()
            current_node = toVisit.pop(0)
            visited.append(current_node)

            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                path.append(current_node.position)
                return path[::-1]

            (x, y) = current_node.position
            neighbors = [[-1, 0], [1, 0], [0, -1], [0, 1]]

            for any_move in neighbors:
                next = list(map(add, any_move, [x, y]))

                if not((0 <= next[0] <= 19) and (0 <= next[1] <= 19)):
                    continue

                nextNode = self.repo.mapM.surface[next[0]][next[1]]

                if nextNode == 1:
                    continue

                neighbor = Node(next, current_node)

                if neighbor in visited:
                    continue

                Service.ManhattanHeuristic(neighbor, current_node, start_node, goal_node)

                if Service.add_to_open(toVisit, neighbor):
                    toVisit.append(neighbor)
        return None


    def displayWithPath2(self, path1, path2, color1=GREEN, color2=RED):
        mark = pygame.Surface((20, 20))
        image = self.repo.mapM.image()
        mark.fill(color1)
        for move in path1:
            image.blit(mark, (move[1] * 20, move[0] * 20))
        mark.fill(color2)
        for move in path2:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        mark.fill(ORANGE)
        for move in path1:
            if move in path2:
                image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    def displayWithPath(self, path1, color1=GREEN):
        mark = pygame.Surface((20, 20))
        image = self.repo.mapM.image()
        mark.fill(color1)
        for move in path1:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image




