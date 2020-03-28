import os
from tqdm import tqdm

def createClient(idx):
	os.system("python -W ignore \"federated_main_local_ini.py\" --model=cnn --dataset=mnist \
				--epochs=1000 --iid=0 --epoch=0 --client=" + str(idx))

def runClient(idx):
	os.system("python -W ignore \"federated_main_local.py\" --model=cnn --dataset=mnist \
				--epochs=1 --iid=0 --epoch=1 --client=" + str(idx))

if __name__== "__main__":
	path_project = ".tartarus"
	n_group = int(input("Enter Group No.: "))
	n_clients = 100
	n_groups = 4
	epochs = 100
	epoch = [0]*100
	while 1:
		firstClient = int(n_group*n_clients/n_groups)
		nextClient = int(((n_group+1)*n_clients/n_groups))
		for i in range(firstClient, nextClient):
			if os.path.isfile("."+str(i)):
				if epoch[i] == 0:
					createClient(i)
					epoch[i]=1
				else:
					runClient(i)
				os.system("scp "+path_project+"/params/param_Client["+str(i)+"]_weights.pt btp4@172.16.117.133:~/Documents/Centralized/src/common/param_Client["+str(i)+"]_weights.pt")
				os.system("scp "+path_project+"/params/param_Client["+str(i)+"]_acc.pt btp4@172.16.117.133:~/Documents/Centralized/src/common/param_Client["+str(i)+"]_acc.pt")
				os.system("scp "+path_project+"/params/param_Client["+str(i)+"]_loss.pt btp4@172.16.117.133:~/Documents/Centralized/src/common/param_Client["+str(i)+"]_loss.pt")
				os.remove("."+str(i))
				os.remove(path_project+"/params/param_Client["+str(i)+"]_weights.pt")