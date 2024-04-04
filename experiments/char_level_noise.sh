#!/bin/bash

#SBATCH --job-name=char_noise    # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=10               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --partition=gpu          # Name of the partition
##SBATCH --nodelist=octopod       # Node is only available in gpu partition
#SBATCH --gpus=1                # Total number of gpus
#SBATCH --mem=100G                # Total memory allocated
#SBATCH --hint=multithread       # we get logical cores (threads) not physical (cores)
#SBATCH --time=20:00:00          # total run time limit (HH:MM:SS)
#SBATCH --array=0-9
#SBATCH --output=logs/test_noise_%a.out   # output file name
#SBATCH --error=logs/test_noise_%a.out    # error file name


echo "### Running $SLURM_JOB_NAME ###"

set -x # print out every command that's run with a +

nvidia-smi

module purge
module load conda
conda --version
module load cuda/10.2
nvcc --version

# Set your conda environment
source /home/$USER/.bashrc
conda info --envs

which python
. "/home/nbafna1/miniconda3/etc/profile.d/conda.sh" && conda deactivate && conda activate llmrob2
which python

cd "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/"
## SCRIPT TO RUN
# bash scripts/run.sh vi openai-community/gpt2 

langs=("hi" "de")
theta=("0.0" "0.25" "0.5" "0.75" "1.0")
lang_idx=$((SLURM_ARRAY_TASK_ID / 5))
theta_idx=$((SLURM_ARRAY_TASK_ID % 5))
lang=${langs[$lang_idx]}
theta=${theta[$theta_idx]}
echo "Running for lang: $lang and theta: $theta"

model_path="openai-community/gpt2" 
tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
device=cuda

tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
device=cuda

all_noise_params="character_level:lang=${lang},swap_theta=${theta}"
output_base_path="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/"
mkdir -p ${output_base_path}
noised_data_outdir="$output_base_path/noised_data/$lang/$all_noise_params/"
mkdir -p ${noised_data_outdir}
results_outdir="$output_base_path/results/$lang/"
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
