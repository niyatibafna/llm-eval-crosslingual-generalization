#!/usr/bin/env bash

#$ -N test_trans
#$ -wd /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation
#$ -m e
# #$ -t 4
#$ -j y -o /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/experiments/qsub_logs/test_noise.log

# Fill out RAM/memory (same thing) request,
# the number of GPUs you want,
# and the hostnames of the machines for special GPU models.
#$ -l ram_free=30G,mem_free=30G,gpu=1,hostname=!c08*&!c07*&!c04*&!c25*&c*

# Submit to GPU queue
#$ -q g.q

source ~/.bashrc
which python

conda deactivate
conda activate test2
which python

# Assign a free-GPU to your program (make sure -n matches the requested number of GPUs above)
source /home/gqin2/scripts/acquire-gpu -n 1

echo "HOSTNAME: $(hostname)"
echo
echo CUDA in ENV:
env | grep CUDA
echo
echo SGE in ENV:
env | grep SGE

set -x # print out every command that's run with a +
nvidia-smi


cd "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/"
## SCRIPT TO RUN
# bash scripts/run.sh vi openai-community/gpt2 

lang="de"
model_path="openai-community/gpt2" 
# model_path="google/mt5-base"
# tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
tasks=wmt16-de-en
device=cuda
theta=0.01

all_noise_params="character_level:lang=${lang},swap_theta=${theta}"
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
