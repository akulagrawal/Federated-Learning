import os
import torch
import time
import numpy as np
import pickle

def delLast(x):
	os.remove(".last")
	return "Done"

def runGlobal(client, frac=0.2, epoch=1, epochs=100):
	os.system("python -W ignore \"federated_main_global.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --frac="+str(frac)+" --num_users=100 \
				--epoch=" + str(epoch) + " --client="+str(client))

def main(client, frac=0.2, num_users=100, n_groups=4):
	path_project = ".tartarus"
	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + "/logs"):
		os.makedirs(path_project + "/logs")
	if not os.path.isdir(path_project + "/params"):
		os.makedirs(path_project + "/params")

	while os.path.isfile(".flag_"+client):
		time.sleep(0.5)

	if os.path.isfile(path_project + "/params/param_Client[" + client + "]_weights.pt"):
		runGlobal(int(client))
		os.system("scp common/weights.pt btp4@172.16.117.133:~/Documents/Decentralized/src/common/"+client+"_weights.pt")
		os.system("scp common/results.pkl btp4@172.16.117.133:~/Documents/Decentralized/src/common/"+client+"_results.pkl")

	if os.path.isfile(".next") == False:
		file = open(".next", "w")
		file.close()
	with open(".next", "r") as f:
		lines = f.readlines()

	if len(lines) == 0 or lines[0]=="":
		m = int((frac*num_users))
		idxs_users = np.random.choice(range(num_users-1), m, replace=False)
		for i in range(len(idxs_users)):
			if ((client != 0) and (idxs_users[i] == int(client))):
				idxs_users[i] = num_users-1
		with open(".next", "w") as f:
			for idx in idxs_users:
				if idx >= 75:
					f.write("5\n")
				else:
					f.write(str(1+int(idx/25))+"\n")
				if idx<25:
					f.write("172.16.117.148\n")
				elif idx<50:
					f.write("172.16.117.147\n")
				elif idx<75:
					f.write("172.16.117.131\n")
				else:
					f.write("172.16.117.132\n")
				f.write(str(8000+(idx%25))+"\n")
				f.write(str(idx)+"\n")

		with open(".post_info", "w") as f:
			for idx in idxs_users:
				if idx<25:
					f.write("'172.16.117.148'.\n")
				elif idx<50:
					f.write("'172.16.117.147'.\n")
				elif idx<75:
					f.write("'172.16.117.131'.\n")
				else:
					f.write("'172.16.117.132'.\n")
				f.write("'"+str(8000+(idx%25))+"'.\n")
				f.write("'"+str(idx)+"'.\n")

		file = open(".last", "w")
		file.close()
	
	with open(".next", "r") as f:
		lines = f.readlines()

	for i in range(len(lines)):
		lines[i] = lines[i].strip('\n')
	with open(".next", "w") as f:
		for i in range(4,len(lines)):
			f.write(lines[i]+"\n")
	with open(".client", "w") as f:
		f.write("'"+str(lines[3])+"'.\n")

	if os.path.isfile("common/weights"):
		os.system("scp common/weights.pt btp"+lines[0]+"@"+lines[1]+":~/Documents/Decentralized/src/common/weights.pt")
	os.system("scp .next btp"+lines[0]+"@"+lines[1]+":~/Documents/Decentralized/src/.next")
	os.system("scp .client btp"+lines[0]+"@"+lines[1]+":~/Documents/Decentralized/src/.client")

	with open(".prolNext", "w") as f:
		f.write("'"+str(lines[1])+"'.\n")
		f.write("'"+str(lines[2])+"'.\n")

	return "Done"