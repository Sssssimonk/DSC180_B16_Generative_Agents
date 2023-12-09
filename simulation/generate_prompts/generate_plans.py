import os
import json
from utils.initialize_model import generate

def generate_plans(description, model, tokenizer, plans):
    prompt_meta = '''### Instruction:
{}

### Response:'''
    
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../prompts_template/plan.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        prompt_template = data['prompt_template']
    for name, info in description.items():
        prompt = prompt_template.format(name, info, ', '.join(list(description.keys())))
        plans[name] = generate(prompt_meta.format(prompt), model, tokenizer)
    return None