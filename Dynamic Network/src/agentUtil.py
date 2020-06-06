import os
import torch
import time
import numpy as np
import pickle
from runLocal import runClient2
import pandas as pd

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
	if os.path.isfile("._no_"+agent):
		os.remove("._no_"+agent)

	neighbours = []
	
	if client != "":
		runClient2(client)
		runGlobal(agent, int(client))
		os.system("cp common/"+agent+"_weights.pt ~/Documents/Decentralized/src/common/"+agent+"_"+client+"_weights.pt")
		os.system("cp common/"+agent+"_results.pkl ~/Documents/Decentralized/src/common/"+agent+"_"+client+"_results.pkl")

		while(os.path.isfile(".lock1")):
			pass
		df = pd.read_csv("topology.csv", header = None)

		for i in range(len(df[0])):
			if (df[0][i] == int(client)):
				neighbours.append(df[1][i])
			elif (df[1][i] == int(client)):
				neighbours.append(df[0][i])
		if len(neighbours) == 0:
			f = open("._no_"+agent, "w")
			f.close()
			idx = int(client)
		else:
			temp = np.random.choice(range(len(neighbours)), 1, replace=False)
			idx = neighbours[temp[0]]
		
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
