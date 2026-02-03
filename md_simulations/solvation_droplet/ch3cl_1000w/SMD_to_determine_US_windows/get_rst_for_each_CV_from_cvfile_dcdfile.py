import sys
import numpy as np
import MDAnalysis as mda

if len(sys.argv) != 6:
    print ("cvfile, psf, dcd, tol(in CV unit), every(cvframe*every=dcdframe)")
    exit()

cvfilename = sys.argv[1]
psfname = sys.argv[2]
dcdname = sys.argv[3]
tol = float(sys.argv[4])
every = int(sys.argv[5])

## Read US settings
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
cv = np.asarray(cv)
kappa = np.asarray(kappa)
nwindows = len(cv)

cvinf = open(cvfilename,"r")
cvdata = cvinf.readlines()
cvinf.close()

u = mda.Universe(psfname,dcdname)
atoms = u.select_atoms("all")
box = u.trajectory.dimensions
if box is None:
# if (box == np.array([0.,0.,0.,90.,90.,90.])).all():
    box = [20.0,20.0,20.0]
else: box = box[:3]

curr_w = 0
#for i in range(len(cvdata)-1,0,-1):
for i in range(1,len(cvdata)):
    ll = cvdata[i].split()
    cvvalue = float(ll[1])
    if abs(cvvalue - cv[curr_w]) < tol:
        print ("Preparing %d out of %d"%(curr_w+1,nwindows))
        dcd_frame = (i-1)*every
        u.trajectory[dcd_frame]
        pos = atoms.positions

        outfile = open("./rst/%d.rst"%(curr_w),"w")
        outfile.write('<?xml version="1.0" ?>\n')
        outfile.write('<State openmmVersion="8.1" time="0" type="State" version="1">\n')
        outfile.write('    <PeriodicBoxVectors>\n')
        outfile.write('        <A x="'+str(box[0]/10.)+'" y="0" z="0"/>\n')
        outfile.write('        <B x="0" y="'+str(box[1]/10.)+'" z="0"/>\n')
        outfile.write('        <C x="0" y="0" z="'+str(box[2]/10.)+'"/>\n')
        outfile.write('    </PeriodicBoxVectors>\n')
        outfile.write('    <Positions>\n')
        for j in range(len(pos)):
            outfile.write("                <Position x=\"%.12f\" y=\"%.12f\" z=\"%.12f\" />\n"%(pos[j][0]/10.,pos[j][1]/10.,pos[j][2]/10.))
        outfile.write('    </Positions>\n')
        outfile.write("<\State>")
        outfile.close()

        curr_w += 1
    if curr_w >= nwindows: break

print ("Complete")

