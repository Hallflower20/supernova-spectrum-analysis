#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import shlex
import pandas as pd
import numpy as np
from astropy.table import Table
from astropy.table import Column
import os
import glob2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import SNID_Analysis
import numpy as np


# In[2]:


sample = Table.read("/mnt/c/users/20xha/Documents/Caltech/Research/SEDM_ML_sample.ascii", format = "ascii")


# In[3]:


sample_location = "/home/hallflower/sample/spectra/"
source = "/mnt/c/users/20xha/Documents/Caltech/Research/SNID/snid_outputs/"
image_output = "/mnt/c/users/20xha/Documents/Caltech/Research/SNID/snid_outputs/SNIDimages/"
param = "/mnt/c/users/20xha/Documents/GitHub/supernova-spectrum-analysis/snid.param"
snid = "/mnt/c/users/20xha/Documents/Caltech/Research/SNID/snid-5.0/snid"


# In[4]:


#sample[np.where(sample["col1"] == "ZTF17aaaukqn")]


# In[5]:


error_array = []
counter = 0
for i in np.unique(sample["col1"])[300::]:
    try:
        fnamelist = ""
        #for j in (sample[np.where(i == sample["col1"])]["col8"]):
        #    fnamelist += sample_location + str(j) + " "
        fnamelist = sample_location + sample[np.where(i == sample["col1"])]["col8"][-1]
        sample_location_temp = sample_location + str(i)

        output, error = SNID_Analysis.run_files(sample_location_temp, fnamelist, source)

        if(not("No template meets" in str(output))):
            SNID_Analysis.plot_best_15(sample_location_temp, fnamelist, source, image_output)
            SNID_Analysis.parse_output(sample_location_temp, fnamelist, source)
        else:
            print(i)
    except:
        print("Not Normal Error")
        print(output)
        print(error)
        print(i)
    
    if(counter % 100 == 0):
        print(counter)
    counter+=1


# In[ ]:


#output, error = SNID_Analysis.run_files(sample_location_temp, fnamelist, source)


# In[ ]:


#fnamelist


# In[ ]:


#"No template meets" in str(output)


# In[ ]:




