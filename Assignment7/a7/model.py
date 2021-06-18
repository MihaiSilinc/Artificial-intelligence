# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F


class Net(torch.nn.Module):
    # the class for the network

    def __init__(self, n_feature, n_hidden, n_output):
        # we have two layers: a hidden one and an output one
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden)
        self.hidden2= torch.nn.Linear(n_hidden, n_hidden)
        self.output = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        # x - batch
        # pass the input through a fully connected layer, followed by the activation function
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))

        # output is passed through the output layer
        x = self.output(x)
        return x

