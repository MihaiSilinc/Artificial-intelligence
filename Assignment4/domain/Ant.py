from random import randint, random, choice

from typing import List

import numpy as np

from domain.Map import Map


class Ant:
    def __init__(self, adjacency_matrix: List, current_pheromone: List, sensor_id: int, sensor_nr: int, energy: int, path=None):
        # constructor pentru clasa ant
        if path is None:
            self.path = []

        self.path.append(sensor_id)

        self.sensor_nr = sensor_nr
        self.current_sensor_id = sensor_id
        self.energy = energy
        self.toVisit = [id for id in range(sensor_nr)]
        self.toVisit.remove(self.current_sensor_id)

        self.adjacency_matrix = adjacency_matrix
        self.current_pheromone = current_pheromone


    # def distMove(self, a):
    #     # returneaza o distanta empirica data de numarul de posibile mutari corecte
    #     # dupa ce se adauga pasul a in path
    #     dummy = ant(self.n, self.m)
    #     dummy.path = self.path.copy()
    #     dummy.path.append(a)
    #     return (9 - len(dummy.nextMoves(a)))

    def addMove(self, q0, alpha, beta):
        if len(self.toVisit) == 0:
            return False

        # calculam produsul trace^alpha si vizibilitate^beta
        probablilities = []
        total = 0

        max = -1
        max_neXt = None

        for index in range(len(self.toVisit)):
            prob = ((self.current_pheromone[self.current_sensor_id][self.toVisit[index]]) ** alpha) * (self.adjacency_matrix[self.current_sensor_id][self.toVisit[index]] ** (-beta))
            probablilities.append(prob)
            total += prob

            if prob > max:
                max = prob
                max_neXt = self.toVisit[index]

        if (random() < q0):
            # adaugam cea mai buna dintre mutarile posibile
            next = max_neXt

        else:
            next = np.random.choice(self.toVisit, 1, False, [prob / total for prob in probablilities])
        next = int(next)
        self.toVisit.remove(next)
        self.path.append(next)
        self.current_sensor_id = next

        return True

    def fitness(self):
        # un drum e cu atat mai bun cu cat este mai lung
        # problema de minimizare, drumul maxim e n * m
        total = 0
        for index in range(len(self.path) - 1):
            total += self.adjacency_matrix[self.path[index]][self.path[index + 1]]

        return total




# def epoca(noAnts, alpha, beta, q0, ovidiu, adjacency_matrix: List, current_pheromone: List, sensor_id: int, sensor_nr: int, energy: int):
#     antSet = [Ant(adjacency_matrix, current_pheromone, sensor_id, sensor_nr, energy) for i in range(noAnts)]
#     for i in range(sensor_nr - 1):
#         # degradare
#         for i in range(sensor_nr):
#             for j in range(sensor_nr):
#                 current_pheromone[i][j] *= ovidiu
#
#         for x in antSet:
#             x.addMove(q0, alpha, beta)
#             current_position = x.current_sensor_id
#             last_position = x.path[-1]
#             current_pheromone[last_position][current_position] += (1 - ovidiu) * (1/adjacency_matrix[last_position][current_position])
#
#     # return best ant path
#     f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
#     f = min(f)
#     return antSet[f[1]].path
#
#
# def main(n=8, m=8, noEpoch=100, noAnts=3, alpha=1.9, beta=0.9, rho=0.05, q0=0.5):
#     sol = []
#     bestSol = []
#     trace = [[1 for i in range(n * m)] for j in range(n * m)]
#     print("Programul ruleaza! Dureaza ceva timp pana va termina!")
#     for i in range(noEpoch):
#         sol = epoca(noAnts, n, m, trace, alpha, beta, q0, rho).copy()
#         if len(sol) > len(bestSol):
#             bestSol = sol.copy()
#     print("lungimea celei mai bune solutii depistate la aceasta rulare:", len(bestSol))
#     print("Drumul detectat este:", bestSol)
#
#
# main()
