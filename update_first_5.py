import json
import re

user_data = """
| Item                 | Price (₹) |
| -------------------- | --------: |
| Tea / Coffee         |        15 |
| Ginger Coffee        |        20 |
| Lemon Tea            |        20 |
| Green Tea            |        20 |
| Badam Milk           |        20 |
| Horlicks / Bournvita |        20 | 

| Item                     | Price (₹) |
| ------------------------ | --------: |
| Idli (2 Nos)             |        40 |
| Ghee Pudi Idli (2 Nos)   |        50 |
| Idli Vada (Single)       |        60 |
| Vada (1 No)              |        35 |
| 2 Idli 1 Vada            |        70 |
| Rava Idli with Ghee Pudi |        50 |
| Ghee Kharabath           |        35 |
| Ghee Kesaribath          |        35 |
| Ghee Chow Chow Bath      |        70 |
| Rice Bath                |        60 |
| Poori Sagu               |        70 |
| Ghee Bisi Bele Bath      |        60 |
| Ghee Pongal              |        60 |
| Curd Vada                |        50 |
| Mangalore Bajji / Pakoda |        40 |
| Buns (2 Nos)             |        70 |
| Bonda Soup               |        50 |
| Shavige Bath             |        60 |
| Curd Rice                |        50 |
| Ghee Thatte Idli         |        40 |
| Batan Idli               |        40 |
| Ragi Dosa                |        80 |
| Breakfast Combo          |       120 |
| Mini Combo               |       100 |

| Item                           | Price (₹) |
| ------------------------------ | --------: |
| Plain Dosa                     |        60 |
| Ghee Plain Dosa                |        70 |
| Butter Plain Dosa              |        80 |
| Paneer Plain Dosa              |        90 |
| Cheese Plain Dosa              |        90 |
| Paper Plain Dosa               |        90 |
| Masala Dosa                    |        70 |
| Ghee Masala Dosa               |       100 |
| Butter Masala Dosa             |       100 |
| Paneer Masala Dosa             |       100 |
| Cheese Masala Dosa             |       100 |
| Paper Masala Dosa              |       110 |
| Set Dosa                       |        70 |
| Khali Dosa                     |        70 |
| Khali Butter Dosa              |        80 |
| Onion Dosa                     |        90 |
| Rava Dosa                      |        90 |
| Rava Onion Dosa                |       100 |
| Rava Masala Dosa               |       100 |
| Rava Onion Masala Dosa         |       110 |
| Open Butter Masala Dosa        |        80 |
| Mysore Masala Dosa             |       100 |
| SRV Special Dosa               |       110 |
| Day Special Dosa               |       100 |
| Butter Akki Rotti / Ragi Rotti |        90 |
| Neer Dosa                      |        70 |
| Menthe Dosa                    |        80 |
| Palak Dosa                     |        80 |

| Item                 | Price (₹) |
| -------------------- | --------: |
| Tomato Soup          |        90 |
| Cream of Veg Soup    |        85 |
| Sweet Corn Soup      |        85 |
| Hot & Sour Soup      |        90 |
| Manchow Clear Soup   |        95 |
| Veg Clear Soup       |        85 |
| Lemon Coriander Soup |        80 |
| Cream of Mushroom    |        90 |
| Schezwan Palak Soup  |        90 |
| French Onion Soup    |        90 |

| Item                | Price (₹) |
| ------------------- | --------: |
| Paneer Tikka        |       210 |
| Aloo Tikka          |       190 |
| Veg Sheekh Kebab    |       190 |
| Mushroom Tikka      |       210 |
| Gobi Tikka          |       180 |
| Harabara Kebab      |       190 |
| Special Veg Platter |       240 |
"""

# Parse the tables
tables = user_data.split('Item                     | Price (₹)') # Just split by double newline roughly, but wait, the headers are slightly different spacing.
# Better to find all tables
table_blocks = re.split(r'\|\s*Item\s*\|\s*Price.*?\n\|[-\s]+\|[-\s:]+\|', user_data)
# table_blocks[0] is empty. 1 to 5 are the data.

category_names = ["Hot Beverages", "Breakfast", "Dosa's", "Soup", "Tandoori Starters"]
parsed_categories = {}

for i in range(1, 6):
    lines = table_blocks[i].strip().split('\n')
    items = []
    for line in lines:
        if not line.strip() or not '|' in line: continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            name = parts[1]
            price_str = parts[2]
            try:
                price = int(price_str)
                items.append({
                    "name": name,
                    "self_price": price,
                    "ac_price": price + 5, # Estimate AC price as +5 or +10
                    "image": "assets/images/" + name.lower().replace(' ', '_').replace('/', '_') + ".jpg"
                })
            except:
                pass
    parsed_categories[category_names[i-1]] = items

# Load existing menu.js
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

# Update the 5 categories
for cat in data:
    if cat['category'] in parsed_categories:
        cat['items'] = parsed_categories[cat['category']]

new_js_content = "const menuData = " + json.dumps(data, indent=2) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Updated 5 categories successfully")
