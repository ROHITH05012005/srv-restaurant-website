import difflib

# Old items "Only in Old menu"
old_only = [
    ('Badam Milk', 55),
    ('Bajji (Mirchi / Onion)', 40),
    ('Chapati (3 pcs) + Curry', 80),
    ('Curd Rice', 60),
    ('Dahi Puri (6 pcs)', 60),
    ('Dinner Special Combo', 150),
    ('Filter Coffee', 25),
    ('French Fries', 70),
    ('Fresh Mango Juice', 60),
    ('Full Meals (Unlimited)', 120),
    ('Idli (2 pcs)', 40),
    ('Kesari Bath', 45),
    ('Masala Chai', 20),
    ('Masala Dosa', 70),
    ('Medu Vada (2 pcs)', 50),
    ('Mini Meals', 80),
    ('Pani Puri (6 pcs)', 50),
    ('Parotta + Salna', 90),
    ('Poori (2 pcs) + Bhaji', 65),
    ('Samosa (2 pcs)', 30),
    ('Set Dosa (3 pcs)', 60),
    ('Veg Biryani', 130),
    ('Veg Club Sandwich', 80),
    ('Veg Hakka Noodles', 100),
    ('Ven Pongal', 55)
]

# Read index.html names and prices
import re
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(
    r'<div class="food-card".*?'
    r'<div class="food-name">([^<]+)</div>.*?'
    r'<span class="food-price">₹(\d+)</span>',
    re.DOTALL
)
matches = pattern.findall(content)
new_menu = {name.strip(): int(price) for name, price in matches}

print("Searching for similar items and comparing prices:")
for old_name, old_price in old_only:
    # Find best match in new_menu
    best_matches = difflib.get_close_matches(old_name, new_menu.keys(), n=1, cutoff=0.5)
    if best_matches:
        new_name = best_matches[0]
        new_price = new_menu[new_name]
        print(f"Old: '{old_name}' (Rs.{old_price})  -->  New: '{new_name}' (Rs.{new_price})")
    else:
        print(f"No match for '{old_name}' (Rs.{old_price})")
