import json
import re

user_text = """
SELF MENU (Service Menu PDF)
6. Chinese Starters
Item	Price (₹)
Gobi Manchurian	110
Baby Corn Manchurian	130
Mushroom Manchurian	140
Paneer Manchurian	150
Veg 65	120
Gobi 65	120
Baby Corn 65	130
Mushroom 65	140
Paneer 65	150
Crispy Veg	140
Crispy Corn	140
Crispy Baby Corn	150
Crispy Mushroom	160
Crispy Paneer	170
Chilli Gobi	130
Chilli Baby Corn	140
Chilli Mushroom	150
Chilli Paneer	160
Total Items: 18

7. Special Tawa Pulao
Item	Price (₹)
Veg Pulao	110
Kashmiri Pulao	130
Paneer Pulao	140
Mushroom Pulao	140
Ghee Rice	90
Jeera Rice	90
Veg Biryani	140
Paneer Biryani	150
Mushroom Biryani	150

Total Items: 9

8. Papad
Item	Price (₹)
Roasted Papad	20
Masala Papad	40
Fry Papad	25

Total Items: 3

9. North Indian Dry
Item	Price (₹)
Gobi Dry	140
Veg Kolhapuri Dry	150
Veg Kadai Dry	150
Paneer Butter Masala Dry	180
Paneer Kadai Dry	180
Mushroom Masala Dry	170
Mushroom Kadai Dry	170

Total Items: 7

10. Indian Bread
Item	Price (₹)
Tandoori Roti	25
Butter Roti	30
Plain Naan	40
Butter Naan	50
Garlic Naan	60
Kulcha	60
Butter Kulcha	70
Paratha	60
Butter Paratha	70

Total Items: 9

11. RAITHA / SALAD
Item	Price (₹)
Plain Raitha	50
Onion Raitha	60
Cucumber Raitha	60
Veg Salad	70
Green Salad	70

Total Items: 5

12. MAIN COURSE
Item	Price (₹)
Veg Kurma	130
Veg Kolhapuri	140
Veg Kadai	140
Veg Hyderabadi	140
Veg Handi	140
Paneer Butter Masala	160
Kadai Paneer	160
Palak Paneer	160
Mushroom Masala	150
Mushroom Kadai	150
Mix Veg Curry	140

Total Items: 11

13. SPECIAL DISH
Item	Price (₹)
Paneer Butter Masala Special	180
Paneer Tikka Masala	180
Mushroom Pepper Dry	170
Veg Tawa Fry	160
SRV Special Veg	180

Total Items: 5

14. CHINESE RICE
Item	Price (₹)
Veg Fried Rice	120
Schezwan Fried Rice	130
Gobi Fried Rice	130
Mushroom Fried Rice	140
Paneer Fried Rice	150
Veg Noodles	120
Schezwan Noodles	130
Gobi Noodles	130
Mushroom Noodles	140
Paneer Noodles	150

Total Items: 10

15. COMBOS
Item	Price (₹)
Fried Rice + Manchurian	170
Noodles + Manchurian	170
Fried Rice + Noodles + Manchurian	220

Total Items: 3

16. CHINESE SPECIAL
Item	Price (₹)
Dragon Paneer	170
Dragon Mushroom	160
Dragon Baby Corn	150
Hong Kong Noodles	150
American Chopsuey	160

Total Items: 5

17. MEALS
Item	Price (₹)
South Meals	100
Special Meals	150
Mini Meals	80

Total Items: 3

18. EXTRA ITEMS
Item	Price (₹)
Extra Curry	30
Extra Sambar	20
Extra Chutney	20
Curd	30
Pickle	10

Total Items: 5

19. BASUMATHI SPECIAL
Item	Price (₹)
Veg Dum Biryani	150
Paneer Dum Biryani	170
Mushroom Dum Biryani	170
Kashmiri Biryani	160
Jeera Rice	90

Total Items: 5

20. CHATS
Item	Price (₹)
Masala Puri	50
Pani Puri	50
Sev Puri	50
Dahi Puri	60
Bhel Puri	50
Special Chat	70

Total Items: 6

21. TAWA KA KAMAL
Item	Price (₹)
Tawa Pulav	110
Veg Tawa Masala	140
Paneer Tawa Masala	160
Mushroom Tawa Masala	150
Tawa Biryani	140

Total Items: 5

22. SANDWICH
Item	Price (₹)
Veg Sandwich	70
Grilled Sandwich	90
Cheese Sandwich	100
Paneer Sandwich	110
Club Sandwich	120

Total Items: 5

23. JUICE
Item	Price (₹)
Sweet Lime	60
Orange	70
Pineapple	70
Watermelon	60
Grape	70
Mosambi	60
Apple Juice	80
Pomegranate	90

Total Items: 8

24. FRUIT SHAKE
Item	Price (₹)
Banana Shake	80
Apple Shake	90
Pineapple Shake	90
Chikoo Shake	90
Mango Shake	100
Dry Fruit Shake	120

Total Items: 6

25. LASSI
Item	Price (₹)
Sweet Lassi	60
Salt Lassi	60
Special Lassi	80

Total Items: 3

26. SODA
Item	Price (₹)
Lemon Soda	40
Sweet Lime Soda	50
Salt Soda	40
Masala Soda	50

Total Items: 4

27. SWEETS
Item	Price (₹)
Gulab Jamun	40
Carrot Halwa	50
Gajar Halwa	50
Kesari Bath	40
Special Sweet	60

Total Items: 5

28. ICE CREAM
Item	Price (₹)
Vanilla	40
Strawberry	40
Butterscotch	50
Chocolate	50
Pista	50

Total Items: 5

29. ICE CREAM SHAKE
Item	Price (₹)
Vanilla Shake	90
Strawberry Shake	90
Chocolate Shake	100
Butterscotch Shake	100

Total Items: 4

30. FRUIT SALAD
Item	Price (₹)
Fruit Salad	90
Fruit Salad with Ice Cream	120

Total Items: 2

31. SPECIAL ICE CREAM
Item	Price (₹)
Gadbad Ice Cream	120
Dry Fruit Delight	140
Special Ice Cream	130
Banana Split	150

Total Items: 4

====================

AC MENU PDF
6. Chinese Starters
Item	Price (₹)
Gobi Manchurian	140
Baby Corn Manchurian	150
Mushroom Manchurian	170
Paneer Manchurian	180
Veg 65	140
Gobi 65	150
Baby Corn 65	160
Mushroom 65	170
Paneer 65	180
Crispy Veg	160
Crispy Corn	160
Crispy Baby Corn	170
Crispy Mushroom	180
Crispy Paneer	190
Chilli Gobi	150
Chilli Baby Corn	160
Chilli Mushroom	170
Chilli Paneer	180
Total Items: 18

7. Special Tawa Pulao
Item	Price (₹)
Veg Pulao	140
Kashmiri Pulao	160
Paneer Pulao	180
Mushroom Pulao	180
Ghee Rice	120
Jeera Rice	120
Veg Biryani	180
Paneer Biryani	190
Mushroom Biryani	190

Total Items: 9

8. Papad
Item	Price (₹)
Roasted Papad	30
Masala Papad	50
Fry Papad	35

Total Items: 3

9. North Indian Dry
Item	Price (₹)
Gobi Dry	170
Veg Kolhapuri Dry	180
Veg Kadai Dry	180
Paneer Butter Masala Dry	220
Paneer Kadai Dry	220
Mushroom Masala Dry	200
Mushroom Kadai Dry	200

Total Items: 7

10. Indian Bread
Item	Price (₹)
Tandoori Roti	30
Butter Roti	40
Plain Naan	50
Butter Naan	60
Garlic Naan	70
Kulcha	70
Butter Kulcha	80
Paratha	70
Butter Paratha	80

Total Items: 9

11. RAITHA / SALAD
Item	Price (₹)
Plain Raitha	70
Onion Raitha	80
Cucumber Raitha	80
Veg Salad	90
Green Salad	90

Total Items: 5

12. MAIN COURSE
Item	Price (₹)
Veg Kurma	170
Veg Kolhapuri	180
Veg Kadai	180
Veg Hyderabadi	180
Veg Handi	180
Paneer Butter Masala	220
Kadai Paneer	220
Palak Paneer	220
Mushroom Masala	200
Mushroom Kadai	200
Mix Veg Curry	180

Total Items: 11

13. SPECIAL DISH
Item	Price (₹)
Paneer Butter Masala Special	240
Paneer Tikka Masala	240
Mushroom Pepper Dry	220
Veg Tawa Fry	200
SRV Special Veg	240

Total Items: 5

14. CHINESE RICE
Item	Price (₹)
Veg Fried Rice	150
Schezwan Fried Rice	160
Gobi Fried Rice	160
Mushroom Fried Rice	180
Paneer Fried Rice	190
Veg Noodles	150
Schezwan Noodles	160
Gobi Noodles	160
Mushroom Noodles	180
Paneer Noodles	190

Total Items: 10

15. COMBOS
Item	Price (₹)
Fried Rice + Manchurian	220
Noodles + Manchurian	220
Fried Rice + Noodles + Manchurian	280

Total Items: 3

16. CHINESE SPECIAL
Item	Price (₹)
Dragon Paneer	220
Dragon Mushroom	200
Dragon Baby Corn	190
Hong Kong Noodles	190
American Chopsuey	220

Total Items: 5

17. MEALS
Item	Price (₹)
South Meals	140
Special Meals	200
Mini Meals	120

Total Items: 3

18. EXTRA ITEMS
Item	Price (₹)
Extra Curry	40
Extra Sambar	30
Extra Chutney	30
Curd	40
Pickle	20

Total Items: 5

19. BASUMATHI SPECIAL
Item	Price (₹)
Veg Dum Biryani	190
Paneer Dum Biryani	220
Mushroom Dum Biryani	220
Kashmiri Biryani	200
Jeera Rice	120

Total Items: 5

20. CHATS
Item	Price (₹)
Masala Puri	70
Pani Puri	70
Sev Puri	70
Dahi Puri	80
Bhel Puri	70
Special Chat	100

Total Items: 6

21. TAWA KA KAMAL
Item	Price (₹)
Tawa Pulav	140
Veg Tawa Masala	180
Paneer Tawa Masala	220
Mushroom Tawa Masala	200
Tawa Biryani	180

Total Items: 5

22. SANDWICH
Item	Price (₹)
Veg Sandwich	90
Grilled Sandwich	120
Cheese Sandwich	130
Paneer Sandwich	140
Club Sandwich	160

Total Items: 5

23. JUICE
Item	Price (₹)
Sweet Lime	80
Orange	90
Pineapple	90
Watermelon	80
Grape	90
Mosambi	80
Apple Juice	110
Pomegranate	120

Total Items: 8

24. FRUIT SHAKE
Item	Price (₹)
Banana Shake	110
Apple Shake	120
Pineapple Shake	120
Chikoo Shake	120
Mango Shake	130
Dry Fruit Shake	160

Total Items: 6

25. LASSI
Item	Price (₹)
Sweet Lassi	80
Salt Lassi	80
Special Lassi	110

Total Items: 3

26. SODA
Item	Price (₹)
Lemon Soda	60
Sweet Lime Soda	70
Salt Soda	60
Masala Soda	70

Total Items: 4

27. SWEETS
Item	Price (₹)
Gulab Jamun	60
Carrot Halwa	70
Gajar Halwa	70
Kesari Bath	60
Special Sweet	90

Total Items: 5

28. ICE CREAM
Item	Price (₹)
Vanilla	60
Strawberry	60
Butterscotch	70
Chocolate	70
Pista	70

Total Items: 5

29. ICE CREAM SHAKE
Item	Price (₹)
Vanilla Shake	120
Strawberry Shake	120
Chocolate Shake	130
Butterscotch Shake	130

Total Items: 4

30. FRUIT SALAD
Item	Price (₹)
Fruit Salad	120
Fruit Salad with Ice Cream	160

Total Items: 2

31. SPECIAL ICE CREAM
Item	Price (₹)
Gadbad Ice Cream	160
Dry Fruit Delight	190
Special Ice Cream	180
Banana Split	200

Total Items: 4
"""

