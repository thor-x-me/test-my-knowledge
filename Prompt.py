def get_prompt(prompt_name):
    with open(f'prompt_library/{prompt_name}') as f:
        prompt = f.read()
    return prompt
