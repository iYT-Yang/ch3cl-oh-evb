import glob
import os,sys
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from scipy.stats import norm
from scipy.optimize import curve_fit

###### method 1 #######
#file_location = os.path.join('US*','colvar')
#filenames = glob.glob(file_location)
#print(filenames)

###### method 2 #######
#delta_kappa_list = [[2.0,250],[1.5,250],[1.0,500],[0.6,800],[0.4,1000],[0.2,2000],[0.1,2500],[0.0,2500],[-0.1,2500],[-0.2,2000],[-0.4,1000],[-0.6,800],[-1.0,500],[-1.5,250],[-2.0,250]]
#filenames = []
#for delta_kappa in delta_kappa_list:
#    d = str(delta_kappa[0])
#    k = str(delta_kappa[1])
#    dic = "US_" + d + "_k" + k + "/colvar"
#    filenames.append(dic)
#print(filenames)


###### method 3 #######
#if len(sys.argv)!=2:
  #  print ("Need input: run cycle number")
  #  exit()

#metafileName="metafile_"+sys.argv[1]
metafileName="metafile"

with open(metafileName,"rt") as fn:
    lines = fn.readlines()
    # Remove lines starting with '#' character
    lines = [line.strip() for line in lines if not line.startswith('#')]
    filenames = []
    for x in lines:
        filenames.append(x.split(' ')[0])
print(filenames)

fig,ax = plt.subplots(figsize=(15,7))

for f in filenames:
    try:
        with open(f, 'r') as file:
            data = np.genfromtxt(fname=f,skip_header=1)
    except FileNotFoundError:
        print(f"File '{f}' does not exist.")
        continue
    cv = data[:,1]
    n_bins = (max(cv)-min(cv))*50
    n_bins = int(n_bins)

    ### use sns ###
    # sns.histplot(cv,kde=True,bins=n_bins,color=np.random.rand(3,))
   
    ### use hist and fit Gaussian distribution ###
    def gaussian(x, amp, cen, wid):
        return amp * np.exp(-(x-cen)**2 / (2*wid**2))
    counts, bin_edges = np.histogram(cv, bins=n_bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    p0 = [1.0, np.mean(cv), np.std(cv)]
    #coeff, _ = curve_fit(gaussian, bin_centers, counts, p0=p0)
    x = np.linspace(np.min(cv), np.max(cv), 50) 
    #y = gaussian(x, *coeff)   
    ax.hist(cv, bins=n_bins, density=True, alpha=0.5, label=f)
    ax.xaxis.set_ticks(np.arange(0,50,5))
    #ax.plot(x, y, 'r-')
    #cen = coeff[1]
    #ax.axvline(x=cen, color='k', linestyle='--') # label='Central point: {:.2f}'.format(cen)) # Label central point of Gaussian function on the plot
    ax.legend()

    ax.set_xlabel(r"$\xi$")
    ax.set_ylabel('Density')

plt.savefig('overlapping.png',dpi=300)
plt.show()
