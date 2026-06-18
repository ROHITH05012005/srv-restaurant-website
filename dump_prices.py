import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all panels using a regex that extracts the ID and the inner content of the panel
# We look for <div class="menu-panel..." id="tab-..."> ... up to next <div class="menu-panel or </section>
panel_pattern = re.compile(r'<div class="menu-panel[^"]*" id="tab-([^"]+)"(.*?)((?=<div class="menu-panel)|(?=</section>))', re.DOTALL)
panels = panel_pattern.findall(content)

print(f"Found {len(panels)} menu panels.")

for tab_id, panel_content, _ in panels:
    print(f"\n=================== Category: {tab_id.upper()} ===================")
    
    # Extract all cards in this panel content
    card_pattern = re.compile(
        r'<div class="food-card".*?'
        r'<div class="food-name">([^<]+)</div>.*?'
        r'<span class="food-price">₹(\d+)</span>',
        re.DOTALL
    )
    cards = card_pattern.findall(panel_content)
    for name, price in cards:
        print(f" - {name.strip():<40} : Rs. {price}")
