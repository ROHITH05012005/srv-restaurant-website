import json
import re

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON part
match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
if not match:
    print("Could not find menuData in menu.js")
    exit(1)

json_str = match.group(1)
menu_data = json.loads(json_str)

# Update "Tea / Coffee" and "Filter Coffee" to use the new image
updated = 0
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] in ['Tea / Coffee', 'Filter Coffee']:
            item['image'] = 'assets/images/filter_coffee_new.png'
            updated += 1

new_json_str = json.dumps(menu_data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {updated} menu items to use filter_coffee_new.png")
