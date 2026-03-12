#!/bin/bash

source ./scripts/run_functions.sh

#running with Qwen on local endpoint (replace localhost and 8891 with the url where the model is served):
MODEL="Qwen/Qwen3-4B-Instruct-2507"
#ENDPOINT="http://localhost:8891/v1/chat/completions"

#UNCOMMENT if running with openai using key
#MODEL="gpt-5-mini"
#ENDPOINT="openai"
#export AZURE_OPENAI_API_KEY=""

echo "Using endpoint: $ENDPOINT, model: $MODEL"

INPUT_SUFFIX='data_w_shortcut'
CONDITION='SIM_100_1_1_1_10'
DIALOG_HISTORY=0
INSTRUCTION='OBJS'

echo "Running the prediction for all datapoints in ${INPUT_SUFFIX}"

run_all $INPUT_SUFFIX $ENDPOINT $MODEL $CONDITION $DIALOG_HISTORY $INSTRUCTION
