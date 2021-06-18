import torch
import math
from numpy import random
def get_function_value(x1,x2):
    return float(torch.sin_(x1 + (x2/math.pi)))

def fill_database():
    #create 1000 tuples of x and y and compute their f associated value
    with open("database.txt",'w') as f:

        # returns tensors with 1000 integers
        x1_values=torch.randint(-(10 ** 7), (10 ** 7),(1000,))
        x2_values=torch.randint(-(10 ** 7), (10 ** 7),(1000,))


        for i in range(1000):

            # get the point coordinates from the tensors
            x1=x1_values[i]
            x2=x2_values[i]

            # find the value of the function to that point and add it to the database
            function_value=float(get_function_value(x1/(10 ** 6), x2/(10 ** 6)))
            f.write(str(int(x1)/1000000) + ',' + str(int(x2)/1000000) + ',' + str(function_value) +'\n')


def get_data():
    # data is stored as x1, x2, f(x1,x2)
    data=[]
    with open("database.txt", 'r') as f:
        for line in f:
            line=line.split(',')
            row=[]
            row.append(float(line[0]))
            row.append(float(line[1]))
            row.append(float(line[2]))
            data.append(row)

    # will be returning a list of lists, a list of [x1,x2,f(x,x2)]
    return data

# fill the database
fill_database()