import json
import re
import os
import time
import urllib.request
import urllib.parse
import subprocess

target_dir = r"assets\images"
os.makedirs(target_dir, exist_ok=True)

print("Reading menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
failed = 0

def save_menu_and_push(batch_number):
    global content
    global menu_data
    
    # Save menu.js
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Update cache buster in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # find current v=X and increment it
    v_match = re.search(r'menu\.js\?v=(\d+)', html)
    if v_match:
        current_v = int(v_match.group(1))
        html = re.sub(r'menu\.js\?v=\d+', f'menu.js?v={current_v + 1}', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
            
    # Push to git
    print(f"Pushing Batch {batch_number} to GitHub...")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", f"Add AI photos batch {batch_number}"], check=False)
    subprocess.run(["git", "push"], check=False)
    print("Push complete.")


batch_size = 10
current_batch_count = 0
batch_number = 1

for category in menu_data:
    for item in category.get('items', []):
        if item['image'] == "logo.png":
            item_name = item['name']
            print(f"Generating AI image for: {item_name}...")
            try:
                # Build Prompt
                prompt = f"{item_name} authentic delicious South Indian food, premium high-end luxury restaurant photography, dark moody background, golden lighting, highly detailed, 4k resolution, professional food photography"
                encoded_prompt = urllib.parse.quote(prompt)
                
                # We use a seed so the style is consistent-ish, or random seed.
                # Adding nologo=true to remove watermarks
                api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"
                
                req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = response.read()
                
                clean_name = item_name.lower().replace(' ', '_').replace("'", "").replace("/", "_")
                file_name = f"{clean_name}_ai.jpg"
                target_path = os.path.join(target_dir, file_name)
                
                with open(target_path, 'wb') as out_file:
                    out_file.write(data)
                
                # Update item
                item['image'] = f"assets/images/{file_name}"
                updated += 1
                current_batch_count += 1
                print(f"Successfully generated and mapped: {item_name}")
                
                if current_batch_count >= batch_size:
                    save_menu_and_push(batch_number)
                    batch_number += 1
                    current_batch_count = 0
                    
            except Exception as e:
                print(f"Failed to generate {item_name}: {e}")
                failed += 1
            
            time.sleep(1) # Small delay to respect free API

print(f"\nFINISHED! Successfully generated: {updated} items. Failed: {failed} items.")

if current_batch_count > 0:
    save_menu_and_push(batch_number)

