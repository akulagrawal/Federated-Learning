import pickle
import time
import os
import time

path_project = ".tartarus"
if not os.path.isdir(path_project):
	os.makedirs(path_project)
if not os.path.isdir("common"):
	os.makedirs("common"):
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

start_time = time.time()

while 1:
	for i in range(num_users):
		dir = "common/"
		if os.path.isfile(dir+str(i)+"_weights.pt") and os.path.isfile(dir+str(i)+"_results.pkl"):
			print("Received from "+str(i))
			os.system("cp "+dir+str(i)+"_weights.pt "+path_project+"/params/"+str(globalIdx[j])+"_weights.pt")
			os.system("cp "+dir+str(i)+"_results.pkl "+path_project+"/params/"+str(globalIdx[j])+"_results.pkl")
			os.remove(dir+str(i)+"_weights.pt")
			os.remove(dir+str(i)+"_results.pkl")
		
			with open("results.pkl", 'rb') as f:
				train_loss, train_acc, test_acc, test_loss, client = pickle.load(f)
			train_acc_arr.append(train_acc)
			train_loss_arr.append(train_loss)
			test_acc_arr.append(test_acc)
			test_loss_arr.append(test_loss)
			client_arr.append(client)
			time_real.append(time.time() - start_time)
			with open("results.pkl", 'wb') as f:
				pickle.dump([train_loss_arr, train_acc_arr, test_acc_arr, test_loss_arr, client_arr, time_real], f)

			globalIdx = globalIdx + 1
