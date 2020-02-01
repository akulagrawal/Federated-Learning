#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import pickle
import numpy as np
from tqdm import tqdm
import time

import torch
from tensorboardX import SummaryWriter

from options import args_parser
from update import LocalUpdate, test_inference
from models import MLP, CNNMnist, CNNFashion_Mnist, CNNCifar
from utils import get_dataset, average_weights, exp_details


if __name__ == '__main__':
	path_project = "./.tartarus"
	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + "/logs"):
		os.makedirs(path_project + "/logs")
	if not os.path.isdir(path_project + "/params"):
		os.makedirs(path_project + "/params")

	# define paths
	logger = SummaryWriter(path_project + "/logs")

	args = args_parser()
	exp_details(args)

	if args.gpu:
	    torch.cuda.set_device(args.gpu)
	device = 'cuda' if args.gpu else 'cpu'

	# load dataset and user groups
	train_dataset, test_dataset, user_groups = get_dataset(args)

	# BUILD MODEL
	if args.model == 'cnn':
	    # Convolutional neural netork
	    if args.dataset == 'mnist':
	        global_model = CNNMnist(args=args)
	    elif args.dataset == 'fmnist':
	        global_model = CNNFashion_Mnist(args=args)
	    elif args.dataset == 'cifar':
	        global_model = CNNCifar(args=args)

	elif args.model == 'mlp':
	    # Multi-layer preceptron
	    img_size = train_dataset[0][0].shape
	    len_in = 1
	    for x in img_size:
	        len_in *= x
	        global_model = MLP(dim_in=len_in, dim_hidden=64,
	                           dim_out=args.num_classes)
	else:
	    exit('Error: unrecognized model')

	# Set the model to train and send it to device.
	global_model.to(device)
	global_model.train()

	# Training
	idx = args.client
	local_model = LocalUpdate(args=args, dataset=train_dataset,
	                          idxs=user_groups[idx], logger=logger)
	w, loss = local_model.update_weights(
	    model=copy.deepcopy(global_model), global_round=args.epoch)

	torch.save(w, path_project + '/params/param_Client[{}]_weights.pt'.format(args.client))
	torch.save(w, path_project + '/params/weights.pt')

	local_model = LocalUpdate(args=args, dataset=train_dataset,
	                          idxs=user_groups[idx], logger=logger)
	acc, loss = local_model.inference(model=global_model)
	torch.save(acc, path_project + '/params/'+str(time.time())+'_acc.pt')
	torch.save(loss, path_project + '/params/'+str(time.time())+'_loss.pt')
	list_acc = []
	list_loss = []
	list_acc.append(acc)
	list_loss.append(loss)
	torch.save(list_acc, path_project + '/params/param_Client[{}]_acc.pt'.format(args.client))
	torch.save(list_loss, path_project + '/params/param_Client[{}]_loss.pt'.format(args.client))



	global_model.load_state_dict(w)
	test_acc, test_loss = test_inference(args, global_model, test_dataset)
	with open("testData.txt", "w") as f:
		f.write(str(test_acc)+","+str(test_loss))