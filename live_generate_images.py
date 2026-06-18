import json
import re
import os
import time
import urllib.request
import urllib.parse
import subprocess

def get_menu_data(content):
    match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
    if not match: return None, None
    return json.loads(match.group(1)), match

def update_cache_buster():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    match = re.search(r'src="menu\.js\?v=(\d+)"', html)
    if match:
        v = int(match.group(1)) + 1
        html = re.sub(r'src="menu\.js\?v=\d+"', f'src="menu.js?v={v}"', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)

def run_git(msg):
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)

def slugify(text):
    text = text.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

menu_data, match = get_menu_data(content)

count = 0
for category in menu_data:
    for item in category.get('items', []):
        if item.get('image') == 'logo.png':
            name = item['name']
            print(f"Processing: {name}", flush=True)
            
            slug = slugify(name)
            filename = f"{slug}_premium.png"
            filepath = os.path.join('assets', 'images', filename)
            
            prompt = f"A beautiful, appetizing, highly realistic professional food photography shot of {name}, traditional Indian vegetarian cuisine. Placed on a dark rustic wooden table, with dramatic warm moody lighting, steam rising. Elegant, premium quality, 4k, matching a dark themed high-end restaurant UI with golden accents."
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=400&nologo=true"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download image for {name}: {e}", flush=True)
                continue
            
            item['image'] = f"assets/images/{filename}"
            
            new_json_str = json.dumps(menu_data, indent=4)
            new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
            
            with open('menu.js', 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            content = new_content
            
            update_cache_buster()
            try:
                run_git(f"Add premium image for {name}")
                print(f"Successfully pushed image for {name}", flush=True)
            except Exception as e:
                print(f"Failed to push {name}: {e}", flush=True)
            
            count += 1
            time.sleep(2)

print(f"Finished processing {count} items.", flush=True)
