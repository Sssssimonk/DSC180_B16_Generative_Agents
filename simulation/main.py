# import networkx as nx
# import torch
# import accelerate
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from utils.initialize_model import initialize_model, generate
from sentence_transformers import SentenceTransformer, util
from environment.initialize_world import initialize_world, initialize_agent
from generate_prompts.generate_plans import generate_plans
from generate_prompts.generate_actions import generate_action_results
import warnings




def initial_environment():
    global_time = 8
    town_areas, world_graph = initialize_world()
    description, memories, compressed_memories, plans, locations = initialize_agent()
    place_we_have = ", ".join(town_areas.keys())
    limit = 5
    return global_time, description, memories, plans, locations, limit, place_we_have, town_areas

def chat_bot(prompt, model, tokenizer):
    prompt_meta = '''### Instruction:
{}

### Response:'''
#     prompt = prompt_template.format(name, info, ', '.join(list(description.keys())))
    talking = generate(prompt_meta.format(prompt), model, tokenizer)
    return talking.strip()

def run_method(global_time, description, locations, plans, place_we_have):
    time_now = 12
    if global_time < 12:
        time_now = "{}:00 AM".format(global_time)
    elif global_time == 12:
        time_now = "12:00 PM"
    else:
        time_now = "{}:00 PM".format(global_time - time_now)
        
    print("It is {} now".format(time_now))
    town_place_people_have = {}
    for key, values in locations.items():
        if values in town_place_people_have.keys():
            town_place_people_have[values].append(key)
        else:
            town_place_people_have[values] = []
            town_place_people_have[values].append(key)
       
    print(" ".join(["{} in {}.".format(", ".join(v), k) for k, v in town_place_people_have.items()]))
    for k, v in town_place_people_have.items():
        if len(v) > 1:
            person_list = ", ".join(v)
            start_prompt = "{} in {}.".format(person_list, k)
            start_prompt += " ".join([description[single_people] for single_people in v])
            start_prompt += " What would they say?"
            talking_part = chat_bot(start_prompt, model, tokenizer)
            print("{} are talking: ".format(person_list))
            print("*******************************")
            print(talking_part)
            print("*******************************")
            for people in v:
                memories[people].append("{} are talking at {}. ".format(person_list, time_now))
    
    
    for name in description.keys():
            
        # Initilized some plans and actions
        if len(plans[name]) == 0:
            # fill in action prompt and daily plan prompts with details
            action_string = initial_action_prompt.format(name, locations[name], description[name], time_now)
            plan_string = initial_plan_prompt.format(description[name])
            # generate initial daily plan
            plans[name] = generate(prompt_meta.format(plan_string), model, tokenizer).strip()
        else:
            # fill in action prompt
            action_string = normal_action_prompt.format(name, locations[name], town_areas[locations[name]], name, plans[name], time_now)
        # gerneate action for next iteration
        action = generate(prompt_meta.format(action_string), model, tokenizer).strip()
        # fill in place prompt
        place_string  =  normal_place_prompt.format(name, locations[name], plans[name], time_now, action, place_we_have)

        # generate place to go next
        place = generate(prompt_meta.format(place_string), model, tokenizer).strip()
   
        for i in town_areas.keys():
            if i.upper() in place.upper():
                place = i
            if "Office".upper() in place.upper():
                if "Police".upper() not in place.upper():
                    place = "City Hall"
        locations[name] = place
        summary_string = action[:-1] + " " + time_now + " and go " + locations[name] + " next hour."
        print("{}: {}".format(name, summary_string))
        if len(memories[name]) == limit:
            memories[name] = memories[name][1:]
        memories[name].append(summary_string)
            
        
    print("==============================")
    print()
    
        
def calculate_sentence_similarity(memories, plans):
    for name in plans.keys():
        memory_summarization = generate(prompt_meta.format(summarize_prompt.format(name, memories[name])), model, tokenizer)
        initial_plan = plans[name]
        embedding_1= sentence_model.encode(memory_summarization, convert_to_tensor=True)
        embedding_2 = sentence_model.encode(initial_plan, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(embedding_1, embedding_2).tolist()[0][0]
        print("The memory consistency score between intial plan and memory summary for {} is {}".format(name, similarity_score))


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    # define some prompt_templates
    prompt_meta = '''### Instruction:{}  ### Response:'''
    initial_action_prompt = "{} and in {}, {}. Right now is {}. What are you doing Now? Be brief, and use at most 3 words and answer from your perspective."
    initial_plan_prompt = "{}. What will you do toay? Be brief, and use at most 5 words and answer from your perspective."
    normal_action_prompt = "{} in {} that is {}, {}'s plan is {} today. Right now is {}. What are you doing Now? Be brief, and use at most 3 words and answer from your perspective."
    normal_place_prompt = "You are {}, and in {}, your goal is {}.Right now is {} and {}. Where will you go next? Choose a place from {}.Be brief, and use at most 3 words and answer from your perspective."
    summarize_prompt = "Summarize {}'s' daily plan based on the memory below {}, at most 20 words"
    
    
    model, tokenizer = initialize_model()
    sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    run_steps = 10

    for i in range(run_steps):
        if i == 0:
            global_time, description, memories, plans, locations, limit, place_we_have, town_areas = initial_environment()
        run_method(global_time, description, locations, plans, place_we_have)
        if global_time == 23:
            global_time = 0
        else:
            global_time += 1
            
    calculate_sentence_similarity(memories, plans)
            
    print("=====END OF SIMULATION=====")

    
    