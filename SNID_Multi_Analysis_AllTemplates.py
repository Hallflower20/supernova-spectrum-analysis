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


sample = Table.read("/home/xhall/Documents/NewZTF/ML_sample.ascii", format = "ascii")
sample.rename_column('col1', 'ZTF_Name')
sample.rename_column('col2', "Class")
sample.rename_column('col8', "Version")

sample_2018 = Table.from_pandas(pd.read_hdf("/home/xhall/Documents/NewZTF/final_rcf_table.h5"))

joined_sample = astropy.table.join(sample_2018,sample)

# In[3]:


sample_location = "/home/xhall/Documents/NewZTF/spectra_nonan/"
source = "/home/xhall/Documents/NewZTF/sample_2020/SNIDoutput/"
image_output = "//home/xhall/Documents/NewZTF/sample_2020/ImageOutput/"
snid = "/home/xhall/Documents/SNID/snid-5.0/snid"


# In[4]:




# In[ ]:


error_array = []
counter = 0
dont_work = 0
dont_work_array = []
for i in sample["Version"]:
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
    if(counter % 50 == 0 and counter != 0):
        print(counter)




