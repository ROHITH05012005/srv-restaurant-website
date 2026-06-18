import json

with open('openrouter_models.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

models = data.get('data', [])
free_image_models = []

for m in models:
    # Check if free
    prompt_price = float(m.get('pricing', {}).get('prompt', -1))
    completion_price = float(m.get('pricing', {}).get('completion', -1))
    is_free = (prompt_price == 0.0 and completion_price == 0.0)
    
    # OpenRouter API doesn't strictly have a boolean for image generation in the model list,
    # but we can look for keywords in the ID or description
    desc = m.get('description', '').lower()
    m_id = m.get('id', '').lower()
    
    if is_free:
        print(f"Free model found: {m_id}")

