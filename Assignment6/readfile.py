import copy
import csv
import random
from math import sqrt
from operator import add

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from domain import Data, Centroid

def read_data():
    data = []
    with open('dataset.csv') as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        next(reader)

        for row in reader:
            data.append(Data([float(row[1]), float(row[2])], row[0]))

        return data