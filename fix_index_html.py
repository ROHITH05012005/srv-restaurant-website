import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all src="xyz_premium.png" and replace with src="assets/images/xyz_premium.png"
# This regex looks for src=" followed by anything ending in _premium.png", where it doesn't already have assets/images/
new_content = re.sub(r'src="(?![^"]*assets/images/)([^"]*_premium\.png)"', r'src="assets/images/\1"', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed index.html image paths.")
