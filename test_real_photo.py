import urllib.request
import json
import re

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Masala_dosa_01.jpg/1280px-Masala_dosa_01.jpg"
target_path = r"assets\images\masala_dosa_real.jpg"

print("Downloading real photo...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
    data = response.read()
    out_file.write(data)
print("Saved to", target_path)

print("Updating menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

updated = False
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] == "Masala Dosa":
            item['image'] = "assets/images/masala_dosa_real.jpg"
            updated = True
            break
    if updated:
        break

new_json_str = json.dumps(menu_data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("menu.js updated successfully.")
