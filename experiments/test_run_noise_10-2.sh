#!/bin/bash

#SBATCH --job-name=test_noise    # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --partition=gpu          # Name of the partition
#SBATCH --gpus=1                # Total number of gpus
#SBATCH --mem=10G                # Total memory allocated
##SBATCH --nodelist=octopod       # Node is only available in gpu partition
#SBATCH --hint=multithread       # we get logical cores (threads) not physical (cores)
#SBATCH --time=20:00:00          # total run time limit (HH:MM:SS)
#SBATCH --output=logs/test_noise_10-2.out   # output file name
#SBATCH --error=logs/test_noise_10-2.out    # error file name


echo "### Running $SLURM_JOB_NAME ###"

# print out every command that's run with a +

nvidia-smi

module purge
module load conda
conda --version
module load cuda/10.2
# module load cuda/12.1
nvcc --version

# Set your conda environment
source /home/$USER/.bashrc
conda info --envs

echo "HOSTNAME: $(hostname)"
echo
echo CUDA in ENV:
env | grep CUDA
echo
echo $CUDA_VISIBLE_DEVICES

which python
. "/home/nbafna1/miniconda3/etc/profile.d/conda.sh" && conda deactivate && conda activate llmrob2
which python

set -x
cd "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/"
## SCRIPT TO RUN
# bash scripts/run.sh vi openai-community/gpt2 

lang="deu"
model_path="openai-community/gpt2" 
# tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
tasks=wmt16-de-en
device=cuda
theta=0.01

all_noise_params="character_level-lang=deu,swap_theta=0.2"
output_base_path="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs_test/"
mkdir -p ${output_base_path}
noised_data_outdir="$output_base_path/noised_data_test/$lang/$all_noise_params/"
mkdir -p ${noised_data_outdir}
results_outdir="$output_base_path/results_test/$lang/"
mkdir -p ${results_outdir}


python main.py \
    --tasks=${tasks} \
    --model_args pretrained=${model_path} \
    --device=${device} \
    --limit 10 \
    --batch_size 8 \
    --write_out \
    --model_alias ${model_path}_${lang} \
    --task_alias ${tasks} \
    --all_noise_params_str ${all_noise_params} \
    --output_base_path ${noised_data_outdir} \
    --output_path ${results_outdir}/$tasks.json \
    

# --output_base_path is a dir where the noised data will be stored along with model outputs for each task example,
# the filename is automatically generated as task_lang_write_out.json
# --output_path is the file where the results JSON will be stored for the entire run, with the noise params as a JSON key
