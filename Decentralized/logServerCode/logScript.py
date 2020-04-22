import pickle
import time
import os
import time

n_agents = 3

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
	for i in range(num_users):
		for j in range(n_agents):
			dir = "common/agent"+str(j)+"_"
			if os.path.isfile(dir+str(i)+"_weights.pt") and os.path.isfile(dir+str(i)+"_results.pkl"):
				print("agent"+str(j)+","+str(i))
				os.system("cp "+dir+str(i)+"_weights.pt "+path_project+"/params/agent"+str(j)+"_"+str(globalIdx)+"_weights.pt")
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
