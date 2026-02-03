# qm/stationary_points_coord

Stationary points on the CH3<sub>3</sub>Cl + OH (+ 4 water) reaction profile used in the paper.

## Contents

- `gaussian_reactant_opt/`
  - `1.gjf`, `1.log`: Gaussian input and output for the optimized **reactant** structure in the chosen model environment.

- `gaussian_product_opt/`
  - `1.gjf`, `1.log`: Gaussian input and output for the optimized **product** structure.

- `gaussian_TS_opt/`
  - `1.gjf`, `1.log`: Gaussian input and output for the optimized **transition state** (TS).

- `reactant.xyz`, `product.xyz`, `TS.xyz`  
  Cartesian geometries of the reactant, product, and TS, extracted from the corresponding Gaussian optimizations (for easy visualization or as starting points for other codes).

These stationary points are consistent with the IRC and PES data in `qm/cluster_irc/` and form the basis for the EVB state definitions and barrier heights discussed in the main text.
