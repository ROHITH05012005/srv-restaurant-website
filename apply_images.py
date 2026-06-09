import os
import json
import difflib

# Read images from assets/images
images_dir = os.path.join('assets', 'images')
images = [f for f in os.listdir(images_dir) if f.endswith('.png') or f.endswith('.jpg')]

# Read menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract JSON
json_str = js_content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

for category in data:
    for item in category['items']:
        name = item['name'].lower().replace(' ', '_').replace('/', '_')
        
        # Try to find a matching image
        best_match = None
        best_score = 0
        for img in images:
            img_name = img.lower().replace('_premium.png', '').replace('.png', '').replace('.jpg', '')
            score = difflib.SequenceMatcher(None, name, img_name).ratio()
            if score > best_score:
                best_score = score
                best_match = img
                
        if best_score > 0.6: # reasonable threshold
            item['image'] = f"assets/images/{best_match}"
        else:
            item['image'] = 'logo.png' # Fallback

# Write back
new_js_content = "const menuData = " + json.dumps(data, indent=4) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Mapped images successfully.")
