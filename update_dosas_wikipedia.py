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

for category in menu_data:
    if category['category'] == "Dosa's":
        for item in category.get('items', []):
            if item['image'] == "logo.png":
                item_name = item['name']
                print(f"Searching Wikipedia for real image of: {item_name}...")
                try:
                    # Search Wikipedia for the image
                    search_term = urllib.parse.quote(item_name)
                    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_term}"
                    
                    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10) as response:
                        data = json.loads(response.read())
                        
                    pages = data['query']['pages']
                    img_url = None
                    for page_id in pages:
                        if 'original' in pages[page_id]:
                            img_url = pages[page_id]['original']['source']
                            break
                    
                    if img_url:
                        print(f"Found Wikipedia image URL: {img_url}")
                        
                        clean_name = item_name.lower().replace(' ', '_').replace("'", "")
                        file_name = f"{clean_name}_real.jpg"
                        target_path = os.path.join(target_dir, file_name)
                        
                        # Download image
                        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(img_req, timeout=10) as response, open(target_path, 'wb') as out_file:
                            out_file.write(response.read())
                        
                        # Update item
                        item['image'] = f"assets/images/{file_name}"
                        updated += 1
                        print(f"Successfully downloaded and mapped {item_name}.")
                    else:
                        print(f"No Wikipedia image found for {item_name}")
                except Exception as e:
                    print(f"Failed to fetch {item_name}: {e}")
                time.sleep(0.5)

print(f"Finished downloading {updated} items.")

if updated > 0:
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("menu.js updated successfully.")
    
    # Update cache buster in index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'menu\.js\?v=\d+', 'menu.js?v=15', html)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html cache buster updated to v=15.")
