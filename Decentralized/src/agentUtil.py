import os
import torch
import socket 
import time

def main(tempArg):
	path_project = "./.tartarus"
	file = open(".flag1", "w")
	file.close()

	with open("IP.txt") as f:
		lines = f.readlines()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	IPAddr = s.getsockname()[0]
	nexIP = '172.16.117.148'
	nextIdx = 1
	for i in range(len(lines)):
		lines[i] = lines[i].strip('\n')
	for i in range(len(lines)):
		if lines[i] == IPAddr:
			nextIdx = 1+((i+1)%len(lines))
			nextIP = lines[nextIdx-1]
			f = open(".next","w")
			f.write("'" + nextIP + "'.")
			print("Moving to btp"+str(nextIdx)+" at IP: "+str(nextIP))
			f.close()

	while os.path.isfile(".flag2"):
		time.sleep(5)
	global_weights = torch.load(path_project + '/params/weights.pt')
	if os.path.isfile('.agent_weights.pt'):
		agent_weights = torch.load('.agent_weights.pt')
		for key in global_weights.keys():
			global_weights[key] += agent_weights[key]
			global_weights[key] = torch.div(global_weights[key], 2)
		torch.save(global_weights, path_project + '/params/weights.pt')
		with open("CR", "r") as f:
			lines = f.readlines()
		cr = int(lines[0])
		torch.save(global_weights, path_project + '/params/global_weights['+str(cr)+'].pt')
		cr = cr+1
		with open("CR", "w") as f:
			f.write(str(cr))
	os.system("scp "+path_project+"/params/weights.pt btp"+str(nextIdx)+"@"+str(nextIP)+":~/Documents/Decentralized/src/.agent_weights.pt")
	os.remove(".flag1")



	return nextIP
