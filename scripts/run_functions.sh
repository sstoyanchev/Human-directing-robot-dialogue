
#!/bin/bash

export SRC_DIR=./scripts
export INPUT_DIR=./input/


run_one() {
    # run one input file
    local input_dir="$1"
    local llm_api="$2"
    local model="$3"
    local condition="$4"
    local dlg_hist="$5"    
    local instruct="$6"
    local utt_id="$7"    

    echo CALLING: PYTHONPATH=$SRC_DIR:$PYTHONPATH python $SRC_DIR/exp_nlu.py --input_dir $input_dir --utt_id=$utt_id --condition=$condition --llm_api $llm_api --model=$model --dlg_hist=$dlg_hist --instruct $instruct -v
    PYTHONPATH=$SRC_DIR:$PYTHONPATH python $SRC_DIR/exp_nlu.py --input_dir $input_dir --utt_id=$utt_id --condition=$condition --llm_api $llm_api --model=$model --dlg_hist=$dlg_hist --instruct $instruct -v
    }

run_all() {
    # run all input files in INPUT_DIR
    local input_suffix="$1"
    local llm_api="$2"
    local model="$3"
    local condition="$4"
    local dlg_hist="$5"  
    local instruction="$6"

    echo "Running for all files in ${INPUT_DIR}${input_suffix}/*"

    for file in ${INPUT_DIR}${input_suffix}/*
    do
        if [[ -d $file ]]; then
            # get the file name without path. this is utt id
            utt_id="${file##*/}"
            run_one $input_suffix $llm_api $model $condition $dlg_hist $instruction $utt_id 

        else
            echo "skip $file"
        fi
    done
}


