import os
import torch
import time
import numpy as np
import pickle
from runLocal import runClient2

def runGlobal(agent, client, frac=0.2, epoch=1, epochs=100):
	os.system("python -W ignore \"federated_main_global.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --frac=" + str(frac) + " --num_users=100 \
				--epoch=" + str(epoch) + " --client=" + str(client) + " --agent=" + agent)

def main(args, num_users=100, n_groups=4, clientsInGap=50, topology="STAR"):
	
	client = args.split('.')[0]
	agent = args.split('.')[1]
	agentFile = "._"+agent
	clientFile = "._client_"+agent
	nextFile = "._prolNext_"+agent
	path_project = "._tartarus"
	countFile = "._"+agent+"_count"

	with open(agentFile, "w") as f:
		f.write(client)

	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + "/logs"):
		os.makedirs(path_project + "/logs")
	if not os.path.isdir(path_project + "/params"):
		os.makedirs(path_project + "/params")
	
	if client != "":
		runClient2(client)
		runGlobal(agent, int(client))
		os.system("cp common/"+agent+"_weights.pt ~/Documents/Decentralized/src/common/"+agent+"_"+client+"_weights.pt")
		os.system("cp common/"+agent+"_results.pkl ~/Documents/Decentralized/src/common/"+agent+"_"+client+"_results.pkl")

		if topology == "MESH":
			temp = np.random.choice(range(num_users-1), 1, replace=False)
			idx = temp[0]
			if (idx == int(client)):
				idx = num_users-1
		elif topology == "RING":
			temp = np.random.choice(range(2), 1, replace=False)
			direction = temp[0]
			idx = int(client)
			if direction == 0:
				idx = (idx+num_users-1)%num_users
			else:
				idx = (idx+1)%num_users
		elif topology == "STAR":
			arm_size = 9
			n_arms = 11
			idx = int(client)
			if (idx == 0):
				temp = np.random.choice(range(n_arms), 1, replace=False)
				armIdx = temp[0]
				idx = 1+armIdx*arm_size
			elif (idx%arm_size == 0):
				idx = idx-1
			else:
				temp = np.random.choice(range(2), 1, replace=False)
				direction = temp[0]
				if direction == 0:
					idx = idx-1
				else:
					idx = idx+1
	else:
		temp = np.random.choice(range(num_users), 1, replace=False)
		idx = temp[0]


	with open(clientFile, "w") as f:
		f.write("'"+str(idx)+"'.\n")

	with open(nextFile, "w") as f:
		f.write("'172.16.117.133'.\n")
		f.write("'"+str(8000+(idx))+"'.\n")


	if os.path.isfile(countFile) == 0:
		with open(countFile, "w") as f:
			f.write("0")
	else:
		with open(countFile, "r") as f:
			lines = f.readlines()
		clientsVis = int(lines[0])
		if(clientsVis == clientsInGap):
			os.system("cp common/"+agent+"_weights.pt ~/Documents/Decentralized/src/global/"+agent+"_"+client+"_weights.pt")
			clientsVis = 0
		else:
			clientsVis += 1
		with open(countFile, "w") as f:
			f.write(str(clientsVis))

	return "Done"
