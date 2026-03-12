# Human-directing-robot dialogue

This repository contains a dataset of human-robot interactions recorded using interactive [AI2THOR virtual environment](https://ai2thor.allenai.org/) 
with the home scenes from [TEACH dataset](https://arxiv.org/pdf/2110.00534). The users interacted with the virtual robot using text chat and the interpretation of the user directives was manually corrected. ~20% of user utterances in the dataset are isued while the robot is perofming a task, presenting a challenge of interpreting interruptions and corrections.  LLM translates the user's natural language utterance with its context into a corresponding sequence of API calls. The paper presents evaluation results using Qwen3-4B and Gpt-5-mini. The scripts for replicating the experiments or running  with the other models are included.

If you are interested in collecting data using this interface, we would be happy to share the source code of the interactive interface and collaborate future research. Please [get in touch](svetlana.stoyanchev@toshiba.eu).

## [Context-Aware Language Understanding in Human-Robot Dialogue with LLMs](https://aclanthology.org/2026.iwsds-1.27/)


```bibtex
@inproceedings{stoyanchev-etal-2026-context,
    title = "Context-Aware Language Understanding in Human-Robot Dialogue with {LLM}s",
    author = "Stoyanchev, Svetlana  and
      Farag, Youmna  and
      Keizer, Simon  and
      Li, Mohan  and
      Doddipatla, Rama Sanand",
    booktitle = "Proceedings of the 16th International Workshop on Spoken Dialogue System Technology",
    month = Feb,
    year = "2026",
    address = "Trento, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.iwsds-1.27/",
    pages = "262--274",
}
```


## Running the Experiment


### Using Qwen 
Set up conda env: python 310, vllm  

```
cd scripts; ./startQwen3-4B.sh 
```
(may need to change the port number)

### Using OpenAI
You will need the API_KEY:
```
export AZURE_OPENAI_API_KEY="<YOUR API KEY>"
```

Set up conda env: python 310, openai, requests

To verify that you can generate output for one data point (edit the ./scripts/run_one_datapoint.sh to set up the ENDPOINT and MODEL env vars )
```
./scripts/run_one_datapoint.sh 6 
```
If this generates output successfully, run the generation on all data:

```
./scripts/run_all_datapoints.sh
```
### Scoring generated output 
See [scripts/compute_scores.ipynb](#./scripts/compute_scores.ipyn)

## Content
### input/

set_july2025.csv Dataset in the spreadsheet with columns:
    
- *game* - identifier of a game from TEACH	
- *uid*	- annotator ID (A1, A1.1, A2, A3, A4)
- *id*	- utterance ID which is used a a directory name under annotated_data/
- *game_start* - time of the start of the game	
- *utt_time* - time of the utterance
- *context* - json with the state describing known objects and their known relations, e.g. {'oids': ['pot_0', 'sinkbasin_0', ...], 'summary': ['pot_0 is Dirty,   is on top of a countertop_0, etc.}    
- *utt*	- user utterance
- *old_plan* - list of commands and their status, e.g. [{'command': 'Place(potato_0, countertop_0)', 'status': 'SubgoalStatus.NOT_ATTEMPTED'}, ...]
- *new_plan* - plan generated automatically by GPT-mini(for A1) or GPT4.1 (for all other user IDs) 
- *new_plan_correction* - correction entered by the expert annotator during interaction with the system (if empty, no correction was entered)	
- *anno* - 'user' when correction was entered by the expert user pr 'gpt' otherwise 
- *int_type* - contex categiry, automnatically detected based on when the utterance was issued. The context categories are: 
        NO_CONTEXT,IN_CONTEXT_BEFORE_INITIAL, IN_CONTEXT_AFTER_SUCCESS, IN_CONTEXT_AFTER_FAIL, IN_CONTEXT_AFTER_FINAL_FAILED, IN_CONTEXT_AFTER_FINAL_SUCCESS	
    anno_explain	anno_manual_plan_correction	anno_needs_dlg	anno_couldbesolved_by_reasoning	notes
    anno_manual_plan_correction - correction by the author or 'OK'


#### data_w_shortcut/

Contains a folder <ID> for each datapoint (*id* column in set_july2025.csv) with 

Pre-generated few-shot example files:
- *SAME_INTERRUPT_<N>.txt*  N examples randomly selected from matching context 
- *SAME_INTERRUPT_<N>_CHEAT.txt*  same N examples + the TEST example

- *SIM_100_1_1_1_<N>.txt* - N randomly selected examples using similarity with the parameters context similarity = 100 (ensures that examples are selected from the same context) uniform object, state, dialogue history similarity (1,1,1)

- *system_responseGT.json* - Ground Truth response (annotated by the expert and checked by the author) includes CONTINUE_FAILED and CONTINUE_NA shortcuts. These labels simplify the model's task: instead of predicting the full sequence, the model only needs to predict whether the unfinished plan should continue. In a system, these predictions will be automatically expanded based on the state

- *user_turn.txt* - User utterance and state (the input to the model)


#### data_no_shortcut/

Same as *data_w_shortcut* except system_responseGT.json contains full plan without CONTINUE_FAILED and CONTINUE_NA shortcuts

#### instruction/
Instructions for the LLM prompt. 
- instruction_INITIAL.txt
- instruction_OBJ.txt

Instruction type (INITIAL/OBJ) are parameters to the script. Create a new instruction instruction_NEW.txt for another experiment.

### output/

- data_w_shortcut/   - empty folders where output will be generated when you run th experiment(same name as input/)
- data_no_shortcut/ - empty folders where output will be generated when you run th experiment (same name as input/)
- IWSDS2026_data_w_shortcut/   - output generated by the models when running experiemtns presented in IWSDS2026 paper.


### scripts/
- *exp_nlu.py*  - main class for runing experiments
- *remote_llm_wrapper.py*   - library for calling LLM remotely   
- *run_functions.sh* - functions loaded by other scripts 
- *run_all_datapoints.sh*  - run this script to run the experiment on all data points
- *run_one_datapoint.sh* - run this script to generate output for one data point 
- *startQwen3-4B.sh* - script to serve the model using vllm

###   
