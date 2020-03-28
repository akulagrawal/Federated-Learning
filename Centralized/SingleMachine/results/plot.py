import pickle
import matplotlib.pyplot as plt
import numpy as np

name = input ("Enter file name (remove .pkl):")

with open(name+".pkl", "rb") as f:
	train_loss, train_acc, test_acc, test_loss, times = pickle.load(f)

plt.figure()
plt.plot(test_acc)
plt.xticks(np.arange(0, 101, 10))
plt.yticks(np.arange(0, 1.1, .1))
plt.savefig(name+".png")