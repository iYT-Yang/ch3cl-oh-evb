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

cycle=1
window=17

### only for cycle=1
if [[ ${cycle} -eq 1 ]]; then
    cp ../runfolder/nvt-${window}.rst ./rst/${window}.rst
else
    cp ../runfolder-$((cycle - 1))/nvt-${window}.rst ./rst/${window}.rst
fi

python ../nvt2.py ${window} > log/${window}.log

