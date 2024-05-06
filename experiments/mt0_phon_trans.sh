#!/bin/bash
#$ -N phon_trans
#$ -wd /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation
#$ -m e
#$ -t 1-15
#$ -j y -o /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/experiments/qsub_logs/phon_mt0_trans_$TASK_ID.log

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

num_langs=3
num_tasks=1
num_params=5
# langs=("en" "id" "hi" "ar" "es" "ru" "de") # #langs = 7
langs=("en" "hi" "id") # #langs = 3
# langs=("hi") # #langs = 1
tasks_prod_params=$((num_tasks * num_params))
task_id=$((SGE_TASK_ID - 1))
lang=${langs[$((task_id / tasks_prod_params))]}
# tasks=(xwinograd_${lang} xstory_cloze_${lang} xcopa_${lang} arc_${lang} hellaswag_${lang} mmlu_${lang} \
# truthfulqa_${lang} flores200-${lang}-en) # #tasks = 8
# tasks=(xstory_cloze_${lang} arc_${lang} hellaswag_${lang} mmlu_${lang} \
# truthfulqa_${lang} flores200-${lang}-en) # #tasks = 6
# tasks=(truthfulqa_${lang}) # #tasks = 1
tasks=(flores200-${lang}-en) # #tasks = 1
# tasks=(arc_${lang} hellaswag_${lang} mmlu_${lang} \
# truthfulqa_${lang} xwinograd_${lang} xcopa_${lang}) # #tasks = 6
# tasks=(xnli_${lang} xstory_cloze_${lang} xwinograd_${lang} xcopa_${lang}) # #tasks = 4

theta_phons=(0.01 0.05 0.10 0.15 0.3)

x=$((task_id % tasks_prod_params))
task=${tasks[$((x / num_params))]}
theta_phon=${theta_phons[$((x % num_params))]}

echo "lang: $lang"
echo "task: $task"
echo "theta_phon: $theta_phon"


model="hf-seq2seq"
# model="hf-auto"
model_path="bigscience/mt0-xxl-mt" 
model_key="mt0xxlmt~0shot"

# tasks=arc_${lang},hellaswag_${lang},mmlu_${lang}
# tasks=wmt16-de-en
# tasks="xnli_${lang}"
# tasks="xwinograd_${lang},xstory_cloze_${lang},xcopa_${lang},xnli_${lang}"
# tasks="xwinograd_${lang},xstory_cloze_${lang},xcopa_${lang}"
device=cuda
# theta=0
# all_noise_params="character_level-lang=$lang,swap_theta=$theta"
exp_key="phonological-lang=$lang,theta_phon=$theta_phon"
dataset_dir="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/datasets/$lang/"
dataset_file="${dataset_dir}/${task}.txt"
output_dir="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/noiser_artifacts/phonological/$exp_key"
mkdir -p ${output_dir}
all_noise_params_str="phonological-lang=$lang,theta_phon=$theta_phon,text_file=<$dataset_file>,output_dir=<$output_dir>"


limit=300
output_base_path="/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/"
mkdir -p ${output_base_path}
noised_data_outdir="$output_base_path/noised_data/$model_key/$lang/$exp_key~limit-$limit/"
mkdir -p ${noised_data_outdir}
results_outdir="$output_base_path/results/$model_key/$lang/$exp_key~limit-$limit/"
mkdir -p ${results_outdir}


python main.py \
    --model=${model} \
    --tasks=${task} \
    --model_args pretrained=${model_path} \
    --device=${device} \
    --batch_size 2 \
    --write_out \
    --model_alias ${model_path}_${lang} \
    --task_alias ${tasks} \
    --output_base_path ${noised_data_outdir} \
    --output_path ${results_outdir}/$task.json \
    --limit $limit \
    --all_noise_params_str ${all_noise_params_str} \
    

# --output_base_path is a dir where the noised data will be stored along with model outputs for each task example,
# the filename is automatically generated as task_lang_write_out.json
# --output_path is the file where the results JSON will be stored for the entire run, with the noise params as a JSON key
