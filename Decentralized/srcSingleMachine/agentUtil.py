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

def main(args, num_users=100, n_groups=4):
	
	client = args.split('.')[0]
	agent = args.split('.')[1]
	agentFile = "._"+agent
	clientFile = "._client_"+agent
	nextFile = "._prolNext_"+agent
	path_project = "._tartarus"

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

	idxs_users = np.random.choice(range(num_users-1), 1, replace=False)
	if ((client != "") and (idxs_users[0] == int(client))):
		idxs_users[0] = num_users-1
	idx = idxs_users[0]

	with open(clientFile, "w") as f:
		f.write("'"+str(idx)+"'.\n")

	with open(nextFile, "w") as f:
		f.write("'172.16.117.133'.\n")
		f.write("'"+str(8000+(idx))+"'.\n")

	return "Done"
