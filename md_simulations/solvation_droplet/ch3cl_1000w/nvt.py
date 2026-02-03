import openmm as mm
import openmm.app as app
from openmm.unit import *
from sys import stdout, exit, stderr, argv
from datetime import datetime as dtt
import numpy as np
from openmmplumed import *

starttime = dtt.now()
print(starttime)
stdout.flush()

def forcegroupify(system):
    forcegroups = {}
    for i in range(system.getNumForces()):
        force = system.getForce(i)
        force.setForceGroup(i)
        forcegroups[force] = i
    return forcegroups

def getEnergyDecomp(context, forcegroups):
    energies = {}
    for f, i in forcegroups.items():
        energies[f] = context.getState(
            getEnergy=True, groups=1 << i).getPotentialEnergy()
    return energies

window = int(sys.argv[1])

## Read US settings
inf = open("US_settings.txt","r")
data = inf.readlines()
inf.close()
ll = data[window].split()
biascenter = float(ll[0])
kappa = int(ll[1])

#####################Set steps
jobname='nvt-%d'%(window)
forcefield = app.ForceField('../toppar.xml')
Temp=300

dt=0.5*femtoseconds ##use 1.0 fs for DRUDE and flexible H-bonds
equilibrationSteps = 2e06 # 1 ns (equilibrate the system first before production)
steps=int(2*2e06) # 2 ns (production run)

nsavcrd=2000 ###save frequency for .dcd
nprint=2000 ###save frequency for .log

print('###Loading things###')
psf = app.CharmmPsfFile('../sys.psf')

print('###Building system###')
###for nonPBC
system = forcefield.createSystem(psf.topology, nonbondedMethod=app.NoCutoff, constraints=None, rigidWater=False)

###set up a wall potential to prevent evaporated water from escaping
wall = mm.CustomCentroidBondForce(1,"kref*step(r-rmax)*(r-rmax)^2; r=sqrt(x1^2+y1^2+z1^2)")
wall.addPerBondParameter('kref')
wall.addPerBondParameter('rmax')
for i in range(5000):
    if i % 5 == 2:
        continue
    wall.addGroup([i])
for i in range(wall.getNumGroups()):
    wall.addBond([i],[2000.0*kilojoules_per_mole/(nanometer)**2, 6.0*nanometer])
wall.setUsesPeriodicBoundaryConditions(False)
system.addForce(wall)

###plumed script
script = """
UNITS LENGTH=A TIME=fs
c1: COM ATOMS=1-5000   NOPBC
c2: COM ATOMS=5001-5007 NOPBC
origin: FIXEDATOM AT=0,0,0

dist: DISTANCE ATOMS=c1,c2 COMPONENTS NOPBC
dist2: DISTANCE ATOMS=c1,origin NOPBC

restraint: RESTRAINT ARG=dist.z AT=%.5f KAPPA=%i
restraint3: RESTRAINT ARG=dist.x AT=0 KAPPA=83.680
restraint4: RESTRAINT ARG=dist.y AT=0 KAPPA=83.680
restraint2: RESTRAINT ARG=dist2 AT=0 KAPPA=83.680

PRINT ARG=dist.z,restraint.bias STRIDE=200 FILE=CV/%d.cv
"""%(biascenter,kappa,window)

###add plumed force to the system
system.addForce(PlumedForce(script))

###integrator for nonDrude NVT simulations
# integrator = mm.LangevinMiddleIntegrator(Temp*kelvin, 1./picosecond, dt)
# integrator.setConstraintTolerance(1e-06)

###integrator for Drude non-NVE simulations
integrator = mm.DrudeLangevinIntegrator(Temp*kelvin, 5/picosecond, 1*kelvin, 20/picosecond, dt)
integrator.setMaxDrudeDistance(0.02)
integrator.setConstraintTolerance(1e-06)

#for energy decomposition later
fgrps = forcegroupify(system)

platname = 'CUDA'
platform = mm.Platform.getPlatformByName(platname)
prop = dict(CudaPrecision='mixed') ###use mixed for NVT, double for NVE
platform.loadPluginsFromDirectory('/home/yutong/software/myOpenMM-plumed-plugin/openmm-plumed1.0_install/lib/plugins/')

simulation = app.Simulation(psf.topology, system, integrator, platform, prop)

###restart from .rst
print('#Startting from ','.rst')
simulation.loadState('rst/%s.rst'%(window))
simulation.context.setTime(0)
simulation.context.setStepCount(0)

# print out initial energies
print('#Initial Frame Energies')
box = simulation.context.getState().getPeriodicBoxVectors()
print('Box:', box)
state = simulation.context.getState(getPositions=True, getEnergy=True)
print('PE', state.getPotentialEnergy().value_in_unit(kilojoules_per_mole),'kJ/mol')
for k, v in getEnergyDecomp(simulation.context, fgrps).items():
    print(k.__class__.__name__, v.value_in_unit(kilojoules_per_mole),'kJ/mol')

# equilibrate the system before production
print('Equilibrating...')
simulation.step(equilibrationSteps)

####set up reporter object before production run
stdout.flush()
dcd=app.DCDReporter(jobname+'.dcd', nsavcrd)
firstdcdstep = nsavcrd
dcd._dcd = app.DCDFile(dcd._out, simulation.topology,simulation.integrator.getStepSize(), firstdcdstep, nsavcrd)
simulation.reporters.append(dcd)
simulation.reporters.append(app.StateDataReporter(jobname+'.log',nprint, step=True, time=True, kineticEnergy=True, potentialEnergy=True,totalEnergy=True, temperature=True, speed=True,separator=',  '))

# run MD (production run)
print('###Running Dynamics###')
simulation.currentStep = 0
simulation.step(steps)

###create restart file
state = simulation.context.getState(getPositions=True,getVelocities=True,getEnergy=True)
with open(jobname + '.rst', 'w') as f:
    f.write(mm.XmlSerializer.serialize(state))

# print out final energies
print('#Final Frame Energies')
print('PE', state.getPotentialEnergy().value_in_unit(kilojoules_per_mole),'kJ/mol')
for k, v in getEnergyDecomp(simulation.context, fgrps).items():
    print(k.__class__.__name__, v.value_in_unit(kilojoules_per_mole),'kJ/mol')
box = simulation.context.getState().getPeriodicBoxVectors()
print('Box:', box)

endtime = dtt.now()
print(endtime)
print(endtime-starttime)
