import sys
import os
import numpy as np

## Read US settings
metafile = open("metafile","w")
inf = open("US_settings.txt","r")
data = inf.readlines()
inf.close()
nw = len(data)
cv = []
kappa = []
for w in range(nw):
    ll = data[w].split()
    cv.append(float(ll[0]))
    kappa.append(float(ll[1]))
    corr_time = 1000
    metafile.write("CV/%d.cv %.5f %f %d\n"%(w,cv[-1],kappa[-1],corr_time))
metafile.close()

os.system("python ../SMD_to_determine_US_windows/get_rst_for_each_CV_from_cvfile_dcdfile.py ../SMD_to_determine_US_windows/pull.cv ../SMD_to_determine_US_windows/sys.psf ../SMD_to_determine_US_windows/pull.dcd 0.2 1")
