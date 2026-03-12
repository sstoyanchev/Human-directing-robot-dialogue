#!/bin/bash
source ./scripts/run_functions.sh
######################################
# Generate for one data point for testing. 
# to run using openai:
#export AZURE_OPENAI_API_KEY="<YOUR API KEY>"
#export ENDPOINT="openai"
# to run using your own endpoint (replace localhost and 8891 with the url where the model is served):
#export ENDPOINT="http://localhost:8891/v1/chat/completions
######################################


UTT_ID=$1  # first parameter is the id of the data point to run, e.g., 6

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

echo "Running the prediction for ${INPUT_SUFFIX}/${UTT_ID}"


# To call for one data point id=6:
run_one $INPUT_SUFFIX $ENDPOINT $MODEL $CONDITION $DIALOG_HISTORY $INSTRUCTION $UTT_ID

echo "Check output in output/$INPUT_SUFFIX/$UTT_ID"