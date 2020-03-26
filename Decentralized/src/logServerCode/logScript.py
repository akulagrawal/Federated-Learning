import pickle
import time
import os
import time

ip = input("Enter number of agents: ")
n_agents = int(ip)

path_project = ".tartarus"
if not os.path.isdir(path_project):
	os.makedirs(path_project)
for i in range(n_agents):
	if not os.path.isdir("common_" + str(i)):
		os.makedirs("common_" + str(i))
	if not os.path.isdir(path_project + "/params_" + str(i)):
		os.makedirs(path_project + "/params_" + str(i))
globalIdx[n_agents]
num_users = 100
train_loss_arr = []
train_acc_arr = []
test_acc_arr = []
test_loss_arr = []
client_arr = []
time_real = []

start_time = time.time()

while 1:
	for i in range(num_users):
		for j in range(n_agents):
			dir = "common_"+str(j)+"/"
			if os.path.isfile(dir+str(i)+"_weights.pt") and os.path.isfile(dir+str(i)+"_results.pkl"):
				print("Received from "+str(i))
				os.system("cp "+dir+str(i)+"_weights.pt "+path_project+"/params_"+str(j)+"/"+str(globalIdx[j])+"_weights.pt")
				os.system("cp "+dir+str(i)+"_results.pkl "+path_project+"/params_"+str(j)+"/"+str(globalIdx[j])+"_results.pkl")
				os.remove(dir+str(i)+"_weights.pt")
				os.remove(dir+str(i)+"_results.pkl")
			
				with open("results_"+str(j)+".pkl", 'rb') as f:
					train_loss, train_acc, test_acc, test_loss, client = pickle.load(f)
				train_acc_arr.append(train_acc)
				train_loss_arr.append(train_loss)
				test_acc_arr.append(test_acc)
				test_loss_arr.append(test_loss)
				client_arr.append(client)
				time_real.append(time.time() - start_time)
				with open("results_"+str(j)+".pkl", 'wb') as f:
					pickle.dump([train_loss_arr, train_acc_arr, test_acc_arr, test_loss_arr, client_arr, time_real], f)

				globalIdx[j] = globalIdx[j] + 1
