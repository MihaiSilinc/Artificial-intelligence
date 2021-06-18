import copy
import random
from math import sqrt
from operator import add
import numpy as np
import pandas as pd
from domain import Data, Centroid


def compute_stats(data, pair_cluster_to_type):
    conf_matrix = pd.DataFrame({'A': [1, 0, 0, 0], 'B': [0, 0, 0, 0], 'C': [0, 0, 0, 0], 'D': [0, 0, 0, 0]})
    conf_matrix.index = ['A', 'B', 'C', 'D']

    for records in data:
        conf_matrix[records.real_value][pair_cluster_to_type[records.estimated_value]] += 1
    print('confusion matrix:')
    print(conf_matrix)
    total_accuracy_index = np.trace(conf_matrix) / np.sum(np.sum(conf_matrix))
    precision_index_A = conf_matrix['A']['A'] / (conf_matrix['A']['A'] + conf_matrix['B']['A']
                                                 + conf_matrix['C']['A'] + conf_matrix['D']['A'])
    precision_index_B = conf_matrix['B']['B'] / (conf_matrix['A']['B'] + conf_matrix['B']['B']
                                                 + conf_matrix['C']['B'] + conf_matrix['D']['B'])
    precision_index_C = conf_matrix['C']['C'] / (conf_matrix['A']['C'] + conf_matrix['B']['C']
                                                 + conf_matrix['C']['C'] + conf_matrix['D']['C'])
    precision_index_D = conf_matrix['D']['D'] / (conf_matrix['A']['D'] + conf_matrix['B']['D'] + conf_matrix['C']['D']
                                                 + conf_matrix['D']['D'])

    rappel_index_A = conf_matrix['A']['A'] / np.sum(conf_matrix['A'])
    rappel_index_B = conf_matrix['B']['B'] / np.sum(conf_matrix['B'])
    rappel_index_C = conf_matrix['C']['C'] / np.sum(conf_matrix['C'])
    rappel_index_D = conf_matrix['D']['D'] / np.sum(conf_matrix['D'])
    print()
    print('Accuracy=', total_accuracy_index)
    print()
    print('Precision for A=', precision_index_A), print('Precision for B=', precision_index_B), print('Precision for C=', precision_index_C), print('Precision for D=', precision_index_D)
    print()
    print('Rappel for A=', rappel_index_A), print('Rappel for B=', rappel_index_B), print('Rappel for C=', rappel_index_C)\
        , print('Rappel for D=', rappel_index_D)
    print()
    print('Score for A=', 2 * precision_index_A * rappel_index_A / (precision_index_A + rappel_index_A))
    print('Score for B=', 2 * precision_index_B * rappel_index_B / (precision_index_B + rappel_index_B))
    print('Score for C=', 2 * precision_index_C * rappel_index_C / (precision_index_C + rappel_index_C))
    print('Score for D=', 2 * precision_index_D * rappel_index_D / (precision_index_D + rappel_index_D))
    print()
