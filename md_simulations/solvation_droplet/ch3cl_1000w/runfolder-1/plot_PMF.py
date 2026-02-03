import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.pyplot import gca
import numpy as np

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.subplots_adjust(left=0.2,bottom=0.135,right=0.975,top=0.975)

if len(sys.argv) != 2:
    print ("PMFfile")
    exit()

inf = open(sys.argv[1])
data = inf.readlines()
inf.close()

x = []
y = []
yerr = []
for i in range(len(data)):
    ll = data[i].split()
    if len(ll) <= 0: continue
    if ll[0][0] == "#" or ll[0][0] == "!": continue
    x.append(float(ll[0])) ## in nm
    y.append(float(ll[1])/4.184) ## convert to kcal/mol
    yerr.append(float(ll[2])/4.184) ## convert to kcal/mol
    #y.append(float(ll[1])) ## kJ/mol
    #yerr.append(float(ll[2])) ## kJ/mol

x = np.asarray(x)
y = np.asarray(y)
yerr = np.asarray(yerr)

Fmin = y[0]
y -= Fmin
print(y)
plt.errorbar(x,y,yerr=yerr)


#font = font_manager.FontProperties(family='Times New Roman',style='normal',size=18)
ax=gca()
#labels = ax.get_xticklabels() + ax.get_yticklabels()
#[label.set_fontproperties(font) for label in labels]
plt.tick_params(labelsize=12)

#plt.xlim(-2.0,2.4)
#plt.ylim(-100,50)
#plt.xticks(np.arange(-2.0,2.5,0.2))
#plt.yticks(np.arange(-100,50.5,0.5))
plt.xlabel("Distance to droplet center / $\mathrm{\AA}$",fontsize=15)#,fontname="Times New Roman")
plt.ylabel("$\Delta F$ / $\mathrm{kcal\cdot mol}^{-1}$",fontsize=18,fontname="Times New Roman")
#plt.ylabel("$\Delta F$ / $\mathrm{kJ\cdot mol}^{-1}$",fontsize=15)#,fontname="Times New Roman")

plt.savefig('PMF_80ns.png', dpi=300)
plt.show()
