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


# In[2]:


sample_location = "/home/xjh0560/SNID/sample/spectra/"
source = "/home/xjh0560/SNID/snid_outputs/"
image_output = "/home/xjh0560/SNID/snid_outputs/SNIDimages/"
param = "/mnt/c/users/20xha/Documents/GitHub/supernova-spectrum-analysis/snid.param"
snid = "/mnt/c/users/20xha/Documents/Caltech/Research/SNID/snid-5.0/snid"


# In[3]:


def run_files(fname, fnamelist, source):
    new_source = source + fname.split("/")[-1].split(".")[0]
    if(not(os.path.exists(new_source))):
        os.mkdir(new_source)
    bashCommand = snid + " " + param + " " + fnamelist
    process = subprocess.Popen(shlex.split(bashCommand), stdout = subprocess.PIPE, stderr = subprocess.PIPE , cwd=new_source)
    output, error = process.communicate()
    return output, error


# In[4]:


def specplot(x,y,xi,yi,plotfile,title):
    fig = plt.figure()
    plt.plot(xi,yi,color='gray',label='Input Spectrum')
    plt.plot(x,y,color='red',label='SNID fit')
    plt.title(title)
    plt.xlabel('Redshifted Wavelength (A)')
    plt.ylabel('Flux (a.u.)')
    plt.legend()
    plotfile.savefig()
    plt.close()


# In[5]:


def plot_best_15(specfile, flist, overall_source, output):
    fname = specfile.split("/")[-1].split(".")[0]
    source = overall_source + fname
    
    if(specfile==''):
        return(0, 0)
    z,z_err = [],[]
    input_spec = source+'/'+flist.split("/")[-1].split(".")[0]+'_snidflux.dat'
    #input_spec = source+'/'+source+'_snidflux.dat'
    snid_specs = sorted(glob2.glob(source+'/*comp*'))
    plotfile = PdfPages(output + '/snidfits_emclip_'+fname+'.pdf')
    input_data = open(input_spec,'r').readlines()
    xi,yi=[],[]
    for line in input_data[1:]:
        temp = line.split()
        xi.append(float(temp[0]))
        yi.append(float(temp[1]))

    for i, spec in enumerate(snid_specs):
        snidspec_data = open(spec,'r').readlines()
        x,y = [],[]
        header = snidspec_data[0].split()
        title = " ".join(header)
        for line in snidspec_data[2:]:
            temp = line.split()
            x.append(float(temp[0]))
            y.append(float(temp[1]))
        specplot(x,y,xi,yi,plotfile,title)
    plotfile.close()


# In[6]:


def parse_output(specfile, flist, overall_source, returnoutput = False):
    fname = specfile.split("/")[-1].split(".")[0]
    flist_versionname = flist.split("/")[-1].split(".")[0]
    source = overall_source + fname
    
    f = open(source + "/" + flist_versionname + "_snid.output", "r")
    
    lines = f.readlines()
    Types_summary = lines[38:67]
    
    Types_summary_file = open(source + "/" + flist_versionname + "_snid_types.readableoutput", "w")
    for i in Types_summary:
        Types_summary_file.write(i)
    Types_summary_file.close()
    if(returnoutput):
        Types_Summary_Table = Table.read(source + "/" + flist_versionname + "_snid_types.readableoutput", format = "ascii")
    
    Template_Listings = lines[69:-1]
    Template_Listings_file = open(source + "/" + flist_versionname + "_snid_templates.readableoutput", "w")
    for i in Template_Listings:
        Template_Listings_file.write(i)
    Template_Listings_file.close()
    if(returnoutput):
        Template_Listings_Table = Table.read(source + "/" + flist_versionname + "_snid_templates.readableoutput", format = "ascii")
        return Types_Summary_Table, Template_Listings_Table


# In[9]:


def run_all(fname, flist, source, output):
    run_files(fname, flist, source)
    plot_best_15(fname, flist, source, output)
    return(parse_output(fname, flist, source))


# In[162]:





# In[127]:





# In[ ]:





# In[ ]:




