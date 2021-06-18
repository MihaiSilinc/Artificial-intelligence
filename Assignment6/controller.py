import copy
import random
from math import sqrt
from operator import add
import numpy as np
import pandas as pd
from domain import Data, Centroid

data_TYPES = ['A', 'B', 'C', 'D']
CENTROID_TYPES = ['1', '2', '3', '4']
PLOT_COLOR_MAPPING = {'A': 'blue', 'B': 'green', 'C': 'red', 'D': 'purple'}

def initialize_centroids(data):
    # I initialize the centroids randomly
    centroids = []
    for centroid_type in CENTROID_TYPES:
        random_data = random.choice(data)
        centroids.append(Centroid(random_data.values, centroid_type))

    return centroids


def compute_distance(data, centroid):
    distance = 0
    for index in range(len(data.values)):
        distance += (data.values[index] - centroid.values[index]) ** 2
    return sqrt(distance)


def find_nearest_centroid_type(data, centroids):
    distances = {}

    for centroid in centroids:
        distances[centroid.centroid_type] = compute_distance(data, centroid)

    closest_centroid = min(distances, key=distances.get)

    return closest_centroid


def associate_instance_to_centroid(data, centroids):
    for record in data:
        record.estimated_value = find_nearest_centroid_type(record, centroids)


def recompute_centroids(data):
    centroids = []
    sum_cluster_data = {'1': [0, 0], '2': [0, 0], '3': [0, 0], '4': [0, 0]}
    number_data = {'1': 0, '2': 0, '3': 0, '4': 0}

    for data in data:
        sum_cluster_data[data.estimated_value] = list(
            map(add, sum_cluster_data[data.estimated_value], data.values))
        number_data[data.estimated_value] += 1

    for centroid_type in CENTROID_TYPES:
        centroids.append(
            Centroid([value / number_data[centroid_type] for value in sum_cluster_data[centroid_type]],
                     centroid_type))

    return centroids


def assign_cluster_type(data):
    types = copy.deepcopy(data_TYPES)
    # ['A', 'B', 'C', 'D']

    pair_cluster_to_type = {}
    # clusters
    for centroid_type in CENTROID_TYPES:
        # ['1', '2', '3', '4']
        number_data_each_type = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

        for record in data:
            if record.estimated_value == centroid_type:
                number_data_each_type[record.real_value] += 1

        best_match = max(number_data_each_type, key=number_data_each_type.get)

        while best_match not in types:
            del number_data_each_type[best_match]
            best_match = max(number_data_each_type, key=number_data_each_type.get)

        pair_cluster_to_type[centroid_type] = best_match

        types.remove(best_match)
    return pair_cluster_to_type

