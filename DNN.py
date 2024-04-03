from nn import MLP
import random
import Dataset 
from tqdm import tqdm
import os

def loss(Y_pred, Y):

    
    # print([f"{y.data:.2f}" for y in Y_pred], Y)
    # Y_pred = list(map(lambda val: Value(2.71828)**val/sum(map(lambda val: Value(2.71828)**val, Y_pred)), Y_pred))

    # print([f"{y.data:.2f}" for y in Y_pred], Y)
    
    error = [(y_pred-y)**2 for y_pred, y in zip(Y_pred, Y)]
    return sum(error)




ABS_PATH = os.path.abspath("")
DOWNLOAD_PATH = os.path.join(ABS_PATH, "downloads")

dataset = Dataset.CustomImageDataset(root_dir=DOWNLOAD_PATH, transform=Dataset.preprocess_image)
n_labels = int(len(dataset)/8)


losses = []
model = MLP(100, [120, 1])


accuracies = []

for i in range(1000):
    idxs = [i for i in range(32)]
    random.shuffle(idxs)

    for idx in tqdm(idxs, disable=False):

        X = dataset[idx][0]
        Y = [int(idx/n_labels)]

        Y_pred = model(X)
        lossi = loss([Y_pred], Y)
        losses.append(lossi.value)
        model.zero_grad()
        lossi.backward()
        learning_rate = 0.0001 - 0.00009*i/1000
        

        for j, p in enumerate(model.parameters()):
            p.value -= learning_rate * p.gradient
        #print((int(Y_pred.value)+1) == Y[0])    
        accuracy = Y_pred.value - Y[0]
        # accuracy =  np.argmax(np.array([val.data for val in Y_pred]))==np.argmax(np.array(Y))
        accuracies.append(accuracy)
    print(f"{(sum(accuracies[-500:])/500):.4f}")
    if i%10==0:
        print(f"step {i}, lossi {(sum(losses[-32:])* 1/32)}")

# plt.plot(losses)
# plt.show()
# plt.yscale("log")
