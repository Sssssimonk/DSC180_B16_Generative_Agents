import networkx as nx
import json 
import os
import matplotlib.pyplot as plt



def initialize_world():
    world_graph = nx.Graph()
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'world_config.json')
    with open(file_path, "r") as jsonfile:
        data = json.load(jsonfile)
        town_areas = data["town_areas"]
        # town_people = data["town_people"]

    for town_area in town_areas.keys():
        world_graph.add_node(town_area)
    for town_area in town_areas.keys():
        world_graph.add_edge(town_area, "Town Square")

    return world_graph

    # nx.draw(world_graph, with_labels=True)
    # plt.show()

def initialize_agent():
    # initilize memories and plans and locations
    memories = {}
    compressed_memories = {}
    plans = {}
    locations = {}

    # read town_people in the config file
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'world_config.json')
    with open(file_path, "r") as jsonfile:
        data = json.load(jsonfile)
        town_people = data["town_people"]
 
    for name in town_people.keys():
        memories[name] = []
        plans[name] = []
        compressed_memories[name] = []
        locations[name] = "Town Square" 

    # global_time = 8
    # def generate_description_of_area(x):
    #     text = "It is "+str(global_time)+":00. The location is "+x+"."
    #     people = []
    #     for i in locations.keys():
    #         if locations[i] == x:
    #         people.append(i)

    return memories, compressed_memories, plans, locations