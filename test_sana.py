import urllib.request
import urllib.parse
import os
import time

prompt = "A premium, realistic, mouth-watering close-up photography of Aloo Gobi Masala, potato cubes and cauliflower florets sautéed with ginger and Indian spices, served in a dark ceramic dish, garnished with coriander. Dark background, cinematic lighting, food photography."
encoded_prompt = urllib.parse.quote(prompt)

url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&private=true&enhance=false&model=sana"

print("Downloading from:", url)

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

start_time = time.time()
try:
    with urllib.request.urlopen(req) as response:
        with open("test_sana_aloo_gobi.png", "wb") as f:
            f.write(response.read())
    duration = time.time() - start_time
    print(f"Success! Saved as test_sana_aloo_gobi.png in {duration:.2f} seconds. File size: {os.path.getsize('test_sana_aloo_gobi.png')}")
except Exception as e:
    print("Error:", e)
