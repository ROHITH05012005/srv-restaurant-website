import json
import re
import os
import time
import urllib.request
import urllib.parse
import sys

target_dir = r"assets\images"
os.makedirs(target_dir, exist_ok=True)

# Load token from environment or .env file
hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    if os.path.exists(".env"):
        with open(".env", "r") as env_file:
            for line in env_file:
                if line.startswith("HF_TOKEN="):
                    hf_token = line.split("=", 1)[1].strip()
                    break

if not hf_token:
    print("Error: HF_TOKEN not found in environment or .env file.")
    sys.exit(1)

print("Reading menu.js...")
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove BOM if present
prefix_bom = ""
if content.startswith("\ufeff"):
    prefix_bom = "\ufeff"
    content = content[1:]

match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
if not match:
    print("Error: Could not parse menuData from menu.js")
    sys.exit(1)

json_str = match.group(1)
menu_data = json.loads(json_str)

updated = 0
failed = 0
generated_items = []

model_id = "black-forest-labs/FLUX.1-schnell"
api_url = f"https://router.huggingface.co/hf-inference/models/{model_id}"

# Find the Soup category
soup_category = None
for category in menu_data:
    if 'soup' in category.get('category', '').lower():
        soup_category = category
        break

if not soup_category:
    print("Error: Soup category not found in menu.js")
    sys.exit(1)

items_to_generate = [item for item in soup_category.get('items', []) if item['image'] == "logo.png"]

if not items_to_generate:
    print("All items in the Soup category already have images!")
    sys.exit(0)

print(f"Found {len(items_to_generate)} soup items to generate.")

for item in items_to_generate:
    item_name = item['name']
    print(f"\nGenerating AI image for soup: {item_name} using HF...")
    try:
        # Build optimized prompt for soups
        prompt = f"Mouth-watering award-winning professional food photography of {item_name}. A premium, close-up shot of the freshly cooked piping hot soup served in a rustic ceramic bowl on a wooden coaster, garnished with fresh herbs, a spoon resting on the side. Dramatic warm side-lighting, steam gently rising, depth of field, high-end culinary presentation, 8k resolution, shot with Sony A7R V, highly detailed and photorealistic."
        
        post_data = json.dumps({"inputs": prompt}).encode("utf-8")
        
        req = urllib.request.Request(
            api_url, 
            data=post_data,
            headers={
                'Authorization': f'Bearer {hf_token}',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            },
            method="POST"
        )
        
        # Request image with retry on loading
        response_data = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=45) as response:
                    content_type = response.headers.get("Content-Type", "")
                    if "json" in content_type:
                        res_json = json.loads(response.read().decode("utf-8"))
                        if "error" in res_json and "loading" in res_json.get("error", "").lower():
                            wait_time = res_json.get("estimated_time", 20)
                            print(f"Model loading, waiting {wait_time:.1f} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            raise Exception(f"HF API Error: {res_json.get('error', res_json)}")
                    else:
                        response_data = response.read()
                        break
            except Exception as e:
                if attempt == 2:
                    raise e
                print(f"Error occurred: {e}. Retrying in 5 seconds...")
                time.sleep(5)
        
        if not response_data:
            raise Exception("No image data returned from Hugging Face.")

        clean_name = item_name.lower().replace(' ', '_').replace("'", "").replace("/", "_").replace("&", "and")
        file_name = f"{clean_name}_ai.png"
        target_path = os.path.join(target_dir, file_name)
        
        with open(target_path, 'wb') as out_file:
            out_file.write(response_data)
        
        # Update item
        item['image'] = f"assets/images/{file_name}"
        updated += 1
        generated_items.append(item_name)
        print(f"Successfully generated and mapped: {item_name}")
        
    except Exception as e:
        print(f"Failed to generate {item_name}: {e}")
        failed += 1
        
    time.sleep(2) # Delay between items

print(f"\nFINISHED! Generated {updated} soup items: {', '.join(generated_items)}")

if updated > 0:
    new_json_str = json.dumps(menu_data, indent=4)
    new_content = prefix_bom + content[:match.start(1)] + new_json_str + content[match.end(1):]
    with open('menu.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("menu.js updated successfully.")
    
    # Update cache buster in index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        v_match = re.search(r'menu\.js\?v=(\d+)', html)
        if v_match:
            current_v = int(v_match.group(1))
            html = re.sub(r'menu\.js\?v=\d+', f'menu.js?v={current_v + 1}', html)
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"index.html cache buster updated to v={current_v + 1}.")
    except Exception as e:
        print(f"Warning: Could not update index.html cache buster: {e}")
