#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import pickle
import numpy as np
from tqdm import tqdm

import torch
from tensorboardX import SummaryWriter

from options import args_parser
from update import LocalUpdate, test_inference
from models import MLP, CNNMnist, CNNFashion_Mnist, CNNCifar
from utils import get_dataset, average_weights, exp_details


if __name__ == '__main__':
	path_project = ".tartarus"
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

	if os.path.isfile(path_project + '/params/param_Client[{}]_weights.pt'.format(args.client)):
		global_model.load_state_dict(torch.load(path_project + '/params/param_Client[{}]_weights.pt'.format(args.client)))

	# Training
	idx = args.client
	local_model = LocalUpdate(args=args, dataset=train_dataset,
	                          idxs=user_groups[idx], logger=logger)
	w, loss = local_model.update_weights(
	    model=copy.deepcopy(global_model), global_round=args.epoch)

	torch.save(w, path_project + '/params/param_Client[{}]_weights.pt'.format(args.client))

	local_model = LocalUpdate(args=args, dataset=train_dataset,
	                          idxs=user_groups[idx], logger=logger)
	acc, loss = local_model.inference(model=global_model)
	
	with open(path_project + '/params/trainData_[{}].pkl'.format(args.client), 'wb') as f:
		pickle.dump([loss, acc], f)
