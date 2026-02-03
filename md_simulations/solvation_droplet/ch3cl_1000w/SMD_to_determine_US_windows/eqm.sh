#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=GGPU,SGPU
#SBATCH --gres=gpu:1 --ntasks=1
#SBATCH --time=5:00:00

source ~/.bashrc

conda activate omm8plumed

export OPENMM_CPU_THREADS=1
export OMP_NUM_THREADS=1

python eqm.py > eqm.out
