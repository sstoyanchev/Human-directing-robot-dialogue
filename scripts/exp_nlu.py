#######################################################################
# Human-directing-robot-dialogue project (HDRD)
# Copyright (c) 2026 Toshiba Europe
# Licensed for research and academic use only.
# Author: Svetlana Stoyanchev 
# Run the experiment using pre-generated inputs
#######################################################################

from remote_llm_wrapper import RemoteLLMWrapper
import json
#import numpy as np
import argparse
import traceback
import os



def run(llm_api, model_name, temp, topp, prompt_instruction_str, prompt_examples_str, user_turn, logfile):
        ''' 
        create prompt and run llm
        '''
        print (f"logfile={logfile}")
        llm = RemoteLLMWrapper(llm_api, model_name, temperature=temp, top_p=topp, logfile=logfile)

        prompt = [{'role':'system', 'content': prompt_instruction_str + prompt_examples_str }]
        # TODO: append dialogue history
        prompt.append({"role": "user", "content":user_turn}) 

    
        try:
            raw_response =  llm.get_result(prompt)
        except Exception as ex:
            raw_response = "ERROR in LLM planning: "+ str(ex) + traceback.format_exc()
        
        return raw_response




if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    exp_dir = './'  # change if needed
    parser.add_argument("--llm_api", type=str, default="openai", help="openai or url for http endpoint")
    parser.add_argument("--model", type=str, default="gpt-5-mini", help="model name for openai or for the endpoint")
    parser.add_argument("--temp", type=float, default=0)
    parser.add_argument("--topp", type=float, default=0.95)
    parser.add_argument("--dlg_hist", type=int, default=0)
    parser.add_argument("--utt_id", type=str, default="sveta_203")
    parser.add_argument("--input_dir", type=str, default="annotated_data")# we will need to run one input multiple times
    parser.add_argument("--instruct", type=str, default="INITIAL")
    parser.add_argument("--condition", type=str, default="RANDOM_ALL_EXCLUDE_50")
    parser.add_argument("-v", "--verbous", action='store_true' )

    args = parser.parse_args()


    # all output is stored in a subdirectory wiht the same name as input
    in_dir = exp_dir + 'input/' + args.input_dir
    out_dir =  exp_dir + 'output/' + args.input_dir
    log_dir =  exp_dir + 'log/' + args.input_dir

    if not os.path.exists(out_dir):
            os.mkdir(out_dir)

    if not os.path.exists(log_dir):
            os.mkdir(log_dir)

    dlg_hist_suffix = ""

    if args.dlg_hist>0:
         dlg_hist_suffix = f'_hist{args.dlg_hist}'

    examples_fname = f'{in_dir}/{args.utt_id}/{args.condition}{dlg_hist_suffix}.txt' 

    user_turn_fname = f'{in_dir}/{args.utt_id}/user_turn{dlg_hist_suffix}.txt'


    if not os.path.exists(f'{out_dir}/{args.utt_id}'):
        print(f'creating {out_dir}/{args.utt_id}')
        os.mkdir(f'{out_dir}/{args.utt_id}')

    if not os.path.exists(f'{log_dir}/{args.utt_id}'):
        print(f'creating {log_dir}/{args.utt_id}')
        os.mkdir(f'{log_dir}/{args.utt_id}')        

    #get model id for the directory
    model_short = args.model
         
    if '/' in args.model:
         model_short = args.model[args.model.find('/'):]

    if not args.model.startswith('gpt-5'): # do not use topp and temp
         model_short += f'_temp{args.temp}_tp{args.topp}'


    if not os.path.exists(f'{out_dir}/{args.utt_id}/{model_short}'):
        print(f'creating {out_dir}/{args.utt_id}/{model_short}')
        os.mkdir(f'{out_dir}/{args.utt_id}/{model_short}')     

    if not os.path.exists(f'{log_dir}/{args.utt_id}/{model_short}'):
        print(f'creating {log_dir}/{args.utt_id}/{model_short}')
        os.mkdir(f'{log_dir}/{args.utt_id}/{model_short}')   

    out_fname = f'{out_dir}/{args.utt_id}/{model_short}/{args.condition}_instruct{args.instruct}{dlg_hist_suffix}.json'  
    log_fname = f'{log_dir}/{args.utt_id}/{model_short}/{args.condition}_instruct{args.instruct}{dlg_hist_suffix}.log'  

    if  os.path.exists(out_fname):
            print ('Output already exists! ' + out_fname)
            exit(1)
            
    prompt_instruction = ""
    instruction_fname = f"{exp_dir}/input/instruction/instruction_{args.instruct}.txt"
    with open(instruction_fname, 'r') as f:
        prompt_instruction = f.read()
        if (args.verbous):
             print(f"Read instruction from {instruction_fname}")

    prompt_examples = ""
    with open(examples_fname, 'r') as f:
         prompt_examples = f.read()

    user_turn = ""
    with open(user_turn_fname, 'r') as f:
         user_turn = f.read()      

    result = run(args.llm_api, args.model, args.temp, args.topp, prompt_instruction, prompt_examples, user_turn, log_fname)
    with open(out_fname, 'w') as f:
        f.write(json.dumps(result))
        if (args.verbous):
            print(f"Wrote to {out_fname}")
        


    
    