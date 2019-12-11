import os
from tqdm import tqdm
import time

def createClient(idx, epochs, num_users):
	os.system("python -W ignore \"federated_main_local_ini.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=0 \
				--num_users=" + str(num_users) + " --client=" + str(idx))

def runClient(idx, epoch, epochs, num_users):
	os.system("python -W ignore \"federated_main_local.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=" + str(epoch) + " \
				--num_users=" + str(num_users) + " --client=" + str(idx))

def main(client, epochs=10, num_users=2):
	for epoch in tqdm(range(epochs)):
		if epoch == 0:
			createClient(client, epochs, num_users)
		else:
			while os.path.isfile(".flag"+str(client)) == False:
				time.sleep(5)
			runClient(client, epoch, epochs, num_users)
			os.remove(".flag"+str(client))
		file = open("."+str(client)+"flag", "w")
		file.close()
	return "Done"

main(0, 10, 2)