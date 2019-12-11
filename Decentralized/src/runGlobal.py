import os
from tqdm import tqdm
import time

def runGlobal(epoch, epochs, num_users):
	os.system("python -W ignore \"federated_main_global.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --num_users=" + str(num_users) + " --iid=0 --epoch=" + str(epoch))

def main(epochs=10, num_users=2):
	for epoch in tqdm(range(epochs)):
		while ((os.path.isfile(".0flag") == False) or (os.path.isfile(".1flag") == False)):
			time.sleep(5)
		runGlobal(epoch, epochs, num_users)
		for i in range(n_clients):
			os.remove("."+str(i)+"flag")
			file = open(".flag"+str(i), "w")
			file.close()

main(2,10)