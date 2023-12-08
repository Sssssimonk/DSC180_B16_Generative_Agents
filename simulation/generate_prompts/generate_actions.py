import json
import os
from utils.initialize_model import generate

# Generate actions and store memories
def generate_action_results(town_areas, description, locations, plans, memories, model, tokenizer):
    prompt_meta = '''### Instruction:
{}

### Response:'''
    action_results = {}
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../prompts_template/action.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        prompt_template = data['prompt_template']
    action_prompts = {}
    for location, loc_description in town_areas.items():
        people_in_location = [name for name, loc in locations.items() if loc == location]
        for name in people_in_location:
            person_description = description[name]
            person_plan = plans[name]
            people_descriptions = [f"{person}: {description[person]}" for person in people_in_location]
            people_descriptions_str = '. '.join(people_descriptions)
#             memory_text = '. '.join(memories[name][-10:])

            prompt = prompt_template.format(name, person_description, person_plan, location, 
            description, ', '.join(people_in_location), people_descriptions_str)

            action_prompts[name] = prompt
    for name, prompt in action_prompts.items():
        action_results[name] = generate(prompt_meta.format(prompt), model, tokenizer)
        
    for location in town_areas.keys():
        people_in_location = [name for name, loc in locations.items() if loc == location]
        for name in people_in_location:
            for name_two in people_in_location:
                memories[name].append('[Person: {}. Memory: {}]\n'.format(name_two, action_results[name_two]))
    return action_results