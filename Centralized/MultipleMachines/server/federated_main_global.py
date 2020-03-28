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

    path_project = "./.tartarus"
    if not os.path.isdir(path_project):
        os.makedirs(path_project)
    if not os.path.isdir(path_project + "/logs"):
        os.makedirs(path_project + "/logs")
    if not os.path.isdir(path_project + "/params"):
        os.makedirs(path_project + "/params")

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
    m = max(int(args.frac * args.num_users), 1)
    idxs_users = []
    with open("clients.txt", "r") as f:
    	lines = f.readlines()
    last_line = lines[-1].split(',')
    for i in range(m):
        idxs_users.append(int(last_line[i].strip("\n")))

    for idx in idxs_users:
        w = torch.load("common/param_Client[{}]_weights.pt".format(idx))
        local_weights.append(copy.deepcopy(w))

    # update global weights
    global_weights = average_weights(local_weights)

    # update global weights
    global_model.load_state_dict(global_weights)

    # Calculate avg training accuracy over all users at every epoch
    list_acc, list_loss = [], []
    global_model.eval()
    for c in idxs_users:
        acc = torch.load('common/param_Client[{}]_acc.pt'.format(c))
        loss = torch.load('common/param_Client[{}]_loss.pt'.format(c))
        list_acc.append(acc[-1])
        list_loss.append(loss[-1])

    train_acc = np.sum(list_acc)/len(idxs_users)
    train_loss = np.sum(list_loss)/len(idxs_users)
    with open("trainData.txt", "a") as f:
    	f.write(str(train_acc)+","+str(train_loss)+"\n")

    # Test inference after completion of training
    test_acc, test_loss = test_inference(args, global_model, test_dataset)
    with open("testData.txt", "a") as f:
    	f.write(str(test_acc)+","+str(test_loss)+"\n")

    torch.save(global_weights, path_project + '/params/global_weights['+str(args.epoch)+'].pt')

    # Saving the objects train_loss and train_accuracy:
    #file_name = '../save/objects/{}_{}_{}_C[{}]_iid[{}]_E[{}]_B[{}].pkl'.\
    #    format(args.dataset, args.model, args.epochs, args.frac, args.iid,
    #           args.local_ep, args.local_bs)

    #with open(file_name, 'wb') as f:
    #    pickle.dump([train_loss, train_accuracy], f)
