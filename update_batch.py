import json
import re

updates = {
    "Horlicks / Bournvita": "assets/images/horlicks_premium.png",
    "Idli (2 Nos)": "assets/images/idli_premium_new.png",
    "Ghee Pudi Idli (2 Nos)": "assets/images/ghee_pudi_idli_premium.png",
    "Idli Vada (Single)": "assets/images/idli_vada_premium.png",
    "Vada (1 No)": "assets/images/vada_premium.png"
}

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] in updates:
            item['image'] = updates[item['name']]
            updated += 1

new_json_str = json.dumps(menu_data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {updated} items.")
