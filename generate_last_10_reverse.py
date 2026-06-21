import json
import re
import os
import time
import urllib.request
import urllib.parse
import subprocess

target_dir = os.path.join("assets", "images")
os.makedirs(target_dir, exist_ok=True)

print("Reading menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

# Find all items with logo.png
missing_items = []
for category in menu_data:
    for item in category.get('items', []):
        if item['image'] == "logo.png":
            missing_items.append(item)

# Take last 10 and reverse
target_items = list(reversed(missing_items[-10:]))

updated = 0
generated_names = []

for item in target_items:
    item_name = item['name']
    print(f"Generating AI image for: {item_name}...")
    try:
        # Build Prompt
        prompt = f"{item_name} authentic delicious South Indian food, premium high-end luxury restaurant photography, dark moody background, golden lighting, highly detailed, 4k resolution, professional food photography"
        encoded_prompt = urllib.parse.quote(prompt)
        
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"
        
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        
        clean_name = item_name.lower().replace(' ', '_').replace("'", "").replace("/", "_")
        clean_name = re.sub(r'[^a-z0-9_]', '', clean_name)
        file_name = f"{clean_name}_ai.jpg"
        target_path = os.path.join(target_dir, file_name)
        
        with open(target_path, 'wb') as out_file:
            out_file.write(data)
        
        # Update item
        item['image'] = f"assets/images/{file_name}"
        updated += 1
        generated_names.append(item_name)
        print(f"Successfully generated and mapped: {item_name}")
        
    except Exception as e:
        print(f"Failed to generate {item_name}: {e}")
        
    time.sleep(2) # Delay

if updated > 0:
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("menu.js updated successfully.")
    
    # Update cache buster in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    v_match = re.search(r'menu\.js\?v=(\d+)', html)
    if v_match:
        current_v = int(v_match.group(1))
        html = re.sub(r'menu\.js\?v=\d+', f'menu.js?v={current_v + 1}', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"index.html cache buster updated to v={current_v + 1}.")

    # Git push
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Add {updated} images from the end using Pollinations'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("Successfully pushed to GitHub")
else:
    print("No items updated.")
