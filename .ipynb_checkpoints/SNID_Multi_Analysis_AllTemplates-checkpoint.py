#!/usr/bin/env python
# coding: utf-8

# In[1]:

import astropy
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


sample = Table.read("/home/xhall/Documents/ZTFI/stuff_left.csv")

# In[3]:


sample_location = "/home/xhall/Documents/ZTFI/sample_nonan/"
source = "/home/xhall/Documents/ZTFI/remaining_output/"
image_output = "/home/xhall/Documents/ZTFI/remaining_image_output/"
snid = "/home/xhall/Documents/SNID/snid-5.0/snid"


# In[4]:




# In[ ]:


error_array = []
counter = 0
dont_work = 0
dont_work_array = []
for i in sample["Version"]:
    print(counter)
    gc.collect()
    try:
        counter += 1

        filenoascii = i.split(".")[0]

        fnamelist = sample_location + str(i)

        outputname = str(filenoascii)

        sample_location_temp = sample_location + str(filenoascii)

        output, error, bashCommand = SNID_Analysis.run_files(sample_location_temp, fnamelist, source, filenoascii)
    except:
        print(i)
    if(counter % 50 == 0):
        print(counter, len(sample))
    break



