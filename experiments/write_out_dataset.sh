#!/bin/bash

#SBATCH --job-name=write_out_dataset    # create a short name for your job
#SBATCH --nodes=4                # node count
#SBATCH --ntasks=7               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --partition=cpu          # Name of the partition
# #SBATCH --nodelist=octopod       # Node is only available in gpu partition
# #SBATCH --gpus=2               # Total number of gpus
#SBATCH --mem=50G                # Total memory allocated
#SBATCH --hint=multithread       # we get logical cores (threads) not physical (cores)
#SBATCH --time=00:40:00          # total run time limit (HH:MM:SS)
#SBATCH --array=0-6
#SBATCH --output=logs/write_%a.out   # output file name
#SBATCH --error=logs/write_%a.out    # error file name


echo "### Running $SLURM_JOB_NAME ###"

echo "HOSTNAME: $(hostname)"
echo
echo CUDA in ENV:
env | grep CUDA
echo

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

set -x # print out every command that's run with a +
cd "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/"
## SCRIPT TO RUN
# bash scripts/run.sh vi openai-community/gpt2 

num_langs=7
num_tasks=1
langs=("id" "hi" "es" "ar" "ru" "de" "en") # #langs = 7
# langs=("hi" "ar") # #langs = 2
lang=${langs[$SLURM_ARRAY_TASK_ID / $num_tasks]}
# tasks=(xwinograd_${lang} xstory_cloze_${lang} xcopa_${lang} arc_${lang} hellaswag_${lang} mmlu_${lang} \
# truthfulqa_${lang} flores200-${lang}-en) # #tasks = 8
# tasks=(flores200-${lang}-en truthfulqa_${lang} xnli_${lang}) # #tasks = 3
# tasks=(flores200-${lang}-en truthfulqa_${lang} xnli_${lang}) # #tasks = 3
tasks=(truthfulqa_${lang}) # #tasks = 1
# tasks=(xnli_${lang}) #tasks = 1
task=${tasks[$SLURM_ARRAY_TASK_ID % $num_tasks]}

model="hf-seq2seq"
model_path="google-bert/bert-base-uncased" 
model_key="bert-base-uncased"

device=cuda

dataset_save_dir="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/datasets/$lang/"
mkdir -p ${dataset_save_dir}
dataset_outfile="${dataset_save_dir}/${task}.txt"

python main.py \
    --model ${model} \
    --tasks=${task} \
    --model_args pretrained=${model_path} \
    --device=${device} \
    --batch_size 1 \
    --model_alias ${model_path}_${lang} \
    --task_alias ${tasks} \
    --dataset_outfile ${dataset_outfile} 
    # --limit $limit \
    # --all_noise_params_str ${all_noise_params} \
    

# --output_base_path is a dir where the noised data will be stored along with model outputs for each task example,
# the filename is automatically generated as task_lang_write_out.json
# --output_path is the file where the results JSON will be stored for the entire run, with the noise params as a JSON key
