from nn import MLP
import os
import random
import matplotlib.pyplot as plt
import numpy as np
from engine import Value


def loss(y_pred, y):
    error = [(y_pred_i-y_i)**2 for y_pred_i, y_i in zip(y_pred, y)]
    return sum(error)

losses = []
 

model = MLP(10, [15,10,10])

X = [Value(int(random.uniform(0, 10))) for _ in range(10)] 
Y = [Value(i-(i*0.5)) for i in range(10)]

for i in range(1000):

    y_pred = model(X)
    lossi = loss(y_pred, Y)
    losses.append(lossi.value)
    model.zero_grad()
    lossi.backward()
    learning_rate = 1- (i+100)/1100
    for p in model.parameters():
        p.value -= learning_rate * p.gradient

    if i%100==0:
        print(f"step {i}, lossi {lossi.value}")

plt.plot(losses)
plt.yscale("log")
plt.show()