import re

def extract_prices(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We find all food-card blocks
    # A food-card typically contains food-name and food-price
    # Let's extract food-name and food-price
    # Simple regex approach:
    # <div class="food-name">([^<]+)</div>
    # ...
    # <span class="food-price">₹(\d+)</span>
    
    # Let's find food-card blocks using regex split or finditer
    cards = []
    # Let's match food-card classes
    # We can match name and price anywhere within reasonable distance, or parse blocks.
    # Let's find all names:
    names = re.findall(r'<div class="food-name">([^<]+)</div>', content)
    prices = re.findall(r'<span class="food-price">₹(\d+)</span>', content)
    
    print(f"File {filename}: Found {len(names)} names, {len(prices)} prices.")
    
    # Let's pair them up. In a well-structured HTML, names and prices should align.
    # To be extremely precise, let's parse using a regular expression that matches name and price together inside a card.
    pattern = re.compile(
        r'<div class="food-card".*?'
        r'<div class="food-name">([^<]+)</div>.*?'
        r'<span class="food-price">₹(\d+)</span>',
        re.DOTALL
    )
    
    matches = pattern.findall(content)
    print(f"File {filename}: Matched {len(matches)} cards with name and price.")
    
    menu = {}
    for name, price in matches:
        menu[name.strip()] = int(price)
        
    return menu

menu_new = extract_prices("index.html")
menu_old = extract_prices("sri-raghavendra-vaibhava-2 (1).html")

print("\n--- Comparing Prices (Old vs New) ---")
all_names = set(menu_new.keys()).union(set(menu_old.keys()))

discrepancies = []
for name in sorted(all_names):
    p_old = menu_old.get(name)
    p_new = menu_new.get(name)
    if p_old is not None and p_new is not None:
        if p_old != p_new:
            discrepancies.append((name, p_old, p_new))
            print(f"Price mismatch for '{name}': Old=Rs.{p_old}, New=Rs.{p_new}")
    elif p_old is not None:
        print(f"Only in Old menu: '{name}' = Rs.{p_old}")
    else:
        # Only in new menu
        pass

if not discrepancies:
    print("No price mismatches found for overlapping items!")
else:
    print(f"Total discrepancies: {len(discrepancies)}")
