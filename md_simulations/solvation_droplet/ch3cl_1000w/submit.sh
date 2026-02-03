#!/bin/bash

cycle=1

for i in {0..19}
do
    sed -i "s/\(cycle=\)[0-9]\+/\1${cycle}/" ../submitscript/US${i}.sh
    sbatch ../submitscript/US${i}.sh
done
cd ../
