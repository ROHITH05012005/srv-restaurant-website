import json
import re
import os
import urllib.request
import urllib.parse
import subprocess

target_dir = r"assets\images"
os.makedirs(target_dir, exist_ok=True)

print("Reading menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
json_str = match.group(1)
menu_data = json.loads(json_str)

item_name = "Ghee Masala Dosa"
print(f"Generating engineered AI image for: {item_name}...")

# Heavily engineered prompt describing the PHYSICAL appearance of a Dosa
prompt = "A giant, paper-thin, crispy, golden-brown rolled crepe. Authentic South Indian Dosa. Placed on a large banana leaf inside a premium dark ceramic plate. Beside the crepe are small stainless steel bowls with white coconut chutney and red sambar soup. Professional high-end luxury food photography, dark moody restaurant lighting, golden accents, 4k, macro lens, hyper-realistic texture."
encoded_prompt = urllib.parse.quote(prompt)

api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux&seed=42"

req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read()

    file_name = "ghee_masala_dosa_pollinations_proper.jpg"
    target_path = os.path.join(target_dir, file_name)

    with open(target_path, 'wb') as out_file:
        out_file.write(data)

    print("Image saved successfully.")

    # Update menu.js
    updated = False
    for category in menu_data:
        for item in category.get('items', []):
            if item['name'] == item_name:
                item['image'] = f"assets/images/{file_name}"
                updated = True
                break
        if updated:
            break

    new_json_str = json.dumps(menu_data, indent=4)
    new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("menu.js updated.")

    # Update index.html cache buster
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    v_match = re.search(r'menu\.js\?v=(\d+)', html)
    if v_match:
        current_v = int(v_match.group(1))
        html = re.sub(r'menu\.js\?v=\d+', f'menu.js?v={current_v + 1}', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Cache buster updated.")

    print("Pushing to GitHub...")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", "Test highly engineered prompt for Dosa"], check=False)
    subprocess.run(["git", "push"], check=False)
    print("Done!")

except Exception as e:
    print(f"Failed: {e}")
