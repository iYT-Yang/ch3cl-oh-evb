import sys
import numpy as np
from scipy.interpolate import make_smoothing_spline
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    print ("inf, outf, lam(0.000001)")
    exit()

inf = open(sys.argv[1],"r")
data = inf.readlines()
inf.close()

x = []
y = []
for i in range(len(data)):
    ll = data[i].split()
    if ll[0][0] == "#" or ll[0][0] == "!": continue
    x.append(float(ll[0]))
    y.append(float(ll[1]))

x = np.asarray(x)
y = np.asarray(y)

ynew = make_smoothing_spline(x, y, lam=float(sys.argv[3]))

outf = open(sys.argv[2],"w")
for i in range(len(x)):
    outf.write("%f %f\n"%(x[i],ynew(x[i])))
outf.close()

plt.plot(x,y)
plt.plot(x,ynew(x))
plt.show()
