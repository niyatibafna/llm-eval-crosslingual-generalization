#!/usr/bin/env bash

#$ -N test_llama
#$ -wd /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation
#$ -m e
#$ -t 1
#$ -j y -o /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/experiments/qsub_logs/test_llama.log

# Fill out RAM/memory (same thing) request,
# the number of GPUs you want,
# and the hostnames of the machines for special GPU models.
#$ -l ram_free=30G,mem_free=30G,gpu=1,hostname=!c08*&!c07*&!c04*&!c24*&!c25*&c*

# Submit to GPU queue
#$ -q g.q

source ~/.bashrc
which python

conda deactivate
conda activate llmrob2
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

# Trying GPT3.5
# export OPENAI_API_SECRET_KEY=""
# model="gpt3"
# model_path="gpt-3.5-turbo-0125"
# tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
# device=cuda

# python main.py \
#     --model ${model} \
#     --tasks=${tasks} \
#     --model_args engine=${model_path} \
#     --device=${device} \
#     --limit 1000 \
#     --batch_size 8 \

# Trying to load Llama
model="hf-auto"
model_path="pretrained=meta-llama/Llama-2-7b-hf"
tasks="arc_vi,hellaswag_vi,mmlu_vi"
device=cuda

python main.py \
    --model ${model} \
    --tasks=${tasks} \
    --model_args ${model_path} \
    --device=${device} \
    --limit 1000 \
    --batch_size 4 