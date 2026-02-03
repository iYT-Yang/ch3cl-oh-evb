# OH Oxidation of Methyl Chloride at Air-Water Interface

This repository contains the data, force-field parameters, EVB implementation, and representative molecular dynamics (MD) simulations accompanying the study:

> *Accelerated OH Oxidation of Methyl Chloride via Surface Accumulation at the Air-Water Interface*  
> *Yutong Yang, Chung Chi Chio, and Ying-Lung Steve Tse*  
> *[Journal, Year, DOI]*

The focus of the work is an empirical valence bond (EVB) model for the oxidation reaction of methyl chloride, CH<sub>3</sub>Cl, by the OH radical at the air-water interface. The repository provides some input files and example outputs needed to reproduce the main calculations and figures in the paper:

- EVB and classical force-field parameters
- Input files and scripts for representative MD simulations
- Processed data (PMFs, RDFs, QM reference PES, etc.)
- Analysis scripts (PMF, Jarzynski analysis, error bars)

If you use this repository, please cite the paper above.

---

## Repository structure

```text
.
├── analysis/          # Python scripts used to analyze trajectories and PMFs
├── data/              # Processed data used for figures (PMFs, RDFs, QM PES, etc.)
├── evb/               # Standalone EVB implementation (Python module)
├── forcefield/        # EVB and classical FF parameters (CHARMM/OpenMM style)
├── md_simulations/    # Representative MD input files, scripts, and selected trajectories
├── qm/                # Quantum chemistry reference data (IRC and stationary points)
└── README.md          # This file
```

---

## Quick start
### 1. EVB model and force-field parameters
The EVB implementation and parameters used in the paper are provided in:

- `evb/` – Python module implementing the EVB Hamiltonian and utilities.
- `forcefield/` – Parameter files:
  - `para.json`: EVB parameter set used in the simulations
  - `off.xml`, `toppar.xml`, `toppar.str`: force-field definitions
  - `computed_energy_with_this_evb_model.txt`: sanity-check energies for the EVB model

These files are also duplicated in relevant MD folders under `md_simulations/` (e.g. in various `inits/` subdirectories) so each system can be run independently.

### 2. MD simulations
`md_simulations/` contains representative input files and scripts for the different types of simulations discussed in the paper:

- `rdf/` – Example simulation and scripts to compute O–O* radial distribution functions.
- `reactive_bulk/` – EVB-based steered MD and umbrella sampling for the reaction in bulk water, using systems with 128, 500, and 1000 waters.
- `reactive_slab/` – EVB-based steered MD and umbrella sampling for the reaction at air–water interfaces with different vertical positions and effective coordination numbers.
- `solvation_droplet/` – Solvation free-energy simulations for CH<sub>3</sub>Cl and OH radical in droplets of various sizes, including umbrella sampling setups.

Each major subdirectory contains its own README describing how the example was run and how to regenerate the key observables (PMFs, etc.).

### 3. Data used for figures
The `data/` directory collects the processed numerical data used in the figures:

- `reactive_pmfs/`: 1D PMFs for the reaction in bulk and slabs, including different numbers of waters and slab positions.
- `solvation_pmfs/`: PMFs for solvation and surface affinity of CH<sub>3</sub>Cl and OH in droplets and slabs.
- `rdf/`: O–O* RDF data.
- `qm_pes/`: QM reference PES along the IRC.

Running the analysis scripts in `analysis/` reproduces processed curves and error estimates from the raw MD outputs.

### 4. Quantum chemistry reference data
The `qm/` folder contains all quantum chemistry input and output files used to construct the reference potential energy surface and stationary points:

- `cluster_irc/`: IRC calculation and single-point TightPNO DLPNO-CCSD(T)/aug-cc-pVQZ energies along the reaction path.
- `stationary_points_coord/`: Optimized geometries and logs for reactant, product, and transition state, plus convenient .xyz files.
