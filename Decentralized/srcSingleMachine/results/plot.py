import pickle
import matplotlib.pyplot as plt
import numpy as np

with open("results.pkl", "rb") as f:
	train_loss, train_acc, test_acc, test_loss, clients, times = pickle.load(f)

avg = []
for i in range(len(test_acc)):
	sum = 0.0
	if i+19 < len(test_acc):
		for j in range(20):
			sum = sum + test_acc[i+j]
		avg.append(sum/20.0)
		i=i+20

plt.figure()
plt.plot(times, avg)
plt.yticks(np.arange(0, 1.1, .1))
plt.savefig('plot.png')