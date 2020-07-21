#!/usr/bin/env python
# coding: utf-8

# In[1]:


import astrodash


# In[2]:


import os
import astropy
import numpy as np
from astropy.table import Table
from astropy.table import Column
import glob
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D


# In[3]:


sample_location = "/home/hallflower/sample/spectra/"
dash = "/mnt/c/users/20xha/Documents/Caltech/Research/DASH/"


# In[4]:


SEDM_ML_sample = Table.read("/mnt/c/Users/20xha/Documents/Caltech/Research/SEDM_ML_sample.ascii", format = "ascii")
SEDM_ML_sample.rename_column('col1', 'ZTF_Name')
SEDM_ML_sample.rename_column('col2', "Class")
SEDM_ML_sample.rename_column('col8', "Version")


# In[5]:


#ZTF18aajnqmp


# In[19]:


output_list = []
counter = 0
for i in np.unique(SEDM_ML_sample["ZTF_Name"]):
    try:
        filenames = []
        for j in (SEDM_ML_sample[np.where(i == SEDM_ML_sample["ZTF_Name"])]["Version"]):
            filenames.append(sample_location + str(j))

        classification = astrodash.Classify(filenames, classifyHost=False, knownZ=False, smooth=6, rlapScores=True)
        output = classification.list_best_matches(n=15, saveFilename= dash + i + '.txt')
        output_name = np.append(np.asarray(output),i)
        output_list.append(output_name)
        if(counter % 100 == 0):
            print(counter)
        counter+=1
    except:
        print(i)
output_list = np.asarray(output_list)


# In[40]:


np.save(dash + "output", output_list)


# In[ ]:




