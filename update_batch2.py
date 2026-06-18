import json
import re

updates = {
    "2 Idli 1 Vada": "assets/images/idli_vada_combo_premium.png",
    "Rava Idli with Ghee Pudi": "assets/images/rava_idli_premium.png",
    "Ghee Kharabath": "assets/images/ghee_kharabath_premium.png",
    "Ghee Kesaribath": "assets/images/ghee_kesaribath_premium.png",
    "Ghee Chow Chow Bath": "assets/images/chow_chow_bath_premium.png",
    "Rice Bath": "assets/images/rice_bath_premium.png"
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