self_menu_text = user_text.split("====================")[0]
ac_menu_text = user_text.split("====================")[1]

def parse_items(text):
    categories = {}
    current_cat = None
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        
        # Match e.g., "6. Chinese Starters"
        m = re.match(r'^\d+\.\s+(.*)$', line)
        if m:
            current_cat = m.group(1).strip()
            # Title case it to match exactly what is in menu.js, EXCEPT there are some weird capitalizations
            # I will store by lowercase key and do case insensitive matching later
            categories[current_cat.lower()] = {}
            continue
            
        if 'Item\tPrice' in line or 'Total Items:' in line:
            continue
        
        # Split by tab
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            try:
                price = int(parts[1].strip().replace('₹', '').strip())
                if current_cat:
                    categories[current_cat.lower()][name] = price
            except:
                pass
    return categories

self_cats = parse_items(self_menu_text)
ac_cats = parse_items(ac_menu_text)

# We have existing menuData.
with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

# Update prices exactly
for cat in data:
    cat_name = cat['category']
    # Skip the first 5 since they are already done!
    if cat_name in ["Hot Beverages", "Breakfast", "Dosa's", "Soup", "Tandoori Starters"]:
        continue
        
    cat_lower = cat_name.lower()
    
    if cat_lower in self_cats:
        cat_items = []
        for name, self_price in self_cats[cat_lower].items():
            ac_price = ac_cats.get(cat_lower, {}).get(name, self_price)
            # Create a clean safe image name
            img_name = name.lower().replace(' ', '_').replace('/', '_').replace('+', 'plus')
            img_name = re.sub(r'[^a-z0-9_]', '', img_name)
            
            cat_items.append({
                "name": name,
                "self_price": self_price,
                "ac_price": ac_price,
                "image": f"assets/images/{img_name}.png"
            })
        cat['items'] = cat_items

new_js_content = "const menuData = " + json.dumps(data, indent=2) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Updated items and prices for remaining categories.")
