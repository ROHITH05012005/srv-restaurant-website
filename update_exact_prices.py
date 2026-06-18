import json
import re

user_text = """
SELF MENU (Service Menu PDF)
1. Hot Beverages
Item	Price (₹)
Tea / Coffee	15
Ginger Coffee	20
Lemon Tea	20
Green Tea	20
Badam Milk	20
Horlicks / Bournvita	20
Total Items: 6
2. Breakfast
Item	Price (₹)
Idli (2 Nos)	40
Ghee Pudi Idli (2 Nos)	50
Idli Vada (Single)	60
Vada (1 No)	35
2 Idli 1 Vada	70
Rava Idli with Ghee Pudi	50
Ghee Kharabath	35
Ghee Kesaribath	35
Ghee Chow Chow Bath	70
Rice Bath	60
Poori Sagu	70
Ghee Bisi Bele Bath	60
Ghee Pongal	60
Curd Vada	50
Mangalore Bajji / Pakoda	40
Buns (2 Nos)	70
Bonda Soup	50
Shavige Bath	60
Curd Rice	50
Ghee Thatte Idli	40
Batan Idli	40
Ragi Dosa	80
Breakfast Combo	120
Mini Combo	100
Total Items: 24
3. Dosa's
Item	Price (₹)
Plain Dosa	60
Ghee Plain Dosa	70
Butter Plain Dosa	80
Paneer Plain Dosa	90
Cheese Plain Dosa	90
Paper Plain Dosa	90
Masala Dosa	70
Ghee Masala Dosa	100
Butter Masala Dosa	100
Paneer Masala Dosa	100
Cheese Masala Dosa	100
Paper Masala Dosa	110
Set Dosa	70
Khali Dosa	70
Khali Butter Dosa	80
Onion Dosa	90
Rava Dosa	90
Rava Onion Dosa	100
Rava Masala Dosa	100
Rava Onion Masala Dosa	110
Open Butter Masala Dosa	80
Mysore Masala Dosa	100
SRV Special Dosa	110
Day Special Dosa	100
Butter Akki Rotti / Ragi Rotti	90
Neer Dosa	70
Menthe Dosa	80
Palak Dosa	80
Total Items: 28
4. Soup
Item	Price (₹)
Tomato Soup	90
Cream of Veg Soup	85
Sweet Corn Soup	85
Hot & Sour Soup	90
Manchow Clear Soup	95
Veg Clear Soup	85
Lemon Coriander Soup	80
Cream of Mushroom	90
Schezwan Palak Soup	90
French Onion Soup	90
Total Items: 10
5. Tandoori Starters
Item	Price (₹)
Paneer Tikka	210
Aloo Tikka	190
Veg Sheekh Kebab	190
Mushroom Tikka	210
Gobi Tikka	180
Harabara Kebab	190
Special Veg Platter	240
Total Items: 7
AC MENU PDF
1. Hot Beverages
Item	Price (₹)
Tea / Coffee	30
Ginger Coffee	35
Lemon Tea	30
Badam Milk	40
Horlicks / Bournvita	40
Total Items: 5
2. Breakfast
Item	Price (₹)
Idli (2 Nos)	50
Ghee Pudi Idli (2 Nos)	60
Idli Vada (Single)	80
Vada (1 No)	40
2 Idli 1 Vada	80
Rava Idli with Ghee Pudi	55
Ghee Kharabath	50
Ghee Kesaribath	50
Ghee Chow Chow Bath	100
Rice Bath	70
Poori Sagu	80
Ghee Bisi Bele Bath	70
Ghee Pongal	70
Curd Vada	60
Mangalore Bajji / Pakoda	50
Buns (2 Nos)	80
Bonda Soup	60
Shavige Bath	70
Curd Rice	85
Ghee Thatte Idli	50
Batan Idli	50
Ragi Dosa	90
Breakfast Combo	140
Mini Combo	130
Total Items: 24
3. Dosa's
Item	Price (₹)
Plain Dosa	70
Ghee Plain Dosa	90
Butter Plain Dosa	90
Paneer Plain Dosa	110
Cheese Plain Dosa	110
Paper Plain Dosa	110
Masala Dosa	85
Butter Masala Dosa	100
Ghee Masala Dosa	100
Paneer Masala Dosa	125
Cheese Masala Dosa	125
Paper Masala Dosa	125
Set Dosa	85
Khali Dosa	85
Khali Butter Dosa	95
Onion Dosa	100
Rava Dosa	100
Rava Onion Dosa	110
Rava Masala Dosa	125
Rava Onion Masala Dosa	125
Open Butter Masala Dosa	110
Mysore Masala Dosa	110
SRV Special Dosa	125
Day Special Dosa	100
Butter Akki Rotti / Ragi Rotti	100
Neer Dosa	80
Menthe Dosa	95
Palak Dosa	95
Total Items: 28
4. Soup
Item	Price (₹)
Tomato Soup	90
Cream of Veg Soup	95
Sweet Corn Soup	95
Hot & Sour Soup	90
Manchow Clear Soup	100
Veg Clear Soup	100
Lemon Coriander Soup	100
Cream of Mushroom	100
Schezwan Palak Soup	110
French Onion Soup	110
Total Items: 10
5. Tandoori Starters
Item	Price (₹)
Paneer Tikka	225
Aloo Tikka	200
Veg Sheekh Kebab	200
Mushroom Tikka	225
Gobi Tikka	200
Harabara Kebab	200
Special Veg Platter	280
Total Items: 7
"""

self_menu_text = user_text.split("AC MENU PDF")[0]
ac_menu_text = user_text.split("AC MENU PDF")[1]

def parse_items(text):
    categories = {}
    current_cat = None
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        # match "1. Hot Beverages"
        m = re.match(r'^\d+\.\s+(.*)$', line)
        if m:
            current_cat = m.group(1).strip()
            categories[current_cat] = {}
            continue
        if 'Item\tPrice' in line or 'Total Items:' in line:
            continue
        
        # Split by tab
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            try:
                price = int(parts[1].strip().replace('₹', '').strip())
                categories[current_cat][name] = price
            except:
                pass
    return categories

self_cats = parse_items(self_menu_text)
ac_cats = parse_items(ac_menu_text)

# We have existing menuData. Let's merge it properly.
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

# Update prices exactly
for cat in data:
    cat_name = cat['category']
    if cat_name in self_cats:
        cat_items = []
        for name, self_price in self_cats[cat_name].items():
            ac_price = ac_cats.get(cat_name, {}).get(name, self_price)
            cat_items.append({
                "name": name,
                "self_price": self_price,
                "ac_price": ac_price,
                "image": "assets/images/" + name.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('&', 'and') + ".jpg"
            })
        cat['items'] = cat_items

new_js_content = "const menuData = " + json.dumps(data, indent=2) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Updated prices for AC and Self menus exactly.")
