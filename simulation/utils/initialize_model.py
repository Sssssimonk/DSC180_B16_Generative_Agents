# import networkx as nx
# import torch
# import accelerate
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import json


def initialize_model():
    # open configuration file to read model configs
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'model_config.json')
    with open(file_path, "r") as jsonfile:
        data = json.load(jsonfile)
        print("Read successful")

    access_token = data["model_config"]["access_token"]
    model_name = data["model_config"]["model_name"]

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=access_token)
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                load_in_4bit=True, 
                                                token=access_token,
                                                device_map="auto") 
    

    return(model, tokenizer)

def generate(prompt, model, tokenizer, customized=True):
    if customized: # generate output using transformer generate function
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        generated_ids = model.generate(**inputs,
                                    do_sample = True,
                                    max_length = (len(prompt) + 128))
        out = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0] # output is a list of str
        # delete unnecessary instructions
        if '### Response:' in out:
            out = out.split('### Response:')[1]
        if '### Instruction:' in out:
            out = out.split('### Instruction:')[0]
        return out
    
    else:  # generate output using transfomer pipeline
        pipe = pipeline(task="text-generation",
                        model=model, 
                        tokenizer=tokenizer,
                        )
        
        output = pipe(prompt, do_sample=True, min_length=10, max_length=len(prompt)+128)
        out = output[0]['generated_text']
        if '### Response:' in out:
            out = out.split('### Response:')[1]
        if '### Instruction:' in out:
            out = out.split('### Instruction:')[0]
        return out

