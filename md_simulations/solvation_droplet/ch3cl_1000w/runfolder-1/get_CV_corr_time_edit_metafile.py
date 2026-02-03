import sys
import numpy as np
from scipy.optimize import curve_fit

if len(sys.argv) != 3:
    print ("inmetafile, outmetafile")
    exit()

inf = open(sys.argv[1],"r")
data = inf.readlines()
inf.close()

outf = open(sys.argv[2], "w")
nfiles = len(data)

max_every = 5000

def func1(t,tau):
    return np.exp(-t/tau)

for file in range(nfiles):
    ll = data[file].split()
    ll = ll[:3] ## exclude correlation time column
    cvfile = ll[0]

    print (cvfile)

    time, x = np.loadtxt(cvfile,usecols=(0,1), unpack=True)
    if len(x) % 2 != 0:
        time = time[:-1]
        x = x[:-1]
    first_t = time[0]
    time -= first_t

    ndata = len(time)
    dt = time[1] - time[0]

    xmean = np.mean(x)
    x -= xmean

    padx = np.zeros(len(time)*2)
    padx[len(time)//2:len(time)+len(time)//2] = x
    X = np.fft.rfft(padx)
    acfx = np.fft.irfft(abs(X)**2)[:ndata] / np.arange(ndata,0,-1)
    norm = acfx[0]
    acfx /= norm

    isfound = False
    for every in range(1,max_every+1):
        nt = len(time[::every])
        newt = np.arange(0,nt,1)
        popt_e, pcov_e = curve_fit(func1,newt,acfx[::every],maxfev=10000,bounds=[[0.000001],[np.inf]])
        if popt_e[0] < 1.0: ## less than 1 step, uncorrelated
            tau = every
            isfound = True
            break

    if not isfound:
        print ("Error: tau_fit_every is beyond 5000 frames for %s."%(cvfile))
        print ("Collect more data first or increase max_every.")
        exit()

    outf.write("%s %s %s %s\n"%(ll[0],ll[1],ll[2],round(tau)))

outf.close()
