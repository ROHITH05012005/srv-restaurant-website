import json
import re

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

all_items = []
for cat in data:
    for item in cat['items']:
        name = item['name'].strip()
        # Filter out garbage
        if len(name) < 3: continue
        if re.search(r'[&?#@]', name): continue
        if name.count(' ') > 5: continue
        # if it contains too many weird chars, skip
        if len(re.findall(r'[^a-zA-Z0-9\s/&()-]', name)) > 2: continue
        # Ignore gibberish that doesn't have at least one valid English word
        if not re.search(r'[A-Za-z]{3,}', name): continue
        
        all_items.append(item)

# Let's map items to 31 categories based on keywords
categories = {
    "Hot Beverages": ["Tea", "Coffee", "Milk", "Bournivita", "Horlicks"],
    "Breakfast": ["Idli", "Vada", "Kharabath", "Kesaribath", "Bath", "Sagu", "Pongal", "Bajji", "Buns", "Bonda"],
    "Dosas": ["Dosa", "Roast"],
    "Soup": ["Soup", "Manchow", "Tomato"],
    "Tandoori Starters": ["Tikka", "Tandoori"],
    "Chinese Starters": ["Gobi", "Babycorn", "Manchurian", "Chilly", "Crispy", "Mushroom", "65", "Pepper Dry"],
    "Special Tawa Pulao": ["Tawa Pulav", "Tawa Pulao"],
    "Papad": ["Papad"],
    "North Indian Dry": [],
    "Indian Bread": ["Roti", "Naan", "Kulcha"],
    "Raitha / Salad": ["Raitha", "Salad"],
    "Main Course": ["Masala", "Palak", "Kurma", "Handi", "Kadai", "Burji", "Koftha", "Kolhapuri", "Hyderabadi", "Do-Pyaza", "Makhani"],
    "Special Dish": [],
    "Chinese Rice": ["Fried Rice"],
    "Combos": ["Combo"],
    "Chinese Special (Noodles)": ["Noodles", "Chow Mein"],
    "Meals": ["Meals"],
    "Extra Items": ["Extra", "Cup Curd", "Butter"],
    "Chats": ["Puri", "Chat", "Pav", "Bhaji", "Samosa"],
    "Puri": ["Poori"],
    "Tawa": [],
    "Sandwich": ["Sandwich"],
    "Juice": ["Juice"],
    "Fruit Shake": ["Shake", "Milkshake"],
    "Lassi": ["Lassi"],
    "Soda": ["Soda"],
    "Sweets": ["Jamoon", "Sweet"],
    "Ice Cream": ["Ice Cream"],
    "Ice Cream Shake": [],
    "Fruit Salad": [],
    "Special Ice Cream": []
}

new_menu = []
used = set()

# Map items
for cat_name, keywords in categories.items():
    cat_items = []
    for item in all_items:
        if item['name'] in used: continue
        # check keywords
        name_lower = item['name'].lower()
        if any(kw.lower() in name_lower for kw in keywords):
            cat_items.append(item)
            used.add(item['name'])
    
    new_menu.append({
        "category": cat_name,
        "items": cat_items
    })

# Place remaining items in Uncategorized if they seem valid
remaining = [item for item in all_items if item['name'] not in used]
if remaining:
    new_menu.append({
        "category": "Uncategorized",
        "items": remaining
    })

# Save new menu
new_js_content = "const menuData = " + json.dumps(new_menu, indent=2) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Reorganized into 31 categories.")
