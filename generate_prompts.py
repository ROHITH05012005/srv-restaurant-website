import json
import os

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)
assets_dir = os.path.join('assets', 'images')
missing = []

for cat in data:
    for item in cat['items']:
        filename = os.path.basename(item['image'])
        full_path = os.path.join(assets_dir, filename)
        if not os.path.exists(full_path):
            clean_name = item['name'].split('(')[0].strip()
            prompt = f"Delicious authentic high quality Indian food photography of {clean_name}, dark background, 4k, professional lighting, photorealistic, cinematic"
            missing.append({
                "item_name": item['name'],
                "filename": filename,
                "prompt": prompt
            })

with open('n8n_prompts.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, indent=2)

print(f"Generated {len(missing)} prompts in n8n_prompts.json")
