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
import gc
import glob


# In[2]:


sample = Table.read("/home/xhall/Documents/NewZTF/ML_sample.ascii", format = "ascii")


# In[3]:


sample_location = "/home/xhall/Documents/NewZTF/spectra/"
source = "/home/xhall/Documents/NewZTF/SNIDoutput/"
image_output = "/home/xhall/Documents/NewZTF/Images/"
snid = "/home/xhall/Documents/SNID/snid-5.0/snid"


# In[4]:


np.size(np.unique(sample["col8"]))


# In[ ]:


error_array = []
counter = 0
dont_work = 0
dont_work_array = []
for i in np.unique(sample["col8"]):
    gc.collect()
    #try:
        filenoascii = i.split(".")[0]

        fnamelist = sample_location + str(i)

        outputname = str(filenoascii)

        sample_location_temp = sample_location + str(filenoascii)

        output, error, bashCommand = SNID_Analysis.run_files(sample_location_temp, fnamelist, source, filenoascii)

        if(not("No template meets" in str(output)) and not("Correlation function is all zero!" in str(output))):
            SNID_Analysis.plot_best_15(sample_location_temp, outputname, source, image_output)
            gc.collect()
            SNID_Analysis.parse_output(sample_location_temp, source, outputname, filenoascii)
            dont_work += 1
            dont_work_array.append(filenoascii)
    #    else:
    #        print(i, bashCommand)
    except:
        print(i, output, bashCommand)

    if(counter % 100 == 0):
        print(counter)
    counter+=1




