import os
import json
import difflib

# Read only premium images from assets/images
images_dir = os.path.join('assets', 'images')
images = [f for f in os.listdir(images_dir) if f.endswith('_premium.png')]

# Read menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract JSON
json_str = js_content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

mapped_count = 0

for category in data:
    for item in category['items']:
        name = item['name'].lower().replace(' ', '_').replace('/', '_')
        
        best_match = None
        best_score = 0
        for img in images:
            img_name = img.lower().replace('_premium.png', '')
            score = difflib.SequenceMatcher(None, name, img_name).ratio()
            if score > best_score:
                best_score = score
                best_match = img
                
        # High threshold to prevent silly matches like "masala_dosa" -> "masala_soda"
        if best_score > 0.80: 
            item['image'] = f"assets/images/{best_match}"
            mapped_count += 1
        # If no good match, KEEP the original item['image']! Don't overwrite it.

# Write back
new_js_content = "const menuData = " + json.dumps(data, indent=4) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print(f"Mapped {mapped_count} PREMIUM images successfully.")
