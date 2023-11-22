# import networkx as nx
# import torch
# import accelerate
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from utils.initialize_model import initialize_model, generate



model, tokenizer = initialize_model()

test_prompt = "In order to use llama2, i need to use"

# out = generate(prompt=test_prompt, model=model,tokenizer=tokenizer, customized=True)
# print(out)