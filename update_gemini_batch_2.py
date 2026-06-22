import json
import re
import os
import shutil
import subprocess

# The images we successfully generated
generated_images = {
    'Kulcha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\kulcha_1782142962136.png',
    'Butter Kulcha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\butter_kulcha_1782142974188.png',
    'Paratha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\paratha_1782142999768.png',
    'Butter Paratha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\butter_paratha_1782143013781.png',
    'Plain Raitha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\plain_raitha_1782143026077.png',
    'Onion Raitha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\onion_raitha_1782143039452.png',
    'Cucumber Raitha': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\cucumber_raitha_1782143050450.png',
    'Veg Kurma': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\veg_kurma_1782143083760.png',
    'Veg Kolhapuri': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\veg_kolhapuri_1782143099574.png',
    'Veg Kadai': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\veg_kadai_1782143113183.png',
    'Veg Hyderabadi': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\veg_hyderabadi_1782143128997.png',
    'Veg Handi': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\veg_handi_1782143141074.png',
    'Paneer Butter Masala': r'C:\Users\rohib\.gemini\antigravity\brain\2b1c2472-a251-42d1-a670-0c347bc524f3\paneer_butter_masala_1782143156232.png'
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
    subprocess.run(['git', 'commit', '-m', f'Add 13 premium images using Gemini'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("Pushed to GitHub")
else:
    print("No items updated.")
