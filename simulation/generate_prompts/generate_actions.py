import json
import os

def generate_action_prompts(town_areas, town_people, locations, global_time, plans, memories):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../prompts_template/action.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        prompt_template = data['prompt_template']
    action_prompts = {}
    for location, description in town_areas.items():
        people_in_location = [name for name, loc in locations.items() if loc == location]

        for name in people_in_location:
            person_description = town_people[name]["description"]
            person_plan = plans[name]
            people_descriptions = [f"{person}: {town_people[person]['description']}" for person in people_in_location]
            people_descriptions_str = '. '.join(people_descriptions)
            memory_text = '. '.join(memories[name][-10:])

            prompt = prompt_template.format(name, person_description, person_plan, location, 
            description, str(global_time), ', '.join(people_in_location), people_descriptions_str)

            action_prompts[name] = prompt
    return action_prompts