import os
from tqdm import tqdm

def createClient(idx, epochs):
	os.system("python -W ignore \"federated_main_local_ini.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=0 --client=" + str(idx))

def runClient(idx, epoch, epochs):
	os.system("python -W ignore \"federated_main_local.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=" + str(epoch) + " --client=" + str(idx))

def runGlobal(epoch, epochs):
	os.system("python -W ignore \"federated_main_global.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=" + str(epoch))

if __name__== "__main__":
	n_clients = 100
	epochs = 100
	for epoch in tqdm(range(epochs)):
		for i in range(n_clients):
			if epoch == 0:
				createClient(i, epochs)
			else:
				runClient(i, epoch, epochs)
		runGlobal(epoch, epochs)