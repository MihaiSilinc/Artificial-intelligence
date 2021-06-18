from operator import add

from utilities import UP, DOWN, LEFT, RIGHT


class Sensor:
    def __init__(self, mapM, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.mapM = mapM

    # def surveillance_area_covered(self):
    #     start_x = self.x
    #     start_y = self.y
    #
    #     surveillance = [0, 0, 0, 0, 0]
    #
    #     for direction in [UP, DOWN, LEFT, RIGHT]:
    #         current_x = start_x
    #         current_y = start_y
    #
    #         next = list(map(add, direction, [current_x, current_y]))
    #
    #         for index in range(5):
    #             if self.mapM.surface[next[0]][next[1]] == 1 or next[0] < 0 or next[0] > 19 or next[1] < 0 or next[1] > 19:  # 1 for wall
    #                 break
    #
    #             if self.mapM.surface[next[0]][next[1]] != 2:  # 2 for already surveilled block
    #                 self.mapM.surface[next[0]][next[1]] = 2
    #                 surveillance[index] += 1
    #
    #             next = list(map(add, direction, [next[0], next[1]]))
    #
    #     return surveillance