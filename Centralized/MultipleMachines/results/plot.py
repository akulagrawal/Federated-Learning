import matplotlib.pyplot as plt

time = []
train_acc = []
train_loss = []
test_acc = []
test_loss = []
path = ""

with open(path+"time.txt", "r") as f:
	lines = f.readlines()
for line in lines:
	time.append(float(line))

with open(path+"trainData.txt", "r") as f:
	lines = f.readlines()
for line in lines:
	words = line.split(',')
	train_acc.append(float(words[0]))
	train_loss.append(float(words[1]))

with open(path+"testData.txt", "r") as f:
	lines = f.readlines()
for line in lines:
	words = line.split(',')
	test_acc.append(float(words[0]))
	test_loss.append(float(words[1]))

plt.figure()
plt.plot(time, test_acc)
plt.savefig("C[0.2]_test_acc.png")

plt.figure()
plt.plot(time, train_acc)
plt.savefig("C[0.2]_train_acc.png")

plt.figure()
plt.plot(time, train_loss)
plt.savefig("C[0.2]_train_loss.png")