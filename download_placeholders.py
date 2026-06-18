import json
import os
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# Load menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

assets_dir = os.path.join(os.getcwd(), 'assets', 'images')
os.makedirs(assets_dir, exist_ok=True)

missing = []

for cat in data:
    for item in cat['items']:
        name = item['name']
        filename = os.path.basename(item['image'])
        full_path = os.path.join(assets_dir, filename)
        
        # If missing or size is very small (like an error message)
        if not os.path.exists(full_path) or os.path.getsize(full_path) < 1000:
            missing.append({
                "name": name,
                "full_path": full_path
            })

def download_placeholder(item):
    name = item['name']
    path = item['full_path']
    # Create a nice dark/gold placeholder
    # Replace spaces with + for the URL text
    text = urllib.parse.quote(name)
    url = f"https://placehold.co/600x400/1a1a1a/d4af37/png?text={text}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        return f"Downloaded placeholder for: {name}"
    except Exception as e:
        return f"Failed placeholder for {name}: {e}"

print(f"Downloading {len(missing)} themed placeholders...")

with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(download_placeholder, missing)

for r in results:
    pass

print("Finished downloading placeholders.")
