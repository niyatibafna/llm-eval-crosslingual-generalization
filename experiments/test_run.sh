
#!/usr/bin/env bash

#$ -N test_run
#$ -wd /export/b08/nbafna1/projects/llm-xlingual-robustness/mlmm-evaluation
#$ -m e
# #$ -t 4
#$ -j y -o /export/b08/nbafna1/projects/llm-xlingual-robustness/experiments/qsub_logs/test_run.log

# Fill out RAM/memory (same thing) request,
# the number of GPUs you want,
# and the hostnames of the machines for special GPU models.
#$ -l ram_free=30G,mem_free=30G,gpu=1,hostname=b19
###!c08*&!c07*&!c04*&!c25*&c*

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


WD="/export/b08/nbafna1/projects/llm-xlingual-robustness/mlmm-evaluation"
cd $WD

# bash scripts/run.sh vi uonlp/okapi-vi-bloom

# bash scripts/run.sh vi mistralai/Mistral-7B-Instruct-v0.2

bash scripts/run.sh vi meta-llama/Llama-2-7b-hf