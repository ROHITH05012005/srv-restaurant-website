import json
import os
import time
import urllib.request
import urllib.parse

# Load menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

assets_dir = os.path.join(os.getcwd(), 'assets', 'images')
os.makedirs(assets_dir, exist_ok=True)

items_to_download = []

for cat in data:
    for item in cat['items']:
        name = item['name']
        img_path = item['image'] # e.g. assets/images/gobi_manchurian.png
        filename = os.path.basename(img_path)
        full_path = os.path.join(assets_dir, filename)
        
        # We assume if size is < 20KB (20000 bytes), it's a placeholder or error.
        if not os.path.exists(full_path) or os.path.getsize(full_path) < 20000:
            items_to_download.append({
                "name": name,
                "full_path": full_path
            })

print(f"Found {len(items_to_download)} placeholder/missing images to replace with real AI photos.")

for i, item in enumerate(items_to_download, 1):
    name = item['name']
    path = item['full_path']
    print(f"[{i}/{len(items_to_download)}] Generating AI image for '{name}'...")
    
    clean_name = name.split('(')[0].strip() # Remove things like "(2 Nos)"
    # Prompt engineering for high quality food
    prompt = f"Delicious authentic high quality Indian food photography of {clean_name}, dark background, 4k, professional lighting, luxury restaurant presentation"
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&private=true"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    success = False
    retries = 3
    while not success and retries > 0:
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                content = response.read()
                # Ensure we didn't just download another error message (which would be small)
                if len(content) > 20000:
                    with open(path, 'wb') as f:
                        f.write(content)
                    print(f"  -> Success! Saved to {os.path.basename(path)}")
                    success = True
                else:
                    print(f"  -> Downloaded file too small ({len(content)} bytes), likely an error. Retrying...")
                    retries -= 1
                    time.sleep(15)
        except Exception as e:
            print(f"  -> Failed: {e}. Retrying...")
            retries -= 1
            time.sleep(15)
            
    # VERY IMPORTANT: Slow down to prevent Rate Limiting / 402 Payment Required
    if i < len(items_to_download):
        print("  Waiting 12 seconds to prevent rate limit...")
        time.sleep(12)

print("Finished generating AI images.")
