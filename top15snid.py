import pandas as pd
import numpy as np
from lxml import html
from astropy.table import Table
from astropy.table import Column
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess, glob2, os, argparse
import requests, getpass

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

def get_spectra(sourcename,username,password,path):
	mainurl = 'http://skipper.caltech.edu:8080'
	specpageurl = "http://skipper.caltech.edu:8080/cgi-bin/growth/view_spec.cgi"
	data = {'name':sourcename}
	s = requests.post(url=specpageurl,auth=(username, password),data=data)
	specpage = html.fromstring(s.content)
	try:
		#print '//td/a[contains(text(),'+source['name']+')]'
		speclist = specpage.xpath('//a[contains(text(),"ASCII")]')
		#print speclist
		specname=[]
		for spec in speclist:
			specname.append(spec.get('href'))
		#specdate = (specname[-1])[13:21]
		specurl = mainurl+specname[-1]
		specfile = os.path.basename(specname[-1])
		prefix = os.path.dirname(specname[-1])
		print("All spectrum files are - ")
		for spec in specname:
			print(os.path.basename(spec))
		proceed = raw_input("Selected file is "+specfile+" .Press enter if this file is ok or enter the name of new file. ")
		if(proceed != ''):
			specfile = proceed
			specurl = mainurl+prefix+'/'+specfile
		subprocess.call('wget '+specurl,cwd='/home/yashvi/ZTF/rcf_at_atels/'+path,shell=True)
	except:
		specurl,specdate='',''
		specfile = ''
		print("ERROR : No spectra found for this source")
	return specfile

# f = open('t1.html','r').read()
# t = np.array(pd.read_html(f)[0])
# t = pd.DataFrame(t)
ztfnames = ['ZTF18acbvpzj']#,'ZTF18aarcchg','ZTF18abcfdzu','ZTF18abtvstb','ZTF18abuqhje','ZTF18acbuemc','ZTF18acbvpzj','ZTF18acrwheu']
# names = sorted(glob2.glob('ZTF*'))
# for name in names:
# 	ztfnames.append(os.path.basename(name).split('.')[0])
# ztfnames = np.array(ztfnames)

new_t = pd.DataFrame(columns=['ZTF Name', 'TNS Name', 'Link', 'Classification', 'z(Marshall)', 'z_host(NED)', 'snid_z_std', 'snid_z_err_avg'])
# errorfile = open('error.txt','a')
z_std, z_err_avg = [],[]
username = ''
password = ''

for s,source in enumerate(ztfnames):
	print(source)
	# if(glob2.glob(source)!=[]):
	# 	continue
	subprocess.call('mkdir '+source, shell=True)
	specfile = get_spectra(source,username,password,source)
	if(specfile==''):
		#errorfile.write(source+'\n')
		z_std.append(0)
		z_err_avg.append(0)
		continue
	try:
		z,z_err = [],[]
		# specfile = names[s]
		#subprocess.call("mv "+specfile+" "+source+"/",shell=True)
		specfile = os.path.basename(glob2.glob(source+'/*.ascii')[0])
		subprocess.call('snid verbose=0 plot=0 fluxout=15 '+specfile, cwd=source,shell=True)
		#print specfile
		input_spec = source+'/'+specfile[0:-6]+'_snidflux.dat'
		#input_spec = source+'/'+source+'_snidflux.dat'
		snid_specs = sorted(glob2.glob(source+'/*comp*'))
		plotfile = PdfPages('snidfits_emclip_'+source+'.pdf')
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
			z.append(float(header[9]))
			z_err.append(float(header[11]))
			title = " ".join(header)
			for line in snidspec_data[2:]:
				temp = line.split()
				x.append(float(temp[0]))
				y.append(float(temp[1]))
			specplot(x,y,xi,yi,plotfile,title)
		plotfile.close()
		z_std.append(np.std(z))
		z_err_avg.append(np.mean(z_err))
	except:
		#errorfile.write(source+' snid error \n')
		z_std.append(0)
		z_err_avg.append(0)
		continue
print(z_std)
print(z_err_avg)



