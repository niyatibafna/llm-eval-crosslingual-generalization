#!/usr/bin/env bash

#$ -N test_openai
#$ -wd /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation
#$ -m e
#$ -t 1
#$ -j y -o /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/experiments/qsub_logs/test_openai.log

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

lang="hi"
# Trying GPT3.5
# model="gpt3"
model="openai"
model_path="gpt-3.5-turbo-0125"
model_key="gpt3.5turbo"
source /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/.env
echo $OPENAI_API_SECRET_KEY
export OPENAI_API_KEY=$OPENAI_API_SECRET_KEY

# task="xstory_cloze_$lang"
task="flores200-${lang}-en"
device=cuda


limit=3
output_base_path="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs_test/"
mkdir -p ${output_base_path}
noised_data_outdir="$output_base_path/noised_data/$model_key/$lang/orig~limit-$limit/"
mkdir -p ${noised_data_outdir}
results_outdir="$output_base_path/results/$model_key/$lang/orig~limit-$limit/"
mkdir -p ${results_outdir}


python main.py \
    --model ${model} \
    --tasks=${task} \
    --model_args engine=${model_path} \
    --device=${device} \
    --write_out \
    --model_alias ${model_path}_${lang} \
    --task_alias ${task} \
    --output_base_path ${noised_data_outdir} \
    --output_path ${results_outdir}/${task}.json \
    --limit $limit \