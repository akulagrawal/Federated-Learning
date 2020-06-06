import pickle
import time
import os
import time
import random

n_agents = 3
edgeBreakProb = 0.1
networkDuration = 900.0
networkIdx = 0.0
topology = "STAR"

path_project = "._tartarus"
if not os.path.isdir(path_project):
	os.makedirs(path_project)
if not os.path.isdir("common"):
	os.makedirs("common")
if not os.path.isdir(path_project + "/params"):
	os.makedirs(path_project + "/params")

globalIdx = 1
num_users = 100
train_loss_arr = []
train_acc_arr = []
test_acc_arr = []
test_loss_arr = []
client_arr = []
time_real = []
agent_arr = []

start_time = time.time()

while 1:
	dur = time.time() - start_time
	if (dur >= (networkIdx*networkDuration)):
		networkIdx = networkIdx + 1.0
		v1 = []
		v2 = []
		if topology == "MESH":
			for i in range(num_users-1):
				for j in range(i+1, num_users):
					rn = random.uniform(0, 1)
					if rn > edgeBreakProb:
						v1.append(i)
						v2.append(j)
		elif topology == "RING":
			for i in range(num_users):
				rn = random.uniform(0, 1)
				if rn > edgeBreakProb:
					v1.append(i)
					v2.append((i+1)%num_users)
		elif topology == "STAR":
			n_arms = 11
			arms_size = 9
			for i in range(n_arms):
				head = 1+(i*9)
				for j in range(head, head+arms_size):
					rn = random.uniform(0, 1)
					if rn > edgeBreakProb:
						v1.append(j-1)
						v2.append(j)
		clientDir = "/home/btp4/Downloads/Decentralized/src/"
		f = open(clientDir + ".lock1", "w")
		f.close()

		with open(clientDir + "topology.csv", "w") as f:
			for i in range(len(v1)):
				f.write(str(v1[i])+","+str(v2[i])+"\n")

		os.remove(clientDir + ".lock1")



	for i in range(num_users):
		for j in range(n_agents):
			dir = "common/agent"+str(j)+"_"
			if os.path.isfile(dir+str(i)+"_weights.pt") and os.path.isfile(dir+str(i)+"_results.pkl"):
				print("agent"+str(j)+","+str(i))
				os.system("cp "+dir+str(i)+"_weights.pt "+path_project+"/params/agent"+str(j)+"_"+str(globalIdx)+"_weights.pt")
				os.remove(dir+str(i)+"_weights.pt")
				
				while 1:
					try:
						with open(dir+str(i)+"_results.pkl", 'rb') as f:
							train_loss, train_acc, test_acc, test_loss, client = pickle.load(f)
						break
					except:
						pass
				
				os.remove(dir+str(i)+"_results.pkl")
				train_acc_arr.append(train_acc)
				train_loss_arr.append(train_loss)
				test_acc_arr.append(test_acc)
				test_loss_arr.append(test_loss)
				client_arr.append(client)
				agent_arr.append(j)
				time_real.append(time.time() - start_time)
				with open("results.pkl", 'wb') as f:
					pickle.dump([train_loss_arr, train_acc_arr, test_acc_arr, test_loss_arr, client_arr, agent_arr, time_real], f)

				globalIdx = globalIdx + 1
