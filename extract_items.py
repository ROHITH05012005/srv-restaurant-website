import json

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

items = []
for cat in data:
    for item in cat['items']:
        items.append(item['name'])

with open('items_list_utf8.txt', 'w', encoding='utf-8') as f:
    for i, name in enumerate(items):
        f.write(f"{i}: {name}\n")
