#!/bin/bash

#SBATCH --partition compute
#SBATCH --job-name="${name}"
#SBATCH --export=ALL
#SBATCH --cpus-per-task=1
#SBATCH --nodes=${nodenumber}
#SBATCH --ntasks-per-node=${ntasks}
##SBATCH --nodelist=tellurium[1-8]
#SBATCH --constraint tellurium

date
hostname
echo SLURM_SUBMIT_DIR: $$SLURM_SUBMIT_DIR
echo TMPDIR: $$TMPDIR/osiris/${name}
source $$OSIRIS/source_osiris.sh
mkdir -p $$TMPDIR/osiris/${name}
cp ${foldername}/simulation.3d $$TMPDIR/osiris/${name}
cd $$TMPDIR/osiris/${name}
export OMP_NUM_THREADS=$$SLURM_CPUS_PER_TASK
${jobnames}
err=?
cp -r * $$SLURM_SUBMIT_DIR/${foldername}
rm -r $$TMPDIR/osiris
echo sacct -j $$SLURM_JOB_ID--format=Elapsed 
date
