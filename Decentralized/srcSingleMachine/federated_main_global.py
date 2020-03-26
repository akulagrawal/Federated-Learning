#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import time
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

	path_project = '.tartarus'
	if not os.path.isdir(path_project):
		os.makedirs(path_project)
	if not os.path.isdir(path_project + '/logs'):
		os.makedirs(path_project + '/logs')
	if not os.path.isdir(path_project + '/params'):
		os.makedirs(path_project + '/params')

	# define paths
	logger = SummaryWriter(path_project + '/logs')

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
	#print(global_model)

	#try:
	#    global_model.load_state_dict(torch.load(path_project + '/params/global_weights.pt'))
	#except:
	#    pass

	# copy weights
	global_weights = global_model.state_dict()

	# Training
	epoch = args.epoch
	local_weights, local_losses = [], []
	print('\n | Global Training Round : ' + str(epoch+1) + ' |\n')

	global_model.train()
	
	w1 = torch.load(path_project + '/params/param_Client[{}]_weights.pt'.format(args.client))
	w2 = w1
	if os.path.isfile('common/weights.pt'):
		w2 = torch.load('common/weights.pt')
	else:
		w2 = torch.load(path_project + '/params/param_Client[{}]_weights.pt'.format(args.client))
	for key in global_weights.keys():
		w2[key] += w1[key]
		global_weights[key] = torch.div(w2[key], 2)

	# update global weights
	global_model.load_state_dict(global_weights)

	# Calculate avg training accuracy over all users at every epoch
	list_acc, list_loss = [], []
	global_model.eval()

	# Test inference after completion of training
	test_acc, test_loss = test_inference(args, global_model, test_dataset)
	train_acc, train_loss = 0.0, 0.0
	with open(path_project + '/params/trainData_[{}].pkl'.format(args.client), 'rb') as f:
		train_loss, train_acc = pickle.load(f)
	with open('common/results.pkl', 'wb') as f:
		pickle.dump([train_loss, train_acc, test_acc, test_loss, args.client], f)

	torch.save(global_weights, 'common/weights.pt')
	torch.save(global_weights, path_project + '/params/param_Client[{}]_weights.pt'.format(args.client))