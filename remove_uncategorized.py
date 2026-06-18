import json

with open('menu.js', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace('const menuData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

# Filter out the 'Uncategorized' category
data = [cat for cat in data if cat['category'] != 'Uncategorized']

new_js_content = "const menuData = " + json.dumps(data, indent=2) + ";\n"
with open('menu.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Removed Uncategorized category")
