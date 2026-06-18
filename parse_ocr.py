import json

def parse_blocks(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    pages = text.split("--- Page ")[1:]
    
    # We define known categories to look for in the text
    known_categories = [
        "HOT BEVERAGES", "BREAKFAST", "DOSA'S", "SOUP", "TANDOORI STARTERS",
        "CHINESE STARTERS", "SPECIAL TAWA PULAO", "PAPAD", "NORTH INDIAN DRY",
        "INDIAN BREAD", "RAITHA / SALAD", "MAIN COURSE", "SPECIAL DISH",
        "CHINESE RICE", "COMBOS", "CHINESE SPECIAL", "MEALS", "EXTRA ITEMS",
        "BASUMATHI SPECIAL", "CHATS", "TAWA KA KAMAL", "SANDWICH", "JUICE",
        "FRUIT SHAKE", "LASSI", "SODA", "SWEETS", "ICE CREAM", "ICE CREAM SHAKE",
        "FRUIT SALAD", "SPECIAL ICE CREAM"
    ]
    
    # Normalize categories for matching
    norm_cats = {c.lower().replace(' ', ''): c for c in known_categories}
    
    all_items = []
    current_cat = "Uncategorized"
    
    for page in pages:
        lines = [line.strip() for line in page.split('\n') if line.strip()]
        
        # Heuristic: Find english names (start with letter, usually more than 1 word)
        # Find prices (just numbers)
        names = []
        prices = []
        
        for line in lines:
            # Check if line is a category
            norm_line = line.lower().replace(' ', '')
            matched_cat = None
            for nc, orig in norm_cats.items():
                if nc in norm_line and len(norm_line) < len(nc) + 5:
                    matched_cat = orig
                    break
            
            if matched_cat:
                current_cat = matched_cat
                continue
                
            # If line is just a number
            if line.isdigit():
                prices.append(int(line))
            elif re.match(r'^[A-Za-z]+', line) and len(line) > 3:
                # Looks like an English name
                names.append(line)
        
        # If lengths roughly match, zip them up
        if len(names) > 0 and len(prices) > 0:
            # Just take the min of both to pair them
            limit = min(len(names), len(prices))
            for i in range(limit):
                all_items.append({
                    "category": current_cat,
                    "name": names[i],
                    "price": prices[i]
                })

    return all_items

import re
ac_items = parse_blocks("ac_menu_raw.txt")
self_items = parse_blocks("self_menu_raw.txt")

# Merge them
merged = {}
for item in ac_items:
    name_key = item['name'].lower().strip()
    if name_key not in merged:
        merged[name_key] = {
            "name": item['name'],
            "category": item['category'],
            "ac_price": item['price'],
            "self_price": item['price'] # default to same if missing
        }

for item in self_items:
    name_key = item['name'].lower().strip()
    # Find best match in merged
    best_match = None
    for k in merged.keys():
        if name_key in k or k in name_key:
            best_match = k
            break
    
    if best_match:
        merged[best_match]["self_price"] = item['price']
    else:
        merged[name_key] = {
            "name": item['name'],
            "category": item['category'],
            "ac_price": item['price'],
            "self_price": item['price']
        }

# Group by category
final_menu = {}
for k, v in merged.items():
    cat = v['category']
    if cat not in final_menu:
        final_menu[cat] = []
    final_menu[cat].append({
        "name": v['name'],
        "ac_price": v['ac_price'],
        "self_price": v['self_price'],
        "image": "placeholder.png" # to be mapped later
    })

# Format as JS
js_content = "const menuData = " + json.dumps([{"category": k, "items": v} for k, v in final_menu.items()], indent=2) + ";\n"

with open("menu.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Created menu.js")
