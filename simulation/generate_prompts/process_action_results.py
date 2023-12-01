from utils.initialize_model import generate

def action_results(action_prompts, model, tokenizer):
    action_results = {}
    for name, prompt in action_prompts.items():
        action_results[name] = generate(prompt, model, tokenizer)
    return action_results