import urllib.request
import urllib.parse
import os

prompt = "A premium, realistic, mouth-watering close-up photography of Channa Masala, spiced chickpeas cooked in a tangy onion-tomato gravy, served warm in a dark clay bowl, garnished with fresh ginger juliennes and coriander. Dark background, dramatic lighting, food photography."
encoded_prompt = urllib.parse.quote(prompt)

url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&private=true&enhance=false"

print("Downloading from:", url)

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        with open("test_channa_masala.png", "wb") as f:
            f.write(response.read())
    print("Success! Saved as test_channa_masala.png. File size:", os.path.getsize("test_channa_masala.png"))
except Exception as e:
    print("Error:", e)
