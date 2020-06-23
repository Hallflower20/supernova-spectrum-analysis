#!/bin/bash
#SBATCH -A p30137               # Allocation
#SBATCH -p normal                # Queue
#SBATCH -t 8:00:00              # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=16G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=4     # Number of Cores (Processors)
#SBATCH --mail-user=xander.hall@northwestern.edu  # Designate email address for job communications
#SBATCH --mail-type=END    # Events options are job BEGIN, END, NONE, FAIL, REQUEUE
#SBATCH --output="jobout0"
#SBATCH --error="joberr0"
#SBATCH --job-name="Calculate Possible FU Oris"       # Name of job

echo deploying job ...

# add a project directory to your PATH (if needed)
export PATH=$PATH:/projects/p30137/xhall/

# load modules you need to use
module purge all
module load anaconda3
source activate snid
python /home/xjh0560/GitHub/supernova-spectrum-analysis/SNID_Multi_Analysis.py
echo Done