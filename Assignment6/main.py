import copy
import csv
import random
from math import sqrt
from operator import add

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from readfile import read_data
from domain import Data, Centroid
from controller import *
from stats import *


def plot(data, pair_cluster_to_type):
    for data in data:
        plt.scatter(data.values[0], data.values[1],
                    c=PLOT_COLOR_MAPPING[pair_cluster_to_type[data.estimated_value]], s=2)
    plt.show()


def main():
    records = read_data()
    centroids = initialize_centroids(records)
    running = True
    associate_instance_to_centroid(records, centroids)
    centroids = recompute_centroids(records)
    compute_stats(records, assign_cluster_type(records))

    while running:

        cmd = input("Enter command: exit // plot // stats")
        if cmd == 'exit':
            running = False
        elif cmd == 'plot':
            plot(records, assign_cluster_type(records))
        elif cmd == 'stats':
            compute_stats(records, assign_cluster_type(records))
        else:
            associate_instance_to_centroid(records, centroids)
            centroids = recompute_centroids(records)
            compute_stats(records, assign_cluster_type(records))


main()
