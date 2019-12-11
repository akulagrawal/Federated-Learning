#!/bin/bash

python3 -W ignore federated_main.py --model=cnn --dataset=mnist --epochs=100 --iid=0 --frac=0.05 --local_ep=10 > main_05_10_100.txt