import os
import torch
import socket 
import time
import numpy as np

def delLast(x):
	os.remove(".last")
	return "Done"

def main(tempArg, frac=0.2, num_users=100, n_groups=4):
	path_project = "./.tartarus"
	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + "/logs"):
		os.makedirs(path_project + "/logs")
	if not os.path.isdir(path_project + "/params"):
		os.makedirs(path_project + "/params")
	file = open(".flag1", "w")
	file.close()

	while os.path.isfile(".flag2"):
		time.sleep(1)

	if os.path.isfile(path_project + '/params/weights.pt'):
		global_weights = torch.load(path_project + '/params/weights.pt')
		if os.path.isfile('.agent_weights.pt'):
			agent_weights = torch.load('.agent_weights.pt')
			for key in global_weights.keys():
				global_weights[key] += agent_weights[key]
				global_weights[key] = torch.div(global_weights[key], 2)
			torch.save(global_weights, path_project + '/params/weights.pt')

	if os.path.isfile(".next") == False:
		file = open(".next", "w")
		file.close()
	with open(".next", "r") as f:
		lines = f.readlines()

	if len(lines) == 0 or lines[0]=="":
		m = int((frac*num_users))
		idxs_users = np.random.choice(range(num_users), m, replace=False)
		with open(".next", "w") as f:
			for idx in idxs_users:
				if idx >= 75:
					f.write("5\n")
				else:
					f.write(str(1+int(idx/25))+"\n")
				if idx<25:
					f.write("172.16.117.148\n")
				elif idx<50:
					f.write("172.16.117.147\n")
				elif idx<75:
					f.write("172.16.117.131\n")
				else:
					f.write("172.16.117.132\n")
				f.write(str(8000+(idx%25))+"\n")
				f.write(str(idx)+"\n")

		with open(".post_info", "w") as f:
			for idx in idxs_users:
				if idx<25:
					f.write("'172.16.117.148'.\n")
				elif idx<50:
					f.write("'172.16.117.147'.\n")
				elif idx<75:
					f.write("'172.16.117.131'.\n")
				else:
					f.write("'172.16.117.132'.\n")
				f.write("'"+str(8000+(idx%25))+"'.\n")
				f.write("'"+str(idx)+"'.\n")

		file = open(".last", "w")
		file.close()
	
	with open(".next", "r") as f:
		lines = f.readlines()

	for i in range(len(lines)):
		lines[i] = lines[i].strip('\n')
	with open(".next", "w") as f:
		for i in range(4,len(lines)):
			f.write(lines[i]+"\n")

	#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#s.connect(("8.8.8.8", 80))
	#IPAddr = s.getsockname()[0]

	if os.path.isfile(path_project + '/params/weights.pt'):
		os.system("scp "+path_project+"/params/weights.pt btp"+lines[0]+"@"+lines[1]+":~/Documents/Decentralized/src/.agent_weights.pt")
	os.system("scp .next btp"+lines[0]+"@"+lines[1]+":~/Documents/Decentralized/src/.next")
	os.remove(".flag1")

	with open(".prolNext", "w") as f:
		f.write("'"+str(lines[1])+"'.\n")
		f.write("'"+str(lines[2])+"'.\n")


	return "Done"