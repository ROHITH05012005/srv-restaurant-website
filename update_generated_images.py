import json
import re
import os
import shutil
import subprocess

# The images we successfully generated
generated_images = {
    'Mushroom Biryani': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\mushroom_biryani_1782079900025.png',
    'Roasted Papad': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\roasted_papad_1782079911778.png',
    'Masala Papad': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\masala_papad_1782079922106.png',
    'Fry Papad': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\fry_papad_1782079931727.png',
    'Gobi Dry': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\gobi_dry_1782079941050.png'
}

target_dir = os.path.join('assets', 'images')
os.makedirs(target_dir, exist_ok=True)

# Read menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
menu_data = json.loads(match.group(1))

updated_count = 0
for category in menu_data:
    for item in category.get('items', []):
        if item['name'] in generated_images and item['image'] == 'logo.png':
            src_path = generated_images[item['name']]
            
            clean_name = item['name'].lower().replace(' ', '_').replace('/', '_').replace('-', '_')
            clean_name = re.sub(r'[^a-z0-9_]', '', clean_name)
            filename = f"{clean_name}_ai.png"
            dest_path = os.path.join(target_dir, filename)
            
            # Copy file
            shutil.copyfile(src_path, dest_path)
            
            # Update menu data
            item['image'] = f"assets/images/{filename}"
            updated_count += 1
            print(f"Updated {item['name']}")

if updated_count > 0:
    # Write back menu.js
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Update cache buster
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    v_match = re.search(r'menu\.js\?v=(\d+)', html)
    if v_match:
        current_v = int(v_match.group(1))
        html = re.sub(r'menu\.js\?v=\d+', f'menu.js?v={current_v + 1}', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated cache buster to v={current_v + 1}")
    
    # Git add, commit, push
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', f'Add 5 new images starting from Mushroom Biryani'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("Pushed to GitHub")
else:
    print("No items updated.")
