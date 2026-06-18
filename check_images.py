import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all image sources in the food cards
img_sources = re.findall(r'<img\s+src="([^"]+)"', html)
print(f"Total image tags in HTML: {len(img_sources)}")

unsplash_count = 0
local_count = 0
missing_local_files = []

for src in img_sources:
    if "unsplash.com" in src:
        unsplash_count += 1
    else:
        local_count += 1
        # Check if file exists locally
        if not os.path.exists(src) or os.path.getsize(src) == 0:
            missing_local_files.append(src)

print(f"Unsplash images count: {unsplash_count}")
print(f"Local images count: {local_count}")
print(f"Missing local files (not yet generated/downloaded): {len(missing_local_files)}")
if missing_local_files:
    print("Some of the missing local files:")
    for f in missing_local_files:
        print(f" - {f}")
