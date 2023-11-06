#!/bin/bash

#SBATCH --partition compute
#SBATCH --job-name="${name}"
#SBATCH --export=ALL
#SBATCH --cpus-per-task=1
#SBATCH --nodes=${nodenumber}
#SBATCH --ntasks-per-node=${ntasks}
##SBATCH --nodelist=tellurium[1-8]
#SBATCH --nodelist tellurium[1-8]
#SBATCH --array=0-${filenumber}%10              # submit as array changing env var SLURM_ARRAY_TASK_ID

date
hostname
echo SLURM_SUBMIT_DIR: $$SLURM_SUBMIT_DIR
echo TMPDIR: $$TMPDIR/osiris/${name}
source $$OSIRIS/source_osiris.sh
mkdir -p $$TMPDIR/osiris/${name}
declare -a file_arr=${path_arr}
echo $${file_arr}
cp $${file_arr[$$SLURM_ARRAY_TASK_ID]}/simulation.3d $$TMPDIR/osiris/${name}
cd $$TMPDIR/osiris/${name}
export OMP_NUM_THREADS=$$SLURM_CPUS_PER_TASK
${jobnames}
err=?
#mkdir * /scratch/fermium/lorenz/$${file_arr[$$SLURM_ARRAY_TASK_ID]}
cp -r * $$SLURM_SUBMIT_DIR/$${file_arr[$$SLURM_ARRAY_TASK_ID]}
#rm -r $$TMPDIR/osiris
echo sacct -j $$SLURM_JOB_ID--format=Elapsed 
date
