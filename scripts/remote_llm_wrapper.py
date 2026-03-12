#######################################################################
# Human-directing-robot-dialogue project (HDRD)
# Copyright (c) 2026 Toshiba Europe
# Licensed for research and academic use only.
# Author: Svetlana Stoyanchev 
# Run the experiment using pre-generated inputs
#######################################################################

#from openai import AzureOpenAI
from openai import OpenAI
import requests
import json

import os

AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")   # returns None if not set


AZURE_OPENAI_ENDPOINT="https://teurcrl.openai.azure.com/"

class RemoteLLMWrapper:
    '''
    the class that wraps around LLM connection
    '''
    def __init__(self, url, model_name = 'gpt5-mini', temperature = None, top_p = None, logfile = None):
        self.url = url
        self.model_name = model_name
        self.logfile = logfile
        self.temperature = temperature
        self.topp = top_p

        if self.url=='openai':
            self.client = OpenAI(
                api_key=AZURE_OPENAI_API_KEY,
                base_url = AZURE_OPENAI_ENDPOINT + 'openai/v1'
                )
        else:
            '''temperature and top_p are expected'''
            self.client = None # we are using http   

    def genUserTurn(self, row, dialog_hist_length=0, include_state = True):

        context = {'discussed_objects': []}
    
        # discussed_objects is either obj summary or oids
        if self.OBJ_SUMMARY in row and ((type(row[self.OBJ_SUMMARY])==str and len(row[self.OBJ_SUMMARY])>3) or \
                                        (type(row[self.OBJ_SUMMARY])==list and len(row[self.OBJ_SUMMARY])>0)): # this would catch empty strings and kwargs[self.OBJ_SUMMARY]!="[]":
            context['discussed_objects'] = self.to_struct(row[self.OBJ_SUMMARY])
        elif self.OIDS in row:
            context['discussed_objects'] = self.to_struct(row[self.OIDS])

        if self.OLD_PLAN in row:
            context[self.OLD_PLAN] = self.to_struct(row[self.OLD_PLAN])

        if self.HOLDING in row: # this is just a string
            context[self.HOLDING] = row[self.HOLDING] 


        dialog_hist_str = ''
        if dialog_hist_length > 0:
            dialog_hist_str = '<PREVIOUS INSTRUCTIONS> ' + self.getDialogHistory( row['utt_id'], row['game_start'], row['utt_time'],dialog_hist_length)       

        include_state_str = ''
        if include_state:
            include_state_str = 'STATE: ' + json.dumps(context)

        assert self.UTT in row 
        return f"{dialog_hist_str} <USER> {row[self.UTT]}; {include_state_str}"


    def get_json_result(self, element):
        '''
        this version decodes from the responces of models running with vllm and 
        accessed with http request
        '''
    # decode utf-8, if string has {}, return content between {...},
        ret_json = {}
        decstr  = element.decode("utf-8")
        # sometimes output has prefix before json, skip it
        if '{' in decstr:
            decstr = decstr[decstr.find('{'):]
        lastchar = decstr.rfind('}')
        if lastchar>0:
            decstr = decstr[:lastchar+1]            
        #out_str = re.sub(pattern, add_quotes, decstr)
        #json_str = json.loads(out_str)
        try:
            ret_json = json.loads(decstr)
        except:
            print('NOT JSON' + decstr)

        if 'choices' in ret_json and len(ret_json['choices'])>0:
            assert 'message' in ret_json['choices'][0]
            assert 'content' in ret_json['choices'][0]['message']
            s = ret_json['choices'][0]['message']['content'].replace ('\\n','')
            return json.loads(s)
            
        return ret_json
    
    def get_json_result_openai(self, element):
        decstr = element
        ret_json = {}
        if '{' in element and '}' in element:
            decstr = element[element.find('{'):(element.find('}')+1)]
            
        try:
            ret_json = json.loads(decstr)
        except:
            print('NOT JSON' + decstr)  

        return ret_json          

    
    def construct_prompt_with_examples(self, usr_utt, sys_instruction, prompt_examples = "",  context={},  old_plan = []):

        # append instruction
        prompt = [{'role':'system', 'content': sys_instruction + prompt_examples }]

        if usr_utt != "": usr_utt += '; '

        # usr_utt is either passed in or comes from context.
        prompt.append({"role": "user", "content": usr_utt + self.em.genUserTurn(context)}) 

        return prompt      

    
    
    def get_result(self, prompt ):
        '''
        call openai or post http request on an endpoint
        '''
        
        if self.url=='openai':

            if self.model_name.startswith('gpt-5'): 
                # these models do not take temperature

                resp = self.client.responses.create(
                    model = self.model_name,
                    input = prompt,
                    #temperature = 0,
                    #seed = 1234,
                    reasoning = {"effort": "medium"},
                    #response_format={"type": "json_object"},
                    text={"verbosity": "low"}                
                )  

            else:  # its not gpt-5 and temperature and topp are specified
                assert self.temperature is not None
                assert self.topp is not None
                resp = self.client.responses.create(
                    model = self.model_name,
                    input = prompt,
                    temperature = self.temperature,
                    top_p= self.top,
                    #seed = 1234,
                    response_format={"type": "json_object"},
                )            

            

            json_resp = resp.output_text 
        else:
            assert self.temperature is not None
            assert self.topp is not None            
            response = requests.post(self.url, json={'model': self.model_name,
                                                     'messages':prompt,
                                                     'temperature':self.temperature,
                                                     'top_p': self.topp,
                                                     'response_format': {"type": "json_object"}}
                                                       )
            json_resp = self.get_json_result(response.content)


        if self.logfile is not None:
            with open(self.logfile, 'a') as f:
                f.write(f'{self.url}: \nPROMPT:\n' + json.dumps(prompt) + '\nOUTPUT:' + json.dumps(json_resp) + '\n')   

        return json_resp