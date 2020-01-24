#!/usr/bin/env python
# coding: utf-8

# In[35]:

#
#import pickle
#import pandas as pd
#
#
## In[42]:
#
#
#for c in {5, 10, 15, 25}:
    #for cr in {10, 50, 100}:
        #for e in {10, 50}:
            #file_name = "mnist_cnn_" + str(cr) + "_C[" + str(c/100) + "]_iid[0]_E[" + str(e) + "]_B[10].pkl"
            #csv_name = "_C[" + str(c/100) + "]_CR[" + str(cr) + "]_E[" + str(e) + "].csv"
            #try:
                #with open(file_name, 'rb') as f:
                    #loss, acc = pickle.load(f)
                    #df = pd.DataFrame(acc)
                    #df.to_csv("acc"+csv_name, index=False, header = None)
                    #df1 = pd.DataFrame(loss)
                    #df1.to_csv("loss"+csv_name, index=False, header = None)
            #except:
                #pass

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
import pandas as pd


if __name__ == '__main__':

    # define paths
    path_project = os.path.abspath('..')
    logger = SummaryWriter('../logs')

    args = args_parser()
    args.model = "cnn"
    args.frac = 0.2

    if args.gpu:
        torch.cuda.set_device(args.gpu)
    device = 'cpu'

    # load dataset and user groups
    train_dataset, test_dataset, user_groups = get_dataset(args)

    # BUILD MODEL
    global_model = CNNMnist(args=args)

    # Set the model to train and send it to device.
    global_model.to(device)
    global_model.train()
    acc = []
    loss = []
    for i in tqdm(range(175)):
	    global_weights = torch.load("tartarus4/params/global_weights["+str(i+1)+"].pt")
	    global_model.load_state_dict(global_weights)
	    global_model.eval()

	    # Test inference after completion of training
	    test_acc, test_loss = test_inference(args, global_model, test_dataset)
	    acc.append(test_acc)
	    loss.append(test_loss)
    df = pd.DataFrame(acc)
    df.to_csv("acc_4.csv", index=False, header = None)
    df1 = pd.DataFrame(loss)
    df1.to_csv("loss_4.csv", index=False, header = None)