#!/usr/bin/env bash

# This is a *TEMPLATE* for running alignment with fast-align.

#$ -N align
#$ -wd /export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/
#$ -m e
#$ -t 1-20
#$ -j y -o qsub_logs/align_log_$TASK_ID.log

# Fill out RAM/memory (same thing) request,
# the number of GPUs you want,
# and the hostnames of the machines for special GPU models.
#$ -l ram_free=10G,mem_free=30G,hostname=b1[123456789]|c0*|c1[123456789]


cd "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors"
conda activate llmrob2
# "bho": "bho_Deva",
    # "awa": "awa_Deva",
    # "mag": "mag_Deva",
    # "mai": "mai_Deva",
    # "hne": "hne_Deva",
    # "zsm": "zsm_Latn",
    # "oci": "oci_Latn",
    # "glg": "glg_Latn",
    # "dan": "dan_Latn",
    # "nor": "nor_Latn",
    # "isl": "isl_Latn",
    # "swe": "swe_Latn",
    # "acm": "acm_Arab",
    # "acq": "acq_Arab",
    # "aeb": "aeb_Arab",
    # "ajp": "ajp_Arab",
    # "apc": "apc_Arab",
    # "ars": "ars_Arab",
    # "ary": "ary_Arab",
    # "arz": "arz_Arab",

# lang_pairs=("hin_Deva-awa_Deva" "hin_Deva-bho_Deva" "hin_Deva-mag_Deva" "hin_Deva-mai_Deva" "hin_Deva-hne_Deva" \
#     "ind_Latn-zsm_Latn" \
#     "fra_Latn-oci_Latn" \
#     "spa_Latn-glg_Latn" \
#     "deu_Latn-dan_Latn" "deu_Latn-isl_Latn" "deu_Latn-swe_Latn" \
#     "arb_Arab-acm_Arab" "arb_Arab-acq_Arab" "arb_Arab-aeb_Arab" "arb_Arab-ajp_Arab" "arb_Arab-apc_Arab" "arb_Arab-ars_Arab" "arb_Arab-ary_Arab" "arb_Arab-arz_Arab" \
#     )

lang_pairs=("arb_Arab-acm_Arab" "arb_Arab-acq_Arab" "arb_Arab-aeb_Arab" "arb_Arab-ajp_Arab" "arb_Arab-apc_Arab" "arb_Arab-ars_Arab" "arb_Arab-ary_Arab" "arb_Arab-arz_Arab" \
    )


OUTPATH="flores_lexicons/"
mkdir -p $OUTPATH
TEMP_PATH="flores_lexicons/temp"
mkdir -p $TEMP_PATH

lang_pair=${lang_pairs[$SGE_TASK_ID-1]}

source_lang=$(echo $lang_pair | cut -d'-' -f1)
target_lang=$(echo $lang_pair | cut -d'-' -f2)
flores_datapath="/export/b08/nbafna1/data/flores200_dataset/devtest/"
source_file="${flores_datapath}${source_lang}.devtest"
target_file="${flores_datapath}${target_lang}.devtest"
INFILE="${TEMP_PATH}/${source_lang}_${target_lang}_formatted_source_target.txt"

src=$(echo $source_lang | cut -d'_' -f1)
tgt=$(echo $target_lang | cut -d'_' -f1)

ALIGN_OUTPUT_FILE="${TEMP_PATH}/${src}_${tgt}_alignments.txt"
OUTFILE="${OUTPATH}/${src}_${tgt}.json"
FAST_ALIGN_PATH="/export/b08/nbafna1/projects/fast_align/build/./fast_align"
python3 /home/nbafna1/misc/alignment/format_raw.py $source_file $target_file $INFILE
$FAST_ALIGN_PATH -i $INFILE -v -o -d > $ALIGN_OUTPUT_FILE
python3 /home/nbafna1/misc/alignment/read_alignments.py $INFILE $ALIGN_OUTPUT_FILE $OUTFILE




# # Existing input files to format_raw.py with simply raw text, one sentence per line, aligned by line number
# flores_datapath="/export/b08/nbafna1/data/flores200_dataset/devtest/"
# source_file="" 
# target_file=""
# # This file will be created by format_raw.py
# INFILE="*formatted_source_target.txt" # (It's called INFILE because it's the input file to fast-align)

# # This file will be created by fast-align
# ALIGN_OUTPUT_FILE="/export/b08/nbafna1/projects/courses/601.764-multilingual-nlp/hw1/using_awesome-align/aa_alignments.txt"

# # This file will be created by read_alignments.py or whatever thing you want to do with the alignments
# OUTFILE="*json" # Or whatever else

# FAST_ALIGN_PATH="/export/b08/nbafna1/projects/fast_align/build/./fast_align" # Path to fast-align

# python3 /home/nbafna1/misc/alignment/format_raw.py $source_file $target_file $INFILE # This code creates the $INFILE using text.txt and du.txt

# # Run fast-align
# $FAST_ALIGN_PATH -i $INFILE -v -o -d > $ALIGN_OUTPUT_FILE # This code creates the $ALIGN_OUTPUT_FILE using $INFILE
# # For alignment with reverse model:
# # $FA_DIR -i $INFILE -r -v -o -d > $ALIGN_OUTPUT_FILE

# # Run whatever code required for processing the Pharaoh alignments produced by the above
# # e.g.
# python3 do_something_with_alignments.py $INFILE $ALIGN_FILE $OUTFILE # This code uses $INFILE and $ALIGN_FILE to create some kind of output 

# # If we want a bilingual source->target dictionary, use
# python3 /home/nbafna1/misc/alignment/read_alignments.py $INFILE $ALIGN_FILE $OUTFILE