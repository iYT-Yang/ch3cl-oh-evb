import sys
import matplotlib.pyplot as plt
import math
import matplotlib
import matplotlib.font_manager as font_manager
import numpy as np

from matplotlib.pyplot import gca

fig = plt.figure(figsize=(3.54,2.54), dpi=600)
#plt.subplots_adjust(left=0.135,bottom=0.125,right=0.98,top=0.98)

Nfile = int((len(sys.argv) - 1))
file = []
for i in range(Nfile):
    file.append(sys.argv[i+1])

for i in range(Nfile):
    f=open(file[i],"r")
    data=f.readlines()
    f.close()
    x=[]
    y=[]
    ycorr=[]
    for j in range(len(data)):
        line = data[j].split()
        if line[0][0] != '#':
            x.append(float(line[0]))
            y.append(float(line[1])) # in kJ/mol
            ycorr.append(float(line[2]))
    x = np.asarray(x)[::100]
    y = np.asarray(y)[::100]-y[0]
    ycorr = np.asarray(ycorr)[::100]
    max_index = np.argmax(y)
    max_x = x[max_index]
    max_y = y[max_index]
    #x,y = zip(*sorted(zip(x, y)))
    #ymin = y[0]
    #y -= ymin
    #plt.plot(x,y,label=sys.argv[i+1])
    print(len(x),len(y))
    if i == 0:
        plt.errorbar(x,y,yerr=ycorr, label=r'CH$_3$Cl+OH+128w',color='red',errorevery=5,linewidth=1,elinewidth=0.5)
        plt.scatter(max_x, max_y, color='red')
        plt.annotate(f'({max_x:.2f}, {max_y:.3f})', (max_x, max_y), textcoords="offset points", xytext=(0,-20), ha='center',color='red')
    if i == 1:
        plt.plot(x,y,label=r'CH$_3$Cl+OH+500w',color='blue')
        plt.scatter(max_x, max_y, color='blue')
        plt.annotate(f'({max_x:.2f}, {max_y:.3f})', (max_x, max_y), textcoords="offset points", xytext=(0,6), ha='center',color='blue')
    
    plt.ylim(top=38)
 
plt.xlabel(r"$\delta (\mathrm{Å})$")
plt.ylabel(r'$\Delta F$ (kJ/mol)')
#plt.title('Free energy profiles for aqueous bulk system averaged over 150 SMD pulls')
#plt.gca().invert_xaxis()
#plt.savefig('SMDPMF.tiff',dpi=600)
plt.legend(loc='lower left')
#plt.grid(alpha=0.5)
plt.savefig('PMF_150_error_block_avg.png',bbox_inches='tight')
plt.show()
