# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 14:20:51 2021

@author: tudor
"""

import torch
import torch.nn.functional as F

import model

from createdb import get_function_value

# we load the model

filepath = "myNet.pt"
ann = model.Net(2,64,1)

ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)


x1 =float( input("x1 = "))
x1 = torch.tensor([x1])
x2=float( input("x2 = "))
x2 = torch.tensor([x2])
print(ann(torch.column_stack((x1,x2))).tolist())
print(get_function_value(x1,x2))