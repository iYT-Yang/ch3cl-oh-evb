import sys
import matplotlib.pyplot as plt
import numpy as np

print ("Make sure the energy is in kJ/mol and CV is in nm in the PES file.")
print ("Change RT in the script if needed.")
print ("Change CVmin and CVmax as needed.")

RT = 8.3145 * 300.0 / 1000.0
CVmin = -4.0 ## should be smaller than PES_CVmin
CVmax = 1.0 ## should be larger than PES_CVmax

if len(sys.argv) != 4:
    print ("pes_file, tol_diff, tol_std")
    exit()

tol_diff = float(sys.argv[2])
tol_std = float(sys.argv[3])

pes_file = open(sys.argv[1],"r")
pesdata = pes_file.readlines()
pes_file.close()
CV = []
PES = []
for i in range(len(pesdata)):
    ll = pesdata[i].split()
    if ll[0][0] == "#": continue
    CV.append(float(ll[0]))
    PES.append(float(ll[1]))

## just to append to head and tail of CV, set equal to the value at bounds.
PESCVmin=CV[0]
PESCVmax=CV[-1]
dCV = (CV[-1] - CV[0]) / len(CV)
Fmin=PES[0]
Fmax=PES[-1]

if PESCVmin > CVmin:
    addCV = []
    addPES = []
    aCV = PESCVmin
    while aCV > CVmin:
        aCV -= dCV
        addCV.append(aCV)
        addPES.append(Fmin)
    addCV.reverse()
    addPES.reverse()
    CV = addCV + CV
    PES = addPES + PES

if PESCVmax < CVmax:
    addCV = []
    addPES = []
    aCV = PESCVmax
    while aCV < CVmax:
        aCV += dCV
        addCV.append(aCV)
        addPES.append(Fmax)
    CV = CV + addCV
    PES = PES + addPES

CV = np.asarray(CV)
PES = np.asarray(PES)

def numerical_force(CV,PES):
    xf = []
    yf = []
    nlines = len(CV)
    for i in range(nlines-1):
        dF = PES[i+1] - PES[i]
        dx = CV[i+1] - CV[i]
        force = -dF/dx
        mid = (CV[i+1] + CV[i]) / 2.
        xf.append(mid)
        yf.append(force)
    return xf, yf

def biasPE(x,kappa,bias_center):
    return 0.5*kappa*(x - bias_center)**2

xf, yf = numerical_force(CV,PES)
xf = np.asarray(xf)
yf = np.asarray(yf)
maxf_slot = np.argmax(abs(yf))

kappaL = np.arange(1,1000,1)
bias_center = xf[maxf_slot]

for kappa in kappaL:
    y_biased = []
    Pb = []
    for i in range(len(CV)):
        y_biased.append(PES[i]+biasPE(CV[i],kappa,bias_center))
        Pb.append(np.exp(-y_biased[-1]/RT))

    xf = np.asarray(xf)
    yf = np.asarray(yf)
    y_biased = np.asarray(y_biased)

    Pb = np.asarray(Pb)
    Pb /= np.sum(Pb)

    mean_biased_x = np.sum(CV*Pb)
    mean_biased_sqx = np.sum(CV**2*Pb)
    std_biased_x = np.sqrt(mean_biased_sqx - mean_biased_x**2)
    diff = abs(mean_biased_x - bias_center)

    slot = np.argmin(abs(CV - bias_center))
    bias_center_force = yf[slot]

    if std_biased_x <= tol_std and diff <= tol_diff:
        print ("set maxforce_CV = bias_center: ", bias_center)
        print ("bias_kappa needed: ", kappa)
        print ("bias_center_PESforce: ", bias_center_force)
        print ("mean(CV): ", mean_biased_x)
        print ("diff between mean(CV) and bias_center: ", diff)
        print ("std(CV): ", std_biased_x)
        exit()

print ("Optimal kappa not found, could be that kappa required is too large.")
print ("Relax the diff and std tolerance.")

