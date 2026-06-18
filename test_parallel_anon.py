import urllib.request
import urllib.parse
import os
import time
from concurrent.futures import ThreadPoolExecutor

test_images = {
    "mosambi_juice_premium_test.png": "A premium, realistic close-up photography of fresh Mosambi Juice sweet lime, served in a tall chilled glass with a lime slice on the rim, drops of condensation on the glass. Dark background, elegant setup, backlighting, food photography.",
    "pineapple_juice_premium_test.png": "A premium, realistic close-up photography of Pineapple Juice, served in a tall glass garnished with a pineapple leaf and cherry, chilled with ice. Dark background, cinematic lighting, food photography.",
    "water_melon_juice_premium_test.png": "A premium, realistic close-up photography of fresh Watermelon Juice, vibrant red juice in a chilled glass with a small watermelon slice on the rim and fresh mint leaves. Dark background, backlighting, food photography.",
    "pomegranate_juice_premium_test.png": "A premium, realistic close-up photography of Pomegranate Juice, dark ruby-red juice in an elegant glass, garnished with pomegranate seeds at the base. Dark background, dramatic lighting, food photography."
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_one(item):
    filename, prompt = item
    print(f"Starting {filename}...")
    start = time.time()
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&private=true&enhance=false&model=sana"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(filename, "wb") as f:
            f.write(data)
        elapsed = time.time() - start
        print(f"Finished {filename} in {elapsed:.1f}s. Size: {len(data)} bytes")
        return True
    except Exception as e:
        print(f"Failed {filename}: {e}")
        return False

def main():
    start_all = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(download_one, test_images.items()))
    print(f"All done in {time.time() - start_all:.1f}s. Results: {results}")

if __name__ == "__main__":
    main()
