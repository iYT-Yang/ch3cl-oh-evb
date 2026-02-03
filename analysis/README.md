# analysis

This directory contains Python scripts used to post-process trajectories and free-energy data from the MD simulations.

## Files

- `plotPMF-errorbar-block-avg.py`  
  Block-averages 1D PMFs to estimate statistical uncertainties.

  **Input:**  
  - One or more PMF files (e.g. WHAM outputs) from independent segments or block partitions.
  - Command-line arguments (see comments at the top of the script).

  **Output:**  
  - Text file with mean PMF and error bars.
  - Optionally, a plot (e.g. PDF/PNG) if configured in the script.

- `smd_jarzynski_analysis.py`  
  Performs Jarzynski analysis of steered MD (SMD) work values.

  **Input:**  
  - Time series of collective variable(s) and work from SMD runs (see `md_simulations/reactive_*` folders for examples).

  **Output:**  
  - Free-energy profile from the nonequilibrium work distribution.
  - Optional plots summarizing convergence.

## Usage

These scripts are meant to be run from within the corresponding simulation result directories under `md_simulations/`. 

For details on which PMF or work files correspond to which figure, see the main paper and the descriptions in:

- `data/reactive_pmfs/`
- `data/solvation_pmfs/`
- `md_simulations/reactive_bulk/README`
- `md_simulations/reactive_slab/README`
- `md_simulations/solvation_droplet/README`
