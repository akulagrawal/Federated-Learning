import pickle
import time
import os
import time
import torch
from time import sleep
import random

n_agents = 3
edgeBreakProb = 0.1
networkDuration = 900.0
networkIdx = 0.0
topology = "RING"

path_project = "._tartarus"
#if not os.path.isdir(path_project):
#	os.makedirs(path_project)
if not os.path.isdir("common"):
	os.makedirs("common")
if not os.path.isdir("global"):
	os.makedirs("global")
#if not os.path.isdir(path_project + "/params"):
#	os.makedirs(path_project + "/params")

globalIdx = 1
num_users = 100
train_loss_arr = []
train_acc_arr = []
test_acc_arr = []
test_loss_arr = []
client_arr = []
time_real = []
agent_arr = []
flag = 0

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



	sleep(0.5)
	for i in range(num_users):
		for j in range(n_agents):
			dir = "common/agent"+str(j)+"_"
			if os.path.isfile(dir+str(i)+"_weights.pt") and os.path.isfile(dir+str(i)+"_results.pkl"):
				print("agent"+str(j)+","+str(i)+",local")
				#os.system("cp "+dir+str(i)+"_weights.pt "+path_project+"/params/agent"+str(j)+"_"+str(globalIdx)+"_weights.pt")
				os.remove(dir+str(i)+"_weights.pt")
			
				with open(dir+str(i)+"_results.pkl", 'rb') as f:
					train_loss, train_acc, test_acc, test_loss, client = pickle.load(f)
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

			dir = "global/agent"+str(j)+"_"

			if os.path.isfile(dir+str(i)+"_weights.pt"):
				print("agent"+str(j)+","+str(i)+",global")
				if flag == 0:
					global_weights = torch.load(dir+str(i)+"_weights.pt")
					flag = 1
				else:
					w = torch.load(dir+str(i)+"_weights.pt")
					for key in global_weights.keys():
						global_weights[key] += w[key]
						global_weights[key] = torch.div(global_weights[key], 2)
				torch.save(global_weights, "global_weights.pt")
				os.remove(dir+str(i)+"_weights.pt")
				clientDir = "/home/btp4/Downloads/Decentralized/src/"
				for k in range(num_users):
					w1 = torch.load("global_weights.pt")
					if os.path.isfile(clientDir+path_project+"/params/param_Client["+str(k)+"]_weights.pt"):
						while 1:
							try:
								w1 = torch.load(clientDir+path_project+"/params/param_Client["+str(k)+"]_weights.pt")
								break
							except:
								pass
					w2 = torch.load("global_weights.pt")
					for key in w1.keys():
						w2[key] += w1[key]
						w2[key] = torch.div(w2[key], 2)
					torch.save(w2, clientDir+path_project+"/params/param_Client["+str(k)+"]_weights.pt")