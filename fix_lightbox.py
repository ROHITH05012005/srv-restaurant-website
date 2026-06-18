import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the openLightbox argument as well
content = re.sub(r'openLightbox\(\'(?![^"]*assets/images/)([^"]*_premium\.png)\'\)', r'openLightbox(\'assets/images/\1\')', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed lightbox paths in index.html.")
