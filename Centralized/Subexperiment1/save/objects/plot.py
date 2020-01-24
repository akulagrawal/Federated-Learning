#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pickle
import pandas as pd


# In[42]:


for c in {5, 10, 15, 25}:
    for cr in {10, 50, 100}:
        for e in {10, 50}:
            file_name = "mnist_cnn_" + str(cr) + "_C[" + str(c/100) + "]_iid[0]_E[" + str(e) + "]_B[10].pkl"
            csv_name = "_C[" + str(c/100) + "]_CR[" + str(cr) + "]_E[" + str(e) + "].csv"
            try:
                with open(file_name, 'rb') as f:
                    loss, acc = pickle.load(f)
                    df = pd.DataFrame(acc)
                    df.to_csv("acc"+csv_name, index=False, header = None)
                    df1 = pd.DataFrame(loss)
                    df1.to_csv("loss"+csv_name, index=False, header = None)
            except:
                pass

