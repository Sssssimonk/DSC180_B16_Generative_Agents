import os
import json
from utils.initialize_model import generate

def generate_plans(town_people, model, tokenizer):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../prompts_template/plan.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        prompt_template = data['prompt_template']
    plans = {}
    for name, info in town_people.items():
        prompt = prompt_template.format(name, info['description'], , ', '.join(list(town_people.keys())))
        plans[name] = generate(prompt, model, tokenizer)
        print(name, plans[name])
    return plans
