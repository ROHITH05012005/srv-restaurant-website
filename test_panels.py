import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find all occurrences of menu-panel class
matches = re.findall(r'<div class="menu-panel[^"]*" id="tab-([^"]+)"', content)
print(f"Matches for menu panels: {matches}")
