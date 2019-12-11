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
    start_time = time.time()

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
    idxs_users = np.random.choice(range(args.num_users), m, replace=False)

    for idx in idxs_users:
        w = torch.load(path_project + "/params/param_Client[{}]_weights.pt".format(idx))
        loss = torch.load(path_project + "/params/param_Client[{}]_losses.pt".format(idx))
        local_weights.append(copy.deepcopy(w))
        local_losses.append(copy.deepcopy(loss))

    # update global weights
    global_weights = average_weights(local_weights)

    # update global weights
    global_model.load_state_dict(global_weights)

    loss_avg = sum(local_losses) / len(local_losses)
    with open(path_project + '/params/loss.txt', "a") as myfile:
        myfile.write(str(loss_avg) + '\n')

    train_loss = []
    with open(path_project + '/params/loss.txt', "r") as myfile:
        for l in myfile.readlines():
            train_loss.append(float(l))

    # Calculate avg training accuracy over all users at every epoch
    list_acc, list_loss = [], []
    global_model.eval()
    for c in range(args.num_users):
        acc = torch.load(path_project + '/params/param_Client[{}]_acc.pt'.format(args.client))
        loss = torch.load(path_project + '/params/param_Client[{}]_loss.pt'.format(args.client))
        list_acc.append(acc)
        list_loss.append(loss)

    train_accuracy = sum(list_acc)/len(list_acc)

    print(' \nAvg Training Stats after ' + str(epoch+1) + ' global rounds:')
    print('Training Loss : ' + str(np.mean(np.array(train_loss))))
    print('Train Accuracy: {:.2f}% \n'.format(100*train_accuracy))

    # Test inference after completion of training
    test_acc, test_loss = test_inference(args, global_model, test_dataset)

    print("|---- Test Accuracy: {:.2f}%".format(100*test_acc))

    torch.save(global_weights, path_project + '/params/global_weights.pt')

    # Saving the objects train_loss and train_accuracy:
    #file_name = '../save/objects/{}_{}_{}_C[{}]_iid[{}]_E[{}]_B[{}].pkl'.\
    #    format(args.dataset, args.model, args.epochs, args.frac, args.iid,
    #           args.local_ep, args.local_bs)

    #with open(file_name, 'wb') as f:
    #    pickle.dump([train_loss, train_accuracy], f)

    print('\n Total Run Time: {0:0.4f}'.format(time.time()-start_time))