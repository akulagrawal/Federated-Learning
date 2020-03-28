import os
from tqdm import tqdm
import time
import numpy as np

def runGlobal(frac, epoch, epochs):
	os.system("python -W ignore \"federated_main_global.py\" --model=cnn --dataset=mnist \
				--epochs=" + str(epochs) + " --iid=0 --frac="+str(frac)+" --num_users=100 --epoch=" + str(epoch))

if __name__== "__main__":
	path_project = ".tartarus"
	start_time = time.time()
	num_users = 100
	n_groups = 4
	epochs = 100
	frac = 0.2
	IP = ["172.16.117.148", "172.16.117.147", "172.16.117.131", "172.16.117.132"]
	f = open("clients.txt", "w")
	f.close()
	f = open("trainData.txt", "w")
	f.close()
	f = open("testData.txt", "w")
	f.close()
	f = open("time.txt", "w")
	f.close()
	for epoch in tqdm(range(epochs)):
		m = max(int(frac * num_users), 1)
		idxs_users = np.random.choice(range(num_users), m, replace=False)
		with open("clients.txt", "a") as f:
			for i in range(m):
				f.write(str(idxs_users[i])+",")
			f.write("\n")
		for i in range(m):
			f = open("."+str(idxs_users[i]), "w")
			f.close()
			ipIdx = int(idxs_users[i]/25)
			group = ipIdx+1
			if group == 4:
				group = 5
			os.system("scp ."+str(idxs_users[i])+" btp"+str(group)+"@"+str(IP[ipIdx])+":~/Documents/Centralized/src/."+str(idxs_users[i]))
			os.remove("."+str(idxs_users[i]))
		while 1:
			arrived = 0
			for i in range(m):
				if os.path.isfile("common/param_Client["+str(idxs_users[i])+"]_loss.pt"):
					arrived = arrived + 1
			if arrived == m:
				runGlobal(frac, epoch, epochs)
				for i in range(m):
					os.remove("common/param_Client["+str(idxs_users[i])+"]_weights.pt")
					os.remove("common/param_Client["+str(idxs_users[i])+"]_acc.pt")
					os.remove("common/param_Client["+str(idxs_users[i])+"]_loss.pt")
				for i in range(num_users):
					ipIdx = int(i/25)
					group = ipIdx+1
					if group == 4:
						group = 5
					os.system("scp "+path_project+"/params/global_weights["+str(epoch)+"].pt btp"+str(group)+"@"+str(IP[ipIdx])+":~/Documents/Centralized/src/"+path_project+"/params/param_Client["+str(i)+"]_weights.pt")
				break
		with open("time.txt", "a") as f:
			finish_time = time.time() - start_time
			f.write(str(finish_time)+"\n")

