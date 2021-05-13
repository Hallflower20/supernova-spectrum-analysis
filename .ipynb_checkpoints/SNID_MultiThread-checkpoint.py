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
import threading
import logging


# In[2]:


sample = Table.read("/home/xhall/Documents/NewZTF/ML_sample.ascii", format = "ascii")


# In[3]:


sample_location = "/home/xhall/Documents/NewZTF/spectra/"
source = "/home/xhall/Documents/NewZTF/SNIDoutput/"
image_output = "/home/xhall/Documents/NewZTF/Images/"
snid = "/home/xhall/Documents/SNID/snid-5.0/snid"


# In[4]:

def SNID_run(i):
    try:
        filenoascii = i.split(".")[0]

        fnamelist = sample_location + str(i)

        outputname = str(filenoascii)

        sample_location_temp = sample_location + str(filenoascii)

        output, error, bashCommand = SNID_Analysis.run_files(sample_location_temp, fnamelist, source, filenoascii)

        if(not("No template meets" in str(output)) and not("Correlation function is all zero!" in str(output))):
            SNID_Analysis.plot_best_15(sample_location_temp, outputname, source, image_output)
            SNID_Analysis.parse_output(sample_location_temp, source, outputname, filenoascii)
    except:
        print(i, bashCommand)


# In[ ]:

if __name__ == "__main__":
    counter = 0
    for i in np.unique(sample["col8"]):
        SNID_run(i)
        counter += 1
        gc.collect()
        if(counter%100 == 0):
            print(counter)
    """
    threads = []
    for i in np.unique(sample["col8"]):
        threads.append(threading.Thread(target=SNID_run, args=(i,)))
    print("Threads Created")
    length = (len(np.unique(sample["col8"])))
    ranges = np.linspace(0,length,500)
    for i in range(len(ranges)-1):
        for i in threads[int(ranges[i]):int(ranges[i+1])]:
            i.start()
        for i in threads[int(ranges[i]):int(ranges[i+1])]:
            i.join()
        print("Round" + str(i))
        break
    """

