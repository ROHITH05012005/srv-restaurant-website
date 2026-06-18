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

# Gather all missing images
missing_items = []
assets_dir = os.path.join(os.getcwd(), 'assets', 'images')
os.makedirs(assets_dir, exist_ok=True)

for cat in data:
    for item in cat['items']:
        # Extract filename from 'assets/images/filename.jpg'
        img_path = item['image']
        filename = os.path.basename(img_path)
        full_path = os.path.join(assets_dir, filename)
        
        if not os.path.exists(full_path):
            missing_items.append({
                "name": item['name'],
                "filename": filename,
                "full_path": full_path
            })

print(f"Found {len(missing_items)} missing images. Starting download...")

def download_image(item):
    name = item['name']
    # Clean up name for prompt
    clean_name = name.split('(')[0].strip() # Remove '(2 Nos)' etc
    prompt = f"Delicious authentic high quality Indian food photography of {clean_name}, dark background, 4k, professional lighting"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=600&height=400&nologo=true"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(item['full_path'], 'wb') as f:
                f.write(response.read())
        return f"Success: {name}"
    except Exception as e:
        return f"Failed: {name} - {str(e)}"

# Download in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(download_image, missing_items)

for r in results:
    print(r)

print("All downloads complete.")
