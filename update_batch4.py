import json
import re
import os
import glob
import shutil

artifact_dir = r"C:\Users\rohib\.gemini\antigravity\brain\5d9e47ef-174a-415f-ab76-c64b90d60d12"
target_dir = r"assets\images"

updates = {
    "Plain Dosa": "plain_dosa_premium",
    "Ghee Plain Dosa": "ghee_plain_dosa_premium",
    "Butter Plain Dosa": "butter_plain_dosa_premium"
}

# 1. Find and copy the latest images from artifacts
for item_name, base_name in updates.items():
    search_pattern = os.path.join(artifact_dir, f"{base_name}_*.png")
    matches = glob.glob(search_pattern)
    if matches:
        latest_file = max(matches, key=os.path.getmtime)
        target_file = os.path.join(target_dir, f"{base_name}.png")
        shutil.copy2(latest_file, target_file)
        print(f"Copied {os.path.basename(latest_file)} to {target_file}")
    else:
        print(f"WARNING: No artifact found for {base_name}")

# 2. Update menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] in updates:
            item['image'] = f"assets/images/{updates[item['name']]}.png"
            updated += 1

new_json_str = json.dumps(menu_data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {updated} items in menu.js.")
