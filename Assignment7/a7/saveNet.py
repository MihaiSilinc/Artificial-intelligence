import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

import model
from createdb import get_data

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))

# the function to be optimized
# y = sin(x1 + x2/pi)


data=get_data()
x1=[]
x2=[]
y=[]

for entry in data:
    x1.append(entry[0])
    x2.append(entry[1])
    y.append(entry[2])

# create a tensor with all the values
y=torch.tensor(y)

# unsqueeze it to a list of 1000 lists with those values
y=torch.unsqueeze(y,dim=1)

# create 2 tensors with all the x1 and x2 input balues
x1=torch.tensor(x1)
x2=torch.tensor(x2)

# this will be a tensor with 1000 [x1,x2] lists
x=torch.column_stack((x1,x2))

# we set up the lossFunction as the mean square error
lossFunction = torch.nn.MSELoss()

# we create the ANN, with 2 neuron inputs, 2 hidden layers of 64 neurons each and a one-neuron output
ann = model.Net(n_feature=2, n_hidden=64, n_output=1)


# we use an optimizer that implements stochastic gradient descent
optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.001)

# we memorize the losses for some graphics
loss_list = []
avg_loss_list = []

loss_plot = []

# we set up the environment for training in batches
batch_size = 10
n_batches = int(len(x) / batch_size)


for epoch in range(1000):

    for batch in range(n_batches):
        # we prepare the current batch  -- please observe the slicing for tensors
        batch_X, batch_y = x[batch * batch_size:(batch + 1) * batch_size, ], y[batch * batch_size:(batch + 1) * batch_size, ]

        # we compute the output for this batch
        prediction = ann(batch_X)

        # we compute the loss for this batch
        loss = lossFunction(prediction, batch_y)

        # we save it for graphics
        loss_list.append(loss)

        # we set up the gradients for the weights to zero (important in pytorch)
        optimizer_batch.zero_grad()

        # we compute automatically the variation for each weight (and bias) of the network
        loss.backward()

        # we compute the new values for the weights
        optimizer_batch.step()

        # we print the loss for all the dataset for each 10th epoch

    if epoch % 10 == 0:
        y_pred = ann(x)
        loss = lossFunction(y_pred, y)
        loss_plot.append(loss.item())
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    # Specify a path
filepath = "myNet.pt"
# save the model to file
torch.save(ann.state_dict(), filepath)

plt.plot(loss_plot)
plt.show()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)
