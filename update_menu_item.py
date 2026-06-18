import json
import re
import sys

if len(sys.argv) != 3:
    print("Usage: python update_menu_item.py 'Item Name' 'image_path.png'")
    sys.exit(1)

item_name = sys.argv[1]
image_path = sys.argv[2]

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON part
match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
if not match:
    print("Could not find menuData in menu.js")
    sys.exit(1)

json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] == item_name:
            item['image'] = image_path
            updated += 1

new_json_str = json.dumps(menu_data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {updated} menu items for '{item_name}'")
