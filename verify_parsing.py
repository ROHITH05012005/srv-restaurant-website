import json

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'): json_str = json_str[:-1]

data = json.loads(json_str)

print(f"Categories: {len(data)}")
for i, cat in enumerate(data):
    if i in [5, 6, 7, 30]:
        print(f"Category {i+1} ({cat['category']}) items: {len(cat['items'])}")
