import json
import re
import os
import urllib.request
import urllib.parse
import sys

def slugify(text):
    text = text.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text

def get_menu_data(content):
    match = re.search(r'const\s+menuData\s*=\s*(\[.*\]);', content, re.DOTALL)
    if not match: return None, None
    return json.loads(match.group(1)), match

def update_cache_buster():
    if not os.path.exists('index.html'):
        return
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    match = re.search(r'src="menu\.js\?v=(\d+)"', html)
    if match:
        v = int(match.group(1)) + 1
        html = re.sub(r'src="menu\.js\?v=\d+"', f'src="menu.js?v={v}"', html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"index.html cache buster updated to v={v}.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_item_image.py \"[Item Name]\"")
        sys.exit(1)
        
    target_item_name = sys.argv[1].strip()
    print(f"Searching for item: '{target_item_name}' in menu.js...")
    
    if not os.path.exists('menu.js'):
        print("Error: menu.js not found in current directory.")
        sys.exit(1)
        
    with open('menu.js', 'r', encoding='utf-8') as f:
        content = f.read()
        
    menu_data, match = get_menu_data(content)
    if not menu_data:
        print("Error: Could not parse menuData from menu.js.")
        sys.exit(1)
        
    # Find item
    found_item = None
    target_lower = target_item_name.lower()
    
    for category in menu_data:
        for item in category.get('items', []):
            if item['name'].lower() == target_lower:
                found_item = item
                break
        if found_item:
            break
            
    if not found_item:
        # Try substring match
        for category in menu_data:
            for item in category.get('items', []):
                if target_lower in item['name'].lower():
                    found_item = item
                    print(f"Matched item: '{item['name']}' using search term '{target_item_name}'")
                    break
            if found_item:
                break
                
    if not found_item:
        print(f"Error: Item '{target_item_name}' not found in the menu.")
        sys.exit(1)
        
    name = found_item['name']
    slug = slugify(name)
    filename = f"{slug}_ai.png"
    filepath = os.path.join('assets', 'images', filename)
    os.makedirs(os.path.join('assets', 'images'), exist_ok=True)
    
    # Custom high-quality prompt template
    prompt = f"A beautiful, appetizing, highly realistic professional food photography shot of {name}, traditional Indian vegetarian cuisine. Placed on a dark rustic wooden table, with dramatic warm moody lighting, steam rising. Elegant, premium quality, 8k, matching a dark themed high-end restaurant UI with golden accents."
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"
    
    print(f"Generating image for '{name}' using Pollinations AI (Flux)...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            
        with open(filepath, 'wb') as out_file:
            out_file.write(data)
            
        print(f"Image successfully saved to {filepath}")
        
        # Update path
        found_item['image'] = f"assets/images/{filename}"
        
        new_json_str = json.dumps(menu_data, indent=4)
        new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
        
        with open('menu.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("menu.js updated successfully.")
        
        update_cache_buster()
        print("Process complete!")
        
    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
