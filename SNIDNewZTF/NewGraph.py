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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator
import glob
from matplotlib import pyplot
import matplotlib.gridspec as gridspec
import gc


# In[2]:


basedir = "/home/xhall/Documents/"

sample200 = Table.from_pandas(pd.read_csv(basedir + "NewZTF/ML_sample_snid200.csv"))
ML_sample_snid_examples = Table.from_pandas(pd.read_csv(basedir + "NewZTF/ML_sample_snid_brightexamples.csv"))
sample_2018 = Table.from_pandas(pd.read_csv(basedir + "NewZTF/sample_2018/ML_sample_snid_norepeat_2018.csv"))


# In[10]:


source = basedir + "NewZTF/sample_2018/SNIDoutput/"
output = basedir + "NewZTF/sample_2018/ImageOutput/"


# In[4]:


def read_tables(files):
    matches_files = files[0:len(files)-1]
    spectra = Table.read(files[-1], format = "ascii", names = ["wavelength", "flux"])
    matches = []
    for i in matches_files:
        input_data = open(i,'r').readlines()[0].split()
        row = [[int(input_data[3][0]), input_data[4],input_data[5][1::],float(input_data[-3].split("-")[-1]),float(input_data[-1])]]
        row.append(Table.read(i, format = "ascii", names = ["redshifted_wavelength", "flux"]))
        matches.append(row)
    return matches, spectra


# In[5]:


def plot_box_spec(wave, flux): 
    flux_plot = np.repeat(flux, 2)
    wv_plot = wave.copy()
    wv_plot[:-1] += np.diff(wave)/2
    wv_plot = np.append(wave[0]-(wave[1]-wave[0])/2, 
                        np.append(np.repeat(wv_plot[0:-1], 2), 
                                  wave[-1]+(wave[-1]-wave[-2])/2))
    
    return wv_plot, flux_plot


# In[6]:


def specplot(x,y,xi,yi,snid_type,fname,output,best_num, z_template, z_template_unc, z_snid,
             spec_num, show_redshift=False):
    fig, ax = plt.subplots(figsize=(8,4.5))
    ax.plot(xi,yi,color='#32384D',alpha=0.5,
             label='New SN')
    ax.plot(x,y,color='#217CA3',
             label='SNID template', lw=3)
    if show_redshift:
        ax.plot(x[-3],y[-3],color='white',lw=0,
                 label=r'$z_\mathrm{} = $ {:.3f}$\,\pm\,${:.3f}'.format("{SNID}", z_template, z_template_unc))
        ax.text(0.78, 0.955, r'$z_\mathrm{} = ${:.4f}'.format("{SN}", z_snid), 
                va='center',
                fontsize=15, transform=plt.gcf().transFigure)
    else:
        ax.text(0.78, 0.955, 'Match #{}'.format(spec_num + 1), 
                va='center',
                fontsize=15, transform=plt.gcf().transFigure)
        
    ax.plot(x[-3],y[-3],color='#217CA3', lw=3)
    ax.set_xlabel(r'Rest Frame Wavelength ($\mathrm{\AA}$)', fontsize=17)
    ax.set_ylabel('Relative Flux', fontsize=17)
    ax.tick_params(which='both',labelsize=15)
    
    ax.grid(axis='x', color='0.7', ls=':')
    ax.xaxis.set_minor_locator(MultipleLocator(250))
    ax.set_yticklabels([])

    
    ax.text(0.105, 0.955, 'SNID type: ', 
            va='center',
            fontsize=15, transform=plt.gcf().transFigure)
    ax.text(0.245, 0.955, snid_type, 
            color='#217CA3', weight='bold', va='center',
            fontsize=23, transform=plt.gcf().transFigure)

    
    
    ax.legend(fancybox=True)
    fig.subplots_adjust(left=0.055,right=0.99,top=0.925,bottom=0.145)
    fig.savefig(output + 'snidfits_emclip_' + fname + "_" + str(best_num) + '.png', dpi = 600)
    plt.close(fig)
    plt.close()


# In[7]:


def plot_best_5(source, output, spectra_name, z_snid, show_redshift=False):
    source_folder = source + spectra_name
    
    files = np.sort(glob.glob(source_folder+"/*.dat"))
    if(len(files)==0):
        print(spectra_name)
        return -1
    matches, spectra = read_tables(files)
    
    for spec_num, i in enumerate(matches):
        z = i[0][3]
        snid_type = i[0][2][:-1]
        
        xi, yi = plot_box_spec(spectra["wavelength"], spectra["flux"])
        xi /= (1+z)
        x, y = i[1]["redshifted_wavelength"] / (1+z), i[1]["flux"]
        specplot(x,y,xi,yi,snid_type,spectra_name,output,i[0][0], z, i[0][4], z_snid, spec_num, show_redshift=show_redshift)


# In[ ]:


counter = 0
for i in sample_2018:
    spectra_name = i["Version"].split(".")[0]
    z_snid = i["z_snid"]
    plot_best_5(source,output,spectra_name,z_snid, show_redshift = False)
    gc.collect()
    if(counter%20 == 0):
        print(counter)
    counter += 1


# In[13]:


pngs = glob.glob(output + "/*.png")


# In[15]:


len(pngs)


# In[17]:


len(sample_2018)*5


# In[25]:


glob.glob(source + "/ZTF18aaxdrjn_20180531_P60_v1/*.*")


# In[23]:


read_tables(np.sort(glob.glob(source + "/ZTF18aaxdrjn_20180531_P60_v1/*.dat")))


# In[27]:


glob.glob(source + "/ZTF18aabssth_20180309_P60_v1/*.dat")


# In[12]:


plot_best_5("/home/xhall/Documents/RandomSNID/","/home/xhall/Documents/RandomSNID/","lris20201012_ZTF20acdehpz",0.1751)


# In[30]:


plt.boxplot([2 * -1, 2 * 1])
plt.hlines(.5,.75,1.25, color = "Blue")


# In[ ]:




