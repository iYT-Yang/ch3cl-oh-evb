import sys
from US_settings_func import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.font_manager as font_manager
from matplotlib.pyplot import gca
matplotlib.rcParams['mathtext.fontset'] = 'stix'
plt.subplots_adjust(left=0.160,bottom=0.140,right=0.980,top=0.985)

print ("\nThis script optimizes the no. of US windows, and their bias_center(furthest that can satisfy tol_std) and kappa(smallest that can satisfy tol_diff) to ensure sufficient coverage of the whole CV space and overlapping between windows. It requires a rough estimate of PMF let's say from 1SMD run.\n")

print ("Settings: tol_diff[in CV unit] is the tolerance for choosing kappa. It controls how close <CV> must be from the bias_center.")
print ("Settings: tol_std[in std(CV)] is the tolerance for controlling CV coverage. Each CV value from CVmin to CVmax must be within tol_std*std(CV) from at least 1 window.\n")

print ("Tips: Roughly at tol_std=1.0: overlap with 2 adjacent windows.")
print ("Tips: Roughly at tol_std=0.8: overlap with 3 adjacent windows.")
print ("Tips: If your PMF is a bit rough, try using smooth_PMF.py first.\n")

print ("Note: up_resolution is set to True, which doubles the no. of points in CV by linear interpolation.")
print ("Note: kappa is in kJ/mol.CVunit^2.")
print ("Note: minimum kappa is set to 100, change kappaL if needed.")
print ("Note: Ubias = 0.5*kappa*(CV-bias_center)**2.")
print ("Note: Output file: US_settings.txt (bias_center, kappa).\n")

if len(sys.argv) != 7:
    print ("pes_file, CVmin, CVmax, Temp(300), tol_diff(0.01), tol_std(0.8)")
    exit()

## double the no. of points along CV
up_resolution = True

## bias strength to consider
#kappaL = np.arange(100,1000000,100) ## the O-H bond kappa in water is around 260k (distance in nm)
kappaL = np.arange(1,50,1) ## the O-H bond kappa in water is around 260k (distance in nm)
pesname = sys.argv[1]
min_bias_center = float(sys.argv[2])
max_bias_center = float(sys.argv[3])
RT = 8.3145 * float(sys.argv[4]) / 1000.0
tol_diff = float(sys.argv[5])
tol_std = float(sys.argv[6]) ## smaller than this value for all CV slots
outf = open("US_settings.txt","w")

CV, PES, dCV = read_pes(pesname,min_bias_center,max_bias_center,up_resolution)
kappa_CV = get_kappa_2nd_d(CV,PES)

first_slot = np.argmin(abs(CV - min_bias_center))
last_slot = np.argmin(abs(CV - max_bias_center))
curr_slot = first_slot

## first window
bias_center = min_bias_center
starting_kappa = kappa_CV[curr_slot]
kappa, w_mean_CV, w_std_CV, Pb = \
get_minkappa_2nd_d(bias_center,kappaL,CV,dCV,PES,RT,min_bias_center,max_bias_center,tol_diff,starting_kappa)

w_coverage_std = abs((CV[curr_slot:last_slot+1] - w_mean_CV) / w_std_CV)
if w_coverage_std[0] > tol_std:
    print ("Error: first window does not cover CVmin. Try tighter tol_diff.")
    exit()

outf.write("%.5f %i\n"%(bias_center,kappa))
print ("##bias_center, kappa, mean(CV), std(CV)##")
print (bias_center, kappa, w_mean_CV, w_std_CV)
plt.plot(CV,Pb)

curr_slot += np.argmax(w_coverage_std > tol_std)
prev_bias_center_slot = first_slot

## intermediate windows
while True:
    search_slot = np.argmin(abs(CV - (CV[curr_slot] + w_std_CV*3)))
    if search_slot > last_slot: search_slot = last_slot
    bias_center = CV[search_slot]

    while True:
        start_kappa = kappa_CV[search_slot]
        kappa, w_mean_CV, w_std_CV, Pb = \
        get_minkappa_2nd_d(bias_center,kappaL,CV,dCV,PES,RT,\
        min_bias_center,max_bias_center,tol_diff,starting_kappa)
        w_coverage_std = abs((CV[curr_slot:last_slot+1] - w_mean_CV) / w_std_CV)
        if w_coverage_std[0] > tol_std:
            search_slot -= 1
            bias_center = CV[search_slot]
            if search_slot < prev_bias_center_slot:
                print ("Error: bias_center, kappa pair not found for CV=%.5f."%(CV[curr_slot]))
                exit()
            continue
        break

    print (bias_center, kappa, w_mean_CV, w_std_CV)
    outf.write("%.5f %i\n"%(bias_center,kappa))
    plt.plot(CV,Pb)

    ## check if all CV slots are well covered
    if np.all(w_coverage_std <= tol_std): break

    curr_slot += np.argmax(w_coverage_std > tol_std)
    prev_bias_center_slot = search_slot
outf.close()

plt.xlabel('CV',fontsize=18,fontname="Times New Roman")
plt.ylabel(r'$P^\mathrm{b}$',fontsize=18,fontname="Times New Roman")

font = font_manager.FontProperties(family='Times New Roman',style='normal',size=14)
ax=gca()
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname("Times New Roman") for label in labels]
plt.tick_params(labelsize=18)

plt.xlim(np.min(CV),np.max(CV))
plt.savefig("estimated_overlapping.png", dpi=300)
plt.show()

