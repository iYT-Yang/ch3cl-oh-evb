#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=SGPU,GGPU
#SBATCH --gres=gpu:1 --ntasks=1
#SBATCH --time=24:00:00

source ~/.bashrc

conda activate omm8plumed
module load gcc/9.3.0 openmpi/3.1.6gcc9

export OPENMM_CPU_THREADS=1
export OMP_NUM_THREADS=1

cd runfolder
for i in {0..19}
do
    python ../nvt.py ${i} > log/${i}.log
done
cd ../
