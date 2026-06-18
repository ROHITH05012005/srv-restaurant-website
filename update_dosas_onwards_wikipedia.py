import json
import re
import os
import time
import urllib.request
import urllib.parse

target_dir = r"assets\images"
os.makedirs(target_dir, exist_ok=True)

print("Reading menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
not_found = 0
start_processing = False

for category in menu_data:
    if category['category'] == "Dosa's":
        start_processing = True
        
    if not start_processing:
        continue
        
    for item in category.get('items', []):
        if item['image'] == "logo.png":
            item_name = item['name']
            try:
                search_term = urllib.parse.quote(item_name)
                api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_term}"
                
                req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read())
                    
                pages = data.get('query', {}).get('pages', {})
                img_url = None
                for page_id in pages:
                    if 'original' in pages[page_id]:
                        img_url = pages[page_id]['original']['source']
                        break
                
                if img_url and img_url.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.PNG')):
                    print(f"FOUND: {item_name} -> {img_url}")
                    
                    clean_name = item_name.lower().replace(' ', '_').replace("'", "")
                    ext = img_url.split('.')[-1]
                    file_name = f"{clean_name}_wiki.{ext}"
                    target_path = os.path.join(target_dir, file_name)
                    
                    # Download image
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(img_req, timeout=10) as response, open(target_path, 'wb') as out_file:
                        out_file.write(response.read())
                    
                    # Update item
                    item['image'] = f"assets/images/{file_name}"
                    updated += 1
                else:
                    not_found += 1
            except Exception as e:
                not_found += 1
            time.sleep(0.2) # Small delay to respect Wikipedia API

print(f"\nFINISHED! Successfully downloaded: {updated} items. Failed to find: {not_found} items.")

if updated > 0:
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("menu.js updated successfully.")
    
    # Update cache buster in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'menu\.js\?v=\d+', 'menu.js?v=17', html)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html cache buster updated to v=17.")
