import os
from tqdm import tqdm
import time
import numpy as np

def createClient(idx, epochs, num_users):
	os.system("python -W ignore \"federated_main_local_ini.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=0 \
				--num_users=" + str(num_users) + " --client=" + str(idx))

def runClient(idx, epoch, epochs, num_users):
	os.system("python -W ignore \"federated_main_local.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --epoch=" + str(epoch) + " \
				--num_users=" + str(num_users) + " --client=" + str(idx))

def createClient2(idx):
	os.system("python -W ignore \"federated_main_local_ini.py\" --model=cnn --dataset=mnist \
				--epochs=1 --iid=0 --epoch=0 --num_users=100 --client=" + idx)

def runClient2(idx):
	os.system("python -W ignore \"federated_main_local.py\" --model=cnn --dataset=mnist \
				--epochs=1 --iid=0 --epoch=1 --num_users=100 --client=" + idx)

def runAll(clientGroup, n_groups=4, epochs=5000, num_users=100, frac=0.2):
	path_project = "./.tartarus"
	with open("Time.txt", "a") as f:
		f.write("START")
	start_time = time.time()
	for epoch in tqdm(range(epochs)):
		firstClient = int(clientGroup*num_users/n_groups)
		nextClient = int((clientGroup+1)*num_users/n_groups)
		m = int((frac*num_users)/n_groups)
		idxs_users = np.random.choice(range(firstClient,nextClient), m, replace=False)
		for client in idxs_users:
			file = open(".flag2", "w")
			file.close()
			if os.path.isfile(path_project + '/params/param_Client[{}]_acc.pt'.format(client)) == False:
				createClient(client, epochs, num_users)
			else:
				runClient(client, epoch, epochs, num_users)
			os.remove(".flag2")
			while os.path.isfile(".flag1"):
				time.sleep(5)
		with open("Time.txt", "a") as f:
			f.write('\n' + str(epoch) + ': {0:0.4f}'.format(time.time()-start_time))

def main(client):
	path_project = "./.tartarus"
	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + "/logs"):
		os.makedirs(path_project + "/logs")
	if not os.path.isdir(path_project + "/params"):
		os.makedirs(path_project + "/params")
	
	if os.path.isfile(".starttime") == False:
		with open(".starttime", "w") as f:
			f.write(str(time.time()))
	while os.path.isfile(".flag2"):
		time.sleep(1)
	file = open(".flag2", "w")
	file.close()
	if os.path.isfile(path_project + '/params/param_Client[{}]_acc.pt'.format(client)) == False:
		createClient2(client)
	else:
		runClient2(client)
	with open("testData.txt","r") as f:
		s = f.readlines()[0]
	with open("results.txt", "a") as f:
		f.write(str(time.time())+","+s+"\n")
	os.remove(".flag2")
	return client+" Done"